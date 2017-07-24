import os
import requests
import pandas as pd
import time
import datetime as datetime

#Formatting-- Display prices only out to three decimal points:
pd.set_option('display.float_format', lambda x: '%.3f' % x)

# List the Crypto-currency symbols you're interested in tracking:
currency_list = ["BTC", "ETH", 'FCT', 'GNT', 'ICN', 'SC', 'CFI']

#All Available fields from the API call to Crypto-Compare:                            
columns = ['LASTUPDATE', 'HIGH24HOUR',  'LASTVOLUMETO',
                                'MKTCAP', 'LASTVOLUME', 'PRICE', 'SUPPLY', 'CHANGEPCT24HOUR',
                                'LOW24HOUR', 'OPEN24HOUR', 'VOLUME24HOURTO', 'FLAGS',
                                'VOLUME24HOUR', 'CHANGE24HOUR', 'TYPE', 'LASTTRADEID',
                                'FROMSYMBOL', 'LASTMARKET', 'MARKET', 'TOSYMBOL']

df = pd.DataFrame({}, columns=columns)


currency_str = ','.join(currency_list)
parameters  = {'fsyms': currency_str, 'tsyms': 'USD'}





while True:
    response = requests.get('https://min-api.cryptocompare.com/data/pricemultifull', params=parameters)

    for currency in currency_list:
        crypt = response.json()['RAW'][currency]['USD']
        df = df.append(crypt, ignore_index=True)
    print ("\n") 
    print "Time of last update: {0}".format(datetime.datetime.now().strftime("%m-%d-%Y|%H:%M")) #If you want to change time.sleep var
    print df.loc[:, ['FROMSYMBOL', 'TOSYMBOL', 'PRICE', 'LOW24HOUR', 'CHANGEPCT24HOUR', 'VOLUME24HOUR']].head(7)
    print ("\n") 
    
    print "Coins with a 24 Hour Percent Increase OR Decrease over 10%:"
    for v in df[(df["CHANGEPCT24HOUR"] > 10.0) | (df["CHANGEPCT24HOUR"] < -10)]['FROMSYMBOL'].values:
        print v

    time.sleep(60) #update every minute
    
    
    

