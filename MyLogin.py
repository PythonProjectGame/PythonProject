import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import _thread
import json

import MyNetwork
import MyVal


# main class inherits from tkinter window class
class Windows(tk.Tk):
    # constant fonts for buttons and lables

    def __init__(self, *args, **kwargs) -> None:
        tk.Tk.__init__(self, *args, **kwargs)

        # initial setup of screen
        self.wm_title("Main Project")
        self.geometry("500x500")

        # setting background
        self.config(bg="#2e9e80")

        # creating a menubar
        self.menubar = tk.Menu(self)

        self.file = tk.Menu(self.menubar, tearoff=0)
        self.file.add_command(label="Exit", command=quit)
        self.file.add_command(label="Back", command=lambda: self.show_frame(LoginPage))
        self.menubar.add_cascade(label="File", menu=self.file)

        self.settings = tk.Menu(self.menubar, tearoff=0)
        self.settings.add_command(label="Logout", command=lambda: self.logout())
        self.menubar.add_cascade(label="Settings", menu=self.settings)

        self.config(menu=self.menubar)

        self.adjust = tk.Frame(self)
        self.adjust.grid(row=0, column=3, sticky="ne")

        self.focus = LoginPage

        # weights the first and third columns and rows to centre the frames
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # creates a dictionary of frames via classes
        self.frames = {}
        for F in (LoginPage, LoggedIn, NewAccount, Sound, BGMusic):
            frame = F(self)

            self.frames[F] = frame
            frame.grid(row=1, column=1, sticky="nsew")

        # shows first frame
        self.show_frame(self.focus)

        # sets minimum size of the window to the biggest frame
        self.minsize(
            width=max(self.frames[i].winfo_height() for i in self.frames),
            height=max(self.frames[i].winfo_height() for i in self.frames),
        )

    # function to raise a frame to the top so that it is visible
    def show_frame(self, cont) -> None:

        self.menubar

        frame = self.frames[cont]
        frame.tkraise()

    def logout(self) -> None:
        self.show_frame(LoginPage)
        self.settings.delete(1, "end")


# first frame which is shown: main login screen
class LoginPage(tk.Frame):
    def __init__(self, parent: object, *args, **kwargs) -> None:
        """
        Initialize the LoginPage frame.

        :param parent: The parent widget.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """
        self.parent = parent

        # Initialize the frame
        tk.Frame.__init__(self, self.parent, *args, **kwargs)

        # Entry for username
        self.uservar = tk.StringVar(value="Username")
        self.username = tk.Entry(self, textvariable=self.uservar)
        self.username.grid(row=0, column=0, sticky="we", padx=5, pady=5)
        self.username.bind("<FocusIn>", lambda e: self.on_click(1))
        self.username.bind("<FocusOut>", lambda e: self.focus_out(1))

        # Entry for password
        self.passvar = tk.StringVar(value="Password")
        self.password = tk.Entry(self, textvariable=self.passvar)
        self.password.grid(row=1, column=0, sticky="we", padx=5, pady=5)
        self.password.bind("<FocusIn>", lambda e: self.on_click(2))
        self.password.bind("<FocusOut>", lambda e: self.focus_out(2))

        # Button for login
        login_button = tk.Button(self, text="Login", command=self.login)
        login_button.grid(row=2, column=0, sticky="we", padx=5, pady=5)

        # Label and link to the new account page
        new_account = tk.Label(
            self, text="New to MainProject?\nApply for a New Account", cursor="hand2"
        )
        new_account.config(fg="blue", font=("Arial", 8, "italic"))
        new_account.grid(row=4, column=0, padx=5)
        new_account.bind("<Button-1>", lambda e: self.parent.show_frame(NewAccount))

    def clear(self) -> None:
        """
        Clear the entries of the username and password fields and reset them to their default state.

        This function is called when the user clicks on the "Clear" button.
        """
        # Clear the entries of the username and password fields
        self.uservar.set("Username")
        self.passvar.set("Password")

        # Reset the password field to show the password
        self.password.config(show="")

    def on_click(self, entry: int) -> None:
        """
        Change the state of the entries for username and password when they are clicked.

        If the username or password is the default value, clear the entry. Otherwise, set the
        show option of the password entry to hide the password.

        :param entry: The entry number to change. 1 is username, 2 is password.
        """
        match entry:
            case 1:
                # If the username entry is the default value, clear it
                if self.uservar.get() == "Username":
                    self.uservar.set("")
            case 2:
                # If the password entry is the default value, clear it and hide the password
                if self.passvar.get() == "Password":
                    self.passvar.set("")
                    self.password.config(show="*")

    def focus_out(self, entry: int) -> None:
        """
        Change the state of the entries for username and password when they lose focus.

        If the username or password is empty, reset it to its default value and show the
        password.

        :param entry: The entry number to change. 1 is username, 2 is password.
        """
        match entry:
            case 1:
                # If the username entry is empty, reset it to its default value
                if self.uservar.get() == "":
                    self.uservar.set("Username")
            case 2:
                # If the password entry is empty, reset it to its default value and show the password
                if self.passvar.get() == "":
                    self.passvar.set("Password")
                    self.password.config(show="")

    # runs the sql data base to check login credentials with validation
    def login(self) -> None:
        pswd = self.passvar.get()
        user = self.uservar.get()
        indata = "False"

        if any([user == "Username", pswd == "Password"]):
            user = ""
            pswd = ""

        if all([MyVal.present(user), MyVal.present(pswd)]):
            pass
        else:
            messagebox.showwarning(
                title="Warning", message="Please enter a Username and Password"
            )
            self.clear()
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

            if indata == "True" or indata == "Admin":
                self.parent.show_frame(LoggedIn)

                self.parent.settings.add_command(
                    label="Sound", command=lambda: self.parent.show_frame(Sound)
                )

                self.parent.settings.add_command(
                    label="Music", command=lambda: self.parent.show_frame(BGMusic)
                )

                self.parent.file.delete(1)

                self.parent.file.add_command(
                    label="Back", command=lambda: self.parent.show_frame(LoggedIn)
                )

                if indata == "Admin":
                    pass

            if indata == "False":
                messagebox.showwarning(title="Warning", message="Access Denied")
            return

        except BrokenPipeError:
            messagebox.showwarning(
                title="Warning", message="Server is down, please try again later"
            )
            self.clear()


class LoggedIn(tk.Frame):
    def __init__(self, parent, *args, **kwargs) -> None:
        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        play = tk.Button(self, text="Start Game", command=lambda: self.playGame())
        play.grid(row=1, column=0)

    def playGame(self):
        self.parent.destroy()
        os.system("python3 GameCode/MyClient.py")


class NewAccount(tk.Frame):
    def __init__(self, parent, *args, **kwargs) -> None:
        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        self.firstvar = tk.StringVar(value="FirstName")
        self.firstname = tk.Entry(self, textvariable=self.firstvar)
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

        if any(
            [
                firstname == "FirstName",
                lastname == "Lastname",
                email == "Email",
            ]
        ):
            firstname = ""
            lastname = ""
            email = ""

        if all(
            [MyVal.present(firstname), MyVal.present(lastname), MyVal.present(email)]
        ):
            pass
        else:
            messagebox.showwarning(
                title="Warning", message="Please fill in all entries"
            )
            return

        if all(
            [MyVal.length(firstname, (2, 12), 4), MyVal.length(lastname, (2, 12), 4)]
        ):
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


class Sound(tk.Frame):
    def __init__(self, parent, *args, **kwargs) -> None:
        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        with open("GameCode/GameSettings.json", "r") as f:
            x = f.read()
            self.game_settings = json.loads(x)

        self.mas_vol = tk.IntVar(
            value=self.game_settings["SOUND"]["SOUND_VOLUME"] * 100
        )
        master = tk.Label(self, text="Master Volume", font=("Arial", 10))
        master.grid(row=0, column=0)
        master_volume = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient="horizontal",
            variable=self.mas_vol,
            command=lambda x: self.master_volume(self.mas_vol.get() / 100),
        )
        master_volume.grid(row=1, column=0)

        self.mas_lab = tk.Label(self, text=str(self.mas_vol.get()))
        self.mas_lab.grid(row=1, column=1)

        self.mus_vol = tk.IntVar(
            value=self.game_settings["SOUND"]["MUSIC_VOLUME"] * 100
        )
        music = tk.Label(self, text="Music Volume", font=("Arial", 10))
        music.grid(row=2, column=0)
        music_volume = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient="horizontal",
            variable=self.mus_vol,
            command=lambda x: self.music_volume(self.mus_vol.get() / 100),
        )
        music_volume.grid(row=3, column=0)

        self.mus_lab = tk.Label(self, text=str(self.mus_vol.get()))
        self.mus_lab.grid(row=3, column=1)

        self.sfx_vol = tk.IntVar(value=self.game_settings["SOUND"]["SFX_VOLUME"] * 100)
        sfx = tk.Label(self, text="SFX Volume", font=("Arial", 10))
        sfx.grid(row=4, column=0)
        sfx_volume = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient="horizontal",
            variable=self.sfx_vol,
            command=lambda x: self.sfx_volume(self.sfx_vol.get() / 100),
        )
        sfx_volume.grid(row=5, column=0)

        self.sfx_lab = tk.Label(self, text=str(self.sfx_vol.get()))
        self.sfx_lab.grid(row=5, column=1)

    def master_volume(self, new_volume: int) -> None:

        # Getting Game Settings
        with open("GameCode/GameSettings.json", "r+") as f:
            self.game_settings = json.load(f)
            self.game_settings["SOUND"]["SOUND_VOLUME"] = new_volume
            f.seek(0)
            json.dump(self.game_settings, f, indent=4)
            f.truncate()

        self.mas_lab["text"] = str(self.mas_vol.get())

    def music_volume(self, new_volume: int) -> None:

        # Getting Game Settings
        with open("GameCode/GameSettings.json", "r+") as f:
            self.game_settings = json.load(f)
            self.game_settings["SOUND"]["MUSIC_VOLUME"] = new_volume
            f.seek(0)
            json.dump(self.game_settings, f, indent=4)
            f.truncate()

        self.mus_lab["text"] = str(self.mus_vol.get())

    def sfx_volume(self, new_volume: int) -> None:

        # Getting Game Settings
        with open("GameCode/GameSettings.json", "r+") as f:
            self.game_settings = json.load(f)
            self.game_settings["SOUND"]["SFX_VOLUME"] = new_volume
            f.seek(0)
            json.dump(self.game_settings, f, indent=4)
            f.truncate()

        self.sfx_lab["text"] = str(self.sfx_vol.get())


class BGMusic(tk.Frame):
    def __init__(self, parent, *args, **kwargs) -> None:
        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        with open("GameCode/GameSettings.json", "r") as f:
            x = f.read()
            self.game_settings = json.loads(x)

        self.bgmusic = tk.Label(self, text="BG Music")
        self.bgmusic.grid(row=0, column=0)

        music = self.game_settings["BG_MUSIC"]

        self.v = tk.IntVar()
        self.v.set(self.game_settings["SONG_CHOICE"])

        for song in music:
            button = tk.Radiobutton(
                self,
                text=song,
                value=music.index(song),
                variable=self.v,
                command=self.change_song,
            )
            button.grid(row=music.index(song) + 1, column=0, sticky="w")

    def change_song(self) -> None:

        with open("GameCode/GameSettings.json", "r+") as f:
            self.game_settings = json.load(f)
            self.game_settings["SONG_CHOICE"] = self.v.get()
            f.seek(0)
            json.dump(self.game_settings, f, indent=4)
            f.truncate()


if __name__ == "__main__":
    a = Windows()
    a.mainloop()
