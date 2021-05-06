# --------------------------------------------
# EXTERNAL HELPER FUNCTIONS FOR USER UTILITIES
# --------------------------------------------

# This script contains most of the backend for the database scripts

import sqlite3
import pandas as pd
import getpass
from columnar import columnar
from encryption import load_key, encrypt_pass, decrypt_pass


dbpath = "data/invest_tracker.db"


def user_signin():
    print("Signing in...")
    username = input("Enter account name: ")
    password = getpass.getpass("Enter password: ")
    
    con = sqlite3.connect(dbpath)
    cur = con.cursor()
    cur.execute("select u_id, password from user where acc_name=(?)", (username,))
    user_id = cur.fetchone()
    if (user_id != None):
        encrypted = user_id[1]
        decrypted = decrypt_pass(encrypted)
        if (password == decrypted):
            return user_id[0]
        else:
            return None
    else:
        return None


def create_account():
    con = sqlite3.connect(dbpath)
    cur = con.cursor()
    print("Creating new user...")
    goodAccount = True
   
    acc_name = input("Enter account name (must be unique): ")
    name = input("Enter customer name: ")
    ssn = input("Enter SSN (9 digits): ")
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Confirm password: ")
    
    if (len(ssn) != 9):
        print("Error: SSN length invalid.")
        exit()

    if (password == confirm_password):
        cur.execute("select * from user where acc_name=(?)", (acc_name,))
        exists = cur.fetchone()
        if (exists != None):
            errorcode = "Error: Account {} aready exists.".format(acc_name)
            print(errorcode)
            goodAccount = False
        else:
            encrypted = encrypt_pass(password)
            sql = """
            insert into user(acc_name, name, ssn, password)
            values (?,?,?,?)
            """
            cur.execute(sql, (acc_name, name, ssn, encrypted))
            goodAccount = True
    else:
        print("Error: Passwords do not match.")
        goodAccount = False
    
    con.commit()
    con.close()
    return goodAccount

def close_account(user_id):
    print("WARNING:\nOnce your account is closed, your data is deleted and cannot be recovered.")
    confirm = input("Are you sure? Enter CONFIRM to accept: ")
    if (confirm == "CONFIRM"):
        con = sqlite3.connect(dbpath)
        cur = con.cursor()
        cur.execute("delete from bought where u_id=(?)", (user_id,))
        cur.execute("delete from sold where u_id=(?)", (user_id,))
        cur.execute("delete from value where u_id=(?)", (user_id,))
        cur.execute("delete from user where u_id=(?)", (user_id,))
        con.commit()
        con.close()
        print("Success: Account deleted.")
        return True
    else:
        print("Error: CONFIRM statement invalid.")
        return False

def list_holdings(user_id):
    con = sqlite3.connect(dbpath)
    cur = con.cursor()
    sql = "select * from owns where u_id=({})".format(user_id)
    df = pd.read_sql_query(sql, con)
    
    if (df.empty):
        print("Error: User has no holdings.")
    else:
        headers = ['Ticker', 'Qty']
        data = df.drop(columns=['u_id'])
        data_list = data.values.tolist()
        table = columnar(data_list, headers, no_borders=True)
        print(table)

def add_purchase(user_id):
    ticker = input("Enter ticker: ")
    qty = float(input("Enter quantity of shares bought: "))
    avg_cost = float(input("Enter avg cost per share: "))
    b_date = input("Enter date purchased (YYYY-Mm-Dd): ")

    con = sqlite3.connect(dbpath)
    cur = con.cursor()
    sql = """
    insert into bought(u_id, ticker, qty, avg_cost, b_date)
    values (?,?,?,?,?)
    """
    cur.execute(sql, (int(user_id), str(ticker), qty, avg_cost, str(b_date)))

    # Update owns table
    
    cur.execute("select * from owns where u_id=(?) and ticker=(?)", (user_id, ticker))
    entry = cur.fetchone()
    old_qty = 0.0
    if (entry != None):
        print("Already owned. Updating records...")
        old_qty = float(entry[2])
        qty = qty + old_qty
        cur.execute("delete from owns where u_id=(?) and ticker=(?)", (user_id, ticker))
    else:
        print("Record not found. Adding new entry...")
    cur.execute("insert into owns(u_id, ticker, qty) values (?,?,?)", (user_id, ticker, qty))

    con.commit()
    con.close()

def add_sell(user_id):
    ticker = input("Enter ticker: ")
    qty = float(input("Enter quantity of shares sold: "))
    avg_cost = float(input("Enter avg cost per share: "))
    s_date = input("Enter date sold (YYYY-Mm-Dd): ")

    con = sqlite3.connect(dbpath)
    cur = con.cursor()
    sql = """
    insert into sold(u_id, ticker, qty, avg_cost, s_date)
    values (?,?,?,?,?)
    """
    cur.execute(sql, (int(user_id), str(ticker), qty, avg_cost, str(s_date)))

    # Update owns table
    
    cur.execute("select * from owns where u_id=(?) and ticker=(?)", (user_id, ticker))
    entry = cur.fetchone()
    old_qty = 0.0
    if (entry != None):
        old_qty = float(entry[2])
        qty = old_qty - qty
        if (qty < 0):
            print("Error: Can't sell more shares than you hold.")
            exit()
        cur.execute("delete from owns where u_id=(?) and ticker=(?)", (user_id, ticker))
        if (qty > 0):
            cur.execute("insert into owns(u_id, ticker, qty) values (?,?,?)", (user_id, ticker, qty))
        elif (qty == 0):
            print("You have sold all remaining {} shares.").format(ticker)
    else:
        print("Error: Can't place sell order for stock you don't own.")
        exit()

    con.commit()
    con.close()


