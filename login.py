import tkinter as tk
from tkinter import messagebox
import dashboard

class LoginWindow:
    def __init__(self, master):
        self.master = master
        master.title("Login")
        master.geometry("300x200")

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        tk.Label(master, text="Username").pack()
        tk.Entry(master, textvariable=self.username).pack()
        tk.Label(master, text="Password").pack()
        tk.Entry(master, textvariable=self.password, show='*').pack()
        tk.Button(master, text="Login", command=self.login).pack(pady=10)

    def login(self):
        if self.username.get() == "admin" and self.password.get() == "admin":
            self.master.destroy()
            dashboard.open_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
