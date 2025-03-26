import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import sqlite3

df = pd.DataFrame(columns=['name', 'price', 'size', 'Stadteil in Hamburg', 'adresse', 'date', 'wg_size', 'links'])

print("WG Gesucht Hamburg")
print(50 * "-")
number = int(input("How many pages do you want to scrape? "))
page_num = 1
page_max = number

while page_num <= page_max:

    url = f'https://www.wg-gesucht.de/wg-zimmer-in-Hamburg.55.0.{page_num}.0.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')


    names = soup.find_all('h3', class_='truncate_title')
    prices = soup.find_all('div', class_='col-xs-3')
    sizes = soup.find_all('div', class_='col-xs-3 text-right')
    locations = soup.find_all('div', class_='col-xs-11')
    dates = soup.find_all('div', class_='col-xs-5 text-center')
    links = [a['href'] for a in soup.find_all('a', href=True)]


    sizes = [re.sub(r'\s+', ' ', size.text).strip() for size in sizes]
    names = [re.sub(r'\s+', ' ', n.text).strip() for n in names]
    prices = [re.sub(r'\s+', ' ', price.text).strip() for price in prices]
    locations = [re.sub(r'\s+', ' ', loc.text).strip() for loc in locations]
    hamburg_locations = [re.search(r'(Hamburg.*)', location).group(1) for location in locations]
    dates = [re.sub(r'\s+', ' ', date.text).strip() for date in dates]
    wg_size = [re.search(r'(\d+er WG)', locations[i]).group(1) if re.search(r'(\d+er WG)', locations[i]) else "N/A" for i in range(len(locations))]
    

    min_len = min(len(names), len(prices), len(sizes), len(locations), len(dates))
    stadteil = [re.search(r'^(.*)\s\|', hamburg_locations[i]).group(1) for i in range(min_len)]
    adresse = [re.search(r'\|([^|]*)', hamburg_locations[i]).group(1) for i in range(min_len)]


    temp_df = pd.DataFrame({
        'name': names[:min_len],
        'price': prices[:min_len],
        'size': sizes[:min_len],
        'Stadteil in Hamburg': stadteil,
        'adresse': adresse,
        'date': dates[:min_len],
        'wg_size': wg_size,
        'links': links[:min_len]
    })
    
    df = pd.concat([df, temp_df], ignore_index=True)
    page_num += 1

df.drop_duplicates(inplace=True)
df.to_csv('WG_Gesucht.csv', index=False)
print(df.describe())
print("Number of entries: ", len(df))


conn = sqlite3.connect('WG_Gesucht.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS WG_Gesucht(name TEXT, price TEXT, size TEXT, Stadteil_in_Hamburg TEXT, adresse TEXT, date TEXT, wg_size TEXT, links TEXT)')
conn.commit()
df.to_sql('WG_Gesucht', conn, if_exists='replace', index=False)
conn.close()
print("Data saved in WG_Gesucht.db")
