import matplotlib
import sqlalchemy
import pandas as pd
import utils
import os
from datetime import datetime, timedelta
matplotlib.use('AGG')


def save_plot(d, file_name):
    plot = d.plot()
    plot.legend(loc="best", fancybox=True, framealpha=0.5)
    fig = plot.get_figure()
    fig.savefig('static/'+file_name+'.png')


db_names = ["LNKD", "GILD", "APPL"]
searches = ['%23LNKD OR LNKD OR LinkedIn', '%23GILD OR GILD OR Gilead Sciences', '%23APPL OR APPL OR %23Apple']

# Define which words to count occurrencies for
words = ["up", "down", "good", "bad", "buy", "sell", "hold", "positive", "negative"]

for db_name, search in zip(db_names, searches):
    os.system("python SearchAndStoreTweetsByKeywords.py "+db_name+" "+search)
    output_db_name = "Count_"+db_name+".db"
    utils.fill_counts(db_name, words, output_db_name=output_db_name)
    # Plotting
    db = sqlalchemy.create_engine('sqlite:///'+output_db_name)
    d_full = pd.read_sql("data", db, index_col="index")
    # Last 24 hours plot
    time_cut = datetime.now() - timedelta(hours=25)
    d_last_24_hours = d_full[d_full.index > str(time_cut)]
    d_last_24_hours.index.name = ""
    save_plot(d_last_24_hours, "plot_24_hours_"+db_name)
    # Full plot from the start of the db content
    d_full.index.name = ""
    save_plot(d_full, "plot_full_"+db_name)
