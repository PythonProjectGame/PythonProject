from tkinter import messagebox
import tkinter as tk
import MyVal
import pickle
import socket


# main class inherits from tkinter window class
class windows(tk.Tk):
    # constant fonts for buttons and lables

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # initial setup of screen
        self.wm_title("Main Project")
        self.geometry("500x500")

        # setting background
        self.config(bg="#2e9e80")

        # weights the first and third columns and rows to centre the frames
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # creates a dictionary of frames via classes
        self.frames = {}
        for F in (LoginPage, LoggedIn, NewAccount):
            frame = F(self)

            self.frames[F] = frame
            frame.grid(row=1, column=1, sticky="nsew")

        # shows loginpage
        self.show_frame(LoginPage)

        # sets minimum size of the window to the biggest frame
        self.minsize(
            width=max(self.frames[i].winfo_height() for i in self.frames),
            height=max(self.frames[i].winfo_height() for i in self.frames),
        )

    # function to raise a frame to the top so that it is visible
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# first frame which is shown: main login screen
class LoginPage(tk.Frame):
    def __init__(self, parent: object, *args, **kwargs) -> None:
        self.parent = parent

        # initialises frame
        tk.Frame.__init__(self, self.parent, *args, **kwargs)

        # binds the return key to the login function
        self.parent.bind("<Return>", lambda e: self.login())

        # entries for username and password with login button
        self.uservar = tk.StringVar(value="Username")
        self.username = tk.Entry(self, textvariable=self.uservar)
        self.username.grid(row=0, column=0, sticky="we", padx=5, pady=5)
        self.username.bind("<FocusIn>", lambda e: self.on_click(1))
        self.username.bind("<FocusOut>", lambda e: self.focus_out(1))

        self.passvar = tk.StringVar(value="Password")
        self.password = tk.Entry(self, textvariable=self.passvar)
        self.password.grid(row=1, column=0, sticky="we", padx=5, pady=5)
        self.password.bind("<FocusIn>", lambda e: self.on_click(2))
        self.password.bind("<FocusOut>", lambda e: self.focus_out(2))

        login_button = tk.Button(self, text="Login", command=self.login)
        login_button.grid(row=2, column=0, sticky="we", padx=5, pady=5)

        # links a label to the new account page
        new_account = tk.Label(
            self, text="New to MainProject?\nApply for a New Account", cursor="hand2"
        )
        new_account.config(font=("Arial", 2, "bold"))
        new_account.grid(row=4, column=0, padx=5)
        new_account.bind("<Button-1>", lambda e: self.parent.show_frame(NewAccount))

    def clear(self) -> None:
        self.username.delete(0, "end")
        self.password.delete(0, "end")

    def on_click(self, entry: int) -> None:
        match entry:
            case 1:
                if self.uservar.get() == "Username":
                    self.uservar.set("")
            case 2:
                if self.passvar.get() == "Password":
                    self.passvar.set("")
                    self.password.config(show="*")

    def focus_out(self, entry: int) -> None:
        match entry:
            case 1:
                if self.uservar.get() == "":
                    self.uservar.set("Username")
            case 2:
                if self.passvar.get() == "":
                    self.passvar.set("Password")
                    self.password.config(show="")

    # runs the sql data base to check login credentials with validation
    def login(self) -> None:
        pswd = self.passvar.get()
        user = self.uservar.get()

        if all([user == "Username", pswd == "Password"]):
            user = ""
            pswd = ""

        if all([MyVal.present(user), MyVal.present(pswd)]):
            pass
        else:
            messagebox.showwarning(
                title="Warning", message="Please enter a Username and Password"
            )
            return

        if all([MyVal.length(user, (4, 10), 4), MyVal.length(pswd, (6, 12), 4)]):
            pass
        else:
            messagebox.showwarning(
                title="Warning", message="Username or Password are of an invalid length"
            )
            self.clear()
            return

        try:
            host = "127.0.0.1"
            port = 5555

            login = socket.socket()
            login.connect((host, port))

            data = ["Login", self.username.get(), self.password.get()]
            data = pickle.dumps(data)
            login.send(data)

            indata = login.recv(1024)
            indata = pickle.loads(indata)
            print(indata)

            # login.close()

        except ConnectionRefusedError:
            messagebox.showwarning(
                title="Warning", message="Server is down, please try again later"
            )


class LoggedIn(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        tk.Frame.__init__(self, self.parent)


class NewAccount(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        self.newemail = tk.Entry(self)
        self.newemail.grid(row=0, column=0, padx=5, pady=5)

        self.newusername = tk.Entry(self)
        self.newusername.grid(row=1, column=0, padx=5, pady=5)

        self.newpassword = tk.Entry(self)
        self.newpassword.grid(row=2, column=0, padx=5, pady=5)

        self.apply = tk.Button(self, text="Apply")
        self.apply.grid(row=4, column=0, padx=5, pady=5)


a = windows()
a.mainloop()
