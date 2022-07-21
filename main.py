# This is the import section where various modules and libraries are imported.
from tkinter import *
import sqlite3
from tkinter import messagebox
from PIL import ImageTk, Image

# This is the root.
# This is where all GUI elements are displayed and is the main window of the program.
root = Tk()
root.title("Booklogger")
root.iconbitmap("C:/Users/Yeastov/PycharmProjects/BookloggerV1/images/Booklogger.ico")
root.geometry("350x450")

# Creating a connection to the database.
connect = sqlite3.connect("books.db")
# Creating a cursor, the cursor is the variable that interacts with the database.
cursor = connect.cursor()

# Creating database table for book data.
# This table has been created and has been commented out as if left active
# it would try to re-create the table every time the program runs.
# I have left the code in for reference later and this code does not need to be run.
#cursor.execute("""CREATE TABLE books(
#    series_title text,
#    book_title text,
#    vol_number integer,
#    author_fname text,
#    author_sname text,
#    genre text,
#    book_type text,
#    format text,
#    read text,
#    status text,
#    notes text,
#    cover blob)
#""")

# MANUAL DELETE CODE
# This is code to manually delete entries into the database for testing purposes.
# To delete an entry, enter the oid number after the = , uncomment the code, then run.
# cursor.execute("DELETE from books WHERE oid = ")

# Space for functions.

# A messsage box that closes booklogger.
def box_close():
    answer = messagebox.askokcancel("Exit Booklogger?", "Do you want to close Booklogger?\n"
                                                        "Unsaved data will be lost.")
    if answer == 1:
        root.destroy()


# A function that creates a confirmation message box and uses an if statement to determine if a record
# should be saved or not.
# List of different message boxes: showinfo, showwarning, showerror, askquestion, askokcancel, askyesno.
def confirm():
    global confirm_answer
    confirm_answer = messagebox.askyesno("Confirm", "Do you want to save these details to the database?")

    if confirm_answer == 1:
        # calls the save function that commits entry to database
        save()
        # clear entry boxes
        ent_series.delete(0, END)
        ent_title.delete(0, END)
        ent_vol.delete(0, END)
        ent_fname.delete(0, END)
        ent_sname.delete(0, END)
        ent_genre.delete(0, END)
        ent_type.delete(0, END)
        ent_format.delete(0, END)
        ent_read.delete(0, END)
        ent_status.delete(0, END)
        ent_notes.delete(0, END)
        confirm_answer = 0


# A message box that saves information to the database, but does not clear the entry boxes.
# This is used when entering multiple entries to a series so I don't have to type everything out multiple times.
def box_save_series():
    answer = messagebox.askyesno("Save Series Entry", "Do you want to save these details to the database?")
    if answer == 1:
        save()
        answer = 0


# A function that saves information into the database.
def save():
    # Creating a connection to the database.
    connect = sqlite3.connect("books.db")
    # Creating a cursor.
    cursor = connect.cursor()
    # Space for function code
    cursor.execute("INSERT INTO books VALUES (:series_title, :book_title, :vol_number, :author_fname, :author_sname, "
                   ":genre, :book_type, :format, :read, :status, :notes, :cover)",
    {
        "series_title": ent_series.get(),
        "book_title": ent_title.get(),
        "vol_number": ent_vol.get(),
        "author_fname": ent_fname.get(),
        "author_sname": ent_sname.get(),
        "genre": ent_genre.get(),
        "book_type": ent_type.get(),
        "format": ent_format.get(),
        "read": ent_read.get(),
        "status": ent_status.get(),
        "notes": ent_notes.get(),
        "cover": "",
    })
    # Commiting changes to database (saving data)
    connect.commit()
    # Closing connection to database.
    connect.close()


# A function that views records in the database.
def view():
    # Creating a connection to the database.
    connect = sqlite3.connect("books.db")
    # Creating a cursor.
    cursor = connect.cursor()
    # Space for function code
    cursor.execute("Select *, oid FROM books")
    records = cursor.fetchall()
    print_records = ""
    for record in records:
        print_records += str(record) + "\n"

    lbl_records = Label(root, text=print_records)
    lbl_records.pack()
    # Committing to database.
    connect.commit()
    # Closing connection to database.
    connect.close()


# A function to display all records into the search window.
def fun_search_all():
    # Creating a connection to the database.
    connect = sqlite3.connect("books.db")
    # Creating a cursor.
    cursor = connect.cursor()
    # Space for function code.
    cursor.execute("Select *, oid FROM books")
    records = cursor.fetchall()
    print_records = ""
    for record in records:
        print_records += str(record[0]) + " | " + str(record[1]) + " | Vol: " + str(record[2]) + " | " + str(record[3]) +\
                         " | " + str(record[4]) + " | " + str(record[5]) + " | ID: " + str(record[12]) + \
                         "\n----------\n"

    lbl_records = Label(search, text=print_records)
    lbl_records.grid(row=8, column=0, columnspan=6, rowspan=10)
    # Committing to database.
    connect.commit()
    # Closing connection to database.
    connect.close()


# A function for searching by series name.
def fun_search_series():
    # Creating a connection to the database.
    connect = sqlite3.connect("books.db")
    # Creating a cursor.
    cursor = connect.cursor()
    # Space for function code.
    # WHY THE BELOW WORKS: the % means that it can be any characters before or after the variable in between
    # as there is a % on either side. Inserting the ent_search_series.get in between inserts whatever is
    # entered as a string.
    cursor.execute("SELECT *, oid FROM books WHERE series_title LIKE '%" + ent_search_series.get() + "%' ORDER BY series_title")
    records = cursor.fetchall()
    print_records = ""
    for record in records:
        print_records += str(record[0]) + " | " + str(record[1]) + " | Vol: " + str(record[2]) + " | " + str(record[3]) +\
                         " | " + str(record[4]) + " | " + str(record[5]) + " | ID: " + str(record[12]) + \
                         "\n----------\n"
    # Prints out the results of the search and positions it.
    lbl_records = Label(search, text=print_records)
    lbl_records.grid(row=5, column=0, columnspan=6, rowspan=10)
    # Committing to database.
    connect.commit()
    # Closing connection to database.
    connect.close()


def fun_search_title():
    # Creating a connection to the database.
    connect = sqlite3.connect("books.db")
    # Creating a cursor.
    cursor = connect.cursor()
    # Space for function code.
    cursor.execute(
        "SELECT *, oid FROM books WHERE book_title LIKE '%" + ent_search_title.get() + "%' ORDER BY series_title")
    records = cursor.fetchall()
    print_records = ""
    for record in records:
        print_records += str(record[0]) + " | " + str(record[1]) + " | Vol: " + str(record[2]) + " | " + str(record[3]) +\
                         " | " + str(record[4]) + " | " + str(record[5]) + " | ID: " + str(record[12]) + \
                         "\n----------\n"
    # Prints out the results of the search and positions it.
    lbl_records = Label(search, text=print_records)
    lbl_records.grid(row=6, column=0, columnspan=6, rowspan=10)
    # Committing to database.
    connect.commit()
    # Closing connection to database.
    connect.close()


# A function that searches for records by author name.
def fun_search_author():
    # Creating a connection to the database.
    connect = sqlite3.connect("books.db")
    # Creating a cursor.
    cursor = connect.cursor()
    # Space for function code.
    # WHY THE BELOW WORKS: the % means that it can be any characters before or after the variable in between
    # as there is a % on either side. Inserting the ent_search_series.get in between inserts whatever is
    # entered as a string.
    cursor.execute(
        "SELECT *, oid FROM books WHERE author_fname LIKE '%" + ent_search_author.get() + "%' OR author_sname LIKE '%" + ent_search_author.get() + "%' ORDER BY series_title")
    records = cursor.fetchall()
    print_records = ""
    for record in records:
        print_records += str(record[0]) + " | " + str(record[1]) + " | Vol: " + str(record[2]) + " | " + str(record[3]) +\
                         " | " + str(record[4]) + " | " + str(record[5]) + " | ID: " + str(record[12]) + \
                         "\n----------\n"
    # Prints out the results of the search and positions it.
    lbl_records = Label(search, text=print_records)
    lbl_records.grid(row=7, column=0, columnspan=6, rowspan=10)
    # Committing to database.
    connect.commit()
    # Closing connection to database.
    connect.close()


# A function to save updated information to a record.
def fun_update_save():
    # Creating a connection to the database.
    connect = sqlite3.connect("books.db")
    # Creating a cursor.
    cursor = connect.cursor()
    # Code for Function.
    # variable that stores the selected record ID.
    record_id = ent_select.get()
    # Code that updated the information.
    cursor.execute("""UPDATE books SET
        series_title = :series,
        book_title = :title,
        vol_number = :vol,
        author_fname = :fname,
        author_sname = :sname,
        genre = :genre,
        book_type = :type,
        read = :read,
        format = :format,
        status = :status,
        notes = :notes
        
        WHERE oid = :oid""", {
        'series': ent_series_edit.get(),
        'title': ent_title_edit.get(),
        'vol': ent_vol_edit.get(),
        'fname': ent_fname_edit.get(),
        'sname': ent_sname_edit.get(),
        'genre': ent_genre_edit.get(),
        'type': ent_type_edit.get(),
        'read': ent_read_edit.get(),
        'format': ent_format_edit.get(),
        'status': ent_status_edit.get(),
        'notes': ent_notes_edit.get(),
        'oid': record_id
        })
    # Committing to database.
    connect.commit()
    # Closing connection to database.
    connect.close()


# A message box that confirms if you want to update a record or not.
# List of different message boxes: showinfo, showwarning, showerror, askquestion, askokcancel, askyesno.
def box_update_confirm():
    answer = messagebox.askokcancel("Would you like to save this record?", "Are you sure you want to update this "
                                                                           "record? \n This cannot be undone.")
    if answer == 1:
        fun_update_save()


# A function to delete records from the database.
def fun_delete_record():
    # Creating a connection to the database.
    connect = sqlite3.connect("books.db")
    # Creating a cursor.
    cursor = connect.cursor()
    # Function code.
    cursor.execute("DELETE from books WHERE oid = " + ent_select.get())
    # Clearing the selection box in the search window.
    ent_select.delete(0, END)
    # Committing to database.
    connect.commit()
    # Closing connection to database.
    connect.close()


# Confirmation box for the deletion function.
def box_delete_confirm():
    answer = messagebox.askokcancel("YOU ARE ABOUT TO DELETE A RECORD!", "Are you sure that you want to DELETE this "
                                                                         "record? \n This action cannot be undone.")
    if answer == 1:
        fun_delete_record()
        update.destroy()

# Space for windows

# A window for submitting data into database.
# This function currently does not work.
def win_submit():
    global top
    top = Toplevel()
    # top.geometry("500x500")
    top.title("Booklogger - Create New Record")
    top.iconbitmap("C:/Users/Yeastov/PycharmProjects/BookloggerV1/images/Booklogger.ico")
    # Creating a connection to the database.
    connect = sqlite3.connect("books.db")
    # Creating a cursor.
    cursor = connect.cursor()

    # Code for the window features.

    # This sets a default option for the OptionMenu items
    global selected1
    selected1 = StringVar()
    selected1.set("Select an Option")
    global selected2
    selected2 = StringVar()
    selected2.set("Select an Option")
    global selected3
    selected3 = StringVar()
    selected3.set("Select an Option")
    global selected4
    selected4 = StringVar()
    selected4.set("Select an Option")

    # Menu Title label
    lbl_entry_title = Label(top, text="Create a New Record")
    lbl_entry_title.grid(row=0, column=0, columnspan=2, pady=10)

    # Creating data entry boxes.
    global ent_series
    ent_series = Entry(top, width="30")
    ent_series.grid(row=1, column=1, padx=20, sticky="W")
    global ent_title
    ent_title = Entry(top, width="30")
    ent_title.grid(row=2, column=1)
    global ent_vol
    ent_vol = Entry(top, width="30")
    ent_vol.grid(row=3, column=1)
    global ent_fname
    ent_fname = Entry(top, width="30")
    ent_fname.grid(row=4, column=1)
    global ent_sname
    ent_sname = Entry(top, width="30")
    ent_sname.grid(row=5, column=1)
    # The option menu's are currently causing an issue, I will revert them back to entry boxes for now.
    """
    # This is an option menu which will be used for certain input fields.
    opt_genre = [
        "Fantasy",
        "Sci-Fi",
        "Isekai",
        "Romance",
        "Educational",
        "Cooking",
        "Urban Fantasy",
        "Historical",
        "Comedy"
    ]
     For some reason specifying a width for the OptionMenu causes an error.
    global menu_genre
    menu_genre = OptionMenu(top, selected1, *opt_genre)
    menu_genre.grid(row=5, column=1)
    # OptionMenu for book type.
    opt_type = [
        "Novel",
        "Light Novel",
        "Manga",
        "Graphic Novel",
        "Childrens Book",
        "Comic"
    ]
    global menu_type
    menu_type = OptionMenu(top, selected2, *opt_type)
    menu_type.grid(row=6, column=1)
    # OptionMenu for format.
    opt_format = [
        "Paperback",
        "Hardback",
        "E-Book",
        "Comic"
    ]
    global menu_format
    menu_format = OptionMenu(top, selected3, *opt_format)
    menu_format.grid(row=7, column=1)
    # OptionMenu for read.
    opt_read = [
        "Yes",
        "No",
        "Reading",
        "Dropped"
    ]
    global menu_read
    menu_read = OptionMenu(top, selected4, *opt_read)
    menu_read.grid(row=8, column=1)
    """
    global ent_genre
    ent_genre = Entry(top, width=30)
    ent_genre.grid(row=6, column=1)
    global ent_type
    ent_type = Entry(top, width=30)
    ent_type.grid(row=7, column=1)
    global ent_format
    ent_format = Entry(top, width=30)
    ent_format.grid(row=8, column=1)
    global ent_read
    ent_read = Entry(top, width=30)
    ent_read.grid(row=9, column=1)
    global ent_status
    ent_status = Entry(top, width="30")
    ent_status.grid(row=10, column=1)
    global ent_notes
    ent_notes = Entry(top, width=30)
    ent_notes.grid(row=11, column=1)

    # Labels for entry boxes
    lbl_series = Label(top, text="Series Title:")
    lbl_series.grid(row=1, column=0)
    lbl_title = Label(top, text="Book Title:")
    lbl_title.grid(row=2, column=0)
    lbl_vol = Label(top, text="Volume Number:")
    lbl_vol.grid(row=3, column=0)
    lbl_fname = Label(top, text="Author First Name:")
    lbl_fname.grid(row=4, column=0)
    lbl_sname = Label(top, text="Author Surname:")
    lbl_sname.grid(row=5, column=0)
    lbl_genre = Label(top, text="Genre:")
    lbl_genre.grid(row=6, column=0)
    lbl_type = Label(top, text="Book Type:")
    lbl_type.grid(row=7, column=0)
    lbl_format = Label(top, text="Format:")
    lbl_format.grid(row=8, column=0)
    lbl_read = Label(top, text="Read:")
    lbl_read.grid(row=9, column=0)
    lbl_status = Label(top, text="Status:")
    lbl_status.grid(row=10, column=0)
    lbl_notes = Label(top, text="Notes:")
    lbl_notes.grid(row=11, column=0)

    # Saving data to database.
    btn_save = Button(top, text="Save Record", command=confirm)
    btn_save.grid(row=12, column=1, pady=20)
    # Button that saves series entry (leaves entry boxes filled.)
    btn_save_series = Button(top, text="Save Series\nEntry", command=box_save_series)
    btn_save_series.grid(row=13, column=1, pady=20)
    # A button that closes the window
    btn_close = Button(top, text="Main Menu", command=top.destroy)
    btn_close.grid(row=12, column=0, pady=20, ipadx=5)
    # Committing changes to database (saving data)
    connect.commit()
    # Closing connection to database.
    connect.close()


# The window for searching records
def win_search():
    global search
    search = Toplevel()
    search.title("Booklogger - Search For a Record")
    search.iconbitmap("C:/Users/Yeastov/PycharmProjects/BookloggerV1/images/Booklogger.ico")
    search.geometry("900x900")
    # Creating a connection to the database.
    connect = sqlite3.connect("books.db")
    # Creating a cursor.
    cursor = connect.cursor()

    # Code for window.
    # Global variables.
    global ent_search_series
    global ent_search_title
    global ent_search_author
    global ent_select
    # Entry boxes for search bars.
    ent_search_series = Entry(search, width=50)
    ent_search_series.grid(row=1, column=1, pady=10, padx=10, sticky="W")
    ent_search_title = Entry(search, width=50)
    ent_search_title.grid(row=2, column=1, pady=10, padx=10, sticky="W")
    ent_search_author = Entry(search, width=50)
    ent_search_author.grid(row=3, column=1, pady=10, padx=10, sticky="W")
    # Entry box to select a record.
    ent_select = Entry(search, width=12)
    ent_select.grid(row=1, column=4)
    # Label for window.
    lbl_search_window = Label(search, text="Search For & Access Records")
    lbl_search_window.grid(row=0, column=0, columnspan=6, pady=10)
    # Labels for search boxes.
    lbl_search_series = Label(search, text="Search by Series Name:")
    lbl_search_series.grid(row=1, column=0)
    lbl_search_title = Label(search, text="Search by Book Title:")
    lbl_search_title.grid(row=2, column=0)
    lbl_search_author = Label(search, text="Search by Author Name:")
    lbl_search_author.grid(row=3, column=0)
    # Label for the record selection Entry box.
    lbl_select = Label(search, text="Please select \na record:")
    lbl_select.grid(row=1, column=3, padx=20, sticky="E")

    # Making buttons.
    # Button that searches for items by series name.
    btn_search_series = Button(search, text="Search by Series", command=fun_search_series)
    btn_search_series.grid(row=1, column=2, padx=10, ipadx=6)
    # A button that searches for items by book title.
    btn_search_title = Button(search, text="Search by Title", command=fun_search_title)
    btn_search_title.grid(row=2, column=2, padx=10, ipadx=10)
    # A button that searches for items by author name.
    btn_search_author = Button(search, text="Search by Author", command=fun_search_author)
    btn_search_author.grid(row=3, column=2, padx=10, ipadx=3)
    # A button that displays all records.
    btn_search_all = Button(search, text="Display all records", command=fun_search_all)
    btn_search_all.grid(row=4, column=1)
    # A button for accessing the update window.
    btn_update = Button(search, text="Access Record", command=win_update)
    btn_update.grid(row=2, column=4, padx=10)
    # A button to close the search window.
    btn_close = Button(search, text="Main Menu", command=search.destroy)
    btn_close.grid(row=4, column=4, ipadx=7)
    # Committing changes to database (saving data)
    connect.commit()
    # Closing connection to database.
    connect.close()


# A window for updating and deleting records.
def win_update():
    global update
    update = Toplevel()
    update.title("Booklogger - Record Details")
    update.iconbitmap("C:/Users/Yeastov/PycharmProjects/BookloggerV1/images/Booklogger.ico")
    # Creating a connection to the database.
    connect = sqlite3.connect("books.db")
    # Creating a cursor.
    cursor = connect.cursor()
    # Code for window.
    # Variable that stores the selected record ID.
    record_id = ent_select.get()
    # Global variables for entry boxes.
    global ent_series_edit
    global ent_title_edit
    global ent_vol_edit
    global ent_fname_edit
    global ent_sname_edit
    global ent_genre_edit
    global ent_type_edit
    global ent_format_edit
    global ent_read_edit
    global ent_status_edit
    global ent_notes_edit
    # Label for the window
    lbl_update_header = Label(update, text="Record Details")
    lbl_update_header.grid(row=0, column=0, columnspan=5, pady=20)
    # Entry boxes for the update record form.
    ent_series_edit = Entry(update, width=30)
    ent_series_edit.grid(row=1, column=1, padx=40, sticky="W")
    ent_title_edit = Entry(update, width=30)
    ent_title_edit.grid(row=2, column=1)
    ent_vol_edit = Entry(update, width=30)
    ent_vol_edit.grid(row=3, column=1)
    ent_fname_edit = Entry(update, width=30)
    ent_fname_edit.grid(row=4, column=1)
    ent_sname_edit = Entry(update, width=30)
    ent_sname_edit.grid(row=5, column=1)
    ent_genre_edit = Entry(update, width=30)
    ent_genre_edit.grid(row=6, column=1)
    ent_type_edit = Entry(update, width=30)
    ent_type_edit.grid(row=7, column=1)
    ent_format_edit = Entry(update, width=30)
    ent_format_edit.grid(row=8, column=1)
    ent_read_edit = Entry(update, width=30)
    ent_read_edit.grid(row=9, column=1)
    ent_status_edit = Entry(update, width=30)
    ent_status_edit.grid(row=10, column=1)
    ent_notes_edit = Entry(update, width=30)
    ent_notes_edit.grid(row=11, column=1)
    # Labels for entry boxes
    lbl_series_edit = Label(update, text="Series Title:")
    lbl_series_edit.grid(row=1, column=0)
    lbl_title_edit = Label(update, text="Book Title:")
    lbl_title_edit.grid(row=2, column=0)
    lbl_vol_edit = Label(update, text="Volume Number:")
    lbl_vol_edit.grid(row=3, column=0)
    lbl_fname_edit = Label(update, text="Author First Name:")
    lbl_fname_edit.grid(row=4, column=0)
    lbl_sname_edit = Label(update, text="Author Surname:")
    lbl_sname_edit.grid(row=5, column=0)
    lbl_genre_edit = Label(update, text="Genre:")
    lbl_genre_edit.grid(row=6, column=0)
    lbl_type_edit = Label(update, text="Book Type:")
    lbl_type_edit.grid(row=7, column=0)
    lbl_format_edit = Label(update, text="Format:")
    lbl_format_edit.grid(row=8, column=0)
    lbl_read_edit = Label(update, text="Read:")
    lbl_read_edit.grid(row=9, column=0)
    lbl_status_edit = Label(update, text="Status:")
    lbl_status_edit.grid(row=10, column=0)
    lbl_notes_edit = Label(update, text="Notes:")
    lbl_notes_edit.grid(row=11, column=0)

    # Code that displays the record information into the window entry boxes.
    cursor.execute("SELECT *, oid FROM books WHERE oid = " + record_id)
    records = cursor.fetchall()
    for record in records:
        ent_series_edit.insert(0, record[0])
        ent_title_edit.insert(0, record[1])
        ent_vol_edit.insert(0,record[2])
        ent_fname_edit.insert(0, record[3])
        ent_sname_edit.insert(0, record[4])
        ent_genre_edit.insert(0, record[5])
        ent_type_edit.insert(0, record[6])
        ent_format_edit.insert(0, record[7])
        ent_read_edit.insert(0, record[8])
        ent_status_edit.insert(0, record[9])
        ent_notes_edit.insert(0, record[10])


    # Button to save updated info into record.
    btn_save = Button(update, text="Update Record", command=box_update_confirm)
    btn_save.grid(row=12, column=1, pady=20)
    # Button to delete record.
    btn_delete = Button(update, text="Delete Record", command=box_delete_confirm)
    btn_delete.grid(row=12, column=0, pady=20)
    # A Button to close the record screen.
    btn_close = Button(update, text="Back\nto Search", command=update.destroy)
    btn_close.grid(row=13, column=0, pady=30, sticky="S", ipadx=12)
    # Committing changes to database (saving data)
    connect.commit()
    # Closing connection to database.
    connect.close()


# Image for the main menu.

img_menu_logo = ImageTk.PhotoImage(Image.open("images/main_menu_logo.png"))
lbl_menu_logo = Label(image=img_menu_logo)
lbl_menu_logo.pack(pady=10)

# Buttons for Main Menu

# Button that opens the submit window named "top".
btn_submit = Button(root, text="Create New Record", command=win_submit)
btn_submit.pack(pady=5)
# Button to access the search window named "search".
btn_search = Button(root, text="Access Records", command=win_search)
btn_search.pack(pady=5, ipadx=10)
# a button that closes the applicaiton.
btn_exit = Button(root, text="Exit \nBooklogger", command=box_close)
btn_exit.pack(pady=5, ipadx=20)

# Commiting changes to database (saving data)
connect.commit()
# Closing connection to database, this is best practice to close a connection whenever you open one.
connect.close()
# This mainloop keeps the program open until the code reaches this section.
# The mainloop signifies the end of the program.
root.mainloop()
