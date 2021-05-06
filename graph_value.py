# -----------------------------------------
# GRAPHING FUNCTION FOR INVESTMENT DATABASE
# -----------------------------------------
import pandas as pd
import math
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sqlite3
import datetime

dbpath = "data/invest_tracker.db"

def graph_value(user_id):
    con = sqlite3.connect(dbpath)
    cur = con.cursor()

    value = pd.read_sql_query("select * from value", con)
    # print(value.head())

    values = value[['u_id','mkt_date','value']]
    plot_value = values[(values['u_id'] == user_id)]
    if (plot_value.empty):
        print("Error: No portfolio values to graph.")
        exit()
    plot_value = plot_value.drop(['u_id'], axis=1)

    dates = mdates.num2date(mdates.datestr2num(plot_value['mkt_date']))

    # print(plot_value.head())

    # create graph object

    fig = plt.figure()
    u_plot = fig.add_subplot(1, 1, 1)
    u_plot.plot(dates, plot_value['value'], color ='tab:green')

    maxval = plot_value['value'].max()
    minval = plot_value['value'].min()
    mindate = plot_value['mkt_date'].min()
    maxdate = plot_value['mkt_date'].max()
    # print(minval, maxval)
    max_y = int(math.ceil(maxval / 500.0)) * 500
    min_y = int(math.floor(minval / 500)) * 500
    # print(min_y, max_y)

    # u_plot.set_xlim([mindate, maxdate])
    u_plot.set_ylim([min_y, max_y])
    fig.autofmt_xdate()
    fig.suptitle('Portfolio value')
    fig.savefig('user_value.png')

    con.close()
