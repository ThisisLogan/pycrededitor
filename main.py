from cgitb import text
import json
from tkinter import *
from tkinter import ttk
import getpass
updated_count = 0


def main():

    root = Tk()
    frm = ttk.Frame(root, padding=100)
    root.title("Creds editor")
    global credfile
    credfile = open("creds.json")
    width=600
    height=500
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(alignstr)
    root.resizable(width=False, height=False)
    global data
    data = json.load(credfile)
    colm = 0
    game_frame = Frame(root)
    game_frame.pack()

    table_data = ttk.Treeview(game_frame)
    game_scroll = Scrollbar(game_frame)
    game_scroll.pack(side=RIGHT, fill=Y)

    game_scroll = Scrollbar(game_frame,orient='horizontal')
    game_scroll.pack(side= BOTTOM,fill=X)

    table_data = ttk.Treeview(game_frame,yscrollcommand=game_scroll.set, xscrollcommand =game_scroll.set)
    game_scroll.config(command=table_data.yview)
    game_scroll.config(command=table_data.xview)

    table_data.pack()

    table_data['columns'] = ('Username', 'Password', 'Method')
    table_data.column("Username", anchor=W,width=80)
    table_data.column("Password",anchor=W, width=80)
    table_data.column("Method",anchor=CENTER,width=80)

    table_data.heading("Username",text="Laptop Name",anchor=CENTER)
    table_data.heading("Password",text="Password",anchor=CENTER)
    table_data.heading("Method",text="Method",anchor=CENTER)

    def refresh_table(data):
        for i in table_data.get_children():
            table_data.delete(i)
        for i in data:
            label=Label(root, text="", font=("Courier 22 bold"))
            label.pack()
            for n in data[i][1]:
                if data[i][1]["method"] == 1:
                    table_data.insert(parent='',index='end',text='',values=(i,data[i][0]["password"],"Update"))
                else:
                    table_data.insert(parent='',index='end',text='',values=(i,data[i][0]["password"],data[i][1]["method"]))

    def check_creds_name(name):
        try:
            return data[name]
        except KeyError:
            return False

    # load data into table
    refresh_table(data)


    def search_laptop():
        string = search_entry
        if check_creds_name(string) == False:
            search_label["text=Name does not exist"]
        else:
            # search = Entry(root, width=40, text=("Password: ",check_creds_name(string))).place(x=200,y=300)
            search_label.configure(text=("Password: ",check_creds_name(string)))

    # search.focus_set()


    global add_username
    global add_password
    global add_method

    Label(root, text="Username").place(x=40, y=280)
    add_username = Entry(root)
    add_username.focus_set() 
    add_username["borderwidth"] = "1px"
    add_username.place(x=40, y=300)
    Label(root, text="Password").place(x=40, y=330)
    add_password = Entry(root)
    
    # add_password.focus_set() 
    add_password["borderwidth"] = "1px"
    add_password.place(x=40, y=350)
    Label(root, text="Method").place(x=40, y=380)
    add_method = IntVar()
    R1 = Radiobutton(root, text="Updater", variable=add_method, value=1)
    R1.place(x=40, y=400)
    # add_method = Entry(root)
    # # add_method.focus_set() 
    # add_method["borderwidth"] = "1px"
    # add_method.place(x=40, y=400)

    
    def add_entry():
        global updated_count
        global entry_label
        if add_username.get() == '':
            print("empty")
            return
        else:
            # uname = add_username.get()
            # password = add_password.get()
            # method = add_method.get()
            # print(uname, password, method)
            if updated_count == 0:
                updated_label_count = "Updated!"
                updated_count = updated_count + 1
            else:
                updated_label_count = "Updated! x{}".format(updated_count)
                updated_count = updated_count + 1
            entry_data = {add_username.get().lower():[{"password":add_password.get()},{"method": add_method.get()}]}
            entry_label = Label(root, text=updated_label_count).place(x=40,y=260)
            data.update(entry_data)
            credwrite = open("creds.json", "w+")
            # credfile.close()
            # credfile = open("creds.json","w+")
            credwrite.write(json.dumps(data))
            credwrite.close()
            credfile.seek(0)
            refresh_table(data)
            # credfile.close()
            # credfile = open("creds.json")

    global search_label
    search_entry = Entry(root, width=40, text="Search").place(x=200,y=300)
    search_label = Label(root, text='').place(x=290,y=260)
    ttk.Button(root, text= "Search",width= 20, command= search_laptop).place(x=250, y=450)
    add_entry_button = ttk.Button(root) 
    add_entry_button["text"] = "Add/Edit Entry"
    add_entry_button.place(x=40, y=450)
    add_entry_button["command"] = add_entry

    ttk.Button(root, text="Quit", command=root.destroy).place(x=500, y=450)
    root.mainloop()
    


    credfile.close

# Check if username is in allowed_users file
checkuser = getpass.getuser()

with open("allowed_users.txt") as f:
    if checkuser in f.read():
        main()
    else:
        print("Not Allowed")