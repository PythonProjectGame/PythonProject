import customtkinter as ctk
import bcrypt
import mysql.connector
from PIL import Image

class windows(ctk.CTk):  # main class inherits from tkinter window class
    font1 = ('garamond', 15)
    font2 = ('garamond', 10)

    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self)
        self.wm_title('Main Project')
        self.geometry('500x500')
        ctk.set_default_color_theme('dark-blue')

        self.bind('<Configure>', lambda e: self.configurescreen())

        self.bgimage = ctk.CTkImage(
            light_image=Image.open('Background.png'), 
            dark_image=Image.open('Background.png'),
            size=(self.winfo_width(), self.winfo_height())
        )
        
        self.mylabel = ctk.CTkLabel(
            self,
            text='',
            image=self.bgimage, 
            width=self.winfo_width(), 
            height=self.winfo_height()
        )
        self.mylabel.place(relx=0, rely=0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)


        self.frames = {}
        for F in (LoginPage, LoggedIn, NewAccount):
            frame = F(self)

            self.frames[F] = frame
            frame.grid(row=1, column=1, sticky='nsew')
                    
        self.show_frame(LoginPage)
            
    def show_frame(self, cont):  # function to raise a frame to the top so that it is visible
        frame = self.frames[cont]
        frame.tkraise()
    
    def configurescreen(self):
        self.minsize(
            width=max(self.frames[i].winfo_height() for i in self.frames),
            height=max(self.frames[i].winfo_height() for i in self.frames)
        )

        self.bgimage.configure(
            size=(self.winfo_width(), self.winfo_height())
            )

        self.mylabel.configure(
            width=self.winfo_width(), 
            height=self.winfo_height(), 
            image=self.bgimage
            )
        self.mylabel.place(relx=0, rely=0, anchor='nw')


class LoginPage(ctk.CTkFrame):  # first frame which is shown: main login screen
    def __init__(self, parent):  # initialises with parent location and the controller
        self.parent = parent
        ctk.CTkFrame.__init__(self, self.parent)

        self.parent.bind('<Return>', lambda e: self.login())

        self.username = ctk.CTkEntry(
            self, 
            placeholder_text='Username', 
            corner_radius=16,
            font=windows.font1
        )
        self.username.grid(row=0, column=0, sticky='we', padx=5, pady=5)

        self.password = ctk.CTkEntry(
            self, 
            placeholder_text='Password', 
            show='*',  
            corner_radius=16,
            font=windows.font1
        )
        self.password.grid(row=1, column=0, sticky='we', padx=5, pady=5)

        login_button = ctk.CTkButton(
            self, 
            text='Login', 
            command=self.login,
            font=windows.font1
        )
        login_button.grid(row=2, column=0, sticky='we', padx=5, pady=5)

        new_account = ctk.CTkLabel(
            self,
            text='New to MainProject?\nApply for a New Account',
            font=windows.font2,
            cursor='hand2',
            text_color='blue',
        )
        new_account.grid(row=4, column=0, padx=5)
        new_account.bind('<Button-1>', lambda e: self.parent.show_frame(NewAccount))


    def login(self):
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Skyla1234',
            database='mydatabase'
        )
        mycursor = mydb.cursor()  # cursor used to run sql quiries
        mycursor.execute(f'select Salt from Userdata where Username = \'{self.username.get()}\'')

        try:
            salt = mycursor.fetchone()[0].encode()
        except TypeError:
            self.clear()
            return

        # returns values for which username and password are correct
        mycursor.execute(f'select * from UserData\
                 where Username=\'{self.username.get()}\' \
                 and Password=\'{bcrypt.hashpw(self.password.get().encode(), salt).decode()}\'')

        if mycursor.fetchall():
            self.parent.show_frame(LoggedIn)  # shows logged in page
        else:
            self.clear()

        mydb.close()
    
    def clear(self):
        self.username.delete(0, 'end')
        self.username.configure(placeholder_text='Username')
        self.password.delete(0, 'end')
        self.password.configure(placeholder_text='Password')


class LoggedIn(ctk.CTkFrame):
    def __init__(self, parent):
        self.parent = parent
        ctk.CTkFrame.__init__(self, self.parent)


class NewAccount(ctk.CTkFrame):
    def __init__(self, parent):
        self.parent = parent
        ctk.CTkFrame.__init__(self, self.parent)

        self.newemail = ctk.CTkEntry(
            self,
            placeholder_text='Email',
            font=windows.font1,
            corner_radius=16
        )
        self.newemail.grid(row=0, column=0, padx=5, pady=5)

        self.newusername = ctk.CTkEntry(
            self,
            placeholder_text='Username',
            font=windows.font1,
            corner_radius=16
        )
        self.newusername.grid(row=1, column=0, padx=5, pady=5)

        self.newpassword = ctk.CTkEntry(
            self,
            placeholder_text='Password',
            font=windows.font1,
            corner_radius=16
        )
        self.newpassword.grid(row=2, column=0, padx=5, pady=5)

        self.apply = ctk.CTkButton(
            self,
            corner_radius=16,
            text='Apply',
            font=windows.font1
        )
        self.apply.grid(row=4, column=0, padx=5, pady=5)


a = windows()
a.mainloop()

