from tkinter import *
from file_modification import *
from tkinter import filedialog
from tkinter import messagebox
from fingerprint_client import *
import os


#Define a function to close the popup window
def close_win_encrypt(top, method):
    filename=""
    if unencrypted_listbox.curselection():
        for i in unencrypted_listbox.curselection():
            filename = unencrypted_listbox.get(i)
        unencrypted_listbox.delete(ANCHOR)
        encrypted_listbox.insert(END, filename)
    elif encrypted_listbox.curselection():
        for i in encrypted_listbox.curselection():
            filename = encrypted_listbox.get(i)
    else:
        return
    encrypt_file(filename, method,level_path)
    top.destroy()
#top, mytoty,filename,security_key, methods, keys
def close_win_decrypt(top, mytoty,filename,security_key, methods, keys):
    if mytoty.verify(security_key):
        if not decrypt_file(level_path,filename,methods,keys):
            messagebox.showerror("Failed decryption!", "Wrong input! File cannot be decrypted!")
        else:
            encrypted_listbox.delete(ANCHOR)
            unencrypted_listbox.insert(END, filename)
    else:
        messagebox.showerror("Failed decryption!", "Wrong input! File cannot be decrypted!")
    top.destroy()

def close_win_finger_reg(top):
    if finger_print_verify():
        top.destroy()
        sf.destroy()
        import level3
        print("pass")
    else:
        messagebox.showerror("Failed verification!", "Fail the finger print verification")
        top.destroy()

def add():
    root_path=os.path.expanduser('~')
    sf.filename = filedialog.askopenfilename(initialdir=root_path, title="Select A file", filetypes=(("text file", "*.txt"),))
    if sf.filename:
        add_file(sf.filename,level_path,2)
        unencrypted_listbox.insert(END, os.path.basename(sf.filename))

def encrypt():
    top= Toplevel(sf)
    top.geometry("300x250")
    r = StringVar()
    Radiobutton(top, text="cryptography", variable=r, value="cryptography").pack(pady="5")
    Radiobutton(top, text="aesEncrypt", variable=r, value="aesEncrypt").pack(pady="5")
    Radiobutton(top, text="xorEncrypt", variable=r, value="xorEncrypt").pack(pady="5")
    Radiobutton(top, text="rsaEncrypt", variable=r, value="rsaEncrypt").pack(pady="5")
    #Create a Button Widget in the Toplevel Window
    button= Button(top, text="OK", command=lambda:close_win_encrypt(top,r.get()))
    button.pack(pady=5, side= TOP)

def decrypt():
    if encrypted_listbox.curselection():
        filename=""
        for i in encrypted_listbox.curselection():
            filename = encrypted_listbox.get(i)
        totp = two_factor_verification(filename)
        #Create a Toplevel window
        top= Toplevel(sf)
        top.geometry("300x280")
        #Create an Entry Widget in the Toplevel window
        security_label = Label(top, text="Please enter your security key:").pack()
        entry_sk = Entry(top, width= 25)
        entry_sk.pack(pady=(5, 25))
        order_Label = Label(top, text="Please enter correct decryption order:").pack()
        entry_do= Entry(top, width= 25)
        entry_do.pack(pady=(5, 25))
        keys_Label = Label(top, text="Please enter keys in order:").pack()
        entry_key= Entry(top, width= 25)
        entry_key.pack(pady=(5, 25))
        #Create a Button Widget in the Toplevel Window
        #top,totp,mytext,entry_sk.get(),entry_do.get(),entry_key.get()
        button= Button(top, text="Enter", command=lambda:close_win_decrypt(top,totp,filename,entry_sk.get(),entry_do.get(),entry_key.get()))
        button.pack(pady=5, side= TOP)
    else:
        messagebox.showerror("Wrong Action!", "This file is not been encrypted!")

def delete():
    if unencrypted_listbox.curselection():
        for i in unencrypted_listbox.curselection():
            filename = unencrypted_listbox.get(i)
            delete_file(filename,level_path)
            unencrypted_listbox.delete(ANCHOR)
    else:
        messagebox.showerror("Wrong Action!", "You have to decrypt the file first!")

def edit():
    if unencrypted_listbox.curselection():
        for i in unencrypted_listbox.curselection():
            filename = unencrypted_listbox.get(i)
            edit_file(filename,level_path)
    else:
        messagebox.showerror("Wrong Action!", "You have to decrypt the file first!")

def enter_level3():
    #Create a Toplevel window
    top= Toplevel(sf)
    top.geometry("300x250")

    #Create an Entry Widget in the Toplevel window
    label1= Label(top , text="Finger print validation is required to enter Level 3")
    label1.pack(pady = 20)
    label2= Label(top , text="Press 'ok' button to continue")
    label2.pack(pady = 20)
    #Create a Button Widget in the Toplevel Window
    button= Button(top, text="OK", command=lambda:close_win_finger_reg(top))
    button.pack(pady=5, side= TOP)

def quit():
    sf.destroy()

sf = Tk()
sf.geometry('700x480')
sf.title('Safehouse_level2')
sf['bg']='#BB9981'
level_path = "level1/level2"
f = ("Times bold", 14)
footer_frame = Frame(sf,bg='#BB9981',height=50)
footer_frame.pack(expand=YES,fill=X,side=BOTTOM)
button_quit = Button(footer_frame, text = "QUIT", height = 2,width=7, borderwidth=3, activebackground='#345', relief="ridge",command = quit)
button_quit.pack(padx = 5,side=LEFT)
button_edit = Button(footer_frame, text = "Level 3", height = 2,width=7, borderwidth=3, activebackground='#345', relief="ridge",command = enter_level3)
button_edit.pack(padx = 5,side=RIGHT)

usernameLabel = Label(sf, bg = '#BB9981', text="Normal files", font=("Arial", 15))
usernameLabel.pack()
#expand=YES,
unencrypted_listbox = Listbox(sf, bg='#C5D8A4', fg = 'blue')
unencrypted_listbox.pack(expand=YES,fill=BOTH)
unencrypted_files_list, encrypted_files_list = show_all_files(2)
for item in unencrypted_files_list:
    unencrypted_listbox.insert(END, item)

usernameLabel = Label(sf, bg = '#BB9981', text="Encrypted files", font=("Arial", 15))
usernameLabel.pack()
encrypted_listbox = Listbox(sf, bg='#C5D8A4', fg = '#1A132F')
encrypted_listbox.pack(expand=YES,fill=BOTH)
for item in encrypted_files_list:
    encrypted_listbox.insert(END, item)

button_add = Button(sf, text = "Add", height = 2,width=1, borderwidth=3, relief="ridge",bg='#000',activebackground='#345',command = add).pack(fill=X, expand=TRUE, side=LEFT)
button_encrypt = Button(sf, text = "Encrypt", height = 2,width=1, borderwidth=3, relief="ridge",bg='#000',activebackground='#345',command = encrypt).pack(fill=X, expand=TRUE, side=LEFT)
button_decrypt = Button(sf, text = "Decrypt", height = 2,width=1, borderwidth=3, relief="ridge",bg='#000',activebackground='#345',command = decrypt).pack(fill=X, expand=TRUE, side=LEFT)
button_delete = Button(sf, text = "Delete", height = 2,width=1, borderwidth=3, relief="ridge",bg='#000',activebackground='#345',command = delete).pack(fill=X, expand=TRUE, side=LEFT)
button_edit = Button(sf, text = "Edit", height = 2,width=1, borderwidth=3, relief="ridge",bg='#000',activebackground='#345',command = edit).pack(fill=X, expand=TRUE, side=LEFT)
#button_level = Button(sf, text = "Enter Level3", command = enter_evel3).pack(fill=X, expand=TRUE, side=BOTTOM,pady=5)
sf.mainloop()