from coinbase.wallet.client import Client
import requests
import json
import smtplib


class CoinBot():

    #This is making a request to coinbase website for more specific information that is not available from coinbase API
    global url1, url2, r, r2, data, data2
    url1 = 'https://www.coinbase.com/api/v2/assets/search?base=USD&country=US&filter=listed&include_prices=true&limit=30&order=asc&page=1&query=&resolution=day&sort=rank'
    url2 = 'https://www.coinbase.com/api/v2/assets/search?base=USD&country=US&filter=listed&include_prices=true&limit=30&order=asc&page=2&query=&resolution=day&sort=rank'
    r = requests.get(url1)
    r2 = requests.get(url2)
    data = json.loads(r.text)
    data2 = json.loads(r2.text)


    #init
    def __init__(self, APIKEY, APISECRET):
        self.APIKEY =  APIKEY
        self.APISECRET = APISECRET
        self.client = Client(APIKEY,APISECRET)

    #displays the price of a specified currency
    def display_price(self, symbol):
        for d in data['data']:
            if d['symbol'] == symbol:
                print(float(d['latest']))
        for d in data2['data']:
            if d['symbol'] == symbol:
                print(float(d['latest']))

    #displays the percentage change of a specified currency within the last 24 hours
    def display_percentage(self,symbol):
        for d in data['data']:
            if d['symbol'] == symbol:
                print(str(round(d['percent_change']*100,2)) + '%')
        for d in data2['data']:
            if d['symbol'] == symbol:
                print(str(round(d['percent_change']*100,2)) + '%')

    #Buys a specified currency with a specified amount at a target price
    def buy(self,symbol,buy_price,amount):
        if not isinstance(symbol,str) or not isinstance(buy_price,float) or not isinstance(amount,str):
            return 'Error, please fix argument types'
        payment_method = self.client.get_payment_methods()[0] #This is cash account, script will have access to bank account
        accounts = self.client.get_accounts()
        for acc in accounts.data:
            if acc.currency == symbol and float(self.client.get_buy_price(currency_pair='{}-USD'.format(symbol)).amount) <= buy_price:
                acc.buy(amount=amount,currency=symbol,payment_method=payment_method.id)
                return '{} BOUGHT'.format(symbol)
            else:
                return 'nothing'

    #Buys a specified currency but with a specified amount of dollars at a target price
    def buy_by_dollars(self,symbol,buy_price,amount):
        if not isinstance(symbol,str) or not isinstance(buy_price,float) or not isinstance(amount,float):
            return 'Error, please fix argument types'
        new_amount = amount/buy_price
        payment_method = self.client.get_payment_methods()[0] #This is cash account, script will have access to bank account
        accounts = self.client.get_accounts()
        for acc in accounts.data:
            if acc.currency == symbol and float(self.client.get_buy_price(currency_pair='{}-USD'.format(symbol)).amount) <= buy_price:
                acc.buy(amount=new_amount,currency=symbol,payment_method=payment_method.id)
                return '{} BOUGHT'.format(symbol)
            else:
                return 'nothing'

    #Sells currency once target price has been reached
    def sell(self,symbol,sell_price,amount):
        if not isinstance(symbol,str) or not isinstance(sell_price,float) or not isinstance(amount,str):
            return 'Error, please fix argument types'
        try:
            payment_method = self.client.get_payment_methods()[0] #This is cash account, script will have access to bank account
            accounts = self.client.get_accounts()
            for acc in accounts.data:
                if acc.currency == symbol and float(self.client.get_buy_price(currency_pair='{}-USD'.format(symbol)).amount) >= sell_price:
                    acc.sell(amount=amount,currency=symbol,payment_method=payment_method.id)
                    return '{} SOLD'.format(symbol)
                else:
                    print('nothing')
        except:
            print('Error in accessing your coinbase Account')

    #Display total wallet
    def display_total(self):
        accounts = self.client.get_accounts()
        value = 0.0
        for a in accounts.data:
            print(str(a['name']))
        for wallet in accounts.data:
             print(str(wallet['name'] + ' ' + str(wallet['native_balance'])))
             value+=float(str(wallet['native_balance']).replace('USD ',''))
        print('Total worth: $' + str(value))

    #Send me an email
    def send_email(self,subject,message,user,password):
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(user,password)
            subject = subject
            body = message

            msg = 'Subject: {}\n\n'.format(subject) + '{}'.format(body)

            smtp.sendmail(user,user,msg)
