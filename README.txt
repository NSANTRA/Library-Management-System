**NOTE: The script.bat file does not concern with the LMS.py and the README.txt files.

Library Management System (LMS)
This is a sample command-line-based LMS built using Python. It allows users to manage a library's books, users, and issues. The system uses MySQL database to store and manage the data.

Prerequisites
Python 3.x
MySQL Server
mysql-connector-python and pandas libraries (install using pip)
e.g. pip install [library_name]

Setup
Create a MySQL database named "LMS"
Update the 'host', 'user', and 'passwd' parameters in the 'System' class constructor with your own MySQL server details.
Run the 'init_database' method in the 'System' class to create the required tables.

Usage
