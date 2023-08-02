from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import csv

root = Tk()
root.geometry("1080x1080")
root.title("Student Information System (Version 1)")

# create style
style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
    background="silver",
    foreground="black",
    fieldbackground="silver"
    )

style.map("Treeview",
    background=[('selected', 'Green')]
    )

# Frame for TreeView and scroll
student_tree_frame = Frame(root)
student_tree_frame.pack(pady=10)

# scroll
student_tree_scroll = Scrollbar(student_tree_frame)
student_tree_scroll.pack(side=RIGHT, fill=Y)

# Functions
def display_data_student():
    with open('student.csv', 'r') as displayFile:
        display = csv.reader(displayFile)

        next(display)
        delete_all_student()

        for line in display:
            student_tree.insert(parent='', index='end', iid=line[0], text='',
                           values=(line[0], line[1], line[2], line[3], line[4]))

def delete_all_student():
    for record in student_tree.get_children():
        student_tree.delete(record)

def add_student():
    flag = 0
    with open('student.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            if id_number.get() == row[0]:
                flag += 1
                message_already()
    if flag < 1 and id_number.get() != "":
        with open('student.csv', 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([id_number.get(), name_entry.get(),
                             course_entry.get(), year_entry.get(), gender_entry.get()])
        messagebox.showinfo("Success", "Student added successfully!")
    if id_number.get() == '':
        message_empty()

    display_data_student()

    id_number.delete(0, END)
    name_entry.delete(0, END)
    course_entry.delete(0, END)
    year_entry.delete(0, END)
    gender_entry.delete(0, END)


def remove_one_student():
    selection = student_tree.selection()
    lines = list()
    with open("Student.csv", "r") as file:
        reader = csv.reader(file)
        for line in reader:
            lines.append(line)
            if line[0] in selection:
                lines.remove(line)
    with open("Student.csv", "w", newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    display_data_student()
    messagebox.showinfo("Success", "Student deleted successfully!")


def edit_student():
    flag = 0
    selected = student_tree.focus()
    lines_test = list()
    with open('student.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            lines_test.append(row)
            if row[0] == selected:
                lines_test.remove(row)
    for data in lines_test:
        if data[0] == id_number.get():
            flag += 1
            message_already()

    lines = list()
    members = student_tree.focus()
    count = 0
    with open('student.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            lines.append(row)
            if row[0] == members and id_number.get() != '':
                if flag < 1:
                    lines.remove(row)
                    lines.insert(count, [id_number.get(), name_entry.get(),
                                         course_entry.get(), year_entry.get(), gender_entry.get()])
            count += 1
    with open('student.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    if id_number.get() == '':
        message_empty()
    else:
        messagebox.showinfo("Success", "Student edited successfully!")  # Display success message in a messagebox

    display_data_student()

    id_number.delete(0, END)
    name_entry.delete(0, END)
    course_entry.delete(0, END)
    year_entry.delete(0, END)
    gender_entry.delete(0, END)


def select_student():
    id_number.delete(0, END)
    name_entry.delete(0, END)
    course_entry.delete(0, END)
    year_entry.delete(0, END)
    gender_entry.delete(0, END)

    selected = student_tree.focus()
    values = student_tree.item(selected, 'values')

    # output selected values
    id_number.insert(0, values[0])
    name_entry.insert(0, values[1])
    course_entry.insert(0, values[2])
    year_entry.insert(0, values[3])
    gender_entry.insert(0, values[4])



def back_student(event):
    display_data_student()


def search_student(event):
    for record in student_tree.get_children():
        student_tree.delete(record)

    x = search_entry.get()

    with open('student.csv', "r") as f:
        reader_file = csv.reader(f)

        for items in reader_file:
            for element in items:
                if x in element:
                    student_tree.insert(parent='', index='end', iid=items[0], values=items)
                    break


def search2_student():
    for record in student_tree.get_children():
        student_tree.delete(record)

    x = search_entry.get()

    with open('student.csv', "r") as f:
        reader_file = csv.reader(f)

        for items in reader_file:
            for element in items:
                if x in element:
                    student_tree.insert(parent='', index='end', iid=items[0], values=items)
                    break


def update_student(data):
    student_tree.delete(0, END)

    for item in data:
        student_tree.insert(END, item)


def deselect_student():
    id_number.delete(0, END)
    name_entry.delete(0, END)
    course_entry.delete(0, END)
    year_entry.delete(0, END)
    gender_entry.delete(0, END)


def sort_name_student():
    lines = list()
    with open('student.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        next(reader)
        for row in reader:
            lines.append(row)

    for i in range(1, len(lines)):
        count = 0
        for j in range(0, len(lines) - 1):
            if lines[j][1] > lines[j + 1][1]:
                lines[count], lines[count + 1] = lines[count + 1], lines[count]
            count += 1
    lines.insert(0, ["ID Number", "Name", "Course", "Year Level", "Gender"])
    with open('student.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    display_data_student()


def sort_id_student():
    lines = list()
    with open('student.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        next(reader)
        for row in reader:
            lines.append(row)

    for i in range(1, len(lines)):
        count = 0
        for j in range(0, len(lines) - 1):
            if lines[j][0] > lines[j + 1][0]:
                lines[count], lines[count + 1] = lines[count + 1], lines[count]
            count += 1
    lines.insert(0, ["ID Number", "Name", "Course", "Year Level", "Gender"])
    with open('student.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    display_data_student()


def sort_course_student():
    lines = list()
    with open('student.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        next(reader)
        for row in reader:
            lines.append(row)

    for i in range(1, len(lines)):
        count = 0
        for j in range(0, len(lines) - 1):
            if lines[j][2] > lines[j + 1][2]:
                lines[count], lines[count + 1] = lines[count + 1], lines[count]
            count += 1
    lines.insert(0, ["ID Number", "Name", "Course", "Year Level", "Gender"])
    with open('student.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    display_data_student()


def sort_gender_student():
    lines = list()
    with open('student.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        next(reader)
        for row in reader:
            lines.append(row)

    for i in range(1, len(lines)):
        count = 0
        for j in range(0, len(lines) - 1):
            if lines[j][4] > lines[j + 1][4]:
                lines[count], lines[count + 1] = lines[count + 1], lines[count]
            count += 1
    lines.insert(0, ["ID Number", "Name", "Course", "Year Level", "Gender"])
    with open('student.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    display_data_student()


def message_empty():
    messagebox.showerror("Error", "Please put an ID number.")


def message_already():
    messagebox.showerror("Error", "ID number already existed.")


# Add TreeView
student_tree = ttk.Treeview(student_tree_frame, yscrollcommand=student_tree_scroll.set)

# Defining Columns
student_tree['columns'] = ('ID number', 'Name', 'Course', 'Year Level', 'Gender')

# Formatting Column
student_tree.column("#0", stretch=NO, width=0)
student_tree.column("ID number", width=120, anchor=W)
student_tree.column("Name", width=170, anchor=W)
student_tree.column("Course", width=100, anchor=W)
student_tree.column("Year Level", width=110, anchor=W)
student_tree.column("Gender", width=120, anchor=W)

# Create Headings
student_tree.heading("ID number", text='ID Number', command=sort_id_student, anchor=W)
student_tree.heading("Name", text='Name', command=sort_name_student, anchor=W)
student_tree.heading("Course", text='Course', command=sort_course_student, anchor=W)
student_tree.heading("Year Level", text='Year Level', command=sort_id_student, anchor=W)
student_tree.heading("Gender", text='Gender', command=sort_gender_student, anchor=W)

# Add Data CSV
display_data_student()

# Display TreeView
student_tree.pack()

# configure scrollbar
student_tree_scroll.config(command=student_tree.yview)

# Frame for record entries
add_container = LabelFrame(root, text="Record for Student", padx=4, pady=5)
add_container.pack(anchor='center')
# Frame for actions
add_container2 = LabelFrame(root, text="Actions for Student", padx=56, pady=5)
add_container2.pack(anchor='center')

# Labels
index = Label(root, text='')
index.pack()


il = Label(add_container, text="ID Number")
il.grid(row=0, column=0)

nl = Label(add_container, text="Name")
nl.grid(row=0, column=1)

cl = Label(add_container, text="Course")
cl.grid(row=0, column=2)

yl = Label(add_container, text="Year Level")
yl.grid(row=0, column=3)

gl = Label(add_container, text="Gender")
gl.grid(row=0, column=4)

search_btn = Button(add_container2, text='Search', command=search2_student)
search_btn.grid(row=0, column=6)

# Inputs
id_number = Entry(add_container, borderwidth=2)
id_number.grid(row=1, column=0)

name_entry = Entry(add_container, borderwidth=2)
name_entry.grid(row=1, column=1)

course_entry = Entry(add_container, borderwidth=2)
course_entry.grid(row=1, column=2)

year_entry = Entry(add_container, borderwidth=2)
year_entry.grid(row=1, column=3)

gender_entry = Entry(add_container, borderwidth=2)
gender_entry.grid(row=1, column=4)

search_entry = Entry(add_container2, borderwidth=2)
search_entry.grid(row=0, column=5, padx=10)

# Buttons
add_entry = Button(add_container2, text="Add", command=add_student)
add_entry.grid(row=0, column=0, padx=13)

modify_entry = Button(add_container2, text="Edit", command=edit_student)
modify_entry.grid(row=0, column=1, padx=13)

remove_one = Button(add_container2, text='Delete', command=remove_one_student)
remove_one.grid(row=0, column=2, padx=13)

select_record = Button(add_container2, text='Select', command=select_student)
select_record.grid(row=0, column=3, padx=13)

deselect_record = Button(add_container2, text='Deselect', command=deselect_student)
deselect_record.grid(row=0, column=4, padx=13)

# Create a binding for the search box
search_entry.bind("<KeyPress>", back_student)
search_entry.bind("<Return>", search_student)

# Frame for TreeView and scroll
tree_frame = Frame(root)
tree_frame.pack(pady=10)

# scroll
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Functions for course
def display_data_course():
    with open('course.csv', 'r') as displayFile:
        display = csv.reader(displayFile)

        next(display)
        delete_all_course()

        for line in display:
            my_tree.insert(parent='', index='end', iid=line[0], text='',
                           values=(line[0], line[1]))


def delete_all_course():
    for record in my_tree.get_children():
        my_tree.delete(record)

def add_course():
    flag = 0
    with open('course.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            if course_code.get() == row[0]:
                flag += 1
                message_exists()
    if flag < 1 and course_code.get() != "":
        with open('course.csv', 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([course_code.get(), course_name.get()])
        messagebox.showinfo("Success", "Course added successfully!")    
    if course_code.get() == '':
        message_unfilled()

    display_data_course()

    course_code.delete(0, END)
    course_name.delete(0, END)

def remove_one_course():
    selection = my_tree.selection()
    lines = list()
    with open("Course.csv", "r") as file:
        reader = csv.reader(file)
        for line in reader:
            lines.append(line)
            if line[0] in selection:
                lines.remove(line)
    with open("Course.csv", "w", newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    display_data_course()
    messagebox.showinfo("Success", "Course deleted successfully!")


def edit_course():
    flag = 0
    selected = my_tree.focus()
    lines_test = list()
    with open('course.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            lines_test.append(row)
            if row[0] == selected:
                lines_test.remove(row)
    for data in lines_test:
        if data[0] == course_code.get():
            flag += 1
            message_already()

    lines = list()
    members = my_tree.focus()
    count = 0
    with open('course.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            lines.append(row)
            if row[0] == members and course_code.get() != '':
                if flag < 1:
                    lines.remove(row)
                    lines.insert(count, [course_code.get(), course_name.get()])
            count += 1
    with open('course.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    if course_code.get() == '':
        message_empty()
    else:
        messagebox.showinfo("Success", "Course edited successfully!")

    display_data_course()

    course_code.delete(0, END)
    course_name.delete(0, END)

def selects_course():
    course_code.delete(0, END)
    course_name.delete(0, END)


    selected = my_tree.focus()
    values = my_tree.item(selected, 'values')

    # output selected values
    course_code.insert(0, values[0])
    course_name.insert(0, values[1])

def back_course(event):
    display_data_course()


def search_course(event):
    for record in my_tree.get_children():
        my_tree.delete(record)

    x = search_entry.get()

    with open('course.csv', "r") as f:
        reader_file = csv.reader(f)

        for items in reader_file:
            for element in items:
                if x in element:
                    my_tree.insert(parent='', index='end', iid=items[0], values=items)
                    break


def search2_course():
    for record in my_tree.get_children():
        my_tree.delete(record)

    x = search_entry.get()

    with open('course.csv', "r") as f:
        reader_file = csv.reader(f)

        for items in reader_file:
            for element in items:
                if x in element:
                    my_tree.insert(parent='', index='end', iid=items[0], values=items)
                    break


def update_course(data):
    my_tree.delete(0, END)

    for item in data:
        my_tree.insert(END, item)


def deselects_course():
    course_code.delete(0, END)
    course_name.delete(0, END)


def sort_cname_course():
    lines = list()
    with open('course.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        next(reader)
        for row in reader:
            lines.append(row)

    for i in range(1, len(lines)):
        count = 0
        for j in range(0, len(lines) - 1):
            if lines[j][1] > lines[j + 1][1]:
                lines[count], lines[count + 1] = lines[count + 1], lines[count]
            count += 1
    lines.insert(0, ["Course Code", "Course Name"])
    with open('course.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    display_data_course()


def sort_ccode_course():
    lines = list()
    with open('course.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        next(reader)
        for row in reader:
            lines.append(row)

    for i in range(1, len(lines)):
        count = 0
        for j in range(0, len(lines) - 1):
            if lines[j][0] > lines[j + 1][0]:
                lines[count], lines[count + 1] = lines[count + 1], lines[count]
            count += 1
    lines.insert(0, ["Course Code", "Course Name"])
    with open('course.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    display_data_course()


def message_unfilled():
    messagebox.showerror("Error", "Please put a Course Code.")


def message_exists():
    messagebox.showerror("Error", "Course Code already exist.")


# Add TreeView
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)

# Defining Columns
my_tree['columns'] = ('Course Code', 'Course Name')

# Formatting Column
my_tree.column("#0", stretch=NO, width=0)
my_tree.column("Course Code", width=310, anchor=W)
my_tree.column("Course Name", width=310, anchor=W)

# Create Headings
my_tree.heading("Course Code", text='Course Code', command=sort_ccode_course, anchor=W)
my_tree.heading("Course Name", text='Course Name', command=sort_cname_course, anchor=W)

# Add Data CSV
display_data_course()

# Display TreeView
my_tree.pack()

# configure scrollbar
tree_scroll.config(command=my_tree.yview)

# Frame for record entries
add_container_course = LabelFrame(root, text="Record for Course", padx=152, pady=5)
add_container_course.pack(anchor='center')
# Frame for actions
add_container_course2 = LabelFrame(root, text="Actions for Course", padx=56, pady=5)
add_container_course2.pack(anchor='center')

# Labels
index = Label(root, text='')
index.pack()

cc = Label(add_container_course, text="Course Code")
cc.grid(row=0, column=0)

ca = Label(add_container_course, text="Course Name")
ca.grid(row=0, column=3)

search_bttn = Button(add_container_course2, text='Search', command=search2_course)
search_bttn.grid(row=0, column=6)

# Inputs
course_code = Entry(add_container_course, borderwidth=2)
course_code.grid(row=1, column=0, columnspan=2, padx=20)

course_name = Entry(add_container_course, borderwidth=2)
course_name.grid(row=1, column=3, columnspan=2, padx=20)

search_entry2 = Entry(add_container_course2, borderwidth=2)
search_entry2.grid(row=0, column=5, padx=10)

# Buttons
add_entry_course = Button(add_container_course2, text="Add", command=add_course)
add_entry_course.grid(row=0, column=0, padx=13)

modify_entry_course = Button(add_container_course2, text="Edit", command=edit_course)
modify_entry_course.grid(row=0, column=1, padx=13)

remove_one_course2 = Button(add_container_course2, text='Delete', command=remove_one_course)
remove_one_course2.grid(row=0, column=2, padx=13)

select_record_course = Button(add_container_course2, text='Select', command=selects_course)
select_record_course.grid(row=0, column=3, padx=13)

deselect_record_course = Button(add_container_course2, text='Deselect', command=deselects_course)
deselect_record_course.grid(row=0, column=4, padx=13)

# Create a binding for the search box
search_entry2.bind("<KeyPress>", back_course)
search_entry2.bind("<Return>", search_course)

root.mainloop()