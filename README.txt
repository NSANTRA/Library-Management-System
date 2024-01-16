**NOTE: The basic structure of the LMS Project is completed but I am still implementing some other features/functions that can make it look a little more presentable. The script.bat file does not concern with the LMS.py and the README.txt files. The .py file purely runs on the CLI (Command-Line Interface) i.e. no GUI (Graphical User Interface). The credentials for the "Admin Login" are:
Username: admin
Password: admin

Library Management System (LMS)
This is a sample command-line-based LMS built using Python. It allows users to manage a library's books, users, and issues. The system uses MySQL database to store and manage the data.

Prerequisites
1. Python 3.x
2. MySQL Server
3. mysql-connector-python and pandas libraries (install using pip)
e.g. pip install [library_name]

Setup
1. Create a MySQL database named "LMS"
2. Update the 'host', 'user', and 'passwd' parameters in the 'System' class constructor with your own MySQL server details.
3. Run the 'init_database' method in the 'System' class to create the required tables.

Usage