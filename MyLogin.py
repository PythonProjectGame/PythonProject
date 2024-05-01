import customtkinter as ctk
import bcrypt
import mysql.connector
from PIL import Image

# main class inherits from tkinter window class
class windows(ctk.CTk):
    # constant fonts for buttons and lables
    font1 = ('garamond', 15)
    font2 = ('garamond', 10)

    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)

        # initial setup of screen
        self.wm_title('Main Project')
        self.geometry('500x500')
        ctk.set_default_color_theme('dark-blue')

        # runs self.configurescreen each time the screen size changes
        self.bind('<Configure>', lambda e: self.configurescreen())

        # uploads an image for the background
        self.bgimage = ctk.CTkImage(
            light_image=Image.open('Background.png'), 
            dark_image=Image.open('Background.png'),
            size=(self.winfo_width(), self.winfo_height())
        )
        
        # creates a labek which holds the background image
        self.mylabel = ctk.CTkLabel(
            self,
            text='',
            image=self.bgimage, 
            width=self.winfo_width(), 
            height=self.winfo_height()
        )
        self.mylabel.grid(
            row=0,
            column=0,
            rowspan=3,
            columnspan=3,
            sticky='nsew'
        )

        # weights the first and third columns and rows to centre the frames
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # creates a dictionary of frames via classes
        self.frames = {}
        for F in (LoginPage, LoggedIn, NewAccount):
            frame = F(self, fg_color='#FFFFFF', bg_color='#FFFFFF')

            self.frames[F] = frame
            frame.grid(row=1, column=1, sticky='nsew')
            
        # shows loginpage
        self.show_frame(LoginPage)

    # function to raise a frame to the top so that it is visible
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    # function which resizes the bg
    def configurescreen(self):
        # sets minimum size of the window to the biggest frame
        self.minsize(
            width=max(self.frames[i].winfo_height() for i in self.frames),
            height=max(self.frames[i].winfo_height() for i in self.frames)
        )

        self.bgimage.configure(
            size=(self.winfo_width(), self.winfo_height())
        )

# first frame which is shown: main login screen
class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent

        # initialises frame
        ctk.CTkFrame.__init__(self, self.parent, *args, **kwargs)

        # binds the return key to the login function
        self.parent.bind('<Return>', lambda e: self.login())

        # entries for username and password with login button
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

        # links a label to the new account page
        new_account = ctk.CTkLabel(
            self,
            text='New to MainProject?\nApply for a New Account',
            font=windows.font2,
            cursor='hand2',
            text_color='blue',
        )
        new_account.grid(row=4, column=0, padx=5)
        new_account.bind('<Button-1>', lambda e: self.parent.show_frame(NewAccount))

    # runs the sql data base to check login credentials
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
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        ctk.CTkFrame.__init__(self, self.parent)


class NewAccount(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
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

