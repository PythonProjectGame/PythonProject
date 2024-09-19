from tkinter import messagebox
import tkinter as tk
import MyNetwork
import MyVal
import pickle  # noqa: F401
import socket  # noqa: F401


# main class inherits from tkinter window class
class windows(tk.Tk):
    # constant fonts for buttons and lables

    def __init__(self, *args, **kwargs) -> None:
        tk.Tk.__init__(self, *args, **kwargs)

        # initial setup of screen
        self.wm_title("Main Project")
        self.geometry("500x500")

        # setting background
        self.config(bg="#2e9e80")

        self.adjust = tk.Frame(self)
        self.adjust.grid(row=0, column=3, sticky="ne")

        exit = tk.Button(self.adjust, text="X", command=quit)
        exit.grid(row=0, column=3)

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
    def show_frame(self, cont) -> None:
        frame = self.frames[cont]
        frame.tkraise()


# first frame which is shown: main login screen
class LoginPage(tk.Frame):
    def __init__(self, parent: object, *args, **kwargs) -> None:
        self.parent = parent

        # initialises frame
        tk.Frame.__init__(self, self.parent, *args, **kwargs)


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
        new_account.config(font=("Arial", 2))
        new_account.grid(row=4, column=0, padx=5)
        new_account.bind("<Button-1>", lambda e: self.parent.show_frame(NewAccount))

    def clear(self) -> None:
        self.uservar.set("")
        self.passcar.set("")

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

        if any([user == "Username", pswd == "Password"]):
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
            login = MyNetwork.Network()

            data = ["Login", self.username.get(), self.password.get()]
            
            indata = login.send(data)

            print(indata)

            login.close()

        except ConnectionRefusedError:
            messagebox.showwarning(
                title="Warning", message="Server is down, please try again later"
            )
        
        if indata == "True":
            self.parent.destroy()
        if indata == "Admin":
            self.parent.destroy()
        if indata == "False":
            messagebox.showwarning(
                title="Warning", message="Access Denied"
            )
            return


class LoggedIn(tk.Frame):
    def __init__(self, parent, *args, **kwargs) -> None:
        self.parent = parent
        tk.Frame.__init__(self, self.parent)


class NewAccount(tk.Frame):
    def __init__(self, parent, *args, **kwargs) -> None:
        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        self.firstvar = tk.StringVar(value="FirstName")
        self.firstname= tk.Entry(self, textvariable=self.firstvar)
        self.firstname.grid(row=0, column=0, padx=5, pady=5)
        self.firstname.bind("<FocusIn>", lambda e: self.on_click(1))
        self.firstname.bind("<FocusOut>", lambda e: self.focus_out(1))

        self.lastvar = tk.StringVar(value="LastName")
        self.lastname = tk.Entry(self, textvariable=self.lastvar)
        self.lastname.grid(row=1, column=0, padx=5, pady=5)
        self.lastname.bind("<FocusIn>", lambda e: self.on_click(2))
        self.lastname.bind("<FocusOut>", lambda e: self.focus_out(2))

        self.emailvar = tk.StringVar(value="Email")
        self.newemail = tk.Entry(self, textvariable=self.emailvar)
        self.newemail.grid(row=3, column=0, padx=5, pady=5)
        self.newemail.bind("<FocusIn>", lambda e: self.on_click(3))
        self.newemail.bind("<FocusOut>", lambda e: self.focus_out(3))

        self.apply = tk.Button(self, text="Apply", command=self.apply)
        self.apply.grid(row=4, column=0, padx=5, pady=5)
    
    def on_click(self, entry: int) -> None:
        match entry:
            case 1:
                if self.firstvar.get() == "FirstName":
                    self.firstvar.set("")
            case 2:
                if self.lastvar.get() == "LastName":
                    self.lastvar.set("")
            case 3:
                if self.emailvar.get() == "Email":
                    self.emailvar.set("")

    def focus_out(self, entry: int) -> None:
        match entry:
            case 1:
                if self.firstvar.get() == "":
                    self.firstvar.set("FirstName")
            case 2:
                if self.lastvar.get() == "":
                    self.lastvar.set("LastName")
            case 3:
                if self.emailvar.get() == "":
                    self.emailvar.set("Email")

    def apply(self) -> None:
        firstname = self.firstvar.get()
        lastname = self.lastvar.get()
        email = self.emailvar.get()

        if any([firstname == "FirstName", lastname == "Lastname", email == "Email",]):
            firstname = ""
            lastname = ""
            email = ""
        
        if all([MyVal.present(firstname), MyVal.present(lastname), MyVal.present(email)]):
            pass
        else:
            messagebox.showwarning(
                title="Warning", message="Please fill in all entries"
            )
            return
        
        if all([MyVal.length(firstname, (2, 12), 4), MyVal.length(lastname, (2, 12), 4)]):
            pass
        else:
            messagebox.showwarning(
                title="Warning", message="Please enter names of apropriate length"
            )
            self.clear()
            return
        
        if MyVal.email(email):
            pass
        else:
            messagebox.showwarning(
                title="Warning", message="Please enter a valid email"
            )

a = windows()
a.mainloop()
