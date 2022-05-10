# SOURCE FILE:    LocalSafeHouse.py
# PROGRAM:        LocalSafeHouse application
# FUNCTIONS:      entrance of the application
#                 1. login page
#                 2. registration page
#
# Last Update:    March 18, 2022
# version:        1.0
# DESIGNER:       Yuheng Song A00971421
# PROGRAMMER:     Yuheng Song A00971421
#---------------------------------------------------------------------------------
from tkinter import *
from stego_photo import *
from tkinter import messagebox
from tkinter import filedialog
import time

f = ("Times bold", 14)
attempt_counter = 0

def validateLogin(username, password):
    global attempt_counter
    if attempt_counter < 3:
        name = username_login_entry.get()
        password = password__login_entry.get()
        user_name = get_username()
        if name == user_name:
            user_password = xor_decryption(get_password(), get_key())
            if password == user_password:
                login_screen.destroy()
                import level1
            else:
                attempt_counter+=1
                messagebox.showerror("Failed verification", "Wrong username or password!")
        else:
            attempt_counter+=1
            messagebox.showerror("Failed verification", "Wrong username or password!")
    if attempt_counter == 3:
        messagebox.showerror("Failed verification", "Already tried 3 times! Please try again after 5 minutes!")
        login_btn['state'] = DISABLED
        login_screen.update()
        time.sleep(180)
        login_btn['state'] = NORMAL
        login_screen.update()
        attempt_counter = 0

# write user's registration inputs into config file
def insert(page, name, password, email):
    global photo_name
    counter = load_encode_images(photo_name)
    photo_key = str(counter)
    regi_insert(name, password, email, photo_key)
    messagebox.showinfo("Info", "Registration success, please open App again and login!")
    page.destroy()
    login_screen.destroy()

# record the photo name and path that user upload
def add_photo():
    root_path=os.path.expanduser('~')
    filename = filedialog.askopenfilename(initialdir=root_path, title="Select A file", filetypes=(("png photo file", "*.png"),))
    if filename:
        global photo_name
        photo_name = filename
    else:
        messagebox.showwarning("Warning", "You need to upload you photo!")

# show registration form
def register():
    #Create a Toplevel window
    regi= Toplevel(login_screen)
    regi.geometry("400x300")
    # create a Form label
    heading = Label(regi, text="Registration Form",font=("Arial", 15))
    # create a Name label
    name = Label(regi, text="Name")
    # create a password label
    password = Label(regi, text="Password")
    # create a email label
    email = Label(regi, text="Email")

    heading.grid(row=0, column=1,ipady="10")
    name.grid(row=1, column=0,ipady="10")
    password.grid(row=2, column=0,ipady="10")
    email.grid(row=3, column=0,ipady="10")

    name_field = Entry(regi)
    password_field = Entry(regi,show= '*')
    email_field = Entry(regi)

    name_field.grid(row=1, column=1, ipadx="100")
    password_field.grid(row=2, column=1, ipadx="100")
    email_field.grid(row=3, column=1, ipadx="100")
    photo_name=StringVar()
    upload_photo = Button(regi, text="Upload Photo", width=10, height=2,borderwidth=3, relief="ridge", command=add_photo)
    upload_photo.grid(row=5, column=1)

    submit = Button(regi, text="Submit", width=10, height=2,borderwidth=3, relief="ridge", command=lambda:insert(regi, name_field.get(),password_field.get(),email_field.get()))
    submit.grid(row=8, column=1)


login_screen=Tk()
login_screen.title("Safehouse_login")
login_screen.geometry("400x300")
Label(login_screen, text="Please enter login details",font=("Arial", 20)).pack()
Label(login_screen, text="").pack()
Label(login_screen, text="Username").pack()
username_login_entry = Entry(login_screen, borderwidth=1, textvariable="username")
username_login_entry.pack()
username = StringVar()
Label(login_screen, text="").pack()
Label(login_screen, text="Password").pack()
password__login_entry = Entry(login_screen, textvariable="password",borderwidth=1, show= '*')
password__login_entry.pack()
password = StringVar()
Label(login_screen, text="").pack()
login_btn = Button(login_screen, text="Login", width=10, height=1,borderwidth=3, relief="ridge",command =lambda:validateLogin(username,password))
login_btn.pack(pady = "10")
regi_btn = Button(login_screen, text="Register", width=10, height=1,borderwidth=3, relief="ridge",command = register)
regi_btn.pack(pady = "10")
login_screen.mainloop()