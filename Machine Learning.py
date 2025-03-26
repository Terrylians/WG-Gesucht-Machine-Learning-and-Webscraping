import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# Read the data
data = pd.read_csv('wg_gesucht.csv')

# Clean the data
data = data.dropna()


data['price'] = data['price'].str.replace('€', '')
data['price']=pd.to_numeric(data['price'], errors='coerce')

data['size'] = data['size'].str.replace('m²', '')

mean_price = data['price'].mean()
data['price'].fillna(mean_price, inplace=True)

plt.scatter(data['size'], data['price'])
plt.xlabel('Size in m2')
plt.ylabel('Price in euro')
plt.show()


X = data['size'].values.reshape(-1, 1)
y = data['price'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=0)

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
y_pred = np.zeros(y_test.shape)


regressor = LinearRegression()
regressor.fit(X_train, y_train)

y_pred = regressor.predict(X_test)
X_test=scaler.inverse_transform(X_test)

plt.scatter(X_test, y_test, color='gray')
plt.plot(X_test, y_pred, color='red', linewidth=2)
plt.xlabel('Size in m2')
plt.ylabel('Price in euro')
plt.show()

print('Mean Absolute Error:', np.mean(np.abs(y_test - y_pred)))
print('Mean Squared Error:', np.mean((y_test - y_pred) ** 2))
print('Root Mean Squared Error:', np.sqrt(np.mean((y_test - y_pred) ** 2)))
print('R2 Score:', regressor.score(X_test, y_test))
print('Intercept:', regressor.intercept_)

print('Coefficient:', regressor.coef_)

print('Price for 50m2:', regressor.predict(scaler.transform([[50]])))
print('Price for 25m2:', regressor.predict(scaler.transform([[25]])))
print('Price for 20m2:', regressor.predict(scaler.transform([[20]])))
print('Price for 10m2:', regressor.predict(scaler.transform([[10]])))

