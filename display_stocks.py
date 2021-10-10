# Displays data about all of the stocks
# import os
import pickle
import os

os.chdir('/Users/ryanscarbrough/Documents/workspace/Projects/Trading-Bot')

choice = input('"adx" or "bb"?: ')

if choice.lower() == 'adx':
    from stock_class_adx import Stock
elif choice.lower() == 'bb':
    from stock_class_bb import Stock
else:
    print('input is wrong')
    quit()

with open(f'{choice.lower()}_stocklist.pkl', 'rb') as f:
    stocks = pickle.load(f)

for i in stocks:
    print(f'{i.symbol}: last bought: {i.last_bought_time},last_sold: {i.last_sold_time} , holding: {i.holding}, bought_for_list: {i.bought_for_amt}, everbought: {i.everbought}, eversold: {i.eversold}')
