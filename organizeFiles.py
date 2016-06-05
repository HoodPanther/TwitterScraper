import os
# import time
import utils

# timestr = time.strftime("%Y_%m_%d-%H:%M:%S")
# print timestr

# file_list = os.listdir(".")
# Reverse order to have the oldest files last
# previous_files = sorted([x for x in file_list if (x.find("scrapeTwitter_") != -1 and x.find("sqlite") != -1)], reverse=True)
# print previous_files

# Maximum number of files to keep

# max_files = 12

# if "MH370.sqlite" in file_list:
#     print "moving MH370.sqlite to scrapeTwitter_"+timestr+".sqlite"
#     os.system("mv MH370.sqlite scrapeTwitter_"+timestr+".sqlite")
#     # Check if the previous files were already 12 and if so remove the older one
#     if len(previous_files) >= max_files:
#         print "removing older files:"
#         for i in range(max_files, len(previous_files)):
#             print "rm "+previous_files[i]
#             os.system("rm "+previous_files[i])
#
#

db_name = "LNKD"

file_name = db_name+".sqlite"


# If this is the first file perform a scan and fill the db
if not os.path.isfile(db_name+"_previous.sqlite"):
    pass
    # This is the first file: find both min and max and insert a value for each count every 2 hours.
    # Start from max time and move backwards until the difference between the current time and the min
    # time is less than 2 hours. Only count full 2 hours intervals.
else:
    # Extract the latest tweet time from the previous file
    print utils.most_recent_tweet_time(file_name)
    # Analyze the new file by only counting tweets older than that time
    # Move the new file over the old file
# os.system("mv "+db_name+".sqlite "+db_name+"_previous.sqlite")