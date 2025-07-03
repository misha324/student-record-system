import tkinter as tk
from tkinter import messagebox
import sqlite3

def add_record():
    name = entry_name.get()
    roll = entry_roll.get()
    dept = entry_dept.get()
    gpa = entry_gpa.get()

    if name and roll:
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, roll_no, department, gpa) VALUES (?, ?, ?, ?)", 
                       (name, roll, dept, gpa))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Record added")
    else:
        messagebox.showwarning("Input Error", "Name and Roll No are required")

def open_dashboard():
    global entry_name, entry_roll, entry_dept, entry_gpa
    dash = tk.Tk()
    dash.title("Dashboard")
    dash.geometry("400x300")

    tk.Label(dash, text="Student Name").pack()
    entry_name = tk.Entry(dash)
    entry_name.pack()

    tk.Label(dash, text="Roll Number").pack()
    entry_roll = tk.Entry(dash)
    entry_roll.pack()

    tk.Label(dash, text="Department").pack()
    entry_dept = tk.Entry(dash)
    entry_dept.pack()

    tk.Label(dash, text="GPA").pack()
    entry_gpa = tk.Entry(dash)
    entry_gpa.pack()

    tk.Button(dash, text="Add Record", command=add_record).pack(pady=10)
    dash.mainloop()
