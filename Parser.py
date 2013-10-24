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
            raise sqlite3.DatabaseError("Database is not recognized browser history file.")
            print("Invalid file. Exiting")
            sys.exit(1)

        self.hist_data = hist_data

    def urlformat(self, url):
        try:
            temp = list(reversed(urlparse.urlparse(url)[1].split(".")))
            out = temp[1] + '.' + temp[0]
            return (out if ((len(out) > 5 and not temp[0].isdigit()) or out == "x.org") else (".".join(reversed(temp)) if temp[0].isdigit() else temp[2] + '.' + out)) #This line recognizes country codes, IPv4 addresses, and the exception that is x.org
        except:
            raise NameError("malformed URL")

    def graphmaker(self):
        histcount = dict()
        for i in range(len(self.hist_data) - 1): #strange range to make sure we stay in the bounds of the list
            #format each URL properly, exclude URLs where they are the same domain name
            #put both URLs in tuple
            try:
                fromurl = self.urlformat(self.hist_data[i][0])
                tourl = self.urlformat(self.hist_data[i+1][0])
                if fromurl == tourl:
                    continue
                fromto = (fromurl, tourl)
                try:
                    histcount[fromto] += 1
                except:
                    histcount[fromto] = 1
            except NameError:
                continue
        fromGraph = nx.DiGraph() #edge from a to b means a direct user to node b
        toGraph = nx.DiGraph() #edge from a to b means a is directed from node b
        for (fromurl, tourl),count in histcount.items():
            fromGraph.add_edge(fromurl, tourl,weight = count)
            toGraph.add_edge(tourl, fromurl, weight = count)
        print histcount.items(), "hello"
        return (fromGraph, toGraph)


