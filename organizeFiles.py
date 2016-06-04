import os
import time

timestr = time.strftime("%Y_%m_%d-%H:%M:%S")
# print timestr

file_list = os.listdir(".")
# Reverse order to have the oldest files last
previous_files = sorted([x for x in file_list if (x.find("scrapeTwitter_") != -1 and x.find("sqlite") != -1)], reverse=True)
# print previous_files

# Maximum number of files to keep

max_files = 12

if "MH370.sqlite" in file_list:
    print "moving MH370.sqlite to scrapeTwitter_"+timestr+".sqlite"
    os.system("mv MH370.sqlite scrapeTwitter_"+timestr+".sqlite")
    # Check if the previous files were already 12 and if so remove the older one
    if len(previous_files) >= max_files:
        print "removing older files:"
        for i in range(max_files, len(previous_files)):
            print "rm "+previous_files[i]
            os.system("rm "+previous_files[i])
