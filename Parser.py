__author__ = 'zac'
import sqlite3
import sys
import urlparse
import os.path
import networkx as nx
class Parser:
    def __init__(self,historyFile):
        self.data = []
        self.hist_read(historyFile)
    def hist_read(self, histloc):
      #Chromium/Chrome and Firefox both use sqlite for their history,
        # IE uses what would appear to be a binary file, and Safari uses plist files for history;
        # IE and Safari may not be supported by project deadline
        histloc = os.path.abspath(os.path.expanduser(histloc))
        conn = sqlite3.connect(histloc)
        count_ff = conn.execute("SELECT COUNT(*) FROM sqlite_master WHERE tbl_name LIKE 'moz_%';").fetchall()[0][0]
        count_ch = conn.execute("SELECT COUNT(*) FROM sqlite_master WHERE name = 'downloads_url_chains';").fetchall()[0][0] #this is not ideal, but Chromium doesn't have any easy branding in the history file
        #New history sqlite formats can be added into the following conditional
        if count_ff > 0:
            self.hist_data = conn.execute("SELECT fromurl.url, tourl.url "
                                     "FROM moz_places AS tourl, moz_historyvisits AS tohist, moz_places AS fromurl, moz_historyvisits AS fromhist "
                                      "WHERE tourl.id = tohist.place_id AND fromurl.id = fromhist.place_id AND tohist.id = fromhist.from_visit;")\
                .fetchall()
        elif count_ch > 0:
            self.hist_data = conn.execute("SELECT fromurl.url, tourl.url FROM "
                                     "urls AS fromurl, visits AS fromhist, urls AS tourl, visits AS tohist "
                                     "WHERE tourl.id = tohist.url AND fromurl.id = fromhist.url AND tohist.from_visit = fromhist.id;")\
                .fetchall()
        else:
            print("Invalid file. Exiting")
            sys.exit(1)
        return self.hist_data
    def graphmaker(self):
        histcount = dict()
        for i in self.hist_data:
            #format each URL properly, exclude URLs where they are the same domain name
            #put both URLs in tuple
            fromurl = urlparse.urlparse(i[0])[1]
            tourl = urlparse.urlparse(i[1])[1]
            if fromurl == tourl:
                continue
            fromto = (fromurl, tourl)
            try:
                histcount[fromto] += 1
            except:
                histcount[fromto] = 1
        fromGraph = nx.DiGraph() #edge from a to b means a direct user to node b
        toGraph = nx.DiGraph() #edge from a to b means a is directed from node b
        for (fromurl, tourl),count in histcount.items():
            fromGraph.add_edge(fromurl, tourl,weight = count)
            toGraph.add_edge(tourl, fromurl, weight = count)
        return (fromGraph, toGraph)


