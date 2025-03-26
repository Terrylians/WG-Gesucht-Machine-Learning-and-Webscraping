import sqlite3

conn = sqlite3.connect('WG_Gesucht.db')
c = conn.cursor()


c.execute('''
    SELECT * FROM WG_Gesucht
    WHERE CAST(price AS REAL) > 500 AND CAST(price AS REAL) < 1000
''')


rows = c.fetchall()
print("WG with Price between 500 and 1000")
print(len(rows),"WG Found with the above criteria")
for row in rows:
    print(row)
    print('\n')
    print(5*'-')

c.execute('''
    SELECT * FROM WG_Gesucht
    WHERE CAST(size AS REAL) > 10 AND CAST(size AS REAL) < 20
''')

rows = c.fetchall()
print("WG with Size between 10 and 20")
print(len(rows),"WG Found with the above criteria")
for row in rows:
    print(row)
    print('\n')
    print(5*'-')


c.execute('''
    SELECT * FROM WG_Gesucht
    WHERE CAST(price AS REAL) > 500 AND CAST(price AS REAL) < 1000
    AND CAST(size AS REAL) > 10 AND CAST(size AS REAL) < 20
''')

rows = c.fetchall()
print("WG with Price between 500 and 1000 and Size between 10 and 20")
print(len(rows),"WG Found with the above criteria")
for row in rows:
    print(row)
    print('\n')
    print(5*'-')

c.execute('''
    SELECT * FROM WG_Gesucht
    WHERE "Stadteil in Hamburg" LIKE '%Eims%'
''')
rows=c.fetchall()
print("WG in Eimsbüttel")
print(len(rows),"WG Found with the above criteria")
for row in rows:
    print(row)
    print('\n')
    print(5*'-')

conn.close()

