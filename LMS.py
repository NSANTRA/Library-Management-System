import mysql.connector as conn
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import keyboard
import time
import os

class System:
    def __init__(self):
        # Establishing connection
        self.mydb = conn.connect(host='localhost', user='root', passwd='NeeSan@1234')
        self.mycursor = self.mydb.cursor()

        # URL encoding the password
        password_encoded = quote_plus('NeeSan@1234')

        # Creating the engine
        self.engine = create_engine(f'mysql+mysqlconnector://root:{password_encoded}@localhost')

        # Database initialization
        self.init_database()

    def init_database(self):
        if self.mydb.is_connected():
            # SQL Query for creating a database named LMS
            self.mycursor.execute("CREATE DATABASE IF NOT EXISTS LMS")
            
            # SQL Query for using the above-created database (LMS)
            self.mycursor.execute("USE LMS")
            
            # SQL Query for creating a table named Books to store all the books info.
            self.mycursor.execute("CREATE TABLE IF NOT EXISTS Books (Book_ID INT AUTO_INCREMENT PRIMARY KEY, Title VARCHAR(255) NOT NULL, Author VARCHAR(255) NOT NULL, Available BOOLEAN NOT NULL DEFAULT 1)")
            
            # SQL Query for creating a table named Users a.k.a Customers to store the users info.
            self.mycursor.execute("CREATE TABLE IF NOT EXISTS Users (User_ID INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255) NOT NULL, Email VARCHAR(255) NOT NULL, Password CHAR(12) NOT NULL CHECK (CHAR_LENGTH(Password) >= 4))")
            
            # SQL Query for creating a table named Issues to store the Book Issues info.
            self.mycursor.execute("CREATE TABLE IF NOT EXISTS Issues (Issue_ID INT AUTO_INCREMENT PRIMARY KEY, User_ID INT NOT NULL, Name VARCHAR(255) NOT NULL, Book_ID INT NOT NULL, Title VARCHAR(255) NOT NULL, Issue_Date DATE, FOREIGN KEY (User_ID) REFERENCES Users(User_ID), FOREIGN KEY (Book_ID) REFERENCES Books(Book_ID))")

            # print("Database and Tables created successfully.")
            self.mydb.commit()
        
        else:
            print("Connection Failure")

    # Books Management System Options Start

    def create(self):
        bname = input("Enter Title: ")
        authname = input("Enter Author Name: ")

        no = int(input("Number of copies: "))

        for i in range(no):
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

            if a == 1:      # Shows all Book records
                sql = "SELECT * FROM LMS.Books;"
                res = pd.read_sql_query(sql, self.engine).sort_values(by = 'Title')
                
                if not res.empty:
                    print(res)
                    input("\nPress Enter to continue...")
                    # input()
                
                else:
                    print("No records found")
                    time.sleep(.7)

            elif a == 2:    # Filters by conditions
                while True:
                    os.system('cls')
                    print("Filter by:")
                    b = int(input("1. Book ID\n2. Title\n3. Author\n4. Back\n\nEnter the choice: "))

                    if b == 1:      # Filter by Book ID
                        id = int(input("Search Book ID: "))

                        if not res.empty and id in res['Book_ID'].values:
                            sql = f"SELECT * FROM Books WHERE Book_ID = {id};"
                            res = pd.read_sql_query(sql, self.engine).sort_values(by = 'Title')
                            print(res)
                            print()
                        
                        else:
                            print("No records found")
                            print()
                    
                    elif b == 2:    # Filter by Title
                        title = input("Search by Title: ")

                        sql = f"SELECT * FROM Books WHERE Title LIKE '%{title}%';"
                        res = pd.read_sql_query(sql, self.engine).sort_values(by = 'Title')

                        if not res.empty:
                            print(res)
                            print()
                        
                        else:
                            print("No record found")
                            print()
                    
                    elif b == 3:    # Filter by Author Name
                        auth = input("Search by Author: ")

                        sql = f"SELECT * FROM Books WHERE Author LIKE '%{auth}%';"
                        res = pd.read_sql_query(sql, self.engine).sort_values(by = 'Title')

                        if not res.empty:
                            print(res)
                            print()
                        
                        else:
                            print("No record found")
                            print()

                    elif b == 4:    # Exit this function
                        print("Thank you")
                        break

                    else:
                        print("Invalid choice")
                        print()

            elif a == 3:
                print("Thank you")
                print()
                break

            else:
                print("Invalid choice")
                print()

    def modify(self):
        while True:
            os.system('cls')
            sql = "SELECT * FROM Lms.Books;"
            res = pd.read_sql_query(sql, self.engine)
            
            id = int(input("\nUpdate Book ID: "))
            
            if not res.empty and  id in res['Book_ID'].values:
                a = int(input("\nUpdate:\n1. Title\n2. Author\n3. Back\n\nEnter the choice: "))

                if a == 1:
                    new = input("Update Title: ")

                    sql = "UPDATE Books SET Title = %s WHERE Book_ID = %s;"
                    val = (new, id)

                    self.mycursor.execute(sql, val)
                    self.mydb.commit()
                    
                    print("Updates done successfully.")
                    print()
                    break

                elif a == 2:
                    new = input("Update Author: ")

                    sql = "UPDATE Books SET Author = %s WHERE Book_ID = %s;"
                    val = (new, id)

                    self.mycursor.execute(sql, val)
                    self.mydb.commit()

                    print("Updates done successfully.")
                    print()
                    break

                elif a == 3:
                    print("Thank you")
                    break

                else:
                    print("Invalid Choice")
                    print()
            else:
                print("No recorded books")
                print()
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

        if bid in res['Book_ID'].values and res['Available'].values == 1:
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

    # Books Management System Options End
            
    # Users Management System Options Start

    def uadd(self):
        name = input("Enter Name: ")
        email = input("Enter Email ID: ")
        pas = input("Password: ")

        sql = "INSERT INTO Users (Name, Email, Password) VALUES (%s, %s, %s);"
        val = (name, email, pas)

        self.mycursor.execute(sql, val)
        self.mydb.commit()
    
    def ushow(self):
        while True:
            os.system('cls')
            a = int(input("1. Show All Users\n2. Filter\n3. Back\n\nEnter your choice: "))

            match a:
                case 1:      # Show All Users
                    sql = "SELECT * FROM LMS.Users;"
                    res = pd.read_sql_query(sql, self.engine).sort_values(by = 'Name').set_index('User_ID')

                    if not res.empty:
                        print(res)
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
                            case 1:      # Filter by User ID
                                id = int(input("Search User ID: "))

                                if not res.empty and id in res['User_ID'].values:
                                    sql = f"SELECT * FROM LMS.Users WHERE User_ID = {id};"
                                    res = pd.read_sql_query(sql, self.engine).sort_values(by = 'Name')
                                    print(res)
                                    input("\nPress Enter to continue...")
                                
                                else:
                                    print("No records found")
                                    time.sleep(.7)
                            
                            case 2:    # Filter by User Name
                                name = input("Search User Name: ")

                                sql = f"SELECT * FROM LMS.Users WHERE Name LIKE '%{name}%';"
                                res = pd.read_sql_query(sql, self.engine).sort_values(by = 'Name')

                                if not res.empty:
                                    print(res)
                                    input("\nPress Enter to continue...")
                                
                                else:
                                    print("No records found")
                                    time.sleep(.7)

                            case 3:
                                email = input("Search Email: ")

                                sql = f"SELECT * FROM LMS.Users WHERE Email LIKE '%{email}%';"
                                res = pd.read_sql_query(sql, self.engine).sort_values(by = 'Name')

                                if not res.empty:
                                    print(res)
                                    input("\nPress Enter to continue...")
                                
                                else:
                                    print("No records found")
                                    time.sleep(.7)

                            case 4:
                                print("Thank you!")
                                break

                            case _:
                                print("Invalid choice!")
                                time.sleep(.7)

                case 3:
                    print("Thank you!")
                    break

                case _:
                    print("Invalid choice!")
                    time.sleep(.7)

    def umod(self, id):
        while True:
            os.system('cls')
            a = int(input("Update:\n1. Name\n2. Email\n3. Password\n4. Back\n\nEnter the choice: "))

            __sql__ = f"SELECT * FROM LMS.Users WHERE User_ID = {id};"

            match a:
                case 1:                                                                    
                    sql = "UPDATE Users SET Name = %s WHERE User_ID = %s;"
                    val = (input("Update Name: "), id)

                    self.mycursor.execute(sql, val)
                    self.mydb.commit()

                    print("Updated successfully")
                                                                    
                    res = pd.read_sql_query(__sql__, self.engine)
                    time.sleep(0.7)

                case 2:
                    sql = "UPDATE Users SET Email = %s WHERE User_ID = %s;"
                    val = (input("Update Email: "), id)

                    self.mycursor.execute(sql, val)
                    self.mydb.commit()

                    res = pd.read_sql_query(__sql__, self.engine)
                    print("Updated successfully")
                    time.sleep(.7)

                case 3:
                    for i in range(3, 0, -1):
                        pwd = input("Update Password: ")
                        repeat = input("Re-enter Password: ")

                        if repeat == pwd:
                            sql = "UPDATE Users SET Password = %s WHERE User_ID = %s;"
                            val = (pwd, id)

                            self.mycursor.execute(sql, val)
                            self.mydb.commit()

                            res = pd.read_sql_query(f"SELECT * FROM LMS.Users WHERE User_ID = {id} AND Password = {pwd}", self.engine)
                            print("Updated successfully")
                            break
                                                                        
                        else:
                            print(f"Passwords do not match. Try again! {i - 1} chances left!")
                                                                
                case 4:
                    print("Thank you")
                    time.sleep(.7)
                    break
                                                                
                case _:
                    print("Invalid choice!")                                                    
                    time.sleep(.7)

            return res

    def udel(self, id):
        sql = "DELETE FROM Users WHERE User_ID = %s;"
        val = (id)

        self.mycursor.execute(sql, val)
        self.mydb.commit()

    # Users Management System Options End

if __name__ == "__main__":
    os.system('cls')
    x = System()
    
    while True:
        os.system('cls')
        print("--------------------Welcome to The Library Management System--------------------")
        a = int(input("1. Admin Login\n2. User Login\n3. Exit\n\nEnter the choice: "))
        match a:
            case 1:     # Admin Login
                uname = input("Username: ")
                pwd = input("Password: ")

                if uname == "admin" and pwd == "admin":
                    os.system('cls')
                    print("Welcome, Administrator!")
                    print()
                    while True:
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
                                os.system('cls')
                                x.ushow()
                                os.system('cls')

                            case 3:    # LMS System Exit
                                print("Thank you!")
                                break

                            case _:
                                print("Invalid Choice!")
                                time.sleep(0.7)
                                os.system('cls')

                else:
                    print("Wrong credentials")
                    time.sleep(0.7)
                    os.system('cls')

            case 2:    # User Login
                while True:
                    # For account deletion to directly go to the Register/Login Page
                    flag = False
                    os.system('cls')
                    a = int(input("1. Register\n2. Login\n3. Back\n\nEnter the choice: "))
                    match a:
                        case 1:
                            # Code for registering a new user
                            x.uadd()
                            print("Successfully registered!")
                            time.sleep(0.7)
                        
                        case 2:
                            # Code for user login
                            uid = input("User ID: ")
                            pwd = input("Password: ")

                            # Query the database to check the user's credentials
                            __sql__ = f"SELECT * FROM LMS.Users WHERE User_ID = {uid} AND Password = {pwd};"
                            res = pd.read_sql_query(__sql__, x.engine)

                            # If the user's credentials are correct, it will print the Welcome message along with other options for different functionalities
                            if not res.empty:
                                os.system('cls')
                                while True:
                                    os.system('cls')
                                    
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
                                                            print(__res__.sort_values(by = 'Issue_Date'))
                                                            input("\nPress Enter to continue...")

                                                        else:
                                                            print("No borrowed books!")
                                                            time.sleep(.7)

                                                    case 3:
                                                       x.borrow()

                                                    case 4:
                                                        pass

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
                exit()

            case _:
                print("Invalid choice!")
                time.sleep(0.7)