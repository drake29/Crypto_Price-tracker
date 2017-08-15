import os
import requests
import pandas as pd
import time
import datetime as datetime
from twilio.rest import Client
from credentials import account_sid, auth_token, my_cell, my_twilio


#Formatting-- Display prices only out to three decimal points:
pd.set_option('display.float_format', lambda x: '%.3f' % x)

# visit https://www.cryptocompare.com/coins/#/btc for all options.
# List the Crypto-currency symbols you're interested in tracking:
currency_list = ["BTC", "ETH", 'FCT', 'GNT', 'ICN', 'SC', 'REP', 'CFI']

#All Available fields from the API call to Crypto-Compare:                            
columns = ['LASTUPDATE', 'HIGH24HOUR',  'LASTVOLUMETO',
                                'MKTCAP', 'LASTVOLUME', 'PRICE', 'SUPPLY', 'CHANGEPCT24HOUR',
                                'LOW24HOUR', 'OPEN24HOUR', 'VOLUME24HOURTO', 'FLAGS',
                                'VOLUME24HOUR', 'CHANGE24HOUR', 'TYPE', 'LASTTRADEID',
                                'FROMSYMBOL', 'LASTMARKET', 'MARKET', 'TOSYMBOL', 'NET_POS']



df = pd.DataFrame({}, columns=columns)


currency_str = ','.join(currency_list)
parameters  = {'fsyms': currency_str, 'tsyms': 'USD'}

#Insert your coin 'FROMSYMBOL', the 'Num_Coins' you have, and the purchase price (or weighted avg if multiple purchases)
my_positions = {'FROMSYMBOL': ["BTC", "ETH", 'FCT', 'GNT', 'ICN', 'SC', 'REP', 'CFI'],
             'Num_Coins': [0, 74.765, 207.81, 2838.65, 0, 41903.59, 18.15, 0]}#,
             #'Weighted_avgPrice': [1788, 236.5836, 8.13, 0.36, 0, 0.01256, 0]}
df2 = pd.DataFrame(my_positions)
#df2['Net_Investment']= df2.Num_Coins * df2.Weighted_avgPrice


upper_threshold = 10.0
lower_threshold = -10.0

big_upper_swing = 25.0
big_lower_swing = -25.0


while True:
    response = requests.get('https://min-api.cryptocompare.com/data/pricemultifull', params=parameters)

    for currency in currency_list:
        crypt = response.json()['RAW'][currency]['USD']
        df = df.append(crypt, ignore_index=True)
        #df['Net_Position'] = (df.PRICE * df2.Num_Coins) -df2.Net_Investment
        df['Portfolio Balance'] = (df.PRICE * df2.Num_Coins)

    print ("\n")    
    print ('---------------------------------------------------------------------------------')
    print (df.loc[:, ['FROMSYMBOL', 'TOSYMBOL', 'PRICE', 'LOW24HOUR', 'CHANGEPCT24HOUR', 'VOLUME24HOUR']]) #Subset df to display columns your interested in
    print ('---------------------------------------------------------------------------------')
    print (df.loc[:, ['FROMSYMBOL', 'Portfolio Balance']]) #Check your net position for each coin
    print  ("As of: " + "{0}".format(datetime.datetime.now().strftime("%m-%d-%Y|%H:%M")))
    print ("Your Net Holding is: $ %.2f" %(df['Portfolio Balance'].sum())) #Calculates your total net position
    print ('---------------------------------------------------------------------------------')

    print ("Coins to Watch.....")
    print ("24 Hour Percent Increase / Decrease over 10%:") 
    for v in df[(df["CHANGEPCT24HOUR"] > upper_threshold) | (df["CHANGEPCT24HOUR"] < lower_threshold)]['FROMSYMBOL'].values:
        print (v) #Change lower/upper threshold amounts above, if your want +/- 10%

    
    def big_swings(dframe):
    	for change, symbol in dframe[(dframe["CHANGEPCT24HOUR"] > big_upper_swing) | (dframe["CHANGEPCT24HOUR"] < big_lower_swing)][['CHANGEPCT24HOUR','FROMSYMBOL']].values:
        	my_str= (symbol + ":  " + str(change))
        	client = Client(account_sid, auth_token)
        	message = client.messages.create(
                   to= my_cell,
                   from_=my_twilio,
                   body= "\n Yo!\n We got some over a 25% Swing for:\n\n  {0}".format(my_str))

    
    
    big_swings(df)
    
    time.sleep(300) #update every 5 minutes

    
    df = pd.DataFrame({}, columns=columns) #clear the df & run again.
