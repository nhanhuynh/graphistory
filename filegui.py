from histparse import histparse
import Tkinter as tk
import tkFileDialog
import tkMessageBox
import ttk
from Graphistory import Graphistory

window = tk.Tk()
window.title("Graphistory")
window.resizable(False, False)
top = window.winfo_toplevel()
top.rowconfigure(0, weight=1)
top.columnconfigure(0, weight=1)
mframe = ttk.Frame(window, padding='0.5c')
mframe.grid(column=0, row=0)
mframe.columnconfigure(0, weight=1)
mframe.columnconfigure(3, pad='1.75i')
mframe.rowconfigure(0,weight=1)

path = tk.StringVar()
url = tk.StringVar()
path_entry = ttk.Entry(mframe, textvariable=path, width=50)
url_entry = ttk.Entry(mframe, textvariable=url, width=50)

def browse_win():
    #open file browser window
    #choose file
    #put path to file in path_entry
    pathtmp = tkFileDialog.askopenfilename()
    path.set(pathtmp)

browse_button = ttk.Button(mframe, text="Browse", command=browse_win)

def drawgraph(fileloc=''):
    #grab path from path_entry
    #run it through histparse
    #call function to draw graph
    try:
        if fileloc == '': fileloc = str(path.get())
        histgraph = histparse(fileloc)
        #need to pass histgraph to networkx functions
        #print(histgraph)
        g = Graphistory(fileloc)
        urlfrom = str(url.get())
        if(urlfrom == ''):
            g.draw_from_site("facebook.com")
        else:
            g.draw_from_site(urlfrom)
    except Exception as e:
        tkMessageBox.showerror(message=e)
    pass

confirm_button = ttk.Button(mframe, text="Draw!", command=drawgraph)

path_entry.bind('<Return>', lambda e: drawgraph())

browse_button.grid(column=1, row=4, padx='1c', pady='0.25c', sticky=tk.E+tk.W)
confirm_button.grid(column=5, row=4, padx='1c', pady='0.25c', sticky=tk.E+tk.W)
path_entry.grid(column=1,row=2,padx='1c', pady='0.5c', columnspan=5, sticky=tk.E+tk.W+tk.N+tk.S)
url_entry.grid(column=1, row=6, padx='1c', pady='0.5c', columnspan=5, sticky=tk.E+tk.W)
path_entry.focus()

window.mainloop()
