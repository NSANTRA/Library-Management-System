# Library Management System (LMS) - Command-Line Interface

## Overview

The **Library Management System (LMS)** is a command-line-based application designed to manage library operations efficiently. Built using Python, this system facilitates the management of books, users, and book issues within a library setting. Data management is handled through a MySQL database, ensuring robust and reliable storage of all necessary information.

## Features

1. **Book Management**: Add, update, delete, and search for books within the library.
2. **User Management**: Register new users, update user information, and manage user records.
3. **Issue Management**: Issue books to users, track issued books, and manage return processes.
4. **Database Integration**: Utilizes MySQL for data storage, ensuring data integrity and persistence

## Getting Satrted

### Prequisites

Ensure you have the following installed:

1. **Python 3.x** - [Download Python](https://www.python.org/downloads/)
2. **MySQL Server** - [Download MySQL Server](https://dev.mysql.com/downloads/installer/)
3. Ensure MySQL Server is running and accessible.
4. The following Python libraries:
    - `mysql-connector-python`
    - `pandas`
    - `sqlalchemy`
    - `urllib.parse`
    - `pwinput`

    <!-- To install these Python libraries, you can use the following command:

    ```sh
    pip install mysql-connector-python pandas sqlalchemy pwinput -->

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/NSANTRA/Library-Management-System.git
    ```
2. Then change directory:
    ```sh
    cd Library-Management-System
    ```
3. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

### Usage

Run the **lms.py** script to start the application:
```sh
py lms.py
```
Follow the on-screen prompts to navigate through the system's functionalities.

### Admin Login

Use the following credentials to log in as an admin:
- **Username**: admin
- **Password**: admin

## Features

### Admin Features

1. **Add Books**: Admins can add new books to the library's inventory. This includes entering details such as:
    - **Title**: The name of the book.
    - **Author**: The author of the book.
    - **Quantity**: The number of copies available.

    This feature ensures that the library catalog is always up-to-date with the latest acquisitions and accurate inventory levels.

2. **Modify Books**: Admins can update the details of existing books in the inventory. This allows for corrections and updates to Title, Author, and Quantity. Keeping book records accurate and current improves the reliability of the library's database.

3. **Delete Books**: Admins can remove books from the library's inventory. This includes deleting books that are no longer available or needed. This helps in managing the inventory by removing outdated or irrelevant entries.

4. **View Books**: Admins can view the list of all available books in the library. This includes capabilities to:
    - Browse the complete catalog.
    - Search for specific books using filters such as title, author, and availability.
    - Sort books based on various criteria such as publication year, author name, or title.

    This provides admins with a comprehensive view of the library's collection and inventory status.

5. **View Users**: Admins can view the list of all registered users. This includes accessing user details such as user ID, name, and contact information. This feature aids in user management and monitoring user activities.

### User Features

1. **Register**: New users can create an account by providing necessary information such as Name, contact information, and password.
This feature allows users to access the library's resources and services.

2. **Login**: Existing users can log in using their username and password. Secure access ensures that only registered users can utilize the library's functionalities.

3. **Issue Books**: Users can borrow books from the library by selecting the desired book and initiating the issue process. The system records the issue date and sets a due date for return. This feature manages book circulation and ensures users can borrow books efficiently.

4. **Return Books**: Users can return borrowed books by identifying the book being returned and confirming the return process. The system updates the inventory to reflect the return. This feature ensures that borrowed books are tracked and returned on time.

5. **View Books**: Users can view the list of all available books in the library. This includes browsing the catalog, searching for specific books, and filtering by criteria such as title, author, or availability. Users can find and choose books they are interested in borrowing.

6. **Update Profile**: Users can update their personal information, including name, contact details, and password. This feature ensures that user profiles are current and accurate.

7. **Delete Account**: Users can delete their accounts if they no longer wish to use the library services. This feature allows users to manage their presence and data within the system.

## File Structure
    - **lms.py** - The main script for running the Library Management System. This script contains all core functionalities and commands for both admin and user operations.
    - **README.md** - This file, providing detailed information about the project, including installation, configuration, and usage instructions.
    - **requirements.txt** - A file listing all required Python libraries. Running pip install -r requirements.txt will install all necessary dependencies.
    - **script.bat** - (Optional) A batch script for automating certain tasks. Not directly related to lms.py or README.md.