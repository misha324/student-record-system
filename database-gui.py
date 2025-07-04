import sqlite3
from tkinter import *

# Connect to SQLite database (or create if not exists)
conn = sqlite3.connect('students.db')
c = conn.cursor()

# Create table
c.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
)
''')

# Insert Function
def insert_data():
    name = entry_name.get()
    age = entry_age.get()
    c.execute("INSERT INTO students (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    entry_name.delete(0, END)
    entry_age.delete(0, END)

# Tkinter GUI
root = Tk()
root.title("Student Record System")

Label(root, text="Name").grid(row=0, column=0)
entry_name = Entry(root)
entry_name.grid(row=0, column=1)

Label(root, text="Age").grid(row=1, column=0)
entry_age = Entry(root)
entry_age.grid(row=1, column=1)

Button(root, text="Save", command=insert_data).grid(row=2, column=0, columnspan=2)

root.mainloop()
conn.close()
