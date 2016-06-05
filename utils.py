import os
import sqlite3
import pandas as pd
import sqlalchemy
import utils
from datetime import datetime, timedelta


def select_count(file_name, word_selection, from_time, to_time):
    con = sqlite3.connect(file_name)
    cur = con.cursor()
    selection = "WHERE created_at > '"+from_time+"' AND created_at <= '"+to_time+"' AND "+word_selection
    # query = "SELECT count(*) FROM hashtags WHERE "+selection+";"
    query = "SELECT count(*) FROM hashtags "+selection+";"
    count = cur.execute(query).fetchone()[0]
    con.close()
    return count
    

def query_time(file_name, find_oldest=False):
    con = sqlite3.connect(file_name)
    cur = con.cursor()
    # query = "SELECT MAX(created_at) FROM hashtags;"
    # The inserted_date is when the result is filled in the db. The first
    # time is immediately after the query to Twitter.
    query = "SELECT MIN(inserted_date) FROM hashtags;"
    if find_oldest:
        query = "SELECT MIN(created_at) FROM hashtags;"
    most_recent = cur.execute(query).fetchone()[0]
    con.close()
    return most_recent


def oldest_tweet_time(file_name):
    return query_time(file_name, find_oldest=True)


def build_dataframe(db_name, words, from_time, to_time):
    file_name = db_name+".sqlite"
    word_counts = dict()
    for word in words:
        word_counts[word] = []

    date_time = [to_time]
    # print "file date =", file_date
    for word in word_counts:
        selection = "content LIKE '% "+word+" %'"
        count = select_count(file_name, selection, from_time, to_time)
        # print word, "=", count
        word_counts[word].append(count)
    return pd.DataFrame(data=word_counts, index=pd.DatetimeIndex(date_time))


def fill_db(dataframe, db_file_name):
    """
    Fills the dataframe content in the database one row at a time checking for duplicates.
    The database was built using the index of the dataframe as the primary key. This
    function is fine as long as the dataframe is not large. Because we append to the
    database this is not a big concern.
    """
    # Create the table if the file is not there. This is necessary because there does not seem to be a way
    # to specify a primary key in the dataframe to_sql command. We want a primary key to avoid filling
    # duplicates.
    file_exists = os.path.isfile(db_file_name)
    db = sqlalchemy.create_engine('sqlite:///'+db_file_name)
    if not file_exists:
        d_schema = pd.io.sql.get_schema(dataframe.reset_index(), 'data', keys='index')
        db.execute(d_schema)
    # Append the new values to the table.
    num_rows = len(dataframe)
    for i in range(num_rows):
        try:
            dataframe.iloc[i:i+1].to_sql('data', db, if_exists='append')
        except sqlalchemy.exc.IntegrityError:
            # print "skipping duplicate"
            pass


def fill_counts(db_name, words, output_db_name):
    # Note that this function requires at least one tweet in the db
    previous_file_name = db_name + "_previous.sqlite"
    file_name = db_name + ".sqlite"

    start = datetime.strptime(utils.oldest_tweet_time(file_name), "%Y-%m-%d %H:%M:%S.%f")
    if os.path.isfile(previous_file_name):
        start = datetime.strptime(utils.query_time(previous_file_name), "%Y-%m-%d %H:%M:%S.%f")

    finish = datetime.strptime(utils.query_time(file_name), "%Y-%m-%d %H:%M:%S.%f")
    # elapsed_time = finish - start
    # print "elapsed time in seconds =", elapsed_time.total_seconds()
    # print "elapsed time in hours =", int(elapsed_time.total_seconds()/3600.)

    current_hour = finish - timedelta(hours=2)

    df = pd.DataFrame()
    while current_hour > start:
        df = df.append(build_dataframe(db_name, words, str(current_hour), str(current_hour+timedelta(hours=2))))
        current_hour -= timedelta(hours=2)
    fill_db(df, output_db_name)

    os.system("mv " + file_name + " " + previous_file_name)


# --------------
# Web page utils
# --------------


def append_figures(figures_list, figure_type, figure_text):
    page_text = ""
    for figure in figures_list:
        if figure.find(figure_type) == -1:
            continue
        figure_name = figure.strip("plot_"+figure_type).rstrip(".png")
        page_text += '<a name="'+figure_name+'">'+figure_name+' '+figure_text+'</a>\n'
        page_text += "---------------\n"
        page_text += '![alt text](\static\\'+figure+' "'+figure_name+' '+figure_text+'")\n\n'
    return page_text


def build_page():
    content = "Twitter Scraper\n"
    content +="===============\n"
    content +="\n"
    figures_list = [x for x in os.listdir("./static/") if x.find(".png") != -1]
    for figure in figures_list:
        if figure.find("24_hours") != -1:
            figure_name = figure.strip("plot_24_hours").rstrip(".png")
            content += "* ["+figure_name+" last 24 hours](#"+figure_name+")\n"
        else:
            figure_name = figure.strip("full").rstrip(".png")
            content += "* [" + figure_name + " full](#" + figure_name + ")\n"
    content += "\n"
    content += append_figures(figures_list, "24_hours", "last 24 hours")
    content += append_figures(figures_list, "full", "full")
    return content
