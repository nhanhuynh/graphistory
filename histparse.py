import sqlite3
import sys
import urllib.parse
import os.path

#####
# Purpose of module:
# To determine what browser(s) hsitory should be pulled for, pull the data from sqlite files, and parse it to put it into a form to be used by outside modules
#####

###
# Get history file and extracting data
# takes: history file from a web browser in sqlite format (currently, only Firefox is supported)
# returns: list of tuples from output of SQL query
###

def hist_read(histloc):
    #Chromium/Chrome and Firefox both use sqlite for their history, IE uses what would appear to be a binary file, and Safari uses plist files for history; IE and Safari may not be supported by project deadline
    histloc = os.path.abspath(os.path.expanduser(histloc))
    conn = sqlite3.connect(histloc)
    count_ff = conn.execute("SELECT COUNT(*) FROM sqlite_master WHERE tbl_name LIKE 'moz_%';").fetchall()[0][0]
    count_ch = conn.execute("SELECT COUNT(*) FROM sqlite_master WHERE name = 'downloads_url_chains';").fetchall()[0][0] #this is not ideal, but Chromium doesn't have any easy branding in the history file
    #New history sqlite formats can be added into the following conditional
    if count_ff > 0:
        hist_data = conn.execute("SELECT moz_places.url FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id ORDER BY moz_historyvisits.visit_date ASC;").fetchall()
    elif count_ch > 0:
        hist_data = conn.execute("SELECT urls.url FROM urls, visits WHERE urls.id = visits.url ORDER BY visits.visit_time ASC;").fetchall()
    else:
        print("Invalid file. Exiting")
        sys.exit(1)
    return hist_data

###
# Create graph from data
# takes: list of tuples of output from SQL query
# returns: list of tuples of form ((fromurl, tourl), count)
###

def graphmaker(hist_data):
    histcount = dict()
    for i in range(len(hist_data) - 1): #strange range to make sure we stay in the bounds of the list
        #format each URL properly, exclude URLs where they are the same domain name
        #put both URLs in tuple
        fromurl = urllib.parse.urlparse(hist_data[i][0])[1]
        tourl = urllib.parse.urlparse(hist_data[i+1][0])[1]
        if fromurl == tourl:
            continue
        fromto = (fromurl, tourl)
        try:
            histcount[fromto] += 1
        except:
            histcount[fromto] = 1
    return list(histcount.items())

#This is for testing the module, feel free to ignore/tweak/whatever to do any kind of testing
if __name__ == "__main__":
    histloc = os.path.expanduser(input("What file would you like to analyze?\n"))
    hist_data = hist_read(histloc)
    hist_graph = graphmaker(hist_data)
    print(hist_graph)
