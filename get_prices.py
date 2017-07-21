import os
import requests
import pandas as pd
import time
import datetime as datetime

# maximum size of API query for currency prices is 23
currency_top = ["BTC", "ETH", 'FCT', 'GNT', 'ICN', 'SC', 'CFI']
                            
columns = ['LASTUPDATE', 'HIGH24HOUR',  'LASTVOLUMETO',
                                'MKTCAP', 'LASTVOLUME', 'PRICE', 'SUPPLY', 'CHANGEPCT24HOUR',
                                'LOW24HOUR', 'OPEN24HOUR', 'VOLUME24HOURTO', 'FLAGS',
                                'VOLUME24HOUR', 'CHANGE24HOUR', 'TYPE', 'LASTTRADEID',
                                'FROMSYMBOL', 'LASTMARKET', 'MARKET', 'TOSYMBOL']

df = pd.DataFrame({}, columns=columns)
currency_str = ','.join(currency_top)
parameters  = {'fsyms': currency_str, 'tsyms': 'USD'}


while True:
    response = requests.get('https://min-api.cryptocompare.com/data/pricemultifull', params=parameters)

    for currency in currency_top:
        crypt = response.json()['RAW'][currency]['USD']
        df = df.append(crypt, ignore_index=True)
    print df.loc[:, ['FROMSYMBOL', 'TOSYMBOL', 'PRICE', 'LOW24HOUR', 'CHANGEPCT24HOUR', 'VOLUME24HOUR']].head(7)
    print "Time of last update: {0}".format(datetime.datetime.now().strftime("%m-%d-%Y_%H:%M"))
    time.sleep(60)

