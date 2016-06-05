import matplotlib
import sqlalchemy
import pandas as pd
matplotlib.use('AGG')
import utils
import os

db_names = ["LNKD", "GILD"]
searches = ['%23LNKD OR LNKD OR LinkedIn', '%23GILD OR GILD OR Gilead Sciences']

# Define which words to count occurrencies for
words = ["up", "down", "good", "bad", "buy", "sell", "hold", "positive", "negative"]

for db_name, search in zip(db_names, searches):
    os.system("python SearchAndStoreTweetsByKeywords.py "+db_name+" "+search)
    # d = utils.build_dataframe(db_name, words)
    utils.fill_counts(db_name, words, "Count_"+db_name+".db")

# # Plot the last 24 hours
# plot = d.plot()
# fig = plot.get_figure()
# fig.savefig('static/plot_24_hours.png')
#
# # Fill the new values in the db
# db_file_name = "test.db"
# utils.fill_db(d, db_file_name)
#
# # Full plot from the start of the db content
# db = sqlalchemy.create_engine('sqlite:///'+db_file_name)
# new_d = pd.read_sql("data", db, index_col="index")
# new_d.index.name=""
# new_plot = new_d.plot()
#
# new_fig = new_plot.get_figure()
# new_fig.savefig('static/plot_full.png')
