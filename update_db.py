# ------------------------------------------
# EXTERNAL FUNCTIONS FOR INVESTMENT DATABASE
# ------------------------------------------

from pandas_datareader import data as pdr
from datetime import datetime, date, timedelta
import yfinance as yf
yf.pdr_override() # overrides yfinance to expect pandas datareader
import pandas as pd
import sqlite3

dbpath = "data/invest_tracker.db"
today = date.today()
delta = timedelta(days=1)
    

def getData(ticker, last_date):
    # Connect to sqlite3 database
    con = sqlite3.connect(dbpath)
    cur = con.cursor()   
    data = pdr.get_data_yahoo(ticker, start=last_date.date(), end=today)

    data.reset_index(inplace=True)
    
    data.columns = ['mkt_date', 'open', 'high', 'low', 'close', 'adj_close', 'volume']
    data.insert(1, 'ticker', ticker)
    data.set_index('ticker')
    
    sql = "INSERT or IGNORE INTO stock (mkt_date, ticker, open, high, low, close, adj_close, volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

    for i in range(len(data)):
        # Insert each row into database
        row = data.iloc[i]
        date_stripped = row.mkt_date.date()
        cur.execute(sql, (str(date_stripped), str(row.ticker), float(row.open), float(row.high), float(row.low), float(row.close), float(row.adj_close), int(row.volume)))
    con.commit()
    con.close()

def calculateSum(u_id, last_date, user_owns):

    # Connect to sqlite3 database
    con = sqlite3.connect(dbpath)
    cur = con.cursor()
    u_id = u_id[0]
    # print("Calculating portfolio value for user", u_id)
    last = last_date.date()
    while last <= today - delta:
        closed = False
        # print("Mkt_date:", last)
    
        cur.execute("select ticker from bought where b_date<=(?) and u_id=(?)", (str(last), int(u_id)))

        buys = cur.fetchall() # list of buys on or before current date in loop
        dailyValue = 0.0

        for tik, qty in user_owns:
            if (tik,) in buys:
                cur.execute("select adj_close from stock where ticker=(?) and mkt_date=(?)", (tik, str(last)))
                adj_close = cur.fetchone()
                if (adj_close != None):
                    adj_close = adj_close[0]
                    dailyValue += (adj_close * qty)
                else:
                    closed = True
                
        if (closed == False):
            # print("DAILY VALUE:", dailyValue)
            cur.execute("insert into value (u_id, mkt_date, value, num_transactions) VALUES (?, ?, ?, ?)", (u_id, str(last), float(dailyValue), 0))
        else:
            # No value reported, most likely market closed
            cur.execute("select MAX(mkt_date), value from value where u_id=(?)", (u_id,))
            last_val_date = cur.fetchone()
            if (last_val_date[0] != None):
                ldate = last_val_date[0]
                lval = last_val_date[1]
                cur.execute("insert into value (u_id, mkt_date, value, num_transactions) VALUES (?, ?, ?, ?)", (int(u_id), str(last), float(lval), 0))

        last += delta
    con.commit()
    con.close()


def update_portfolios():        
    con = sqlite3.connect(dbpath)
    cur = con.cursor() 
    # Get all user IDs who own a stock
    cur.execute("select u_id from owns group by u_id")
    user_ids = cur.fetchall()

    for u in user_ids:
        # Get list of user's stock holdings
        cur.execute("select ticker, qty from owns where u_id=(?)", u)
        user_owns = cur.fetchall()
        last_date = None
        for tik, qty in user_owns:
            # Find last entry of ticker in stock table, update data
            cur.execute("select MAX(mkt_date) from stock where ticker=(?)", (tik,))
            last_date = cur.fetchone()
        
            # Convert date from tuple to datetime
            last_date = last_date[0]
            if (last_date == None):
                # If no data found for ticker, set last date to Jan 1 2021
                last_date = "2021-01-01"

            last_date = datetime.strptime(last_date, "%Y-%m-%d")
            
            if (last_date.date() < today):
                getData(tik, last_date)

            # Find last entry of value (portfolio), calculate daily
            cur.execute("select MAX(mkt_date) from value where u_id=(?)", u)
            last_date = cur.fetchone()
            last_date = last_date[0]
            
            if (last_date == None):
                # If no data found for value, set last day to first purchase
                cur.execute("select MIN(b_date) from bought where u_id=(?)", u)
                last_date = cur.fetchone()
                if (last_date[0] == None):
                    last_date = "2021-01-01"
                else:
                    last_date = last_date[0]
            last_date = datetime.strptime(last_date, "%Y-%m-%d") 
        
        if (last_date.date() <= today - timedelta(days=2)):
            calculateSum(u, last_date, user_owns)

    con.commit()
    con.close()

