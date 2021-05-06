

# Investment Tracker Database  

## A Python/SQL Project  

This project was created by Evan Cole as a part of the final implementation project for CSC 436 (databases) at The University of Rhode Island.  


### Overview  

This Python application is a command-line application designed to demonstrate a relational database working in conjunction with the YFinance API.  

Users are able to sign in, or register if they do not have an account.  
After doing so, the user is provided with several basic functions:  

* List Holdings
* Auto-Update Database
* Add Purchase Transaction
* Add Sell Transaction
* Render Portfolio Value PNG
* Close Account
* Exit


The user inputs a number corresponding to their desired utility, and functions written in external scripts are called by the main processor to execute.  

### Requirements  

Python 3 is required to run the scripts. Several modules also need to be downloaded, which can be done with the following command:  
> pip install -r requirements.txt  

This should install all modules required to run the program.  
SQLite3 is also required in order to connect to the database.  
[Download SQLite](https://www.sqlite.org/download.html)

The script can then be executed via the command line:  
> python3 main.py  

There is a test user configured with a few preset purchases and stock holdings to play around with.  
To sign in to the test user, enter the following credentials:  
Account name: test\_account
Password: password  

This project is publicly available on [GitHub](https://github.com/evancole99/investment_tracker). Anyone is free to repurpose, change, or expand upon this library for educational purposes.  



NOTE: If you try to break the scripts, you will. If you try to break the database, you will. This is not meant to be a secure implementation, only practice and educational content. **DO NOT STORE SENSITIVE DATA HERE.**  


