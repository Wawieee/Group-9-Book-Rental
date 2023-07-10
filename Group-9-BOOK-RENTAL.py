from tkinter import ttk
import tkinter as tk
import customtkinter as ctk
import tkinter.messagebox as messagebox
import mysql.connector
import datetime
import decimal

# Creating connection object
mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'nawawi',
    database = 'book_rental'
)

cursor = mydb.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS book_rental")

cursor.execute('''CREATE TABLE IF NOT EXISTS category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS book (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT,
    title VARCHAR(50),
    author VARCHAR(50),
    price DECIMAL(10,2),
    status VARCHAR(50),
    FOREIGN KEY (category_id) REFERENCES category(category_id) ON DELETE CASCADE ON UPDATE CASCADE
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS borrower (
    borrower_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    phone BIGINT,
    email VARCHAR(50),
    address VARCHAR(100)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS rents (
    rental_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT, 
    borrower_id INT,
    rented_date DATE,
    deadline DATE,
    return_date DATE,
    payment_method VARCHAR(50),
    total_amount DECIMAL(10,2),
    late_fees DECIMAL(10,2),
    status VARCHAR(50),
    FOREIGN KEY (book_id) REFERENCES book(book_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (borrower_id) REFERENCES borrower(borrower_id) ON DELETE CASCADE ON UPDATE CASCADE
)''')

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')


def show_admin_wcode_frame():
   # Create a new top-level window for the password prompt
    password_window = ctk.CTkToplevel(root)
    password_window.geometry("300x190+780+300")

    # Set the title of the password prompt window
    password_window.title("Admin Password")

    # Create a label with the caption "Enter Password"
    label = ctk.CTkLabel(password_window, text="Enter Password", font=ctk.CTkFont('Calibri', size=12, weight='bold'))
    label.pack(padx=32, pady=30)

    # Create an entry box to enter the password
    password_entry = ctk.CTkEntry(password_window, show='*')
    password_entry.place(x=82, y=70)

    def validate_password():
        password = password_entry.get()

        # Check if the entered password matches the admin password
        admin_password = "123"  # Replace with your actual admin password
        if password == admin_password:
            password_window.destroy()  # Close the password prompt window

            # Show the admin frame
            admin_frame.tkraise()
        else:
            # Display an error message in the password prompt window
            messagebox.showerror("Invalid Password", "Incorrect password. Please try again.")

    # Create a login button
    login_button = ctk.CTkButton(password_window, text="Login", command=validate_password)
    login_button.place(x=82, y=105)

    password_window.wm_transient(root)

def show_admin_frame():
    admin_frame.tkraise()

def show_main_frame():
    main_frame.tkraise()
    
    # Clear the entry box
    entry_in_main.delete(0, 'end')
    name_entry.delete(0, 'end')
    address_entry.delete(0, 'end')
    phone_entry.delete(0, 'end')
    email_entry.delete(0, 'end')
    entry_in_rent.delete(0, 'end')
    borrower_id_entry.delete(0, 'end')
    book_id_entry.delete(0, 'end')
    rent_duration_entry.delete(0, 'end')
    book_id_in_return_entry.delete(0, 'end')

    # Retrieve books from the database
    cursor.execute("SELECT book_id, title, author, category_id, price, status FROM book")
    books = cursor.fetchall()
    
    # Clear existing data in the Treeview
    for item in tree.get_children():
        tree.delete(item)
    
    # Populate the Treeview with fetched data
    for book in books:
        tree.insert("", "end", values=book)

def load_categories():
    # Execute the SQL query to fetch categories from the database
    cursor.execute("SELECT category_id, category_name FROM category")
    categories = cursor.fetchall()

    # Get the category names as a list of strings
    category_names = [str(category[1]) for category in categories]

    # Update the combobox with the fetched categories
    combo_box['values'] = category_names
    
def load_categories_in_rent():
    # Execute the SQL query to fetch categories from the database
    cursor.execute("SELECT category_id, category_name FROM category")
    categories = cursor.fetchall()

    # Get the category names as a list of strings
    category_names = [str(category[1]) for category in categories]

    # Update the combobox with the fetched categories
    combo_box_in_rent['values'] = category_names

def get_books_by_category(event):
    # Retrieve the selected category from the combobox
    selected_category = combo_box.get()

    # Execute the SQL query to fetch books of the selected category
    cursor.execute("SELECT book_id, title, author, category_id, price, status FROM book WHERE category_id = (SELECT category_id FROM category WHERE category_name = %s)", (selected_category,))
    books = cursor.fetchall()

    # Clear existing data in the Treeview
    for item in tree.get_children():
        tree.delete(item)

    # Populate the Treeview with fetched data
    for book in books:
        tree.insert("", "end", values=book)
        
def get_books_by_category_in_rent(event):
    # Retrieve the selected category from the combobox
    selected_category = combo_box_in_rent.get()

    # Execute the SQL query to fetch books of the selected category
    cursor.execute("SELECT book_id, title, author, category_id, price, status FROM book WHERE category_id = (SELECT category_id FROM category WHERE category_name = %s)", (selected_category,))
    books = cursor.fetchall()

    # Clear existing data in the Treeview
    tree_rent.delete(*tree_rent.get_children())

    # Populate the Treeview with fetched data
    for book in books:
        tree_rent.insert("", "end", values=book)
        
def list_all_books():
    # Retrieve books from the database
    cursor.execute("SELECT book_id, title, author, category_id, price, status FROM book")
    books = cursor.fetchall()
    
    # Clear existing data in the Treeview
    for item in tree_rent.get_children():
        tree_rent.delete(item)
    
    # Populate the Treeview with fetched data
    for book in books:
        tree_rent.insert("", "end", values=book)
  
def search_books_for_main():
    # Retrieve the search query from the entry box
    query = entry_in_main.get().strip().lower()

    # Clear existing data in the Treeview
    tree.delete(*tree.get_children())

    # Execute the SQL query to fetch the matching books
    cursor.execute("SELECT book_id, title, author, category_id, price, status FROM book WHERE LOWER(title) LIKE %s", ('%' + query + '%',))
    books = cursor.fetchall()

    # Populate the Treeview with fetched data
    for i, book in enumerate(books, start=1):
        tree.insert("", "end", text=i, values=book)

def show_new_borrower_frame():
    new_borrower_frame.tkraise()

def register_new_borrower():
    name = name_entry.get()
    address = address_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()

    # Check if any entry is empty
    if not name or not address or not phone or not email:
        messagebox.showerror("Error", "Please fill in all the required data.")
    else:
        # Retrieve the latest borrower ID from the database
        cursor.execute("SELECT MAX(borrower_id) FROM borrower")
        latest_borrower_id = cursor.fetchone()[0]

        if latest_borrower_id is None:
            # No existing borrower IDs, start from 1
            new_borrower_id = 1
        else:
            # Increment the latest borrower ID to generate a new borrower ID
            new_borrower_id = latest_borrower_id + 1

        # Insert the new borrower into the database
        cursor.execute("INSERT INTO borrower (borrower_id, name, phone, address, email) VALUES (%s, %s, %s, %s, %s)", (new_borrower_id, name, phone, address, email))
        mydb.commit()

        # Display success message with borrower ID
        message = f"New borrower registered successfully!\nBorrower ID: {new_borrower_id}"
        messagebox.showinfo("Success", message)

        # Clear the entry fields
        name_entry.delete(0, 'end')
        address_entry.delete(0, 'end')
        phone_entry.delete(0, 'end')
        email_entry.delete(0, 'end')
        
        show_main_frame()

def search_books_for_rent():
    # Retrieve the search query from the entry box
    query = entry_in_rent.get().strip().lower()

    # Clear existing data in the Treeview
    tree_rent.delete(*tree_rent.get_children())

    # Execute the SQL query to fetch the matching books
    cursor.execute("SELECT book_id, title, author, category_id, price, status FROM book WHERE LOWER(title) LIKE %s", ('%' + query + '%',))
    books = cursor.fetchall()

    # Populate the Treeview with fetched data
    for i, book in enumerate(books, start=1):
        tree_rent.insert("", "end", text=i, values=book)

def show_rent_book_frame():
        rent_book_frame.tkraise()
        rent_tree()
   
def rent_tree():
    # Retrieve books from the database
    cursor.execute("SELECT book_id, title, author, category_id, price, status FROM book")
    books = cursor.fetchall()

    # Clear existing data in the Treeview
    for item in tree_rent.get_children():
        tree_rent.delete(item)

    # Populate the Treeview with fetched data
    for book in books:
        tree_rent.insert("", "end", values=book)

def create_rental_transaction():
    # Check if all entries are filled
    if borrower_id_entry.get() and book_id_entry.get() and rent_duration_entry.get():
        borrower_id = borrower_id_entry.get()
        book_id = book_id_entry.get()
        rent_duration_str = rent_duration_entry.get()
        payment_method = payment_method_combobox.get()

        # Check if borrower ID exists in the database
        cursor.execute("SELECT borrower_id FROM borrower WHERE borrower_id = %s", (borrower_id,))
        if cursor.fetchone():
            # Check if book ID exists in the database
            cursor.execute("SELECT book_id, status FROM book WHERE book_id = %s", (book_id,))
            book_data = cursor.fetchone()
            if book_data:
                book_id, status = book_data

                # Check if the book is currently rented
                if status == 'Rented':
                    messagebox.showinfo("Error", "This book is currently rented.")
                else:
                    # Validate rent duration
                    if rent_duration_str.isdigit():
                        rent_duration = int(rent_duration_str)

                        # Calculate dates
                        rented_date = datetime.datetime.now().date()
                        deadline = rented_date + datetime.timedelta(days=rent_duration)

                        # Get book price
                        cursor.execute("SELECT price FROM book WHERE book_id = %s", (book_id,))
                        price = cursor.fetchone()[0]

                        # Calculate total amount
                        total_amount = price + (rent_duration * 5)

                        # Insert rental transaction into the database
                        cursor.execute("INSERT INTO rents (book_id, borrower_id, rented_date, deadline, payment_method, total_amount, late_fees, status) VALUES (%s, %s, %s, %s, %s, %s, 0, 'Ongoing')",
                                    (book_id, borrower_id, rented_date, deadline, payment_method_combobox.get(), total_amount))
                        mydb.commit()

                        # Update the book status to 'Rented'
                        cursor.execute("UPDATE book SET status = 'Rented' WHERE book_id = %s", (book_id,))
                        mydb.commit()

                        # Show success message
                        message = f"Rental transaction successful.\nReturn book on: {deadline}\nTotal Amount: P{total_amount}\n\nNOTE:\nFailure to return the book on time will result in a daily late fee of P10.00."
                        messagebox.showinfo("Success", message)

                        # Reset the entry fields
                        borrower_id_entry.delete(0, tk.END)
                        book_id_entry.delete(0, tk.END)
                        rent_duration_entry.delete(0, tk.END)

                        # Update the tree_rent with the latest data
                        rent_tree()

                        show_main_frame()
                    else:
                        messagebox.showerror("Error", "Invalid rent duration. Please enter a valid number.")
            else:
                messagebox.showerror("Error", "Invalid book ID")
        else:
            messagebox.showerror("Error", "Invalid borrower ID")
    else:
        messagebox.showerror("Error", "Please fill in all the fields.")

def show_return_book_frame():
    return_book_frame.tkraise()

def print_rented_books(borrower_id):
    # Clear existing data in the Treeview
    tree_return.delete(*tree_return.get_children())

    # Execute the SQL query to fetch the rented books for the specified borrower ID
    cursor.execute("SELECT book.book_id, book.title, book.author, book.category_id, book.price, book.status FROM book INNER JOIN rents ON book.book_id = rents.book_id WHERE rents.borrower_id = %s AND rents.status <> 'Returned'", (borrower_id,))
    rented_books = cursor.fetchall()

    # Populate the Treeview with fetched data
    for book in rented_books:
        tree_return.insert("", "end", values=book)

def check_borrower_id_for_return():
    # Create a new top-level window for the pop-up
    popup_window = ctk.CTkToplevel(root)
    popup_window.geometry("300x190+780+300")

    # Set the title of the pop-up window
    popup_window.title("Book Rental")

    # Create a label with the caption "Enter Borrower ID"
    label = ctk.CTkLabel(popup_window, text="Enter Borrower ID", font=ctk.CTkFont('Arial', size=12, weight='bold'))
    label.pack(padx=32, pady=30)

    # Create an entry box to enter the borrower ID
    entry = ctk.CTkEntry(popup_window)
    entry.place(x=82, y=70)

    def validate_borrower_id():
        borrower_id = entry.get()

        # Check if the borrower ID exists in the database
        cursor.execute("SELECT COUNT(*) FROM borrower WHERE borrower_id = %s", (borrower_id,))
        count = cursor.fetchone()[0]

        if count == 1:
            popup_window.destroy()  # Close the popup window

            # Open the rent book frame
            return_book_frame.tkraise()

            # Print out the rented books in the tree_return
            print_rented_books(borrower_id)
        else:
            # Display an error message in the popup window
            error_label = ctk.CTkLabel(popup_window, text_color='red', text="Borrower ID not found or registered!")
            error_label.place(x=52, y=30)

    # Create a sign-in button
    enter_button = ctk.CTkButton(popup_window, text="Enter", command=validate_borrower_id)
    enter_button.place(x=82, y=105)
    
    popup_window.wm_transient(root)

def return_book():
    # Retrieve the book ID entered by the borrower
    book_id = book_id_in_return_entry.get().strip()

    try:
        # Convert book_id to an integer
        book_id = int(book_id)
        
        # Check if the entered book ID matches any rented books in the tree_return
        book_ids = [tree_return.item(item)['values'][0] for item in tree_return.get_children()]
        if book_id in book_ids:
            # Book ID is valid and matches a rented book in the tree_return
            # Get the current date
            return_date = datetime.date.today()

            # Update the return_date and status columns in the rents table
            cursor.execute(
                "UPDATE rents SET return_date = %s, status = 'Returned' WHERE book_id = %s",
                (return_date, book_id)
            )
            mydb.commit()

            # Update the status column in the book table
            cursor.execute("UPDATE book SET status = 'Available' WHERE book_id = %s", (book_id,))
            mydb.commit()

            # Calculate late fee if applicable
            # Retrieve the deadline from the most recent entry in the rents table that matches the book ID
            cursor.execute("SELECT deadline FROM rents WHERE book_id = %s ORDER BY rental_id DESC LIMIT 1", (book_id,))
            result = cursor.fetchone()

            if result:
                deadline = result[0]  # Extract the deadline from the result

                # Calculate late fee
                late_fee = 0.00
                if return_date > deadline:
                    late_days = (return_date - deadline).days
                    late_fee = late_days * 10.00

                # Update the late_fees column in the rents table for the most recent book ID that matches
                cursor.execute('''
                    UPDATE rents AS r1
                    JOIN (
                        SELECT rental_id
                        FROM rents
                        WHERE book_id = %s
                        ORDER BY rental_id DESC
                        LIMIT 1
                    ) AS r2 ON r1.rental_id = r2.rental_id
                    SET r1.late_fees = %s
                    WHERE r1.book_id = %s
                ''', (book_id, late_fee, book_id))
                mydb.commit()

                if late_fee > 0:
                    messagebox.showinfo("Success", f"Book returned successfully. You have a late fee of {late_fee:.2f}.")
                else:
                    messagebox.showinfo("Success", "Book returned successfully.")

            # Remove the returned book from the treeview
            for item in tree_return.get_children():
                if tree_return.item(item)['values'][0] == book_id:
                    tree_return.delete(item)
                    
            # Clear the entry box
            book_id_in_return_entry.delete(0, 'end')
        else:
            messagebox.showerror("Error", "Invalid book ID.")
    except ValueError:
        messagebox.showerror("Error", "Invalid book ID. Please enter a valid integer.")




def search_data():
    category = category_combobox.get()
    search_query = entry_in_admin.get()

    if category == 'Borrower':
        search_borrower(search_query)
    elif category == 'Book':
        search_book(search_query)
    elif category == 'Category':
        search_category(search_query)
    elif category == 'Rents':
        search_rents(search_query)

def search_borrower(query):
    query = f"SELECT * FROM borrower WHERE borrower_id='{query}' OR name LIKE '%{query}%'"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Clear existing data in the scrollable frame
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # Create a Treeview widget
    stree = ttk.Treeview(scrollable_frame, columns=("Borrower ID", "Name", "Phone", "Email", "Address"), show="headings", height=18)
    stree.pack()

    stree.column("#0", width=0)
    stree.column('Borrower ID', width=200)
    stree.column('Name', width=200)
    stree.column('Phone', width=200)
    stree.column('Email', width=200)
    stree.column('Address', width=200)

    # Define the columns
    stree.heading("#0", text="", anchor="w")
    stree.heading("Borrower ID", text="Borrower ID")
    stree.heading("Name", text="Name")
    stree.heading("Phone", text="Phone")
    stree.heading("Email", text="Email")
    stree.heading("Address", text="Address")
    
    # Display the search results in the Treeview
    for row in rows:
        stree.insert("", tk.END, values=row)

    # Add a scrollbar to the Treeview
    scrollbar = ttk.Scrollbar(scrollable_frame, orient="vertical", command=stree.yview)
    stree.configure(yscroll=scrollbar.set)
    scrollbar.place(x=987, y=0, height=479)

def search_book(query):
    query = f"SELECT book.book_id, book.category_id, category.category_name, book.title, book.author, book.price, book.status FROM book INNER JOIN category ON book.category_id = category.category_id WHERE book.book_id='{query}' OR category.category_name LIKE '%{query}%' OR book.title LIKE '%{query}%' OR book.author LIKE '%{query}%' OR book.status LIKE '%{query}%'"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Clear existing data in the scrollable frame
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # Create a Treeview widget
    stree = ttk.Treeview(scrollable_frame, columns=("Book ID", "Category ID", "Category Name", "Title", "Author", "Price", "Status"), show="headings", height=18)
    stree.pack()
    
    stree.column("#0", width=0)
    stree.column("Book ID", width=50)
    stree.column("Category ID", width=70)
    stree.column("Category Name", width=130)
    stree.column("Title", width=300)
    stree.column("Author", width=250)
    stree.column("Price", width=100)
    stree.column("Status", width=100)

    # Define the columns
    stree.heading("Book ID", text="Book ID")
    stree.heading("Category ID", text="Category ID")
    stree.heading("Category Name", text="Category Name")
    stree.heading("Title", text="Title")
    stree.heading("Author", text="Author")
    stree.heading("Price", text="Price")
    stree.heading("Status", text="Status")

    # Display the search results in the Treeview
    for row in rows:
        stree.insert("", tk.END, values=row)

    # Add a scrollbar to the Treeview
    scrollbar = ttk.Scrollbar(scrollable_frame, orient="vertical", command=stree.yview)
    stree.configure(yscroll=scrollbar.set)
    scrollbar.place(x=987, y=0, height=479)

def search_category(query):
    query = f"SELECT * FROM category WHERE category_id='{query}' OR category_name LIKE '%{query}%'"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Clear existing data in the scrollable frame
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # Create a Treeview widget
    stree = ttk.Treeview(scrollable_frame, columns=("Category ID", "Category Name"), show="headings", height=18)
    stree.pack()

    stree.column("#0", width=0)
    stree.column("Category ID", width=500)
    stree.column("Category Name", width=500)

    # Define the columns
    stree.heading("Category ID", text="Category ID")
    stree.heading("Category Name", text="Category Name")

    # Display the search results in the Treeview
    for row in rows:
        stree.insert("", tk.END, values=row)

    # Add a scrollbar to the Treeview
    scrollbar = ttk.Scrollbar(scrollable_frame, orient="vertical", command=stree.yview)
    stree.configure(yscroll=scrollbar.set)
    scrollbar.place(x=987, y=0, height=479)

def search_rents(query):
    if not query:
        query = "SELECT * FROM rents"
    else:
        query = f"SELECT * FROM rents WHERE rental_id='{query}' OR status LIKE '%{query}%' OR payment_method LIKE '%{query}%'"

    cursor.execute(query)
    rows = cursor.fetchall()

    # Clear existing data in the scrollable frame
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # Create a Treeview widget
    stree = ttk.Treeview(scrollable_frame, columns=("Rental ID", "Book ID", "Borrower ID", "Rented Date", "Deadline", "Return Date", "Payment Method", "Total Amount", "Late Fees", "Status"), show="headings", height=18)
    stree.pack()

    stree.column("#0", width=0)
    stree.column("Rental ID", width=100)
    stree.column("Book ID", width=100)
    stree.column("Borrower ID", width=100)
    stree.column("Rented Date", width=100)
    stree.column("Deadline", width=100)
    stree.column("Return Date", width=100)
    stree.column("Payment Method", width=100)
    stree.column("Total Amount", width=100)
    stree.column("Late Fees", width=100)
    stree.column("Status", width=100)

    # Define the columns
    stree.heading("Rental ID", text="Rental ID")
    stree.heading("Book ID", text="Book ID")
    stree.heading("Borrower ID", text="Borrower ID")
    stree.heading("Rented Date", text="Rented Date")
    stree.heading("Deadline", text="Deadline")
    stree.heading("Return Date", text="Return Date")
    stree.heading("Payment Method", text="Payment Method")
    stree.heading("Total Amount", text="Total Amount")
    stree.heading("Late Fees", text="Late Fees")
    stree.heading("Status", text="Status")

    # Display the search results in the Treeview
    for row in rows:
        values = [value if value is not None else "" for value in row]
        stree.insert("", tk.END, values=values)

    # Add a scrollbar to the Treeview
    scrollbar = ttk.Scrollbar(scrollable_frame, orient="vertical", command=stree.yview)
    stree.configure(yscroll=scrollbar.set)
    scrollbar.place(x=987, y=0, height=479)




def show_category_crudl_frame():
    category_crudl_frame.tkraise()

def show_book_crudl_frame():
    book_crudl_frame.tkraise()

def show_borrower_crudl_frame():
    borrower_crudl_frame.tkraise()

def show_rent_crudl_frame():
    rent_crudl_frame.tkraise()




def show_add_borrower_frame():
    add_borrower_frame.tkraise()

def add_borrower():
    name = add_borrower_name_entry.get()
    phone = add_borrower_phone_entry.get()
    email = add_borrower_email_entry.get()
    address = add_borrower_address_entry.get()

    if name and phone and email and address:
        # Insert the new borrower into the database
        add_borrower_query = "INSERT INTO borrower (name, phone, email, address) VALUES (%s, %s, %s, %s)"
        borrower_values = (name, phone, email, address)
        cursor.execute(add_borrower_query, borrower_values)
        mydb.commit()

        # Display success message
        messagebox.showinfo("Success", "Borrower added successfully!")

        # Clear the entry fields
        add_borrower_name_entry.delete(0, tk.END)
        add_borrower_phone_entry.delete(0, tk.END)
        add_borrower_email_entry.delete(0, tk.END)
        add_borrower_address_entry.delete(0, tk.END)
    else:
        # Display error message if any field is empty
        messagebox.showerror("Error", "Please fill in all the fields.")

def show_delete_borrower_frame():
    delete_borrower_frame.tkraise()

def delete_borrower():
    borrower_id = delete_borrower_id_entry.get()

    if borrower_id:
        # Delete the borrower from the database
        delete_borrower_query = "DELETE FROM borrower WHERE borrower_id = %s"
        borrower_values = (borrower_id,)
        cursor.execute(delete_borrower_query, borrower_values)
        mydb.commit()

        # Display success message
        messagebox.showinfo("Success", "Borrower deleted successfully!")

        # Clear the entry field
        delete_borrower_id_entry.delete(0, tk.END)
    else:
        # Display error message if the borrower ID field is empty
        messagebox.showerror("Error", "Please enter the Borrower ID.")

def show_update_borrower_frame():
    update_borrower_frame.tkraise()

def show_update_borrower_entries_frame():
    update_borrower_entries_frame.tkraise()

def check_borrower_existence():
    borrower_id = update_borrower_id_entry.get()

    if borrower_id:
        # Check if the borrower exists in the database
        select_borrower_query = "SELECT * FROM borrower WHERE borrower_id = %s"
        borrower_values = (borrower_id,)
        cursor.execute(select_borrower_query, borrower_values)
        borrower = cursor.fetchone()

        if borrower:
            # Display the update borrower entries frame
            show_update_borrower_entries_frame()

            # Pre-fill the entry fields with existing data
            
            update_borrower_name_entry.delete(0, tk.END)
            update_borrower_name_entry.insert(0, borrower[1])
            update_borrower_phone_entry.delete(0, tk.END)
            update_borrower_phone_entry.insert(0, borrower[2])
            update_borrower_email_entry.delete(0, tk.END)
            update_borrower_email_entry.insert(0, borrower[3])
            update_borrower_address_entry.delete(0, tk.END)
            update_borrower_address_entry.insert(0, borrower[4])
        else:
            # Display error message if the borrower does not exist
            messagebox.showerror("Error", "Borrower does not exist.")
    else:
        # Display error message if the borrower ID field is empty
        messagebox.showerror("Error", "Please enter the Borrower ID.")

def update_borrower():
    borrower_id = update_borrower_id_entry.get()
    borrower_name = update_borrower_name_entry.get()
    borrower_phone = update_borrower_phone_entry.get()
    borrower_email = update_borrower_email_entry.get()
    borrower_address = update_borrower_address_entry.get()

    # Update the borrower in the database
    update_borrower_query = "UPDATE borrower SET name = %s, phone = %s, email = %s, address = %s WHERE borrower_id = %s"
    borrower_values = (borrower_name, borrower_phone, borrower_email, borrower_address, borrower_id)
    cursor.execute(update_borrower_query, borrower_values)
    mydb.commit()

    # Display success message
    messagebox.showinfo("Success", "Borrower updated successfully!")

    # Clear the entry fields
    update_borrower_id_entry.delete(0, tk.END)
    update_borrower_name_entry.delete(0, tk.END)
    update_borrower_phone_entry.delete(0, tk.END)
    update_borrower_email_entry.delete(0, tk.END)
    update_borrower_address_entry.delete(0, tk.END)

def show_list_borrowers_frame():
    list_borrowers_frame.tkraise()

def list_borrowers():
    
    # Clear previous entries in the treeview
    borrowers_treeview.delete(*borrowers_treeview.get_children())

    # Fetch categories from the database
    fetch_borrowers_query = "SELECT * FROM borrower"
    cursor.execute(fetch_borrowers_query)
    borrowers = cursor.fetchall()

    # Insert categories into the treeview
    for borrower in borrowers:
        borrower_id = borrower[0]
        name = borrower[1]
        phone = borrower[2]
        email = borrower[3]
        address = borrower[4]
        borrowers_treeview.insert('', 'end', values=(borrower_id, name, phone, email, address))




def show_add_book_frame():
    add_book_frame.tkraise()

def add_book():
    category = add_book_category_entry.get()
    author = add_book_author_entry.get()
    title = add_book_title_entry.get()
    price = add_book_price_entry.get()
    status = add_book_status_entry.get()

    if category and author and title and price and status:
        # Insert the book into the database
        insert_book_query = "INSERT INTO book (category_id, author, title, price, status) VALUES (%s, %s, %s, %s, %s)"
        book_values = (category, author, title, price, status)
        cursor.execute(insert_book_query, book_values)
        mydb.commit()

        # Display success message
        messagebox.showinfo("Success", "Book added successfully!")

        # Clear the entry fields
        add_book_category_entry.delete(0, 'end')
        add_book_author_entry.delete(0, 'end')
        add_book_title_entry.delete(0, 'end')
        add_book_price_entry.delete(0, 'end')
        add_book_status_entry.delete(0, 'end')
    else:
        # Display error message if any field is empty
        messagebox.showerror("Error", "All fields must be filled!")

def show_delete_book_frame():
    delete_book_frame.tkraise()

def delete_book():
    book_id = delete_book_id_entry.get()

    if book_id:
        # Delete the book from the database
        delete_book_query = "DELETE FROM book WHERE book_id = %s"
        book_value = (book_id,)
        cursor.execute(delete_book_query, book_value)
        mydb.commit()

        # Display success message
        messagebox.showinfo("Success", "Book deleted successfully!")

        # Clear the entry field
        delete_book_id_entry.delete(0, 'end')
    else:
        # Display error message if book ID field is empty
        messagebox.showerror("Error", "Book ID field must be filled!")

def show_update_book_frame():
    update_book_frame.tkraise()

def show_update_book_entries_frame():
    book_id = update_book_id_entry.get()

    if book_id:
        # Check if the book exists in the database
        check_book_query = "SELECT * FROM book WHERE book_id = %s"
        book_value = (book_id,)
        cursor.execute(check_book_query, book_value)
        book = cursor.fetchone()

        if book:
            # Book exists, switch to the update book entries frame
            update_book_entries_frame.tkraise()

            # Pre-fill the entry fields with existing data
            update_book_category_entry.delete(0, tk.END)
            update_book_category_entry.insert(0, book[1])
            update_book_title_entry.delete(0, tk.END)
            update_book_title_entry.insert(0, book[2])
            update_book_author_entry.delete(0, tk.END)
            update_book_author_entry.insert(0, book[3])
            update_book_price_entry.delete(0, tk.END)
            update_book_price_entry.insert(0, book[4])
            update_book_status_entry.delete(0, tk.END)
            update_book_status_entry.insert(0, book[5])
        else:
            # Book does not exist, display error message
            messagebox.showerror("Error", "Book does not exist!")

            # Clear the entry field
            update_book_id_entry.delete(0, 'end')
    else:
        # Display error message if book ID field is empty
        messagebox.showerror("Error", "Book ID field must be filled!")

def update_book():
    book_id = update_book_id_entry.get()
    category = update_book_category_entry.get()
    title = update_book_title_entry.get()
    author = update_book_author_entry.get()
    price = update_book_price_entry.get()
    status = update_book_status_entry.get()

    if book_id:
        # Update the book entries in the database
        update_book_query = "UPDATE book SET category_id = %s, title = %s, author = %s, price = %s, status = %s WHERE book_id = %s"
        book_values = (category, title, author, price, status, book_id)
        cursor.execute(update_book_query, book_values)
        mydb.commit()

        # Display success message
        messagebox.showinfo("Success", "Book entries updated successfully!")

        # Clear the entry fields
        update_book_id_entry.delete(0, 'end')
        update_book_category_entry.delete(0, 'end')
        update_book_title_entry.delete(0, 'end')
        update_book_author_entry.delete(0, 'end')
        update_book_price_entry.delete(0, 'end')
        update_book_status_entry.delete(0, 'end')
    else:
        # Display error message if book ID field is empty
        messagebox.showerror("Error", "Book ID field must be filled!")

def show_list_books_frame():
    list_books_frame.tkraise()

def list_books():
    
    # Clear previous entries in the treeview
    books_treeview.delete(*books_treeview.get_children())

    # Fetch categories from the database
    fetch_books_query = "SELECT * FROM book"
    cursor.execute(fetch_books_query)
    books = cursor.fetchall()

    # Insert categories into the treeview
    for book in books:
        book_id = book[0]
        category_id = book[1]
        title = book[2]
        author = book[3]
        price = book[4]
        status = book[5]
        books_treeview.insert('', 'end', values=(book_id, category_id, title, author, price, status))




def show_add_category_frame():
    add_category_frame.tkraise()

def add_category():
    category_name = category_entry.get()

    if category_name:
        # Insert category into the database
        insert_category_query = "INSERT INTO category (category_name) VALUES (%s)"
        values = (category_name,)
        cursor.execute(insert_category_query, values)
        mydb.commit()

        # Display success message
        messagebox.showinfo('Success', 'Category added successfully!')

        # Clear entry field
        category_entry.delete(0, 'end')
    else:
        # Display error message if category name is empty
        messagebox.showerror('Error', 'Category name cannot be empty!')

def show_delete_category_frame():
    delete_category_frame.tkraise()

def delete_category():
    category_id = category_id_entry.get()

    if category_id:
        # Check if the category ID exists in the database
        check_category_query = "SELECT * FROM category WHERE category_id = %s"
        values = (category_id,)
        cursor.execute(check_category_query, values)
        result = cursor.fetchone()

        if result:
            # Delete the category from the database
            delete_category_query = "DELETE FROM category WHERE category_id = %s"
            cursor.execute(delete_category_query, values)
            mydb.commit()

            # Display success message
            messagebox.showinfo('Success', 'Category deleted successfully!')
        else:
            # Display error message if category ID does not exist
            messagebox.showerror('Error', 'Category ID does not exist!')
    else:
        # Display error message if category ID is empty
        messagebox.showerror('Error', 'Category ID cannot be empty!')

    # Clear entry field
    category_id_entry.delete(0, 'end')

def show_update_category_frame():
    update_category_frame.tkraise()

def show_update_category_name_frame():
    category_id = update_category_id_entry.get()

    if category_id:
        # Check if the category exists in the database
        check_category_query = "SELECT * FROM category WHERE category_id = %s"
        category_value = (category_id,)
        cursor.execute(check_category_query, category_value)
        category = cursor.fetchone()

        if category:
            # Category exists, switch to the update category name frame
            update_category_name_frame.tkraise()

            # Pre-fill the entry fields with existing data
            update_category_name_entry.delete(0, tk.END)
            update_category_name_entry.insert(0, category[1])
        else:
            # Category does not exist, display error message
            messagebox.showerror("Error", "Category does not exist!")

            # Clear the entry field
            update_category_id_entry.delete(0, 'end')
    else:
        # Display error message if category ID field is empty
        messagebox.showerror("Error", "Please enter a category ID!")

def update_category_name():
    category_id = update_category_id_entry.get()
    category_name = update_category_name_entry.get()

    if category_id:
        # Update the category name in the database
        update_category_query = "UPDATE category SET category_name = %s WHERE category_id = %s"
        category_values = (category_name, category_id)
        cursor.execute(update_category_query, category_values)
        mydb.commit()

        # Display success message
        messagebox.showinfo("Success", "Category name updated successfully!")

        # Clear the entry fields
        update_category_id_entry.delete(0, 'end')
        update_category_name_entry.delete(0, 'end')
    else:
        # Display error message if any field is empty
        messagebox.showerror("Error", "Please enter category name!")

def show_list_categories_frame():
    list_categories_frame.tkraise()

def list_categories():
    # Clear previous entries in the treeview
    categories_treeview.delete(*categories_treeview.get_children())

    # Fetch categories from the database
    fetch_categories_query = "SELECT * FROM category"
    cursor.execute(fetch_categories_query)
    categories = cursor.fetchall()

    # Insert categories into the treeview
    for category in categories:
        category_id = category[0]
        category_name = category[1]
        categories_treeview.insert('', 'end', values=(category_id, category_name))




def show_delete_rent_frame():
    delete_rent_frame.tkraise()

def delete_rent():
    rental_id = delete_rent_id_entry.get()

    if rental_id:
        # Delete the rent from the database
        delete_rent_query = "DELETE FROM rents WHERE rental_id = %s"
        rent_value = (rental_id,)
        cursor.execute(delete_rent_query, rent_value)
        mydb.commit()

        # Display success message
        messagebox.showinfo("Success", "rent deleted successfully!")

        # Clear the entry field
        delete_rent_id_entry.delete(0, 'end')
    else:
        # Display error message if rent ID field is empty
        messagebox.showerror("Error", "rent ID field must be filled!")

def show_update_rent_frame():
    update_rent_frame.tkraise()

def show_update_rent_details_frame():
    rental_id = update_rent_id_entry.get()

    if rental_id:
        # Check if the rent exists in the database
        check_rent_query = "SELECT * FROM rents WHERE rental_id = %s"
        rent_value = (rental_id,)
        cursor.execute(check_rent_query, rent_value)
        rent = cursor.fetchone()

        if rent:
            # Pre-fill the entry fields with the existing rent data
            update_rent_book_entry.delete(0, tk.END)
            update_rent_book_entry.insert(0, rent[1])  # book_id
            update_rent_borrower_entry.delete(0, tk.END)
            update_rent_borrower_entry.insert(0, rent[2])  # borrower_id
            update_rent_payment_method_combobox.set(rent[6])  # payment_method

            # Set the return status combobox based on the rent status
            if rent[9] == 'Returned':
                update_rent_return_status_combobox.set('Returned')
            else:
                update_rent_return_status_combobox.set('Ongoing')

            # Show the Update Rent Details frame
            update_rent_details_frame.tkraise()
        else:
            messagebox.showerror("Error", "Rent with ID {} does not exist.".format(rental_id))
    else:
        messagebox.showerror("Error", "Please enter a rental ID!")

def update_rent_details():
    rental_id = update_rent_id_entry.get()
    book_id = update_rent_book_entry.get()
    borrower_id = update_rent_borrower_entry.get()
    payment_method = update_rent_payment_method_combobox.get()
    return_status = update_rent_return_status_combobox.get()
    extension_days = update_rent_extension_entry.get()

    if rental_id and book_id and borrower_id:
        # Check if the rent exists in the database
        check_rent_query = "SELECT * FROM rents WHERE rental_id = %s"
        rent_value = (rental_id,)
        cursor.execute(check_rent_query, rent_value)
        rent = cursor.fetchone()

        if rent:
            # Update the rent details
            update_rent_query = "UPDATE rents SET book_id = %s, borrower_id = %s, payment_method = %s, status = %s WHERE rental_id = %s"
            rent_values = (book_id, borrower_id, payment_method, return_status, rental_id)
            cursor.execute(update_rent_query, rent_values)

            if return_status == 'Returned':
                return_date = datetime.datetime.now().date()  # Convert to datetime.date
                late_fees = rent[8]
                if rent[4] < return_date:
                    late_fees += (return_date - rent[4]).days * 10  # Calculate late fees

                update_rent_query = "UPDATE rents SET return_date = %s, late_fees = %s WHERE rental_id = %s"
                rent_values = (return_date, late_fees, rental_id)
                cursor.execute(update_rent_query, rent_values)

            # Update the extension and total_amount if the rent status is 'Ongoing'
            if return_status == 'Ongoing' and extension_days:
                return_date = None
                late_fees = decimal.Decimal(0.00)
                extension_days = int(extension_days)
                extended_deadline = rent[4] + datetime.timedelta(days=extension_days)
                total_amount = rent[7] + extension_days * 5

                update_rent_query = "UPDATE rents SET deadline = %s, return_date = %s, total_amount = %s, late_fees = %s  WHERE rental_id = %s"
                rent_values = (extended_deadline, None, total_amount, late_fees, rental_id)
                cursor.execute(update_rent_query, rent_values)

            if return_status == 'Ongoing':
                return_date = None
                late_fees = decimal.Decimal(0.00)

                update_rent_query = "UPDATE rents SET return_date = %s, late_fees = %s WHERE rental_id = %s"
                rent_values = (return_date, late_fees, rental_id)
                cursor.execute(update_rent_query, rent_values)
            mydb.commit()

            # Display success message
            messagebox.showinfo("Success", "Rent details updated successfully!")

            # Clear the entry fields
            update_rent_id_entry.delete(0, 'end')
            update_rent_book_entry.delete(0, 'end')
            update_rent_borrower_entry.delete(0, 'end')
            update_rent_extension_entry.delete(0, 'end')
        else:
            messagebox.showerror("Error", "Rent with ID {} does not exist.".format(rental_id))
    else:
        messagebox.showerror("Error", "Please enter Book ID and Borrower ID!")

def show_list_rents_frame():
    list_rents_frame.tkraise()

def list_rents():
    
    # Clear previous entries in the treeview
    rents_treeview.delete(*rents_treeview.get_children())

    # Fetch categories from the database
    fetch_rents_query = "SELECT * FROM rents"
    cursor.execute(fetch_rents_query)
    rents = cursor.fetchall()

    # Insert categories into the treeview
    for rent in rents:
        rental_id = rent[0]
        book_id = rent[1]
        borrower_id = rent[2]
        rented_date = rent[3]
        deadline = rent[4]
        return_date = rent[5]
        payment_method = rent[6]
        total_amount = rent[7]
        late_fees = rent[8]
        status = rent[9]
        rents_treeview.insert('', 'end', values=(rental_id, book_id, borrower_id, rented_date, deadline, return_date, payment_method, total_amount, late_fees, status))



# ----------------- Window ---------------------

root = ctk.CTk()
root.geometry('900x700+400+60')
root.title('Book Rental')

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Disable window resizing
root.resizable(False, False)


# ---------------- Main Frame ------------------

main_frame = ctk.CTkFrame(root)
main_frame.grid(row=0, column=0, sticky='nsew')

# Title
title_label = ctk.CTkLabel(main_frame, text='Book Rental', font=ctk.CTkFont('Times', size=25, weight='bold'))
title_label.place(x=45, y=18)

# Admin Button
admin_button = ctk.CTkButton(main_frame, fg_color='transparent', hover_color='#252124', text='Admin', width=90, command=show_admin_wcode_frame)
admin_button.place(x=770, y=20)

# Frame of All Books Button and Genre ComboBox
line1 = ctk.CTkFrame(main_frame, height=40)
line1.pack(pady=60, fill='x')

# All Books Button
all_button = ctk.CTkButton(main_frame, fg_color='#333333', bg_color='#333333', hover_color='#252124',  text='All Books', width=90, command=show_main_frame)
all_button.place(x=99, y=67)

# Genre ComboBox and Select Genre Label
combo_box = ttk.Combobox(main_frame, width=20, height=100, values=[''])
combo_box.bind('<<ComboboxSelected>>', get_books_by_category)
combo_box.place(x=850, y=88)
 
load_categories()

select_genre_label = ctk.CTkLabel(main_frame, text='Select Genre:', font=('',12), fg_color='#333333', bg_color='#333333')
select_genre_label.place(x=600, y=65)

# Search Bar
entry_in_main = ctk.CTkEntry(main_frame, placeholder_text='   Search book title', width=578)
entry_in_main.place(x=99, y=140)

# Search Button
search_button = ctk.CTkButton(main_frame, text='Search', width=115, command=search_books_for_main)
search_button.place(x=684, y=140)

# New Borrower Button
new_borrower_button = ctk.CTkButton(main_frame, text='New Borrower', width=115, command=show_new_borrower_frame)
new_borrower_button.place(x=438, y=599)

# Rent Button
rent_button = ctk.CTkButton(main_frame, text='Rent a Book', width=115, command=show_rent_book_frame)
rent_button.place(x=561, y=599)

# Return Button
return_button = ctk.CTkButton(main_frame, text='Return a Book', width=115, command=check_borrower_id_for_return)
return_button.place(x=684, y=599)

# Style the tree
style = ttk.Style()
style.theme_use('clam')

style.configure('Treeview',
    background='#f2f2f0',
    foreground='black',
    rowheight=25,
    fieldbackground='#f2f2f0'
    )

style.map('Treeview',
    background=[('selected', '#1e81b0')])

# Treeview Frame
tree_frame = ctk.CTkFrame(main_frame, width=735, height=420)
tree_frame.pack(padx=100, pady=21)

# Treeview Scrollbar
tree_scroll = ctk.CTkScrollbar(tree_frame, orientation='vertical', command='tree.yview')
tree_scroll.pack(side='right', fill='y')

# Create Treeview
tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, columns=('Book ID', 'Title', 'Author', 'Category', 'Price', 'Status'), show='headings', height=19)
tree.pack(side='left', fill='both', expand=True)

# Configure the scrollbar
tree_scroll.configure(command=tree.yview)

# Format columns
tree.column('#0', width=0, minwidth=25)
tree.column('Book ID', width=60)
tree.column('Title', width=290)
tree.column('Author', width=260)
tree.column('Category', width=80)
tree.column('Price', width=80)
tree.column('Status', width=80)

# Headings
tree.heading('#0', text='')
tree.heading('Book ID', text='Book ID', anchor='center')
tree.heading('Title', text='Title', anchor='center')
tree.heading('Author', text='Author', anchor='center')
tree.heading('Category', text='Category', anchor='center')
tree.heading('Price', text='Price', anchor='center')
tree.heading('Status', text='Status', anchor='center')

# --------------- New Borrower Frame ----------------

new_borrower_frame = ctk.CTkFrame(root)
new_borrower_frame.grid(row=0, column=0, sticky='nsew')

# Title
title_label = ctk.CTkLabel(new_borrower_frame, text='Book Rental', font=ctk.CTkFont('Times', size=25, weight='bold'))
title_label.place(x=45, y=18)

# Frame of All Books Button and Genre ComboBox
line1 = ctk.CTkFrame(new_borrower_frame, height=40)
line1.pack(pady=60, fill='x')

# Frame for fill up form
new_borrower_fill_up_frame = ctk.CTkFrame(new_borrower_frame, width=745, height=360)
new_borrower_fill_up_frame.place(x=75, y=130)

# New Borrower title
new_borrower_label = ctk.CTkLabel(new_borrower_fill_up_frame, text='New Borrower Form', font=ctk.CTkFont('Calibri', size=32, weight='normal'))
new_borrower_label.place(x=50, y=35)

# Enter name
name_label = ctk.CTkLabel(new_borrower_fill_up_frame, text='Name', font=ctk.CTkFont('Calibri', size=12, weight='bold'))
name_label.place(x=50, y=100)

name_entry = ctk.CTkEntry(new_borrower_fill_up_frame, placeholder_text='  Juan Cruz', width=300)
name_entry.place(x=50, y=125)

# Enter address
address_label = ctk.CTkLabel(new_borrower_fill_up_frame, text='Address', font=ctk.CTkFont('Calibri', size=12, weight='bold'))
address_label.place(x=50, y=165)

address_entry = ctk.CTkEntry(new_borrower_fill_up_frame, placeholder_text='  Phase 1 Block 23 Vendetta Street', width=300)
address_entry.place(x=50, y=190)

# Enter phone
phone_label = ctk.CTkLabel(new_borrower_fill_up_frame, text='Phone No.', font=ctk.CTkFont('Calibri', size=12, weight='bold'))
phone_label.place(x=390, y=100)

phone_entry = ctk.CTkEntry(new_borrower_fill_up_frame, placeholder_text='  09XXXXXXXXX', width=300)
phone_entry.place(x=390, y=125)

# Enter address
email_label = ctk.CTkLabel(new_borrower_fill_up_frame, text='Email', font=ctk.CTkFont('Calibri', size=12, weight='bold'))
email_label.place(x=390, y=165)

email_entry = ctk.CTkEntry(new_borrower_fill_up_frame, placeholder_text='  example123@gmail.com', width=300)
email_entry.place(x=390, y=190)

# Register Button
register_button = ctk.CTkButton(new_borrower_fill_up_frame, text='Register', width=100, command=register_new_borrower)
register_button.place(x=50, y=270)

# Cancel Button
cancel_button = ctk.CTkButton(new_borrower_fill_up_frame, fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=100, command=show_main_frame)
cancel_button.place(x=160, y=270)


# --------------- Rent a Book Frame -----------------

rent_book_frame = ctk.CTkFrame(root)
rent_book_frame.grid(row=0, column=0, sticky='nsew')

# Title
title_label = ctk.CTkLabel(rent_book_frame, text='Book Rental', font=ctk.CTkFont('Times', size=25, weight='bold'))
title_label.place(x=45, y=18)

# Frame of All Books Button and Genre ComboBox
line1 = ctk.CTkFrame(rent_book_frame, height=40)
line1.pack(pady=60, fill='x')

# All Books Button
all_button_in_rent = ctk.CTkButton(rent_book_frame, fg_color='#333333', bg_color='#333333', hover_color='#252124',  text='All Books', width=90, command=list_all_books)
all_button_in_rent.place(x=99, y=67)

# Genre ComboBox and Select Genre Label
combo_box_in_rent = ttk.Combobox(rent_book_frame, width=20, height=100, values=[''])
combo_box_in_rent.bind('<<ComboboxSelected>>', get_books_by_category_in_rent)
combo_box_in_rent.place(x=850, y=88)

load_categories_in_rent()

select_genre_label_in_rent = ctk.CTkLabel(rent_book_frame, text='Select Genre:', font=('',12), fg_color='#333333', bg_color='#333333')
select_genre_label_in_rent.place(x=600, y=65)

# Frame for fill up form
fill_up_frame_for_rent = ctk.CTkFrame(rent_book_frame, width=800, height=510)
fill_up_frame_for_rent.place(x=52, y=120)

# Borrower id entry
borrower_id_label = ctk.CTkLabel(fill_up_frame_for_rent, text='Borrower ID', font=ctk.CTkFont('Calibri', size=12, weight='bold'))
borrower_id_label.place(x=40, y=50)

borrower_id_entry = ctk.CTkEntry(fill_up_frame_for_rent)
borrower_id_entry.place(x=40, y=75)

# Book id entry
book_id_label = ctk.CTkLabel(fill_up_frame_for_rent, text='Book ID', font=ctk.CTkFont('Calibri', size=12, weight='bold'))
book_id_label.place(x=40, y=110)

book_id_entry = ctk.CTkEntry(fill_up_frame_for_rent)
book_id_entry.place(x=40, y=135)

# Rent Duration
rent_duration_label = ctk.CTkLabel(fill_up_frame_for_rent, text='Rent Duration (1 Day = P5.00)', font=ctk.CTkFont('Calibri', size=12, weight='bold'))
rent_duration_label.place(x=40, y=170)

rent_duration_entry = ctk.CTkEntry(fill_up_frame_for_rent)
rent_duration_entry.place(x=40, y=195)

# Payment method
payment_method_label = ctk.CTkLabel(fill_up_frame_for_rent, text='Payment Method', font=ctk.CTkFont('Calibri', size=12, weight='bold'))
payment_method_label.place(x=40, y=230)

payment_method_combobox = ctk.CTkComboBox(fill_up_frame_for_rent, values=["Cash", "Credit Card", "Online Payment"])
payment_method_combobox.place(x=40, y=255)

# Search Bar
entry_in_rent = ctk.CTkEntry(fill_up_frame_for_rent, placeholder_text='   Search book title', width=415)
entry_in_rent.place(x=240, y=50)

# Search Button
rent_search_button = ctk.CTkButton(fill_up_frame_for_rent, text='Search', width=100, command=search_books_for_rent)
rent_search_button.place(x=662, y=50)

# Create a button to initiate the rental transaction
confirm_rental_button = ctk.CTkButton(fill_up_frame_for_rent, text="Confirm", width=100, command=create_rental_transaction)
confirm_rental_button.place(x=552, y=445)

# Create a button to cancel the rental transaction
cancel_rental_button = ctk.CTkButton(fill_up_frame_for_rent, text="Cancel", fg_color='transparent', border_color='#1f6aa5', border_width=2, width=100, command=show_main_frame)
cancel_rental_button.place(x=662, y=445)

# Treeview Frame
tree_frame = ctk.CTkFrame(fill_up_frame_for_rent, width=735, height=420)
tree_frame.place(x=240, y=90)

# Treeview Scrollbar
tree_rent_scroll = ctk.CTkScrollbar(tree_frame, orientation='vertical', command='tree.yview')
tree_rent_scroll.pack(side='right', fill='y')

# Create Treeview
tree_rent = ttk.Treeview(tree_frame, yscrollcommand=tree_rent_scroll.set, columns=('Book ID', 'Title', 'Author', 'Category', 'Price', 'Status'), show='headings', height=15)
tree_rent.pack(side='left', fill='both', expand=True)

# Configure the scrollbar
tree_rent_scroll.configure(command=tree.yview)

# Format columns
tree_rent.column('#0', width=0, minwidth=25)
tree_rent.column('Book ID', width=50)
tree_rent.column('Title', width=180)
tree_rent.column('Author', width=180)
tree_rent.column('Category', width=70)
tree_rent.column('Price', width=70)
tree_rent.column('Status', width=80)

# Headings
tree_rent.heading('#0', text='')
tree_rent.heading('Book ID', text='Book ID', anchor='center')
tree_rent.heading('Title', text='Title', anchor='center')
tree_rent.heading('Author', text='Author', anchor='center')
tree_rent.heading('Category', text='Category', anchor='center')
tree_rent.heading('Price', text='Price', anchor='center')
tree_rent.heading('Status', text='Status', anchor='center')


# -------------- Return a Book Frame ---------------

return_book_frame = ctk.CTkFrame(root)
return_book_frame.grid(row=0, column=0, sticky='nsew')

# Title
title_label = ctk.CTkLabel(return_book_frame, text='Book Rental', font=ctk.CTkFont('Times', size=25, weight='bold'))
title_label.place(x=45, y=18)

# Frame for function buttons
line1 = ctk.CTkFrame(return_book_frame, height=40)
line1.pack(pady=60, fill='x')

# Frame for fill up form
fill_up_frame_for_return = ctk.CTkFrame(return_book_frame, width=800, height=400)
fill_up_frame_for_return.place(x=52, y=120)

# Borrower id entry
book_id_in_return_label = ctk.CTkLabel(fill_up_frame_for_return, text='Book ID', font=ctk.CTkFont('Calibri', size=12, weight='bold'))
book_id_in_return_label.place(x=45, y=50)

book_id_in_return_entry = ctk.CTkEntry(fill_up_frame_for_return)
book_id_in_return_entry.place(x=45, y=75)

# Treeview Frame
tree_frame = ctk.CTkFrame(fill_up_frame_for_return, width=735, height=420)
tree_frame.place(x=230, y=50)

# Treeview Scrollbar
tree_return_scroll = ctk.CTkScrollbar(tree_frame, orientation='vertical', command='tree.yview')
tree_return_scroll.pack(side='right', fill='y')

# Create Treeview
tree_return = ttk.Treeview(tree_frame, yscrollcommand=tree_return_scroll.set, columns=('Book ID', 'Title', 'Author', 'Category', 'Price', 'Status'), show='headings', height=8)
tree_return.pack(side='left', fill='both', expand=True)

# Configure the scrollbar
tree_return_scroll.configure(command=tree.yview)

# Format columns
tree_return.column('#0', width=0, minwidth=25)
tree_return.column('Book ID', width=50)
tree_return.column('Title', width=180)
tree_return.column('Author', width=180)
tree_return.column('Category', width=70)
tree_return.column('Price', width=70)
tree_return.column('Status', width=80)

# Headings
tree_return.heading('#0', text='')
tree_return.heading('Book ID', text='Book ID', anchor='center')
tree_return.heading('Title', text='Title', anchor='center')
tree_return.heading('Author', text='Author', anchor='center')
tree_return.heading('Category', text='Category', anchor='center')
tree_return.heading('Price', text='Price', anchor='center')
tree_return.heading('Status', text='Status', anchor='center')

# Return Book Button
confirm_return_button = ctk.CTkButton(fill_up_frame_for_return, text='Confirm', width=100, command=return_book)
confirm_return_button.place(x=540, y=300)

# Cancel button
cancel_return_button = ctk.CTkButton(fill_up_frame_for_return, text="Cancel", fg_color='transparent', border_color='#1f6aa5', border_width=2, width=100, command=show_main_frame)
cancel_return_button.place(x=650, y=300)







































# ---------------- Admin Frame ------------------

admin_frame = ctk.CTkFrame(root)
admin_frame.grid(row=0, column=0, sticky='nsew')

# Title
title_label = ctk.CTkLabel(admin_frame, text='Book Rental', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
title_label.place(x=45, y=18)

# Main Button
home_button = ctk.CTkButton(admin_frame, fg_color='transparent', hover_color='grey', text='Home', width=90, command=show_main_frame)
home_button.place(x=770, y=20)

# Frame for function buttons
line1 = ctk.CTkFrame(admin_frame, height=66)
line1.pack(pady=60, fill='x')

# Search Bar
entry_in_admin = ctk.CTkEntry(admin_frame, placeholder_text='Search', width=500)
entry_in_admin.place(x=93, y=140)

# Search Category Combobox
category_combobox = ttk.Combobox(admin_frame, values=['Borrower', 'Book', 'Category', 'Rents'], width=15, height=80)
category_combobox.place(x=745, y=182)

# Search Button
search_button = ctk.CTkButton(admin_frame, text='Search', width=120, command=search_data)
search_button.place(x=694, y=140)

# Scrollable frame
scrollable_frame = ctk.CTkScrollableFrame(admin_frame, width=800, height=400)
scrollable_frame.place(x=40, y=180)

# Create a Treeview widget for displaying search results
stree = ttk.Treeview(scrollable_frame, columns=("0"), show="headings", height=18)
stree.pack()
stree.column("0", width=1000)

# Function Buttons
borrower_crudl_button = ctk.CTkButton(master=admin_frame, fg_color='#333333', bg_color='#333333', text='Borrower', width=100, font=ctk.CTkFont('Calibri', size=15, weight='bold'), command=show_borrower_crudl_frame)
borrower_crudl_button.place(x=255, y=75)

book_crudl_button = ctk.CTkButton(master=admin_frame, fg_color='#333333', bg_color='#333333', text='Book', width=100, font=ctk.CTkFont('Calibri', size=15, weight='bold'), command=show_book_crudl_frame)
book_crudl_button.place(x=355, y=75)

category_crudl_button = ctk.CTkButton(master=admin_frame, fg_color='#333333', bg_color='#333333', text='Category', width=100, font=ctk.CTkFont('Calibri', size=15, weight='bold'), command=show_category_crudl_frame)
category_crudl_button.place(x=455, y=75)

rent_crudl_button = ctk.CTkButton(master=admin_frame, fg_color='#333333', bg_color='#333333', text='Rent', width=100, font=ctk.CTkFont('Calibri', size=15, weight='bold'), command=show_rent_crudl_frame)
rent_crudl_button.place(x=555, y=75)





# ----------------- Borrower CRUDL Frame -------------------

borrower_crudl_frame = ctk.CTkFrame(root)
borrower_crudl_frame.grid(row=0, column=0, sticky='nsew')

# Add Borrower Title
add_borrower_title_label = ctk.CTkLabel(borrower_crudl_frame, text='CRUDL borrower', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
add_borrower_title_label.place(x=25, y=18)

# Frame for function buttons
add_borrower_fill_up_frame = ctk.CTkFrame(borrower_crudl_frame, width=345, height=360)
add_borrower_fill_up_frame.place(x=255, y=130)

# Function Buttons
add_borrower_button = ctk.CTkButton(master=borrower_crudl_frame, text='Add New Borrower', 
                                    font=ctk.CTkFont('Calibri', size=20, weight='bold'), width=80, command=show_add_borrower_frame)
add_borrower_button.place(x=340, y=165)

delete_borrower_button = ctk.CTkButton(master=borrower_crudl_frame, text='Delete Borrower', 
                                       font=ctk.CTkFont('Calibri', size=20, weight='bold'), width=100, command=show_delete_borrower_frame)
delete_borrower_button.place(x=350, y=215)

update_borrower_button = ctk.CTkButton(master=borrower_crudl_frame, text='Update Borrower', 
                                       font=ctk.CTkFont('Calibri', size=20, weight='bold'), width=120, command=show_update_borrower_frame)
update_borrower_button.place(x=348, y=265)

list_borrowers_button = ctk.CTkButton(master=borrower_crudl_frame, text='List Borrowers', 
                                      font=ctk.CTkFont('Calibri', size=20, weight='bold'), width=120, command=show_list_borrowers_frame)
list_borrowers_button.place(x=359, y=315)

# Cancel Button in Borrower Frame
cancel_borrower_crudl_button = ctk.CTkButton(master=borrower_crudl_frame, fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=80, command=show_admin_frame)
cancel_borrower_crudl_button.place(x=390, y=400)

# ----------------- Book CRUDL Frame -------------------

book_crudl_frame = ctk.CTkFrame(root)
book_crudl_frame.grid(row=0, column=0, sticky='nsew')

# Add Borrower Title
add_borrower_title_label = ctk.CTkLabel(book_crudl_frame, text='CRUDL book', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
add_borrower_title_label.place(x=25, y=18)

# Frame for function buttons
add_book_fill_up_frame = ctk.CTkFrame(book_crudl_frame, width=345, height=360)
add_book_fill_up_frame.place(x=255, y=130)

# Function Buttons
add_book_button = ctk.CTkButton(master=book_crudl_frame, text='Add New Book', 
                                    font=ctk.CTkFont('Calibri', size=20, weight='bold'), width=80, command=show_add_book_frame)
add_book_button.place(x=357, y=165)

delete_book_button = ctk.CTkButton(master=book_crudl_frame, text='Delete Book', 
                                       font=ctk.CTkFont('Calibri', size=20, weight='bold'), width=100, command=show_delete_book_frame)
delete_book_button.place(x=368, y=215)

update_book_button = ctk.CTkButton(master=book_crudl_frame, text='Update Book', 
                                       font=ctk.CTkFont('Calibri', size=20, weight='bold'), width=120, command=show_update_book_frame)
update_book_button.place(x=365, y=265)

list_books_button = ctk.CTkButton(master=book_crudl_frame, text='List Books', 
                                      font=ctk.CTkFont('Calibri', size=20, weight='bold'), width=120, command=show_list_books_frame)
list_books_button.place(x=366, y=315)

# Cancel Button in book Frame
cancel_book_crudl_button = ctk.CTkButton(master=book_crudl_frame, fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=80, command=show_admin_frame)
cancel_book_crudl_button.place(x=390, y=400)

# ----------------- Category CRUDL Frame -------------------

category_crudl_frame = ctk.CTkFrame(root)
category_crudl_frame.grid(row=0, column=0, sticky='nsew')

# Add Borrower Title
add_borrower_title_label = ctk.CTkLabel(category_crudl_frame, text='CRUDL Category', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
add_borrower_title_label.place(x=25, y=18)

# Frame for function buttons
add_category_fill_up_frame = ctk.CTkFrame(category_crudl_frame, width=345, height=360)
add_category_fill_up_frame.place(x=255, y=130)

# Function Buttons
add_category_button = ctk.CTkButton(master=category_crudl_frame, text='Add New Category', 
                                    font=ctk.CTkFont('Calibri', size=20, weight='bold'), width=80, command=show_add_category_frame)
add_category_button.place(x=345, y=165)

delete_category_button = ctk.CTkButton(master=category_crudl_frame, text='Delete Category', 
                                       font=ctk.CTkFont('Calibri', size=20, weight='bold'), width=100, command=show_delete_category_frame)
delete_category_button.place(x=355, y=215)

update_category_button = ctk.CTkButton(master=category_crudl_frame, text='Update Category', 
                                       font=ctk.CTkFont('Calibri', size=20, weight='bold'), width=120, command=show_update_category_frame)
update_category_button.place(x=353, y=265)

list_categories_button = ctk.CTkButton(master=category_crudl_frame, text='List Categories', 
                                      font=ctk.CTkFont('Calibri', size=20, weight='bold'), width=120, command=show_list_categories_frame)
list_categories_button.place(x=362, y=315)

# Cancel Button in category Frame
cancel_category_crudl_button = ctk.CTkButton(master=category_crudl_frame, fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=80, command=show_admin_frame)
cancel_category_crudl_button.place(x=390, y=400)

# ----------------- rent CRUDL Frame -------------------

rent_crudl_frame = ctk.CTkFrame(root)
rent_crudl_frame.grid(row=0, column=0, sticky='nsew')

# Add Borrower Title
add_borrower_title_label = ctk.CTkLabel(rent_crudl_frame, text='CRUDL rent', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
add_borrower_title_label.place(x=25, y=18)

# Frame for function buttons
add_rent_fill_up_frame = ctk.CTkFrame(rent_crudl_frame, width=345, height=360)
add_rent_fill_up_frame.place(x=255, y=130)

# Function Buttons
delete_rent_button = ctk.CTkButton(master=rent_crudl_frame, text='Delete Rent', 
                                       font=ctk.CTkFont('Calibri', size=20, weight='bold'), width=100, command=show_delete_rent_frame)
delete_rent_button.place(x=367, y=165)

update_rent_button = ctk.CTkButton(master=rent_crudl_frame, text='Update Rent', 
                                       font=ctk.CTkFont('Calibri', size=20, weight='bold'), width=120, command=show_update_rent_frame)
update_rent_button.place(x=365, y=215)

list_rents_button = ctk.CTkButton(master=rent_crudl_frame, text='List Rents', 
                                      font=ctk.CTkFont('Calibri', size=20, weight='bold'), width=120, command=show_list_rents_frame)
list_rents_button.place(x=365, y=265)

# Canecl Button in rent Frame
cancel_rent_crudl_button = ctk.CTkButton(master=rent_crudl_frame, fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=80, command=show_admin_frame)
cancel_rent_crudl_button.place(x=390, y=400)












# -------------- Add Borrower Frame Code -------------------

add_borrower_frame = ctk.CTkFrame(root)
add_borrower_frame.grid(row=0, column=0, sticky='nsew')

# Add Borrower Title
add_borrower_title_label = ctk.CTkLabel(master=add_borrower_frame, text='Add New Borrower', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
add_borrower_title_label.place(x=25, y=18)

# Frame for fill up form
add_borrower_fill_up_frame = ctk.CTkFrame(master=add_borrower_frame, width=745, height=360)
add_borrower_fill_up_frame.place(x=85, y=130)

# Name Label
add_borrower_name_label = ctk.CTkLabel(master=add_borrower_frame, fg_color='#333333', bg_color='#333333', text='Name:')
add_borrower_name_label.place(x=100, y=165)
add_borrower_name_entry = ctk.CTkEntry(master=add_borrower_frame, width=300)
add_borrower_name_entry.place(x=100, y=190)

# Phone Label
add_borrower_phone_label = ctk.CTkLabel(master=add_borrower_frame, fg_color='#333333', bg_color='#333333', text='Phone:')
add_borrower_phone_label.place(x=440, y=165)
add_borrower_phone_entry = ctk.CTkEntry(master=add_borrower_frame, width=300)
add_borrower_phone_entry.place(x=440, y=190)

# Email Label
add_borrower_email_label = ctk.CTkLabel(master=add_borrower_frame, fg_color='#333333', bg_color='#333333', text='Email:')
add_borrower_email_label.place(x=100, y=230)
add_borrower_email_entry = ctk.CTkEntry(master=add_borrower_frame, width=300)
add_borrower_email_entry.place(x=100, y=255)

# Address Label
add_borrower_address_label = ctk.CTkLabel(master=add_borrower_frame, fg_color='#333333', bg_color='#333333', text='Address:')
add_borrower_address_label.place(x=440, y=230)
add_borrower_address_entry = ctk.CTkEntry(master=add_borrower_frame, width=300)
add_borrower_address_entry.place(x=440, y=255)

# Add Borrower Button
add_borrower_button = ctk.CTkButton(master=add_borrower_frame, text='Add Borrower', width=120, command=add_borrower)
add_borrower_button.place(x=100, y=400)

# Cancel Button in Add Borrower Frame
cancel_add_borrower_button = ctk.CTkButton(master=add_borrower_frame,  fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=80, command=show_borrower_crudl_frame)
cancel_add_borrower_button.place(x=230, y=400)

# -------------- Delete Borrower Frame Code -------------------

delete_borrower_frame = ctk.CTkFrame(root)
delete_borrower_frame.grid(row=0, column=0, sticky='nsew')

# Frame for function buttons
delete_borrower_fill_up_frame = ctk.CTkFrame(master=delete_borrower_frame, width=345, height=360)
delete_borrower_fill_up_frame.place(x=255, y=130)

# Delete Borrower Title
delete_borrower_title_label = ctk.CTkLabel(master=delete_borrower_frame, fg_color='transparent', text='Delete Borrower', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
delete_borrower_title_label.place(x=25, y=18)

# Borrower ID Label
delete_borrower_id_label = ctk.CTkLabel(master=delete_borrower_frame, fg_color='#333333', bg_color='#333333', text='Borrower ID:')
delete_borrower_id_label.place(x=390, y=230)

# Borrower ID Entry
delete_borrower_id_entry = ctk.CTkEntry(master=delete_borrower_frame, width=100)
delete_borrower_id_entry.place(x=380, y=265)

# Delete Borrower Button
delete_borrower_button = ctk.CTkButton(master=delete_borrower_frame, text='Delete Borrower', width=120, command=delete_borrower)
delete_borrower_button.place(x=370, y=350)

# Cancel Button in Delete Borrower Frame
cancel_delete_borrower_button = ctk.CTkButton(master=delete_borrower_frame, fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=80, command=show_borrower_crudl_frame)
cancel_delete_borrower_button.place(x=390, y=400)

# -------------- Update Borrower Frame Code -------------------

update_borrower_frame = ctk.CTkFrame(root)
update_borrower_frame.grid(row=0, column=0, sticky='nsew')

# Frame for function buttons
update_borrower_fill_up_frame = ctk.CTkFrame(master=update_borrower_frame, width=345, height=360)
update_borrower_fill_up_frame.place(x=255, y=130)

# Update Borrower Title
update_borrower_title_label = ctk.CTkLabel(master=update_borrower_frame, text='Update Borrower', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
update_borrower_title_label.place(x=25, y=18)

# Borrower ID Label
update_borrower_id_label = ctk.CTkLabel(master=update_borrower_frame, fg_color='#333333', bg_color='#333333', text='Borrower ID:')
update_borrower_id_label.place(x=390, y=230)

# Borrower ID Entry
update_borrower_id_entry = ctk.CTkEntry(master=update_borrower_frame, width=100)
update_borrower_id_entry.place(x=380, y=265)

# Update Borrower Button
update_borrower_button = ctk.CTkButton(master=update_borrower_frame, text='Update Borrower', width=120, command=check_borrower_existence)
update_borrower_button.place(x=370, y=350)

# Cancel Button in Update Borrower Frame
cancel_update_borrower_button = ctk.CTkButton(master=update_borrower_frame, fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=80, command=show_borrower_crudl_frame)
cancel_update_borrower_button.place(x=390, y=400)

# -------------- Update Borrower Entries Frame Code -------------------

update_borrower_entries_frame = ctk.CTkFrame(root)
update_borrower_entries_frame.grid(row=0, column=0, sticky='nsew')

# Update Borrower Entries Title
update_borrower_entries_title_label = ctk.CTkLabel(master=update_borrower_entries_frame, text='Update Borrower Entries', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
update_borrower_entries_title_label.place(x=25, y=18)

# Frame for fill up form
update_borrower_fill_up_frame = ctk.CTkFrame(master=update_borrower_entries_frame, width=745, height=360)
update_borrower_fill_up_frame.place(x=85, y=130)

# New Borrower title
update_borrower_label = ctk.CTkLabel(master=update_borrower_entries_frame, fg_color='#333333', bg_color='#333333', text='Updation!', font=ctk.CTkFont('Calibri', size=32, weight='normal'))
update_borrower_label.place(x=100, y=165)

# Borrower Name Label
update_borrower_name_label = ctk.CTkLabel(master=update_borrower_entries_frame, fg_color='#333333', bg_color='#333333', text='Borrower Name:')
update_borrower_name_label.place(x=100, y=230)

# Borrower Name Entry
update_borrower_name_entry = ctk.CTkEntry(master=update_borrower_entries_frame, width=300)
update_borrower_name_entry.place(x=100, y=255)

# Borrower Phone Label
update_borrower_phone_label = ctk.CTkLabel(master=update_borrower_entries_frame, fg_color='#333333', bg_color='#333333', text='Borrower Phone:')
update_borrower_phone_label.place(x=440, y=230)

# Borrower Phone Entry
update_borrower_phone_entry = ctk.CTkEntry(master=update_borrower_entries_frame, width=300)
update_borrower_phone_entry.place(x=440, y=255)

# Borrower Address Label
update_borrower_address_label = ctk.CTkLabel(master=update_borrower_entries_frame, fg_color='#333333', bg_color='#333333', text='Borrower Address:')
update_borrower_address_label.place(x=100, y=295)

# Borrower Address Entry
update_borrower_address_entry = ctk.CTkEntry(master=update_borrower_entries_frame, width=300)
update_borrower_address_entry.place(x=100, y=320)

# Borrower Email Label
update_borrower_email_label = ctk.CTkLabel(master=update_borrower_entries_frame, fg_color='#333333', bg_color='#333333', text='Borrower Email:')
update_borrower_email_label.place(x=440, y=295)

# Borrower Email Entry
update_borrower_email_entry = ctk.CTkEntry(master=update_borrower_entries_frame, width=300)
update_borrower_email_entry.place(x=440, y=320)

# Update Borrower Entries Button
update_borrower_entries_button = ctk.CTkButton(master=update_borrower_entries_frame, text='Update Entries', width=100, command=update_borrower)
update_borrower_entries_button.place(x=100, y=400)

# Cancel Button in Update Borrower Entries Frame
cancel_update_borrower_entries_button = ctk.CTkButton(master=update_borrower_entries_frame, fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=80, command=show_borrower_crudl_frame)
cancel_update_borrower_entries_button.place(x=210, y=400)

# -------------- List Borrowers Frame Code -------------------

list_borrowers_frame = ctk.CTkFrame(root)
list_borrowers_frame.grid(row=0, column=0, sticky='nsew')

# List borrowers Title
list_borrowers_title_label = ctk.CTkLabel(master=list_borrowers_frame, text='List Borrowers', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
list_borrowers_title_label.place(x=25, y=18)

# Treeview for listing borrowers
borrowers_treeview = ttk.Treeview(list_borrowers_frame, columns=('borrower_id', 'name', 'phone', 'email', 'address'), show='headings')
borrowers_treeview.column('borrower_id', width=50)
borrowers_treeview.column('name', width=200)
borrowers_treeview.column('phone', width=100)
borrowers_treeview.column('email', width=200)
borrowers_treeview.column('address', width=200)

borrowers_treeview.heading('borrower_id', text='Borrower ID')
borrowers_treeview.heading('name', text='Name')
borrowers_treeview.heading('phone', text='Phone No.')
borrowers_treeview.heading('email', text='Email')
borrowers_treeview.heading('address', text='Address')
borrowers_treeview.place(x=40, y=80, width=1050, height=500)

# Scrollbar for the treeview
borrowers_scrollbar = ttk.Scrollbar(list_borrowers_frame, orient='vertical', command=borrowers_treeview.yview)
borrowers_scrollbar.place(x=1090, y=80, height=500)

borrowers_treeview.configure(yscrollcommand=borrowers_scrollbar.set)

# List borrowers Button
list_borrowers_button = ctk.CTkButton(master=list_borrowers_frame, text='List borrowers', width=120, command=list_borrowers)
list_borrowers_button.place(x=300, y=500)

# Cancel Button in Update Borrower Entries Frame
cancel_list_borrowers_button = ctk.CTkButton(master=list_borrowers_frame, fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=80, command=show_borrower_crudl_frame)
cancel_list_borrowers_button.place(x=470, y=500)














#-------------- Add Book Frame Code -------------------

add_book_frame = ctk.CTkFrame(root)
add_book_frame.grid(row=0, column=0, sticky='nsew')

# Add Book Title
add_book_title_label = ctk.CTkLabel(master=add_book_frame, text='Add New Book', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
add_book_title_label.place(x=25, y=18)

# Frame for fill up form
add_book_fill_up_frame = ctk.CTkFrame(master=add_book_frame, width=745, height=370)
add_book_fill_up_frame.place(x=85, y=130)

# Add Book Form
add_book_category_label = ctk.CTkLabel(master=add_book_frame, fg_color='#333333', bg_color='#333333', text='Category:')
add_book_category_label.place(x=100, y=165)
add_book_category_entry = ctk.CTkEntry(master=add_book_frame, width=300)
add_book_category_entry.place(x=100, y=190)

add_book_title_label = ctk.CTkLabel(master=add_book_frame, fg_color='#333333', bg_color='#333333', text='Title:')
add_book_title_label.place(x=440, y=165)
add_book_title_entry = ctk.CTkEntry(master=add_book_frame, width=300)
add_book_title_entry.place(x=440, y=190)

add_book_author_label = ctk.CTkLabel(master=add_book_frame, fg_color='#333333', bg_color='#333333', text='Author:')
add_book_author_label.place(x=100, y=230)
add_book_author_entry = ctk.CTkEntry(master=add_book_frame, width=300)
add_book_author_entry.place(x=100, y=255)

add_book_price_label = ctk.CTkLabel(master=add_book_frame, fg_color='#333333', bg_color='#333333', text='Price:')
add_book_price_label.place(x=440, y=230)
add_book_price_entry = ctk.CTkEntry(master=add_book_frame, width=300)
add_book_price_entry.place(x=440, y=255)

add_book_status_label = ctk.CTkLabel(master=add_book_frame, fg_color='#333333', bg_color='#333333', text='Status:')
add_book_status_label.place(x=100, y=300)
add_book_status_entry = ctk.CTkEntry(master=add_book_frame, width=300)
add_book_status_entry.place(x=100, y=320)

# Add Book Button
add_book_button = ctk.CTkButton(master=add_book_frame, text='Add Book', width=120, command=add_book)
add_book_button.place(x=100, y=400)

# Cancel Button in Add Book Frame
cancel_add_book_button = ctk.CTkButton(master=add_book_frame,  fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=80, command=show_book_crudl_frame)
cancel_add_book_button.place(x=230, y=400)

# -------------- Delete Book Frame Code -------------------

delete_book_frame = ctk.CTkFrame(root)
delete_book_frame.grid(row=0, column=0, sticky='nsew')

# Frame for function buttons
delete_book_fill_up_frame = ctk.CTkFrame(master=delete_book_frame, width=345, height=360)
delete_book_fill_up_frame.place(x=255, y=130)

# Delete Book Title
delete_book_title_label = ctk.CTkLabel(master=delete_book_frame, text='Delete Book', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
delete_book_title_label.place(x=25, y=18)

# Delete Book ID Entry
delete_book_id_label = ctk.CTkLabel(master=delete_book_frame, fg_color='#333333', bg_color='#333333', text='Book ID:')
delete_book_id_label.place(x=390, y=230)
delete_book_id_entry = ctk.CTkEntry(master=delete_book_frame, width=100)
delete_book_id_entry.place(x=380, y=265)

# Delete Book Button
delete_book_button = ctk.CTkButton(master=delete_book_frame, text='Delete Book', width=120, command=delete_book)
delete_book_button.place(x=370, y=350)

# Cancel Button in Delete Book Frame
cancel_delete_book_button = ctk.CTkButton(master=delete_book_frame, fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=80, command=show_book_crudl_frame)
cancel_delete_book_button.place(x=390, y=400)

# -------------- Update Book Frame Code -------------------

update_book_frame = ctk.CTkFrame(root)
update_book_frame.grid(row=0, column=0, sticky='nsew')

# Frame for function buttons
update_book_fill_up_frame = ctk.CTkFrame(master=update_book_frame, width=345, height=360)
update_book_fill_up_frame.place(x=255, y=130)

# Update Book Title
update_book_title_label = ctk.CTkLabel(master=update_book_frame, text='Update Book', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
update_book_title_label.place(x=25, y=18)

# Update Book ID Entry
update_book_id_label = ctk.CTkLabel(master=update_book_frame, fg_color='#333333', bg_color='#333333', text='Book ID:')
update_book_id_label.place(x=390, y=230)
update_book_id_entry = ctk.CTkEntry(master=update_book_frame, width=100)
update_book_id_entry.place(x=380, y=265)

# Update Book Button
update_book_button = ctk.CTkButton(master=update_book_frame, text='Update Book', width=120, command=show_update_book_entries_frame)
update_book_button.place(x=370, y=350)

# Cancel Button in Update Book Frame
cancel_update_book_button = ctk.CTkButton(master=update_book_frame, fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=80, command=show_book_crudl_frame)
cancel_update_book_button.place(x=390, y=400)

# -------------- Update Book Entries Frame Code -------------------

update_book_entries_frame = ctk.CTkFrame(root)
update_book_entries_frame.grid(row=0, column=0, sticky='nsew')

# Update Book Entries Title
update_book_entries_title_label = ctk.CTkLabel(master=update_book_entries_frame, text='Update Book Entries', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
update_book_entries_title_label.place(x=25, y=18)

# Frame for fill up form
update_book_fill_up_frame = ctk.CTkFrame(master=update_book_entries_frame, width=745, height=400)
update_book_fill_up_frame.place(x=85, y=130)

# New Book title
update_book_label = ctk.CTkLabel(master=update_book_entries_frame, fg_color='#333333', bg_color='#333333', text='Updation!', font=ctk.CTkFont('Calibri', size=32, weight='normal'))
update_book_label.place(x=100, y=165)

# Update Book Category Entry
update_book_category_label = ctk.CTkLabel(master=update_book_entries_frame, fg_color='#333333', bg_color='#333333', text='Category:')
update_book_category_label.place(x=100, y=230)
update_book_category_entry = ctk.CTkEntry(master=update_book_entries_frame, width=300)
update_book_category_entry.place(x=100, y=255)

# Update Book Title Entry
update_book_title_label = ctk.CTkLabel(master=update_book_entries_frame, fg_color='#333333', bg_color='#333333', text='Title:')
update_book_title_label.place(x=440, y=230)
update_book_title_entry = ctk.CTkEntry(master=update_book_entries_frame, width=300)
update_book_title_entry.place(x=440, y=255)

# Update Book Author Entry
update_book_author_label = ctk.CTkLabel(master=update_book_entries_frame, fg_color='#333333', bg_color='#333333', text='Author:')
update_book_author_label.place(x=100, y=295)
update_book_author_entry = ctk.CTkEntry(master=update_book_entries_frame, width=300)
update_book_author_entry.place(x=100, y=320)

# Update Book Price Entry
update_book_price_label = ctk.CTkLabel(master=update_book_entries_frame, fg_color='#333333', bg_color='#333333', text='Price:')
update_book_price_label.place(x=440, y=295)
update_book_price_entry = ctk.CTkEntry(master=update_book_entries_frame, width=300)
update_book_price_entry.place(x=440, y=320)

# Update Book Status Entry
update_book_status_label = ctk.CTkLabel(master=update_book_entries_frame, fg_color='#333333', bg_color='#333333', text='Status:')
update_book_status_label.place(x=100, y=360)
update_book_status_entry = ctk.CTkEntry(master=update_book_entries_frame, width=300)
update_book_status_entry.place(x=100, y=385)

# Update Borrower Entries Button
update_book_entries_button = ctk.CTkButton(master=update_book_entries_frame, text='Update Entries', width=100, command=update_book)
update_book_entries_button.place(x=100, y=450)

# Cancel Button in Update Borrower Entries Frame
cancel_update_book_entries_button = ctk.CTkButton(master=update_book_entries_frame, fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=80, command=show_book_crudl_frame)
cancel_update_book_entries_button.place(x=230, y=450)

# -------------- List Books Frae Code -------------------

list_books_frame = ctk.CTkFrame(root)
list_books_frame.grid(row=0, column=0, sticky='nsew')

# List Books Title
list_books_title_label = ctk.CTkLabel(master=list_books_frame, text='List Books', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
list_books_title_label.place(x=25, y=18)

# Treeview for listing books
books_treeview = ttk.Treeview(list_books_frame, columns=('book_id', 'category_id', 'title', 'author', 'price', 'status'), show='headings')
books_treeview.column('book_id', width=100)
books_treeview.column('category_id', width=100)
books_treeview.column('title', width=300)
books_treeview.column('author', width=300)
books_treeview.column('price', width=100)
books_treeview.column('status', width=100)

books_treeview.heading('book_id', text='Book ID')
books_treeview.heading('category_id', text='Category ID')
books_treeview.heading('title', text='Title')
books_treeview.heading('author', text='Author')
books_treeview.heading('price', text='Price')
books_treeview.heading('status', text='Status')
books_treeview.place(x=40, y=80, width=1050, height=500)

# Scrollbar for the treeview
books_scrollbar = ttk.Scrollbar(list_books_frame, orient='vertical', command=books_treeview.yview)
books_scrollbar.place(x=1090, y=80, height=500)

books_treeview.configure(yscrollcommand=books_scrollbar.set)

# List Books Button
list_books_button = ctk.CTkButton(master=list_books_frame, text='List Books', width=120, command=list_books)
list_books_button.place(x=300, y=500)

# Cancel Button in List Books Frame
cancel_list_books_button = ctk.CTkButton(master=list_books_frame, fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=80, command=show_book_crudl_frame)
cancel_list_books_button.place(x=470, y=500)















# -------------- Add Category Frame Code -------------------

add_category_frame = ctk.CTkFrame(root)
add_category_frame.grid(row=0, column=0, sticky='nsew')

# Add Category Title
add_category_title_label = ctk.CTkLabel(master=add_category_frame, text='Add Category', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
add_category_title_label.place(x=25, y=18)

# Frame for fill up form
add_category_fill_up_frame = ctk.CTkFrame(master=add_category_frame, width=500, height=200)
add_category_fill_up_frame.place(x=200, y=130)

# Category Name Label
category_name_label = ctk.CTkLabel(master=add_category_frame, fg_color='#333333', bg_color='#333333', text='Category Name:')
category_name_label.place(x=250, y=145)

# Category Name Entry
category_entry = ctk.CTkEntry(add_category_frame, width=300)
category_entry.place(x=250, y=170)

# Add Category Button
add_category_button = ctk.CTkButton(master=add_category_frame, text='Add Category', width=120, command=add_category)
add_category_button.place(x=250, y=250)

cancel_category_button = ctk.CTkButton(master=add_category_frame, fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=120, command=show_category_crudl_frame)
cancel_category_button.place(x=380, y=250)

# -------------- Delete Category Frame Code -------------------

delete_category_frame = ctk.CTkFrame(root)
delete_category_frame.grid(row=0, column=0, sticky='nsew')

# Frame for function buttons
delete_category_fill_up_frame = ctk.CTkFrame(master=delete_category_frame, width=345, height=360)
delete_category_fill_up_frame.place(x=255, y=130)

# Delete Category Title
delete_category_title_label = ctk.CTkLabel(master=delete_category_frame, text='Delete Category', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
delete_category_title_label.place(x=25, y=18)

# Category ID Label
category_id_label = ctk.CTkLabel(master=delete_category_frame, fg_color='#333333', bg_color='#333333', text='Category ID:')
category_id_label.place(x=390, y=230)

# Category ID Entry
category_id_entry = ctk.CTkEntry(delete_category_frame, width=100)
category_id_entry.place(x=380, y=265)

# Delete Category Button
delete_category_button = ctk.CTkButton(master=delete_category_frame, text='Delete Category', width=120, command=delete_category)
delete_category_button.place(x=370, y=350)

# Cancel Button in Delete Category Frame
cancel_delete_category_button = ctk.CTkButton(master=delete_category_frame, fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=80, command=show_category_crudl_frame)
cancel_delete_category_button.place(x=390, y=400)

# -------------- Update Category Frame Code -------------------

update_category_frame = ctk.CTkFrame(root)
update_category_frame.grid(row=0, column=0, sticky='nsew')

# Frame for function buttons
update_category_fill_up_frame = ctk.CTkFrame(master=update_category_frame, width=345, height=360)
update_category_fill_up_frame.place(x=255, y=130)

# Update Category Title
update_category_title_label = ctk.CTkLabel(master=update_category_frame, text='Update Category', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
update_category_title_label.place(x=25, y=18)

# Update Category ID Label
update_category_id_label = ctk.CTkLabel(master=update_category_frame, fg_color='#333333', bg_color='#333333', text='Category ID:')
update_category_id_label.place(x=390, y=230)

# Update Category ID Entry
update_category_id_entry = ctk.CTkEntry(master=update_category_frame, width=100)
update_category_id_entry.place(x=380, y=265)

# Update Category Button
update_category_button = ctk.CTkButton(master=update_category_frame, text='Update Category', width=120, command=show_update_category_name_frame)
update_category_button.place(x=370, y=350)

# Cancel Button in Update Category Frame
cancel_update_category_button = ctk.CTkButton(master=update_category_frame, fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=80, command=show_category_crudl_frame)
cancel_update_category_button.place(x=390, y=400)

# -------------- Update Category Name Frame Code -------------------

update_category_name_frame = ctk.CTkFrame(root)
update_category_name_frame.grid(row=0, column=0, sticky='nsew')

# Update Category Name Title
update_category_name_title_label = ctk.CTkLabel(master=update_category_name_frame, text='Update Category Name', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
update_category_name_title_label.place(x=25, y=18)

# Frame for fill up form
update_category_fill_up_frame = ctk.CTkFrame(master=update_category_name_frame, width=345, height=360)
update_category_fill_up_frame.place(x=255, y=130)

# Update Category Name Label
update_category_name_label = ctk.CTkLabel(master=update_category_name_frame, fg_color='#333333', bg_color='#333333', text='Category Name:')
update_category_name_label.place(x=390, y=200)
update_category_name_entry = ctk.CTkEntry(master=update_category_name_frame, width=300)
update_category_name_entry.place(x=280, y=235)

# Update Category Name Button
update_category_name_button = ctk.CTkButton(master=update_category_name_frame, text='Update Name', width=120, command=update_category_name)
update_category_name_button.place(x=370, y=350)

# Cancel Button in Update Category Name Frame
cancel_update_category_name_button = ctk.CTkButton(master=update_category_name_frame, fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=80, command=show_category_crudl_frame)
cancel_update_category_name_button.place(x=390, y=400)

# -------------- List Categories Frame Code -------------------

list_categories_frame = ctk.CTkFrame(root)
list_categories_frame.grid(row=0, column=0, sticky='nsew')

# List Categories Title
list_categories_title_label = ctk.CTkLabel(master=list_categories_frame, text='List Categories', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
list_categories_title_label.place(x=25, y=18)

# Treeview for listing categories
categories_treeview = ttk.Treeview(list_categories_frame, columns=('category_id', 'category_name'), show='headings')
categories_treeview.column('category_id', width=100)
categories_treeview.column('category_name', width=300)
categories_treeview.heading('category_id', text='Category ID')
categories_treeview.heading('category_name', text='Category Name')
categories_treeview.place(x=250, y=80, width=600, height=500)

# Scrollbar for the treeview
categories_scrollbar = ttk.Scrollbar(list_categories_frame, orient='vertical', command=categories_treeview.yview)
categories_scrollbar.place(x=850, y=80, height=500)

categories_treeview.configure(yscrollcommand=categories_scrollbar.set)

# List Categories Button
list_categories_button = ctk.CTkButton(master=list_categories_frame, text='List Categories', width=120, command=list_categories)
list_categories_button.place(x=300, y=500)

# Cancel Button in List Categories Frame
cancel_list_categories_button = ctk.CTkButton(master=list_categories_frame, fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=80, command=show_category_crudl_frame)
cancel_list_categories_button.place(x=470, y=500)




















# -------------- Delete rent Frame Code -------------------

delete_rent_frame = ctk.CTkFrame(root)
delete_rent_frame.grid(row=0, column=0, sticky='nsew')

# Frame for function buttons
delete_rent_fill_up_frame = ctk.CTkFrame(master=delete_rent_frame, width=345, height=360)
delete_rent_fill_up_frame.place(x=255, y=130)

# Delete rent Title
delete_rent_title_label = ctk.CTkLabel(master=delete_rent_frame, text='Delete Rent', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
delete_rent_title_label.place(x=25, y=18)

# Delete rent ID Entry
delete_rent_id_label = ctk.CTkLabel(master=delete_rent_frame, fg_color='#333333', bg_color='#333333', text='Rental ID:')
delete_rent_id_label.place(x=405, y=230)
delete_rent_id_entry = ctk.CTkEntry(master=delete_rent_frame, width=100)
delete_rent_id_entry.place(x=380, y=265)

# Delete rent Button
delete_rent_button = ctk.CTkButton(master=delete_rent_frame, text='Delete Rent', width=120, command=delete_rent)
delete_rent_button.place(x=370, y=350)

# Cancel Button in Delete rent Frame
cancel_delete_rent_button = ctk.CTkButton(master=delete_rent_frame, fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=80, command=show_rent_crudl_frame)
cancel_delete_rent_button.place(x=390, y=400)

# -------------- Update Rent Frame Code -------------------

update_rent_frame = ctk.CTkFrame(root)
update_rent_frame.grid(row=0, column=0, sticky='nsew')

# Update Rent Title
update_rent_title_label = ctk.CTkLabel(master=update_rent_frame, text='Update Rent', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
update_rent_title_label.place(x=25, y=18)

# Frame for function buttons
update_rent_fill_up_frame = ctk.CTkFrame(master=update_rent_frame, width=345, height=360)
update_rent_fill_up_frame.place(x=255, y=130)

# Update Rent ID Label
update_rent_id_label = ctk.CTkLabel(master=update_rent_frame, fg_color='#333333', bg_color='#333333', text='Rental ID:')
update_rent_id_label.place(x=405, y=230)
update_rent_id_entry = ctk.CTkEntry(master=update_rent_frame, width=100)
update_rent_id_entry.place(x=380, y=265)

# Update Rent Button
update_rent_button = ctk.CTkButton(master=update_rent_frame, text='Update Rent', width=120, command=show_update_rent_details_frame)
update_rent_button.place(x=370, y=350)

# Cancel Button in Update Rent Frame
cancel_update_rent_button = ctk.CTkButton(master=update_rent_frame, fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=80, command=show_rent_crudl_frame)
cancel_update_rent_button.place(x=390, y=400)

# -------------- Update Rent Details Frame Code -------------------

update_rent_details_frame = ctk.CTkFrame(root)
update_rent_details_frame.grid(row=0, column=0, sticky='nsew')

# Update Rent Details Title
update_rent_details_title_label = ctk.CTkLabel(master=update_rent_details_frame, text='Update Rent Details', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
update_rent_details_title_label.place(x=25, y=18)

# Frame for fill up form
update_rent_fill_up_frame = ctk.CTkFrame(master=update_rent_details_frame, width=745, height=400)
update_rent_fill_up_frame.place(x=85, y=130)

# New Book title
update_rent_label = ctk.CTkLabel(master=update_rent_details_frame, fg_color='#333333', bg_color='#333333', text='Updation!', font=ctk.CTkFont('Calibri', size=32, weight='normal'))
update_rent_label.place(x=100, y=165)

# Update Book ID Label
update_rent_book_label = ctk.CTkLabel(master=update_rent_details_frame, fg_color='#333333', bg_color='#333333', text='Book ID:')
update_rent_book_label.place(x=100, y=230)
update_rent_book_entry = ctk.CTkEntry(master=update_rent_details_frame, width=300)
update_rent_book_entry.place(x=100, y=255)

# Update Borrower ID Label
update_rent_borrower_label = ctk.CTkLabel(master=update_rent_details_frame, fg_color='#333333', bg_color='#333333', text='Borrower ID:')
update_rent_borrower_label.place(x=440, y=230)
update_rent_borrower_entry = ctk.CTkEntry(master=update_rent_details_frame, width=300)
update_rent_borrower_entry.place(x=440, y=255)

# Create the label and entry for rental deadline extension
update_rent_extension_label = ctk.CTkLabel(update_rent_details_frame, fg_color='#333333', bg_color='#333333', text="Extension (in days):")
update_rent_extension_label.place(x=440, y=295)
update_rent_extension_entry = ctk.CTkEntry(update_rent_details_frame)
update_rent_extension_entry.place(x=440, y=320)

# Create the payment method combobox
update_rent_payment_method_label = ctk.CTkLabel(master=update_rent_details_frame, fg_color='#333333', bg_color='#333333', text="Payment Method:",)
update_rent_payment_method_label.place(x=100, y=295)
update_rent_payment_method_combobox = ttk.Combobox(master=update_rent_details_frame, values=["Cash", "Credit Card", "Online Payment"])
update_rent_payment_method_combobox.place(x=125, y=410)

# Create the return status combobox
update_rent_return_status_label = ctk.CTkLabel(master=update_rent_details_frame, fg_color='#333333', bg_color='#333333', text="Status:")
update_rent_return_status_label.place(x=100, y=360)
update_rent_return_status_combobox = ttk.Combobox(master=update_rent_details_frame, values=["Ongoing", "Returned"])
update_rent_return_status_combobox.place(x=125, y=490)

# Update Rent Details Button
update_rent_details_button = ctk.CTkButton(master=update_rent_details_frame, text='Update Details', width=120, command=update_rent_details)
update_rent_details_button.place(x=100, y=450)

# Cancel Button in Update Rent Details Frame
cancel_update_rent_details_button = ctk.CTkButton(master=update_rent_details_frame, fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=80, command=show_rent_crudl_frame)
cancel_update_rent_details_button.place(x=230, y=450)

# -------------- List rents Frae Code -------------------

list_rents_frame = ctk.CTkFrame(root)
list_rents_frame.grid(row=0, column=0, sticky='nsew')

# List rents Title
list_rents_title_label = ctk.CTkLabel(master=list_rents_frame, text='List rents', font=ctk.CTkFont('Calibri', size=25, weight='bold'))
list_rents_title_label.place(x=25, y=18)

# Treeview for listing rents
rents_treeview = ttk.Treeview(list_rents_frame, columns=('rental_id', 'book_id', 'borrower_id', 'rented_date', 'deadline', 'return_date', 'payment_method', 'total_amount', 'late_fees', 'status'), show='headings')
rents_treeview.column('rental_id', width=50)
rents_treeview.column('book_id', width=50)
rents_treeview.column('borrower_id', width=50)
rents_treeview.column('rented_date', width=100)
rents_treeview.column('deadline', width=100)
rents_treeview.column('return_date', width=100)
rents_treeview.column('payment_method', width=100)
rents_treeview.column('total_amount', width=100)
rents_treeview.column('late_fees', width=100)
rents_treeview.column('status', width=100)


rents_treeview.heading('rental_id', text='Rental ID')
rents_treeview.heading('book_id', text='Book ID')
rents_treeview.heading('borrower_id', text='Borrower ID')
rents_treeview.heading('rented_date', text='Rented')
rents_treeview.heading('deadline', text='Deadline')
rents_treeview.heading('return_date', text='Return Date')
rents_treeview.heading('payment_method', text='Payment Method')
rents_treeview.heading('total_amount', text='Amount')
rents_treeview.heading('late_fees', text='Late Fees')
rents_treeview.heading('status', text='Status')
rents_treeview.place(x=40, y=80, width=1050, height=500)

# Create the vertical scrollbar
rents_v_scrollbar = ttk.Scrollbar(list_rents_frame, orient='vertical', command=rents_treeview.yview)
rents_v_scrollbar.place(x=1090, y=80, height=500)
rents_treeview.configure(yscrollcommand=rents_v_scrollbar.set)

# Create the horizontal scrollbar
rents_h_scrollbar = ttk.Scrollbar(list_rents_frame, orient='horizontal', command=rents_treeview.xview)
rents_h_scrollbar.place(x=40, y=580, width=1050)
rents_treeview.configure(xscrollcommand=rents_h_scrollbar.set)

# List rents Button
list_rents_button = ctk.CTkButton(master=list_rents_frame, text='List rents', width=120, command=list_rents)
list_rents_button.place(x=300, y=500)

# Cancel Button in List rents Frame
cancel_list_rents_button = ctk.CTkButton(master=list_rents_frame, fg_color='transparent', border_color='#1f6aa5', border_width=2, text='Cancel', width=80, command=show_rent_crudl_frame)
cancel_list_rents_button.place(x=470, y=500)


show_main_frame()
root.mainloop()