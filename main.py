from coinbase.wallet.client import Client
import requests
import json
import smtplib
from CoinBot import CoinBot


APIKEY = '******' #Replace your API key with the stars
APISECRET = '*******' #Replace API Secret with the stars

my_bot = CoinBot(APIKEY,APISECRET)
how_many = input('how many coins would you like to put down?: ')
coins = []
index = 0
#Adding info to a list
for x in range(int(how_many)):
    coin = input('What is the symbol of the coin (Ex. BTC): ')
    buy_price = input('What is your buy price?: ')
    amount = input('How many would you like to purchase (in dollars worth)')
    sell_price = input('What is your sell price?: ')
    coin_dict = {
        'coin': coin,
        'buy_price': buy_price,
        'amount': amount,
        'sell_price': sell_price,
        'buy_trigger': False,
        'sell_trigger': False
    }
    coins.append(coin_dict)

#Runs on a loop
while True:
    for x in coins:
        if x['buy_trigger'] == False:
            buy = my_bot.buy_by_dollars(x['coin'],x['buy_price'],x['amount'])
            if buy == '{} BOUGHT'.format(x['coin']):
                x['buy_trigger'] = True
                subject = '{} has been purchased!'.format(x['coin'])
                my_bot.send_email(subject)
        if x['sell_trigger'] == False:
            buy = my_bot.sell(x['coin'],x['buy_price'],x['amount'])
            if buy == '{} SOLD'.format(x['coin']):
                x['sell_trigger'] = True
                subject = '{} has been purchased!'.format(x['coin'])
                my_bot.send_email(subject)
































