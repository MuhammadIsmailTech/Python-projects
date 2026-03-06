import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pymysql
import csv
from PIL import Image, ImageTk

# ---------------- DATABASE FUNCTION ---------------- #

def db_connect():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="mysql@9295",
        database="school1"
    )


# ---------------- LOGIN WINDOW ---------------- #

def open_main():
    login_window.destroy()
    root = tk.Tk()
    StudentSystem(root)
    root.mainloop()


def login():
    if user_entry.get() == "admin" and pass_entry.get() == "1234":
        open_main()
    else:
        messagebox.showerror("Error", "Invalid Login")


login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("300x200")

tk.Label(login_window, text="Username").pack(pady=5)
user_entry = tk.Entry(login_window)
user_entry.pack()

tk.Label(login_window, text="Password").pack(pady=5)
pass_entry = tk.Entry(login_window, show="*")
pass_entry.pack()

tk.Button(login_window, text="Login", command=login).pack(pady=15)

# ---------------- MAIN SYSTEM ---------------- #

class StudentSystem:

    def __init__(self, root):

        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1200x700")

        title = tk.Label(root,
                         text="Student Management System",
                         font=("Arial", 28, "bold"),
                         bg="lightgreen")

        title.pack(fill="x")

        # Left Menu
        menu = tk.Frame(root, bd=4, relief="ridge")
        menu.place(x=10, y=80, width=250, height=600)

        tk.Button(menu, text="Add Student", width=40,
                  command=self.add_student).pack(pady=10)

        tk.Button(menu, text="Search Student", width=40,
                  command=self.search_student).pack(pady=40)

        tk.Button(menu, text="Update Student", width=40,
                  command=self.update_student).pack(pady=10)

        tk.Button(menu, text="Delete Student", width=40,
                  command=self.delete_student).pack(pady=10)

        tk.Button(menu, text="Show All", width=40,
                  command=self.show_all).pack(pady=10)

        tk.Button(menu, text="Export CSV", width=40,
                  command=self.export_csv).pack(pady=10)

        tk.Button(menu, text="Total Students", width=40,
                  command=self.total_students).pack(pady=10)

        # Table
        frame = tk.Frame(root)
        frame.place(x=270, y=80, width=900, height=600)

        scroll_y = tk.Scrollbar(frame)
        scroll_y.pack(side="right", fill="y")

        self.table = ttk.Treeview(frame,
                                  yscrollcommand=scroll_y.set,
                                  columns=("roll", "name", "fname",
                                           "sub", "grade",
                                           "email", "phone", "photo"))

        scroll_y.config(command=self.table.yview)

        self.table.heading("roll", text="Roll")
        self.table.heading("name", text="Name")
        self.table.heading("fname", text="Father")
        self.table.heading("sub", text="Subject")
        self.table.heading("grade", text="Grade")
        self.table.heading("email", text="Email")
        self.table.heading("phone", text="Phone")
        self.table.heading("photo", text="Photo")

        self.table["show"] = "headings"
        self.table.pack(fill="both", expand=1)

        self.show_all()

    # ---------------- ADD STUDENT ---------------- #

    def add_student(self):

        self.win = tk.Toplevel(self.root)
        self.win.title("Add Student")
        self.win.geometry("400x500")

        labels = ["Roll", "Name", "Father", "Subject",
                  "Grade", "Email", "Phone"]

        self.entries = {}

        for i, text in enumerate(labels):
            tk.Label(self.win, text=text).grid(row=i, column=0, pady=5)
            e = tk.Entry(self.win)
            e.grid(row=i, column=1)
            self.entries[text] = e

        tk.Button(self.win, text="Upload Photo",
                  command=self.upload_photo).grid(row=7, column=0)

        tk.Button(self.win, text="Save",
                  command=self.save_student).grid(row=8, column=0)

        tk.Button(self.win, text="Clear",
                  command=self.clear_fields).grid(row=8, column=1)

        self.photo_path = ""

    def upload_photo(self):
        self.photo_path = filedialog.askopenfilename()

    def clear_fields(self):
        for e in self.entries.values():
            e.delete(0, tk.END)

    def save_student(self):

        data = [e.get() for e in self.entries.values()]

        if "" in data:
            messagebox.showerror("Error", "Fill all fields")
            return

        con = db_connect()
        cur = con.cursor()

        cur.execute("""INSERT INTO student
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (*data, self.photo_path))

        con.commit()
        con.close()

        messagebox.showinfo("Success", "Student Added")

        self.win.destroy()
        self.show_all()

    # ---------------- SHOW ALL ---------------- #

    def show_all(self):

        con = db_connect()
        cur = con.cursor()

        cur.execute("SELECT * FROM student")
        rows = cur.fetchall()

        self.table.delete(*self.table.get_children())

        for r in rows:
            self.table.insert("", "end", values=r)

        con.close()

    # ---------------- SEARCH ---------------- #

    def search_student(self):

        win = tk.Toplevel(self.root)
        win.title("Search")

        tk.Label(win, text="Enter Name").pack()

        entry = tk.Entry(win)
        entry.pack()

        def search():

            con = db_connect()
            cur = con.cursor()

            cur.execute("SELECT * FROM student WHERE name LIKE %s",
                        ('%' + entry.get() + '%',))

            rows = cur.fetchall()

            self.table.delete(*self.table.get_children())

            for r in rows:
                self.table.insert("", "end", values=r)

            con.close()

        tk.Button(win, text="Search", command=search).pack()

    # ---------------- UPDATE ---------------- #

    def update_student(self):

        win = tk.Toplevel(self.root)
        win.title("Update")

        tk.Label(win, text="Roll No").pack()
        roll = tk.Entry(win)
        roll.pack()

        tk.Label(win, text="New Grade").pack()
        grade = tk.Entry(win)
        grade.pack()

        def update():

            con = db_connect()
            cur = con.cursor()

            cur.execute(
                "UPDATE student SET grade=%s WHERE rollNo=%s",
                (grade.get(), roll.get()))

            con.commit()
            con.close()

            messagebox.showinfo("Updated", "Record Updated")

            self.show_all()

        tk.Button(win, text="Update", command=update).pack()

    # ---------------- DELETE ---------------- #

    def delete_student(self):

        win = tk.Toplevel(self.root)
        win.title("Delete")

        tk.Label(win, text="Roll No").pack()
        roll = tk.Entry(win)
        roll.pack()

        def delete():

            confirm = messagebox.askyesno(
                "Confirm", "Delete this student?")

            if confirm:

                con = db_connect()
                cur = con.cursor()

                cur.execute("DELETE FROM student WHERE rollNo=%s",
                            (roll.get()))

                con.commit()
                con.close()

                messagebox.showinfo("Deleted", "Student Removed")

                self.show_all()

        tk.Button(win, text="Delete", command=delete).pack()

    # ---------------- EXPORT CSV ---------------- #

    def export_csv(self):

        con = db_connect()
        cur = con.cursor()

        cur.execute("SELECT * FROM student")
        rows = cur.fetchall()

        with open("students.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["Roll", "Name", "Father", "Subject",
                 "Grade", "Email", "Phone", "Photo"])

            writer.writerows(rows)

        con.close()

        messagebox.showinfo("Exported", "Data exported to students.csv")

    # ---------------- TOTAL STUDENTS ---------------- #

    def total_students(self):

        con = db_connect()
        cur = con.cursor()

        cur.execute("SELECT COUNT(*) FROM student")
        total = cur.fetchone()[0]

        con.close()

        messagebox.showinfo("Total Students",
                            f"Total Students = {total}")


login_window.mainloop()