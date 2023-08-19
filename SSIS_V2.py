from tkinter import *
from tkinter import ttk
# from PIL import ImageTk, Image
import sqlite3
from tkinter import messagebox

root = Tk()
root.title('Simple Student Information System')
root.configure(bg="#BFBEDA")
root.geometry("890x540")

# Create Style
style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
    background="silver",
    foreground="black",
    fieldbackground="silver"
    )

style.map("Treeview",
    background=[('selected', '#2E165B')]
    )

# Student TreeView
# Frame for TreeView and scroll
tree_frame = Frame(root)
tree_frame.grid(row=1, column=2, columnspan=3, pady=10)

# scroll
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Add TreeView
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)

# Defining Columns
my_tree['columns'] = ('ID number', 'Name', 'Course', 'Year Level', 'Gender')

# Formatting Column
my_tree.column("#0", stretch=NO, width=0)
my_tree.column("ID number", width=120, anchor=W)
my_tree.column("Name", width=170, anchor=W)
my_tree.column("Course", width=120, anchor=W)
my_tree.column("Year Level", width=90, anchor=W)
my_tree.column("Gender", width=120, anchor=W)

# Create Headings
my_tree.heading("ID number", text='ID Number', anchor=W)
my_tree.heading("Name", text='Name', anchor=W)
my_tree.heading("Course", text='Course', anchor=W)
my_tree.heading("Year Level", text='Year Level', anchor=W)
my_tree.heading("Gender", text='Gender', anchor=W)

# Display TreeView
my_tree.pack()

# configure scrollbar
tree_scroll.config(command=my_tree.yview)

# Course TreeView
# Frame for TreeView and scroll
tree_frame2 = Frame(root)
tree_frame2.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky='w')

# scroll
tree_scroll2 = Scrollbar(tree_frame2)
tree_scroll2.pack(side=RIGHT, fill=Y)

# Add TreeView
my_tree2 = ttk.Treeview(tree_frame2, yscrollcommand=tree_scroll2.set)

# Defining Columns
my_tree2['columns'] = ('Course Code', 'Course Name')

# Formatting Column
my_tree2.column("#0", stretch=NO, width=0)
my_tree2.column("Course Code", width=120, anchor=W)
my_tree2.column("Course Name", width=250, anchor=W)


# Create Headings
my_tree2.heading("Course Code", text='Course Code', anchor=W)
my_tree2.heading("Course Name", text='Course Name', anchor=W)

# Display Treeview
my_tree2.pack()

# configure scrollbar
tree_scroll2.config(command=my_tree2.yview)

def ssisdb():
    # initiate or connects data base

    connect = sqlite3.connect('SSIS.db')
    cursor = connect.cursor()
    # create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "Course"(
        Course_Code TEXT,
        Course_Name TEXT,
        PRIMARY KEY(Course_Code)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS "Student"(
        ID_number TEXT NOT NULL,
        Name TEXT   NOT NULL,
        Course  TEXT NOT NULL,
        Year_Level TEXT NOT NULL,
        Gender TEXT NOT NULL,
        PRIMARY KEY(ID_number),
        FOREIGN KEY(Course_Code) REFERENCES Course(Course_Code)
        );
    """)

    connect.close()

    return 0


def search(e):
    for record in my_tree.get_children():
        my_tree.delete(record)

    conn = sqlite3.connect('SSIS.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Student WHERE ID_number=? ", (search_entry.get(),))
    records = c.fetchall()

    for i in records:
        my_tree.insert('', 'end', value=i)

    if search_entry.get() == '':
        delete_data()
        displaydata()
    return

def searchb():
    for record in my_tree.get_children():
        my_tree.delete(record)

    conn = sqlite3.connect('SSIS.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Student WHERE ID_number=? ", (search_entry.get(),))
    records = c.fetchall()

    if len(records) > 0:
        for i in records:
            my_tree.insert('', 'end', value=i)
        messagebox.showinfo("Search Result", f"{len(records)} record(s) found.")
    else:
        messagebox.showinfo("Search Result", "No records found.")

    if search_entry.get() == '':
        delete_data()
        displaydata()
    return

def add():
    if id_number.get() == '':
        return messagebox.showwarning("Warning!", "Please fill in all required fields.")
    elif name_entry.get() == '':
        return messagebox.showwarning("Warning!", "Please fill in all required fields.")
    elif course_entry.get() == '':
        return messagebox.showwarning("Warning!", "Please select a course")
    elif year_entry.get() == '':
        return messagebox.showwarning("Warning!", "Please select a year level")
    elif gender_entry.get() == '':
        return messagebox.showwarning("Warning!", "Please select a gender")

    # Check if the ID number already exists in the database
    conn = sqlite3.connect('SSIS.db')
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM Student WHERE ID_number=?", (id_number.get(),))
    id_count = c.fetchone()[0]

    conn.close()

    if id_count > 0:
        return messagebox.showwarning("Warning!", "ID number already exists in the database.")
    
    # connect the database
    conn = sqlite3.connect('SSIS.db')
    c = conn.cursor()

    c.execute("INSERT INTO Student VALUES (:id_number, :name, :course, :year_level, :gender)",
              {
                  'id_number': id_number.get(),
                  'name': name_entry.get(),
                  'course': course_entry.get(),
                  'year_level': year_entry.get(),
                  'gender': gender_entry.get()
              }
              )

    # Commit changes
    conn.commit()

    # Close Connection
    conn.close()

    delete_data()
    displaydata()
    
    messagebox.showinfo("Success", "Student added successfully!")

    return


def delete_data():
    for record in my_tree.get_children():
        my_tree.delete(record)


def delete():
    if messagebox.askyesno("Delete Confirmation", "Are you sure to delete this student?") == False:
        return
    else:
        conn = sqlite3.connect("SSIS.db")
        c = conn.cursor()
        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')


        c.execute("DELETE from Student WHERE ID_number=?", (values[0],))

        conn.commit()
        conn.close()

    delete_data()
    displaydata()
    
    messagebox.showinfo("Success", "Student deleted successfully!")


def select_record(e):
    id_number.delete(0, END)
    name_entry.delete(0, END)
    course_entry.delete(0, END)
    year_entry.delete(0, END)
    gender_entry.delete(0, END)

    selected = my_tree.focus()
    values = my_tree.item(selected, 'values')

    id_number.insert(0, values[0])
    name_entry.insert(0, values[1])
    course_entry.insert(0, values[2])
    year_entry.insert(0, values[3])
    gender_entry.insert(0, values[4])
    clear2()

def modify():
    conn = sqlite3.connect('SSIS.db')
    c = conn.cursor()
    data1 = id_number.get()
    data2 = name_entry.get()
    data3 = course_entry.get()
    data4 = year_entry.get()
    data5 = gender_entry.get()

    selected = my_tree.selection()
    item_value = my_tree.item(selected, "values")
    
    if item_value:
        original_id = item_value[0]  # Get the original ID_number value
        my_tree.item(selected, values=(data1, data2, data3, data4, data5))
        c.execute(
            "UPDATE Student SET ID_number=?, Name=?, Course=?, Year_Level=?, Gender=? WHERE ID_number=?",
            (data1, data2, data3, data4, data5, original_id))  # Use the original_id variable

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Student edited successfully!")  

        delete_data()
        displaydata()
    else:
        messagebox.showwarning("Warning", "Please select a student to edit.")


def displaydata():
    conn = sqlite3.connect('SSIS.db')

    c = conn.cursor()

    c.execute("SELECT * FROM Student")
    records = c.fetchall()

    global count
    count = 0

    for record in records:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2],
                                                                               record[3], record[4]), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2],
                                                                               record[3], record[4]), tags=('oddrow',))
        count += 1

    return


def displaydata2():
    conn = sqlite3.connect('SSIS.db')

    c = conn.cursor()

    c.execute("SELECT * FROM Course")
    records = c.fetchall()

    global count2
    count2 = 0

    for record in records:
        if count2 % 2 == 0:
            my_tree2.insert(parent='', index='end', iid=count2, text='', values=(record[0], record[1]), tags=('evenrow',))
        else:
            my_tree2.insert(parent='', index='end', iid=count2, text='', values=(record[0], record[1]), tags=('oddrow',))
        count2 += 1

    return


def delete_data2():
    for record in my_tree2.get_children():
        my_tree2.delete(record)


def clear():
    id_number.delete(0, END)
    name_entry.delete(0, END)
    course_entry.delete(0, END)
    year_entry.delete(0, END)
    gender_entry.delete(0, END)

    course_entry.set("Select Course")
    year_entry.set("Select Year Level")
    gender_entry.set("Select Gender")


def add2():
    if ccode_entry.get() == '':
        return messagebox.showwarning("Warning!", "Please fill in all required fields.")
    elif cname_entry.get() == '':
        return messagebox.showwarning("Warning!", "Please fill in all required fields.")
    
    conn = sqlite3.connect('SSIS.db')
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM Course WHERE Course_Code=?", (ccode_entry.get(),))
    code_count = c.fetchone()[0]

    conn.close()

    if code_count > 0:
        return messagebox.showwarning("Warning!", "Course code already exists in the database.")


    # connect the database
    conn = sqlite3.connect('SSIS.db')
    c = conn.cursor()

    c.execute("INSERT INTO Course VALUES (:code, :name)",
              {
                  'code': ccode_entry.get(),
                  'name': cname_entry.get(),
              }
              )

    # Commit changes
    conn.commit()

    # Close Connection
    conn.close()

    addCourse()
    delete_data2()
    displaydata2()
    
    messagebox.showinfo("Success", "Course added successfully!")

    return


def delete2():
    selected = my_tree2.focus()
    values = my_tree2.item(selected, 'values')
    course_code = values[0]

    conn = sqlite3.connect("SSIS.db")
    c = conn.cursor()

    # Check if there are students associated with the course
    c.execute("SELECT COUNT(*) FROM Student WHERE Course=?", (course_code,))
    student_count = c.fetchone()[0]

    conn.close()

    if student_count > 0:
        messagebox.showwarning("Warning", "Cannot delete course with associated students.")
        return

    if messagebox.askyesno("Delete Confirmation", "Are you sure to delete this course?"):
        conn = sqlite3.connect("SSIS.db")
        c = conn.cursor()
        c.execute("DELETE from Course WHERE Course_Code=?", (course_code,))
        conn.commit()
        conn.close()

        addCourse()
        delete_data2()
        displaydata2()

        messagebox.showinfo("Success", "Course deleted successfully!")


def modify2():
    conn = sqlite3.connect('SSIS.db')
    c = conn.cursor()
    data1 = ccode_entry.get()
    data2 = cname_entry.get()

    selected = my_tree2.selection()
    item_values = my_tree2.item(selected, "values")

    if item_values:
        original_ccode = item_values[0]
        my_tree2.item(selected, values=(data1, data2))
        c.execute(
            "UPDATE Course SET Course_Code=?, Course_Name=? WHERE Course_Code=?",
            (data1, data2, original_ccode))

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Course edited successfully!")

        delete_data2()
        displaydata2()
    else:
        messagebox.showwarning("Warning", "Please select a course to edit.")


def clear2():
    ccode_entry.delete(0, END)
    cname_entry.delete(0, END)


def select_record2(e):
    ccode_entry.delete(0, END)
    cname_entry.delete(0, END)

    selected = my_tree2.focus()
    values = my_tree2.item(selected, 'values')

    ccode_entry.insert(0, values[0])
    cname_entry.insert(0, values[1])
    clear()

def search2(e):

    for record in my_tree2.get_children():
        my_tree2.delete(record)

    conn = sqlite3.connect('SSIS.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Course WHERE Course_Code=? ", (search_entry2.get(),))
    records = c.fetchall()

    for i in records:
        my_tree2.insert('', 'end', value=i)

    if search_entry2.get() == '':
        delete_data2()
        displaydata2()
    return

def search2b():

    for record in my_tree2.get_children():
        my_tree2.delete(record)

    conn = sqlite3.connect('SSIS.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Course WHERE Course_Code=? ", (search_entry2.get(),))
    records = c.fetchall()

    if len(records) > 0:
        for i in records:
            my_tree2.insert('', 'end', value=i)
        messagebox.showinfo("Search Result", f"{len(records)} record(s) found.")
    else:
        messagebox.showinfo("Search Result", "No records found.")

    if search_entry2.get() == '':
        delete_data2()
        displaydata2()
    return

def addCourse():
    ex = sqlite3.connect('SSIS.db')
    x = ex.cursor()

    x.execute("SELECT Course_Code FROM Course")
    rec = x.fetchall()
    xlist = []
    for i in rec:
        xlist.append(i[0])

    course_entry = ttk.Combobox(leftside, width=18)
    course_entry.set("Select Course")
    course_entry['values'] = xlist  # ("BSCS", "BSIT", "BSCA")
    course_entry.grid(row=3, column=1, pady=10)

ex = sqlite3.connect('SSIS.db')
x = ex.cursor()


x.execute("SELECT Course_Code FROM Course")
rec = x.fetchall()
xlist = []
for i in rec:
    xlist.append(i[0])


title_label = Label(root, text="SSIS Version 2.0", font=("Times New Roman Bold", 20), fg="#371c4b", bg="#BFBEDA")
title_label.grid(row=0, column=0, columnspan=3, padx=10, ipadx=50)

# Make a frame for search and Title
srch = Frame(root, bg="#BFBEDA")
srch.grid(row=0, column=4, pady=5, sticky="e")

search_entry = Entry(srch, text="Search...", borderwidth=2)
search_entry.grid(row=0, column=3, padx=10, ipadx=50)

search_btn = Button(srch, text="Search ID Number", fg="#ffffff", bg="#371c4b", command=searchb)
search_btn.grid(row=0, column=4, ipadx=10)

# Entries Frame
leftside = Frame(root, bg="#BFBEDA")
leftside.grid(row=1, column=1, padx=10)

rightSide = Frame(root, bg="#BFBEDA")
rightSide.grid(row=2, column=3, columnspan=3, padx=10, sticky='w')

# Labels
il = Label(leftside, text="ID Number", bg="#BFBEDA")
il.grid(row=1, column=0, sticky='w', padx=5)
nl = Label(leftside, text="Name", bg="#BFBEDA")
nl.grid(row=2, column=0, sticky='w', padx=5)
cl = Label(leftside, text="Course", bg="#BFBEDA")
cl.grid(row=3, column=0, sticky='w', padx=5)
yl = Label(leftside, text="Year Level", bg="#BFBEDA")
yl.grid(row=4, column=0, sticky='w', padx=5)
gl = Label(leftside, text="Gender", bg="#BFBEDA")
gl.grid(row=5, column=0, sticky='w', padx=5)

# Lower Labels
cc = Label(rightSide, text='Course Code', bg='#BFBEDA')
cc.grid(row=1, column=0, sticky='w', padx=5)
cn = Label(rightSide, text='Course Name', bg='#BFBEDA')
cn.grid(row=2, column=0, sticky='w', padx=5)

# Entries
id_number = Entry(leftside, borderwidth=2)
id_number.grid(row=1, column=1, pady=2)

name_entry = Entry(leftside, borderwidth=2)
name_entry.grid(row=2, column=1, pady=2)

course_entry = ttk.Combobox(leftside, width=18)
course_entry.set("Select Course")
course_entry['values'] = xlist # ("BSCS", "BSIT", "BSCA")
course_entry.grid(row=3, column=1, pady=2)

"""root_gender = ttk.Combobox(root, width=25, font=("Lucida Console", 10))
    root_gender.set("Select Gender")
    root_gender['values'] = ("Male", "Female")
    root_gender.place(x=130, y=100)"""

year_entry = ttk.Combobox(leftside, width=18)
year_entry.set("Select Year Level")
year_entry['values'] = ("1", "2", "3", "4")
year_entry.grid(row=4, column=1, pady=2)

gender_entry = ttk.Combobox(leftside, width=18)
gender_entry.set("Select Gender")
gender_entry['values'] = ("Male", "Female")
gender_entry.grid(row=5, column=1, pady=2)

# Lower Entries
ccode_entry = Entry(rightSide, borderwidth=2, width=26)
ccode_entry.grid(row=1, column=1, pady=2)

cname_entry = Entry(rightSide, borderwidth=2, width=26)
cname_entry.grid(row=2, column=1, pady=2)

search_entry2 = Entry(rightSide, borderwidth=2, width=35)
search_entry2.grid(row=0, column=0, columnspan=3, pady=40, sticky='w', padx=10)

# rightSide buttons
add_btn2 = Button(rightSide, text="Add", fg="#ffffff", bg="#371c4b", command=add2, width=7)
add_btn2.grid(row=1, column=2, sticky='e', pady=3, padx=10)

del_btn2 = Button(rightSide, text="Delete",fg="#ffffff", bg="#371c4b", command=delete2, width=7)
del_btn2.grid(row=2, column=2, sticky='e', pady=3, padx=10)

mod_btn2 = Button(rightSide, text="Edit", fg="#ffffff", bg="#371c4b", command=modify2, width=7)
mod_btn2.grid(row=1, column=3, pady=3, padx=10)

clr_btn2 = Button(rightSide, text="Clear", fg="#ffffff", bg="#371c4b", command=clear2, width=7)
clr_btn2.grid(row=2, column=3, pady=3, padx=10)

"""search_btn2 = Button(rightSide, text="Search Course", fg="#ffffff", bg="#371c4b", command=search2, width=7)
search_btn2.grid(row=0, column=3, pady=10, ipadx=10)"""

search_btn2 = Button(rightSide, text="Search Course Code", fg="#ffffff", bg="#371c4b", command=search2b)
search_btn2.grid(row=0, column=2, columnspan=2, ipadx=10, sticky='e')

# Buttons Left_side
# columnspan=2, ipadx=10,

add_btn = Button(leftside, text="Add", fg="#ffffff", bg="#371c4b", command=add, width=7)
add_btn.grid(row=6, column=0, sticky='e', pady=3)

del_btn = Button(leftside, text="Delete", fg="#ffffff", bg="#371c4b", command=delete, width=7)
del_btn.grid(row=7, column=0, sticky='e', pady=3)

mod_btn = Button(leftside, text="Edit", fg="#ffffff", bg="#371c4b", command=modify, width=7)
mod_btn.grid(row=6, column=1, pady=3)

clr_btn = Button(leftside, text="Clear", fg="#ffffff", bg="#371c4b", command=clear, width=7)
clr_btn.grid(row=7, column=1, pady=3)

"""sel_btn = Button(leftside, text="Select", fg="#ffffff", bg="#371c4b", command=select_record, width=10)
sel_btn.grid(row=7, column=1, pady=3)"""

# make or connect to database
ssisdb()

# Display data on tree view
displaydata()
displaydata2()

# Bindings
my_tree.bind("<ButtonRelease-1>", select_record)
my_tree2.bind("<ButtonRelease-1>", select_record2)
search_entry2.bind("<KeyRelease>", search2)
search_entry.bind("<KeyRelease>", search)



root.mainloop()
