graphistory
===========

Project for CS410/510 Quantified Life, Fall 2013 by David Harwood, Nhan Huynh, Ruri McMurray, Sanjukta Sen

This project reads in a history file provided by either Firefox or Chrome/Chromium, pulls chronological data for history, then generates a graph displaying the sites that have been visited from the selected node. Each node in the graph is sized according to how many times it has been visited from the selected node, where the larger the node, the more often the user has visited that site from the selected site.

The project can be run with the command <pre>python2 filegui.py</pre>
This will bring up a small GUI where the user can choose the file to analyze, the site to use as the selected node, whether the user wants to display edges coming FROM that node to other nodes or going TO the selected node from other nodes, and the maximum number of nodes that will be shown in the graph to keep from slowing down the machine.

Sources
-------

For this project, we draw out graphs with the libraries matplotlib, pygraphviz, and networkx, all of which can be accessed from the official Python Package Index at https://pypi.python.org/pypi. Note that the version of Python required is 2.6+, due to the pygraphviz not supporting python version 3+.
Data used in pictures provided in the repo come from group members' web browsing.

Internal
--------

After parsing the history, hist\_read will transform the data into a list of format ((fromurl, tourl), count) tuples.  Then the graph\_make function will loop through each element in the list and transform the list into two graphs called fromGraph and toGraph. In fromGraph an edge (u,v) with weight w means that site u was accessed right before visiting site v w times. In toGraph, an edge (u,v) with weight w means that the user visit site u right after he visit site v w times.
The program allows the user to specify a website and then draw the graph with this website as the main node. By main node, we mean that the graph only contains edges(u,x) where u is the website user specifies. User can also choose whether they want from or to graph. Depend on user’s choice, the draw function will transform either fromGraph or toGraph mention above into subgraph containing only edges(u,x). Then it’ll called to draw function of networkx library to draw this subgraph.
The GUI is constructed with Tk, libraries for which are provided as part of a default Python installation.

Current Issues
--------------

Currently, pages that are visited in sequence in the same browser session and those that are visited with the browser closed and reopened between visits are not distinguished due to having no way to really tell (as far as we know) when the browser was exited from outside the browser. It would be possible to be able to determine when a browser is open and when it isn't, but it would likely require an extension running inside the browser, which is beyond the scope of this project
