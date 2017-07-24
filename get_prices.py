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
                                'FROMSYMBOL', 'LASTMARKET', 'MARKET', 'TOSYMBOL', 'NET_POS']



df = pd.DataFrame({}, columns=columns)


currency_str = ','.join(currency_list)
parameters  = {'fsyms': currency_str, 'tsyms': 'USD'}

my_positions = {'FROMSYMBOL': ["BTC", "ETH", 'FCT', 'GNT', 'ICN', 'SC', 'CFI'],
             'Num_Coins': [.50, 19.304, 246, 2000, 0, 15000, 0],
             'Weighted_avgPrice': [1788, 236.5836, 8.13, 0.36, 0, 0.01256, 0]}
df2 = pd.DataFrame(my_positions)
df2['Net_Investment']= df2.Num_Coins * df2.Weighted_avgPrice




while True:
    response = requests.get('https://min-api.cryptocompare.com/data/pricemultifull', params=parameters)

    for currency in currency_list:
        crypt = response.json()['RAW'][currency]['USD']
        df = df.append(crypt, ignore_index=True)
        df['Net_Position'] = (df.PRICE * df2.Num_Coins) -df2.Net_Investment
    print ("\n") 
    print '---------------------------------------------------------------------------------'
    print df.loc[:, ['FROMSYMBOL', 'TOSYMBOL', 'PRICE', 'LOW24HOUR', 'CHANGEPCT24HOUR', 'VOLUME24HOUR']]
    print '---------------------------------------------------------------------------------'
    print df.loc[:, ['FROMSYMBOL', 'Net_Position']]
    print  "As of: " + "{0}".format(datetime.datetime.now().strftime("%m-%d-%Y|%H:%M"))
    print "Your Total Net Position is: $ %s" % (df['Net_Position'].sum())
    print '---------------------------------------------------------------------------------'
    print ("\n") 
    print "Coins to Watch....."
    print "24 Hour Percent Increase / Decrease over 10%:"
    for v in df[(df["CHANGEPCT24HOUR"] > 10.0) | (df["CHANGEPCT24HOUR"] < -10)]['FROMSYMBOL'].values:
        print v

    

    time.sleep(60) #update every minute
    df = pd.DataFrame({}, columns=columns)

    
    
    

