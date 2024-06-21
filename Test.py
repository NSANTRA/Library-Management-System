import streamlit as st
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

class LMS:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="yourusername",
            password="yourpassword",
            database="yourdatabase"
        )
        self.mycursor = self.mydb.cursor()
        self.engine = create_engine('mysql+mysqlconnector://yourusername:yourpassword@localhost/yourdatabase')

    def show_books(self):
        sql = "SELECT * FROM Books"
        books = pd.read_sql_query(sql, self.engine)
        st.write(books)
        
    def add_book(self, title, author, available):
        sql = "INSERT INTO Books (Title, Author, Available) VALUES (%s, %s, %s)"
        val = (title, author, available)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        st.success("Book added successfully!")

    def issue_book(self, book_id, user_id):
        sql = f"SELECT Available FROM Books WHERE Book_ID = {book_id}"
        self.mycursor.execute(sql)
        result = self.mycursor.fetchone()
        if result and result[0] == 1:
            sql = "INSERT INTO Issues (Book_ID, User_ID) VALUES (%s, %s)"
            val = (book_id, user_id)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            st.success("Book issued successfully!")
        else:
            st.error("Book not available!")

    # Add more methods here for other functionalities like returning books, managing users, etc.

lms = LMS()

st.title("Library Management System")

menu = ["Show Books", "Add Book", "Issue Book", "Return Book", "Manage Users"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Show Books":
    lms.show_books()

elif choice == "Add Book":
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    available = st.selectbox("Available", [1, 0])
    if st.button("Add Book"):
        lms.add_book(title, author, available)

elif choice == "Issue Book":
    book_id = st.number_input("Book ID", min_value=1)
    user_id = st.number_input("User ID", min_value=1)
    if st.button("Issue Book"):
        lms.issue_book(book_id, user_id)

# Add more Streamlit interface options for other functionalities

