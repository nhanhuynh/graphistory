import sqlite3
import sys

#####
# Purpose of module:
# To determine what browser(s) hsitory should be pulled for, pull the data from sqlite files, and parse it to put it into a form to be used by outside modules
#####

###
# Getting history file(s)
###

def hist_read(histloc):
    #This is where reading the history file and getting the proper data in the proper order goes
    #Chromium/Chrome and Firefox both use sqlite for their history, IE uses what would appear to be a binary blob and may not be supported by project deadline, Safari currently unknown (though since it's also Webkit, I wouldn't be surprised if it's similar to Chromium)
    conn = sqlite3.connect(histloc) #I think there's a better way to do this with os.path, but this'll do for now
    #New history sqlite formats can be added into the following conditional
    if conn.execute("SELECT * FROM sqlite_master WHERE tbl_name LIKE 'moz_%';").rowcount > 0:
        hist_data = conn.execute("SELECT moz_historyvisits.id, mox_places.url, moz_places.visit_count, moz_historyvisits.from_visit FROM moz_places, moz_historyvisits WHERE moz_places.id = moz_historyvisits.place_id;").fetchall()
    else:
        print("Invalid file. Exiting")
        sys.exit(1)
    return hist_data

###
# Creating graph from data
###

#need to figure out how to take list of tuples of strings, put them together to create a useful graph
def graphmaker(hist_data):
    pass #I'll fill this in later when I know how I'm going to do that

#Testing the module, currently non-functional without graphmaker() completed
if __name__ == "__main__":
    histloc = input("What file would you like to analyze?\n")
    hist_data = hist_read(histloc)
    hist_graph = graphmaker(hist_data)
