import sqlite3
import csv
from tkinter import *
from tkinter import ttk, messagebox, filedialog

# --- DATABASE SETUP ---
conn = sqlite3.connect('students.db')
c = conn.cursor()

# Create users table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Create students table
c.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT NOT NULL,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    email TEXT,
    contact TEXT,
    gender TEXT
)
''')

# --- FUNCTIONS ---
def insert_data():
    roll_no = entry_roll.get()
    name = entry_name.get()
    age = entry_age.get()
    email = entry_email.get()
    contact = entry_contact.get()
    gender = gender_var.get()

    if not (roll_no and name and age):
        messagebox.showwarning("Missing Data", "Roll No, Name, and Age are required!")
        return

    c.execute("INSERT INTO students (roll_no, name, age, email, contact, gender) VALUES (?, ?, ?, ?, ?, ?)",
              (roll_no, name, age, email, contact, gender))
    conn.commit()
    clear_fields()
    view_records()

def view_records():
    for row in tree.get_children():
        tree.delete(row)
    c.execute("SELECT * FROM students")
    rows = c.fetchall()
    for row in rows:
        tree.insert('', END, values=row)

def clear_fields():
    entry_roll.delete(0, END)
    entry_name.delete(0, END)
    entry_age.delete(0, END)
    entry_email.delete(0, END)
    entry_contact.delete(0, END)
    gender_var.set("Select Gender")
    update_btn.config(state=DISABLED)
    delete_btn.config(state=DISABLED)
    save_btn.config(state=NORMAL)

def select_item(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected, 'values')
        clear_fields()
        entry_roll.insert(0, values[1])
        entry_name.insert(0, values[2])
        entry_age.insert(0, values[3])
        entry_email.insert(0, values[4])
        entry_contact.insert(0, values[5])
        gender_var.set(values[6])
        update_btn.config(state=NORMAL)
        delete_btn.config(state=NORMAL)
        save_btn.config(state=DISABLED)

def update_record():
    selected = tree.focus()
    if not selected:
        return
    student_id = tree.item(selected, 'values')[0]
    c.execute("""
        UPDATE students SET roll_no=?, name=?, age=?, email=?, contact=?, gender=?
        WHERE id=?
    """, (
        entry_roll.get(), entry_name.get(), entry_age.get(),
        entry_email.get(), entry_contact.get(), gender_var.get(), student_id
    ))
    conn.commit()
    view_records()
    clear_fields()
    messagebox.showinfo("Updated", "Record updated successfully")

def delete_record():
    selected = tree.focus()
    if not selected:
        return
    student_id = tree.item(selected, 'values')[0]
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
    if confirm:
        c.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()
        view_records()
        clear_fields()
        messagebox.showinfo("Deleted", "Record deleted successfully")

def export_to_csv():
    filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv")])
    if filename:
        c.execute("SELECT * FROM students")
        data = c.fetchall()
        headers = ["ID", "Roll No", "Name", "Age", "Email", "Contact", "Gender"]
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)
        messagebox.showinfo("Exported", f"Data exported to {filename}")

# --- LOGIN / SIGNUP ---
def show_login():
    def check_login():
        username = username_entry.get()
        password = password_entry.get()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = c.fetchone()
        if result:
            login_window.destroy()
            open_main_app()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    def open_signup():
        login_window.destroy()
        show_signup()

    login_window = Tk()
    login_window.title("Login")
    login_window.geometry("300x250")

    Label(login_window, text="Username").pack(pady=5)
    username_entry = Entry(login_window)
    username_entry.pack()

    Label(login_window, text="Password").pack(pady=5)
    password_entry = Entry(login_window, show='*')
    password_entry.pack()

    Button(login_window, text="Login", command=check_login).pack(pady=10)
    Button(login_window, text="Sign Up", command=open_signup).pack()

    login_window.mainloop()

def show_signup():
    def register():
        username = username_entry.get()
        password = password_entry.get()
        if username and password:
            try:
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                messagebox.showinfo("Success", "Signup successful. Please login.")
                signup_window.destroy()
                show_login()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists.")
        else:
            messagebox.showwarning("Missing Fields", "Please fill out all fields.")

    signup_window = Tk()
    signup_window.title("Sign Up")
    signup_window.geometry("300x250")

    Label(signup_window, text="Choose Username").pack(pady=5)
    username_entry = Entry(signup_window)
    username_entry.pack()

    Label(signup_window, text="Choose Password").pack(pady=5)
    password_entry = Entry(signup_window, show='*')
    password_entry.pack()

    Button(signup_window, text="Register", command=register).pack(pady=20)
    signup_window.mainloop()

# --- MAIN APP ---
def open_main_app():
    global root, entry_roll, entry_name, entry_age, entry_email, entry_contact, gender_var
    global update_btn, delete_btn, save_btn, tree

    root = Tk()
    root.title("Student Record System")
    root.geometry("850x600")

    input_frame = Frame(root)
    input_frame.pack(pady=10)

    Label(input_frame, text="Roll No").grid(row=0, column=0)
    entry_roll = Entry(input_frame)
    entry_roll.grid(row=0, column=1)

    Label(input_frame, text="Name").grid(row=1, column=0)
    entry_name = Entry(input_frame)
    entry_name.grid(row=1, column=1)

    Label(input_frame, text="Age").grid(row=2, column=0)
    entry_age = Entry(input_frame)
    entry_age.grid(row=2, column=1)

    Label(input_frame, text="Email").grid(row=3, column=0)
    entry_email = Entry(input_frame)
    entry_email.grid(row=3, column=1)

    Label(input_frame, text="Contact").grid(row=4, column=0)
    entry_contact = Entry(input_frame)
    entry_contact.grid(row=4, column=1)

    Label(input_frame, text="Gender").grid(row=5, column=0)
    gender_var = StringVar()
    gender_dropdown = ttk.Combobox(input_frame, textvariable=gender_var, values=["Male", "Female", "Other"])
    gender_dropdown.grid(row=5, column=1)
    gender_dropdown.set("Select Gender")

    button_frame = Frame(root)
    button_frame.pack(pady=10)

    save_btn = Button(button_frame, text="Save", command=insert_data)
    save_btn.grid(row=0, column=0, padx=5)

    update_btn = Button(button_frame, text="Update", command=update_record, state=DISABLED)
    update_btn.grid(row=0, column=1, padx=5)

    delete_btn = Button(button_frame, text="Delete", command=delete_record, state=DISABLED)
    delete_btn.grid(row=0, column=2, padx=5)

    export_btn = Button(button_frame, text="Export to Excel", command=export_to_csv)
    export_btn.grid(row=0, column=3, padx=5)

    tree_frame = Frame(root)
    tree_frame.pack(pady=10)

    tree = ttk.Treeview(tree_frame, columns=("ID", "Roll No", "Name", "Age", "Email", "Contact", "Gender"), show='headings')
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(side=LEFT)

    scrollbar = Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)

    tree.bind("<ButtonRelease-1>", select_item)
    view_records()
    root.mainloop()

# --- START APP ---
show_login()
conn.close()
