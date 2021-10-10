import yfinance as yf
import matplotlib.pyplot as plt
from bollinger_bands import BB

ticker = 'AAPL'
data = BB(ticker)
ups = data[0]
downs = data[1]
MA20 = data[2]
pricedata = yf.Ticker(ticker).history(period=f'{len(ups)}d', interval='1d')
closes = pricedata['Close'].values.tolist()
x_values = [i+1 for i in range(len(ups))]

plt.plot(x_values, ups, color='green', label='Upper')
plt.plot(x_values, downs, color='red', label='Lower')
plt.plot(x_values, MA20, color='purple', label='MA20')
plt.plot(x_values, closes, color='black', label='Price')
plt.legend(loc="upper left", prop={'size': 20}) # legend font size -> 20
plt.show()
