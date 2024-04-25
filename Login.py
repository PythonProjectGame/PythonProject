import tkinter as tk
import mysql.connector
import bcrypt

'''
Login Screen using tkinter classes.

Main class windows handles the other 3 frame classes which hold the buttons and entry boxes which will beused to 
accept credentials.

Once logged in you will be placed on a screen which will allow you to change settings for the game, start the game, 
change your username and password, connect an email address to the game and delete your account.

The new account page will need a username and password, agree to terms and conditions text box along with a hyperlink 
to the terms and conditions page so that data and security of the connection doesnt cause problems.'''


class windows(tk.Tk):  # main class inherits from tkinter window class
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)  # running tkinter initial as it has been inherited
        self.wm_title('Main Project')
        self.minsize(width=500, height=500)

        container = tk.Frame(self, height=400, width=600)  # container for the frames which will be used later
        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}  # list of frame objects
        for F in (LoginPage, LoggedIn, NewAccount):  # list of the frame names
            frame = F(container, self)  # declares the frame with parent and the controller

            self.frames[F] = frame  # hold the object in the dictionary
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(LoginPage)  # shows the main login screen

    def show_frame(self, cont):  # function to raise a frame to the top so that it is visible
        frame = self.frames[cont]
        frame.tkraise()


class LoginPage(tk.Frame):  # first frame which is shown: main login screen
    def __init__(self, parent, controller):  # initialises with parent location and the controller
        tk.Frame.__init__(self, parent)  # frame initialisation from tkinter as it is inherited
        tk.Label(self, text='Username:').grid(row=0, column=0, padx=10, pady=10)  # username label
        tk.Label(self, text='Password:').grid(row=1, column=0, padx=10, pady=10)  # password label

        self.controller = controller  # makes the controller parameter public in the class to be used by all functions

        self.username = tk.Entry(self)  # username entry box
        self.username.grid(row=0, column=1)

        self.password = tk.Entry(self, show='*')  # password entry box
        self.password.grid(row=1, column=1)

        # button to log in using login function
        login_button = tk.Button(
            self,
            text='Login',
            command=self.login,
            width=10
        )
        login_button.grid(row=2, column=0)

        # funtion to clear the entry boxes
        clear_button = tk.Button(
            self,
            text='clear',
            command=self.clear,
            width=10
        )
        clear_button.grid(row=2, column=1)

        # new account button allows to create a new account with username and password
        # by using a hyperlinked label
        new_account = tk.Label(self, text='New account', fg='blue', cursor='hand2')
        new_account.grid(row=4, column=0, pady=10, padx=5, columnspan=2)
        new_account.bind("<Button-1>", lambda e: self.controller.show_frame(NewAccount))  # binds function to label

    def login(self):  # function which checks the username and password
        # opens an sql database which holds usernames and passwords
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Skyla1234',
            database='mydatabase'
        )
        mycursor = mydb.cursor()  # cursor used to run sql quiries
        mycursor.execute(f'select Salt from Userdata where Username = \'{self.username.get()}\'')
        salt = mycursor.fetchone()[0].encode()

        # returns values for which username and password are correct
        mycursor.execute(f'select * from UserData\
                 where Username=\'{self.username.get()}\' \
                 and Password=\'{bcrypt.hashpw(self.password.get().encode(), salt).decode()}\'')

        if mycursor.fetchall():
            self.controller.show_frame(LoggedIn)  # shows logged in page
        else:
            self.clear()

        mydb.close()

    def clear(self):  # function to clear entry boxes so that the code can stay readable and concise
        self.username.delete(0, 'end')
        self.password.delete(0, 'end')


class LoggedIn(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Logged in')
        label.grid(row=0, column=0, padx=10, pady=10)
        switch_window_button = tk.Button(
            self,
            text='Go to the Completion Screen',
            command=lambda: controller.show_frame(LoginPage),
        )

        switch_window_button.grid(row=1, column=0)


class NewAccount(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk.Label(self, text='Username:').grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self, text='Password:').grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self, text='Re-Enter Password:').grid(row=2, column=0, padx=10, pady=10)

        self.controller = controller  # makes controller public across the class

        self.newname = tk.Entry(self)  # username entry box
        self.newname.grid(row=0, column=1)

        self.newpass = tk.Entry(self, show='*')  # password entry box
        self.newpass.grid(row=1, column=1)

        self.renewpass = tk.Entry(self, show='*')  # password entry box
        self.renewpass.grid(row=2, column=1)

        switch_window_button = tk.Button(
            self,
            text='Create New Account',
            command=self.createAccount,
        )
        switch_window_button.grid(row=3, column=0, columnspan=2)

    def createAccount(self):
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Skyla1234',
            database='mydatabase'
        )
        mycursor = mydb.cursor()
        mycursor.execute(f'select * from UserData where Username=\'{self.newname.get()}\'')
        if mycursor.fetchall():
            self.clear()
            return

        if self.newpass.get() != self.renewpass.get():
            self.clear()
            return

        #  mycursor2 = mydb.cursor()
        sql = 'insert into UserData (Username, Password)\
         values (%s, %s)'
        val = (f'{self.newname.get()}', f'{self.newpass.get()}')
        mycursor.execute(sql, val)
        mydb.commit()
        self.controller.show_frame(LoginPage)

    def clear(self):  # function to clear entry boxes so that the code can stay readable and concise
        self.newname.delete(0, 'end')
        self.newpass.delete(0, 'end')
        self.renewpass.delete(0, 'end')


a = windows()
a.mainloop()
