import histparse
import Tkinter as tk
import tkFileDialog
import ttk

window = tk.Tk()
window.title("Graphistory")
mframe = ttk.Frame(window)
mframe.grid(column=0, row=0)
mframe.columnconfigure(0, weight=1)
mframe.rowconfigure(0,weight=1)

path = tk.StringVar()
path_entry = ttk.Entry(mframe, textvariable=path) #need to add size and function when <return> is pushed, sothis needs to be worked with...

def browse_win():
    #open file browser window
    #choose file
    #put path to file in path_entry
    pathtmp = tkFileDialog.askopenfilename()
    path.set(pathtmp)

browse_button = ttk.Button(mframe, text="Browse", command=browse_win) #...as does this

def drawgraph():
    #grab path from path_entry
    #run it through histparse
    #call function to draw graph
    pass

confirm_button = ttk.Button(mframe, text="Draw!", command=drawgraph) #this part is just flat-out broken, I NEED to get info from Nhan on how his code is going together

path_entry.grid()
browse_button.grid()
confirm_button.grid()

window.mainloop()
