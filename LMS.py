import mysql.connector as conn
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import time
import os
from pwinput import pwinput

# Class Start
class System:
    def __init__(self):
        # Password for the MySQL Server Connection
        usr = input("Enter your MySQL username: ")
        pas = pwinput("Enter your MySQL password: ", mask = "*")

        # Establishing connection
        self.mydb = conn.connect(host = 'localhost', user = usr, passwd = pas)
        self.mycursor = self.mydb.cursor()

        # Encoding the password
        pas = quote_plus(pas)
        
        # Creating the engine
        self.engine = create_engine(f'mysql+mysqlconnector://root:{pas}@localhost')

        # Database initialization
        self.init_database()

    def init_database(self):
        if self.mydb.is_connected():
            try:
                # Create database if not exists
                self.mycursor.execute("CREATE DATABASE IF NOT EXISTS LMS")

                # Use the created database
                self.mycursor.execute("USE LMS")

                # Create Books table
                self.mycursor.execute("CREATE TABLE IF NOT EXISTS Books (Book_ID INT AUTO_INCREMENT PRIMARY KEY, Title VARCHAR(255) NOT NULL, Author VARCHAR(255) NOT NULL, Available BOOLEAN NOT NULL DEFAULT 1, INDEX (Title))")

                # Create Users table
                self.mycursor.execute("CREATE TABLE IF NOT EXISTS Users (User_ID INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255) UNIQUE NOT NULL, Email VARCHAR(255) NOT NULL, Password CHAR(12) NOT NULL CHECK (CHAR_LENGTH(Password) >= 4), INDEX (Email))")

                # Create Issues table
                self.mycursor.execute("CREATE TABLE IF NOT EXISTS Issues (Issue_ID INT AUTO_INCREMENT PRIMARY KEY, User_ID INT NOT NULL, Name VARCHAR(255) NOT NULL, Book_ID INT NOT NULL, Title VARCHAR(255) NOT NULL, Issue_Date DATETIME, FOREIGN KEY (User_ID) REFERENCES Users(User_ID), FOREIGN KEY (Book_ID) REFERENCES Books(Book_ID))")

                # Commit changes
                self.mydb.commit()
                print("Database and Tables created successfully.")
                time.sleep(.7)

            except Exception as e:
                print(f"Error during database initialization: {e}")
                time.sleep(.7)

        else:
            print("Connection Failure")
            time.sleep(.7)


    # Books Management System Options Start
    def create(self):
        bname = input("Enter Title: ")
        authname = input("Enter Author Name: ")

        num = int(input("Number of copies: "))

        for i in range(num):
            sql = "INSERT INTO Books (Title, Author) VALUES (%s, %s)"
            val = (bname, authname)

            self.mycursor.execute(sql, val)
            self.mydb.commit()

        print("Updated successfully")
        time.sleep(.7)

    def show(self):
        while True:
            os.system('cls')
            a = int(input("1. Show All Books\n2. Filter\n3. Back\n\nEnter the choice: "))
            match a:
                
                # Shows all Book Records
                case 1:
                    while True:
                        os.system('cls')
                        
                        sql = "SELECT * FROM LMS.Books;"
                        res = pd.read_sql_query(sql, self.engine)
                        
                        b = int(input("1. Original List\n2. Sort\n3. Back\n\nEnter the choice: "))
                        match b:
                            
                            # Original List
                            case 1:
                                os.system('cls')
                                print("-------------------------BOOKS AVAILABLE ON OUR SHELF-------------------------")
                                print()
                                        
                                if not res.empty:
                                    print(res.to_string(index = False))
                                    input("\nPress Enter to continue...")
                                
                                else:
                                    print("No records found")
                                    time.sleep(.7)

                            # Sorted List
                            case 2:
                                while True:
                                    os.system('cls')
                                    c = int(input("1. Title\n2. Author\n3. Back\n\nEnter the choice: "))
                                    match c:

                                        # Sort according to Title
                                        case 1:
                                            while True:
                                                os.system('cls')
                                                d = int(input("1. Ascending A-Z\n2. Descending Z-A\n3. Back\n\nEnter the choice: "))
                                                match d:

                                                    # Ascending
                                                    case 1:
                                                        os.system('cls')
                                                        print("----------------------------ASCENDING SORTING BASED ON TITLE----------------------------")
                                                        
                                                        if not res.empty:
                                                            print(res.sort_values(by = 'Title'))
                                                            input("\nPress Enter to continue...")
                                                        else:
                                                            print("No records found")
                                                            time.sleep(.7)

                                                    # Descending
                                                    case 2:
                                                        os.system('cls')
                                                        print("----------------------------DESCENDING SORTING BASED ON TITLE----------------------------")
                                                        
                                                        if not res.empty:
                                                            print(res.sort_values(by = 'Title', ascending = False))
                                                            input("\nPress Enter to continue...")
                                                        else:
                                                            print("No records found")
                                                            time.sleep(.7)

                                                    case 3:
                                                        break

                                                    case _:
                                                        print("Invalid choice!")
                                                        time.sleep(.7)

                                        # Sort according ot Author
                                        case 2:
                                            while True:
                                                os.system('cls')
                                                e = int(input("1. Ascending A-Z\n2. Descending Z-A\n3. Back\n\nEnter the choice: "))
                                                match e:
                                                    case 1:
                                                        os.system('cls')
                                                        print("----------------------------ASCENDING SORTING BASED ON AUTHOR----------------------------")
                                                        
                                                        if not res.empty:
                                                            print(res.sort_values(by = 'Author'))
                                                            input("\nPress Enter to continue...")
                                                        else:
                                                            print("No records found")
                                                            time.sleep(.7)

                                                    case 2:
                                                        os.system('cls')
                                                        print("----------------------------DESCENDING SORTING BASED ON AUTHOR----------------------------")
                                                        
                                                        if not res.empty:
                                                            print(res.sort_values(by = 'Author', ascending = False))
                                                            input("\nPress Enter to continue...")
                                                        else:
                                                            print("No records found")
                                                            time.sleep(.7)

                                                    case 3:
                                                        break

                                                    case _:
                                                        print("Invalid choice!")
                                                        time.sleep(.7)

                                        case 3:
                                            break

                                        case _:
                                            print("Invalid choice!")
                                            time.sleep(.7)

                            case 3:
                                break

                            case _:
                                print("Invalid choice!")
                                time.sleep(.7)
                
                # Filters by conditions
                case 2:
                    while True:
                        os.system('cls')
                        print("Filter by:")
                        b = int(input("1. Book ID\n2. Title\n3. Author\n4. Available\n5. Back\n\nEnter the choice: "))
                        match b:

                            # Filter by Book ID
                            case 1:
                                id = int(input("Search Book ID: "))
                                os.system('cls')

                                res = pd.read_sql_query("SELECT * FROM LMS.Books", self.engine)

                                if not res.empty and id in res['Book_ID'].values:
                                    sql = f"SELECT * FROM LMS.Books WHERE Book_ID = {id};"
                                    res = pd.read_sql_query(sql, self.engine)

                                    print(res.to_string(index = False))
                                    input("\nPress Enter to continue...")
                                
                                else:
                                    print("No records found")
                                    time.sleep(.7)
                            
                            # Filter by Title
                            case 2:
                                title = input("Search by Title: ")
                                os.system('cls')

                                sql = f"SELECT * FROM LMS.Books WHERE Title LIKE '%{title}%';"
                                res = pd.read_sql_query(sql, self.engine)

                                if not res.empty:
                                    print(res.to_string(index = False))                        
                                    input("\nPress Enter to continue...")

                                else:
                                    print("No record found")
                                    time.sleep(.7)
                            
                            # Filter by Author Name
                            case 3:
                                auth = input("Search by Author: ")
                                os.system('cls')

                                sql = f"SELECT * FROM LMS.Books WHERE Author LIKE '%{auth}%';"
                                res = pd.read_sql_query(sql, self.engine)

                                if not res.empty:
                                    print(res.to_string(index = False))
                                    input("\nPress Enter to continue...")
                                
                                else:
                                    print("No record found")
                                    time.sleep(.7)
                            
                            # Filter by the Availability status (1)
                            case 4:
                                os.system('cls')
                                sql = f"SELECT * FROM LMS.Books WHERE Available = 1;"
                                res = pd.read_sql_query(sql, self.engine)

                                if not res.empty:
                                    print(res.to_string(index = False))
                                    input("\nPress Enter to continue...")
                                
                                else:
                                    print("No records found")
                                    time.sleep(.7)

                            # Exit this function
                            case 5:
                                print("Thank you")
                                time.sleep(.7)
                                break

                            case _:
                                print("Invalid choice")
                                time.sleep(.7)

                case 3:
                    print("Thank you")
                    time.sleep(.7)
                    break

                case _:
                    print("Invalid choice")
                    time.sleep(.7)

    def modify(self):
        while True:
            os.system('cls')
            id = int(input("\nUpdate Book ID: "))
            
            sql = f"SELECT * FROM Lms.Books WHERE Book_ID = {id};"
            res = pd.read_sql_query(sql, self.engine)
            
            if not res.empty and  id in res['Book_ID'].values:
                print(res.to_string(index = False))
                print()
                a = int(input("\nUpdate:\n1. Title\n2. Author\n3. Back\n\nEnter the choice: "))
                match a:
                    case 1:
                        new = input("Update Title: ")

                        sql = "UPDATE Books SET Title = %s WHERE Book_ID = %s;"
                        val = (new, id)

                        self.mycursor.execute(sql, val)
                        self.mydb.commit()
                        
                        print("Updates done successfully.")
                        print()
                        time.sleep(.7)
                        break

                    case 2:
                        new = input("Update Author: ")

                        sql = "UPDATE Books SET Author = %s WHERE Book_ID = %s;"
                        val = (new, id)

                        self.mycursor.execute(sql, val)
                        self.mydb.commit()

                        print("Updates done successfully.")
                        print()
                        time.sleep(.7)
                        break

                    case 3:
                        print("Thank you")
                        time.sleep(.7)
                        break

                    case _:
                        print("Invalid Choice")
                        print()
                        time.sleep(.7)
            else:
                print("No recorded books")
                print()
                time.sleep(.7)
                break
                    
    def delete(self):
        sql = "SELECT * FROM Lms.Books;"
        res = pd.read_sql_query(sql, self.engine)

        a = int(input("\nNumber of Books to be deleted: "))
        
        if a >= 1 and not res.empty:
            for i in range(a):
                id = input("Enter Book ID: ")
                
                if not res.empty and id in res['Book_ID'].values:
                    sql = "DELETE FROM Books WHERE Book_ID = %s;"
                    val = (list(id))

                    self.mycursor.execute(sql, val)
                    self.mydb.commit()

                    print(f"{self.mycursor.rowcount} was deleted.")
                
                else:
                    print("No record found.")

        else:
            print("Invalid number")

    def borrow(self):
        bid = int(input("Enter Book ID: "))
                                                        
        sql = f"SELECT * FROM LMS.Books WHERE Book_ID = {bid};"
        res = pd.read_sql_query(sql, self.engine)

        # The condition is to check for the book's availability
        # If 1, the book is available and if 0, the book's not available
        if not res.empty and res['Available'].values == 1:
            sql = f"INSERT INTO Issues(User_ID, Name, Book_ID, Title, Issue_Date) VALUES({uid}, (SELECT Name FROM LMS.Users WHERE User_ID = {uid}), {bid}, (SELECT Title FROM LMS.Books WHERE Book_ID = {bid}), CURDATE());"

            self.mycursor.execute(sql)

            sql = f"UPDATE Books SET Available = 0 WHERE Book_ID = {bid};"

            self.mycursor.execute(sql)
            self.mydb.commit()

            print("Success")
            time.sleep(.7)
                                                        
        else:
            print("Not available!")
            time.sleep(.7)

    def ret(self, id):
        sql = f"SELECT Issue_ID, Book_ID, Title, Issue_Date FROM LMS.Issues WHERE User_ID = {id};"
        res = pd.read_sql_query(sql, self.engine)

        if not res.empty:
            print(res.to_string(index = False))
            print()

            bid = int(input("Return Book ID: "))

            if bid in res['Book_ID'].values:
                sql1 = f"DELETE FROM Issues WHERE User_ID = {id} AND Book_ID = {bid};"
                sql2 = f"UPDATE Books SET Available = 1 WHERE Book_ID = {bid};"

                self.mycursor.execute(sql1)
                self.mycursor.execute(sql2)

                self.mydb.commit()

                print("Book(s) returned successfully!")
                time.sleep(.7)

            else:
                print("Invalid Book ID!")
                time.sleep(.7)

        else:
            print("No borrowed books!")
            time.sleep(.7)

    # Books Management System Options End
            
    # Users Management System Options Start

    def uadd(self):
        name = input("Enter Name: ")
        email = input("Enter Email ID: ")
        pas = pwinput("Password: ", mask = "*")

        res = pd.read_sql_query("SELECT Name FROM LMS.Users;", self.engine)

        if name not in res.values:
            if len(pas) >= 4:
                sql = "INSERT INTO Users (Name, Email, Password) VALUES (%s, %s, %s);"
                val = (name, email, pas)

                self.mycursor.execute(sql, val)
                self.mydb.commit()

                res = pd.read_sql_query(f"SELECT User_ID FROM LMS.Users WHERE Name = '{name}';", self.engine)

                print("Successfully registered!")
                # time.sleep(.7)
                print(f"Your User ID is {res['User_ID'].values}")
                input("Press Enter to Continue...")
            
            else:
                print("Password length should be >= 4!")
                time.sleep(.7)
        
        else:
            print("User already exists!")
            time.sleep(.7)
    
    def ushow(self):
        while True:
            os.system('cls')
            a = int(input("1. Show All Users\n2. Filter\n3. Back\n\nEnter your choice: "))

            sql = "SELECT * FROM LMS.Users;"
            res = pd.read_sql_query(sql, self.engine)
            
            match a:
                case 1:      # Show All Users
                    if not res.empty:
                        print(res.to_string(index = False))
                        input("\nPress Enter to continue...")
                    
                    else:
                        print("No records found.")
                        time.sleep(.7)
                
                case 2:            # Filter Search Results
                    while True:
                        os.system('cls')
                        print("Filter by:")
                        b = int(input("1. User ID\n2. Name\n3. Email\n4. Back\n\nEnter the choice: "))
                        
                        match b:
                            # Filter by User ID
                            case 1:
                                id = int(input("Search User ID: "))

                                if not res.empty and id in res['User_ID'].values:
                                    sql = f"SELECT * FROM LMS.Users WHERE User_ID = {id};"
                                    res = pd.read_sql_query(sql, self.engine)
                                    print(res.to_string(index = False))
                                    input("\nPress Enter to continue...")
                                
                                else:
                                    print("No records found")
                                    time.sleep(.7)
                            
                            # Filter by User Name
                            case 2:
                                name = input("Search User Name: ")

                                sql = f"SELECT * FROM LMS.Users WHERE Name LIKE '%{name}%';"
                                res = pd.read_sql_query(sql, self.engine)

                                if not res.empty:
                                    print(res.to_string(index = False))
                                    input("\nPress Enter to continue...")
                                
                                else:
                                    print("No records found")
                                    time.sleep(.7)

                            # Filter by Email
                            case 3:
                                email = input("Search Email: ")

                                sql = f"SELECT * FROM LMS.Users WHERE Email LIKE '%{email}%';"
                                res = pd.read_sql_query(sql, self.engine)

                                if not res.empty:
                                    print(res.to_string(index = False))
                                    input("\nPress Enter to continue...")
                                
                                else:
                                    print("No records found")
                                    time.sleep(.7)

                            case 4:
                                print("Thank you!")
                                time.sleep(.7)
                                break

                            case _:
                                print("Invalid choice!")
                                time.sleep(.7)

                case 3:
                    print("Thank you!")
                    time.sleep(.7)
                    break

                case _:
                    print("Invalid choice!")
                    time.sleep(.7)

    # User information updation/modification
    def umod(self, id):
        while True:
            os.system('cls')
            a = int(input("Update:\n1. Name\n2. Email\n3. Password\n4. Back\n\nEnter the choice: "))

            __sql__ = f"SELECT * FROM LMS.Users WHERE User_ID = {id};"

            match a:
                # Name updation
                case 1:                                                                    
                    sql = "UPDATE Users SET Name = %s WHERE User_ID = %s;"
                    val = (input("Update Name: "), id)

                    self.mycursor.execute(sql, val)
                    self.mydb.commit()

                    print("Updated successfully")
                                                                    
                    res = pd.read_sql_query(__sql__, self.engine)
                    time.sleep(0.7)

                # Email updation
                case 2:
                    sql = "UPDATE Users SET Email = %s WHERE User_ID = %s;"
                    val = (input("Update Email: "), id)

                    self.mycursor.execute(sql, val)
                    self.mydb.commit()

                    res = pd.read_sql_query(__sql__, self.engine)
                    print("Updated successfully")
                    time.sleep(.7)

                # Password updation
                case 3:
                    for i in range(3, 0, -1):
                        os.system('cls')
                        pwd = pwinput("Update Password: ", mask = "*")
                        repeat = pwinput("Re-enter Password: ", mask = "*")

                        if len(pwd) >= 4:
                            if repeat == pwd:
                                sql = "UPDATE Users SET Password = %s WHERE User_ID = %s;"
                                val = (pwd, id)

                                self.mycursor.execute(sql, val)
                                self.mydb.commit()

                                res = pd.read_sql_query(f"SELECT * FROM LMS.Users WHERE User_ID = {id} AND Password = {pwd}", self.engine)
                                print("Updated successfully")
                                time.sleep(.7)
                                break
                                                                            
                            else:
                                print(f"Passwords do not match. Try again! {i - 1} chances left!")
                                time.sleep(.7)
                        
                        else:
                            print("Password length should be >= 4!")
                            time.sleep(.7)
                                                                
                case 4:
                    print("Thank you")
                    time.sleep(.7)
                    break
                                                                
                case _:
                    print("Invalid choice!")                                                    
                    time.sleep(.7)

            return res
        
    # User account deletion
    def udel(self, id):
        sql = f"DELETE FROM Users WHERE User_ID = {id};"

        self.mycursor.execute(sql)
        self.mydb.commit()

    # Users Management System Options End
# Class End

# Main Function Start
if __name__ == "__main__":
    os.system('cls')
    x = System()
    
    while True:
        os.system('cls')
        print("--------------------Welcome to The Library Management System--------------------")
        a = int(input("1. Admin Login\n2. User Login\n3. Exit\n\nEnter the choice: "))
        match a:
            # Admin Login
            # Username: admin
            # Password: admin
            case 1:
                uname = input("Username: ")
                pwd = pwinput("Password: ", mask = "*")

                if uname == "admin" and pwd == "admin":
                    os.system('cls')
                    while True:
                        os.system('cls')
                        print("Welcome, Administrator!")
                        print()
                        a = int(input("1. Library\n2. Show Users\n3. Logout\n\nEnter your choice: "))
                        
                        match a:
                            case 1:      # For the Library Management Options
                                while True:
                                    os.system('cls')
                                    ch = int(input("1. New Book Entry\n2. Show Books\n3. Modify Books\n4. Delete Books\n5. Back\n\nEnter the choice: "))

                                    match ch:
                                        case 1:
                                            x.create()
                                            print()

                                        case 2:
                                            x.show()
                                            print()
                                    
                                        case 3:
                                            x.modify()
                                            print()

                                        case 4:
                                            x.delete()
                                            print()
                                    
                                        case 5:
                                            print("Thank you!")
                                            print()
                                            break
                                        
                                        case _:
                                            print("Invalid choice")
                                            time.sleep(.7)

                            case 2:    # For the Users Management Options
                                x.ushow()

                            case 3:    # LMS System Exit
                                print("Thank you!")
                                time.sleep(0.7)
                                break

                            case _:
                                print("Invalid Choice!")
                                time.sleep(0.7)

                else:
                    print("Wrong credentials")
                    time.sleep(0.7)

            # User Login
            case 2:
                while True:
                    # For account deletion to directly go to the Register/Login Page
                    flag = False
                    os.system('cls')
                    a = int(input("1. Register\n2. Login\n3. Back\n\nEnter the choice: "))
                    match a:
                        case 1:
                            # Code for registering a new user
                            x.uadd()
                        
                        case 2:
                            # Code for reading user login
                            uid = input("User ID: ")
                            pwd = pwinput("Password: ", mask = "*")

                            # Query the database for validation of user login credentials
                            __sql__ = f"SELECT * FROM LMS.Users WHERE User_ID = {uid} AND Password = {pwd};"
                            res = pd.read_sql_query(__sql__, x.engine)

                            # If the user's credentials are correct, it will print the Welcome message along with other options for different functionalities
                            if not res.empty:
                                os.system('cls')
                                while True:
                                    os.system('cls')
                                    
                                    # The main interface after the user login starts
                                    print(f"Welcome, {res['Name'].values}")
                                    print()

                                    a = int(input("1. Library\n2. My Account\n3. Logout\n\nEnter the choice: "))
                                    match a:
                                        case 1:
                                            while True:
                                                os.system('cls')
                                                a = int(input("1. Show Books\n2. Show Borrowed Books\n3. Borrow\n4. Return\n5. Back\n\nEnter the choice: "))
                                                match a:
                                                    case 1:
                                                        x.show()

                                                    case 2:
                                                        sql = f"SELECT Issue_ID, Book_ID, Title, Issue_Date FROM LMS.Issues WHERE User_ID = {uid};"
                                                        __res__ = pd.read_sql_query(sql, x.engine)

                                                        if not __res__.empty:
                                                            print(__res__)
                                                            input("\nPress Enter to continue...")

                                                        else:
                                                            print("No borrowed books!")
                                                            time.sleep(.7)

                                                    case 3:
                                                       x.borrow()

                                                    case 4:
                                                        x.ret(uid)

                                                    case 5:
                                                        break

                                                    case _:
                                                        print("Invalid choice")

                                        case 2:
                                            while True:
                                                os.system('cls')
                                                a = int(input("1. View Profile\n2. Update Profile\n3. Delete Account\n4. Back\n\nEnter the choice: "))
                                                match a:
                                                    case 1:
                                                        os.system('cls')
                                                        print(f"User ID: {res['User_ID'].values}")
                                                        print(f"Name: {res['Name'].values}")
                                                        print(f"Email: {res['Email'].values}")
                                                        print(f"Password: {res['Password'].values}")
                                                        print()

                                                        input("\nPress Enter to continue...")
                                                    
                                                    case 2:
                                                        res = x.umod(uid)

                                                    case 3:
                                                        # Asking for confirmation of deletion of account
                                                        c = input("Do you want to remove your account? (Y/N): ")

                                                        if c == 'Y' or c == 'y':
                                                            x.udel(list(uid))
                                                            flag = True
                                                            time.sleep(.7)
                                                            break

                                                        else:
                                                            print("Thank you for staying with us!")
                                                            time.sleep(.7)
                                                    
                                                    case 4:
                                                        break
                                                    
                                                    case _:
                                                        print("Invalid choice!")
                                                        time.sleep(0.7)

                                        case 3:
                                            print(f"Thank you, {res['Name'].values}")
                                            time.sleep(0.7)
                                            break

                                        case _:
                                            print("Invalid choice!")
                                            time.sleep(0.7)

                                    if flag == True:
                                        print("Thank you for using our LMS Portal!")
                                        time.sleep(.7)
                                        break
                            
                            # In case the user enters the wrong credentials
                            else:
                                print("Wrong credentials!")
                                time.sleep(0.7)
                            
                        case 3:
                            print("Thank you")
                            time.sleep(0.7)
                            break
                        
                        case _:
                            print("Invalid choice")
                            time.sleep(0.7)

            case 3:
                print("Thank you for using our LMS Portal!")
                # Deletes the System class instance just before exiting the program 
                del x
                exit()

            case _:
                print("Invalid choice!")
                time.sleep(0.7)
# Main function End