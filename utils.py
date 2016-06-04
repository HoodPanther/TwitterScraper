import os
import sqlite3
import pandas as pd
import sqlalchemy


def select_count(file_name, selection):
    con = sqlite3.connect(file_name)
    cur = con.cursor()
    query = "SELECT count(*) FROM hashtags WHERE "+selection+";"
    count = cur.execute(query).fetchone()[0]
    con.close()
    return count
    
    
def build_dataframe(words):
    word_counts = dict()
    for word in words:
        word_counts[word] = []
    dates = []

    file_list = [f for f in os.listdir(".") if (f.find("scrapeTwitter") != -1 and f.find(".sqlite") != -1)]
    # ---------------------------------------------------------
    # TODO: Check what is that empty symbol, it is not a space.
    # ---------------------------------------------------------
    for f in file_list:
        # Sanitize windows file name
        # file_name = f.replace('?', ' ')
        # file_date = file_name.split("scrapeTwitter_")[1].split(".sqlite")[0].replace(' ', ':')
        file_name = f
        file_date = file_name.split("scrapeTwitter_")[1].split(".sqlite")[0]
        file_date = file_date.replace('-', ' ').replace('_', '-')
        dates.append(file_date)
        # print "file date =", file_date
        for word in word_counts:
            selection = "content LIKE '% "+word+" %' AND content LIKE '%apple%'"
            count = select_count(file_name, selection)
            # print word, "=", count
            word_counts[word].append(count)
    return pd.DataFrame(data=word_counts, index=pd.DatetimeIndex(dates))


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
        d_schema = pd.io.sql.get_schema(d.reset_index(), 'data', keys='index')
        db.execute(d_schema)
    # Append the new values to the table.
    num_rows = len(dataframe)
    for i in range(num_rows):
        try:
            dataframe.iloc[i:i+1].to_sql('data', db, if_exists='append')
        except sqlalchemy.exc.IntegrityError:
            # print "skipping duplicate"
            pass
