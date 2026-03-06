# Student Management System (Python + MySQL)

## Project Overview

The **Student Management System** is a desktop application developed using **Python**, **Tkinter (GUI)**, and **MySQL Database**.
The system allows users to manage student records efficiently by performing operations such as adding, updating, deleting, and searching student information.

This project demonstrates the integration of **Python programming**, **database connectivity**, and **graphical user interface design**.

The application is designed for educational institutions to manage student data in a structured and user-friendly way.

# Objectives of the Project

The main objectives of this project are:

* To store student records in a structured database.
* To perform CRUD operations (Create, Read, Update, Delete).
* To connect a Python application with a MySQL database.
* To provide a graphical interface for easy interaction.
* To export student data for external use.


# Technologies Used

| Technology      | Purpose                                       |
| --------------- | --------------------------------------------- |
| Python          | Programming language used to build the system |
| Tkinter         | Used to create the graphical user interface   |
| MySQL           | Database used to store student records        |
| MySQL Workbench | Database management tool                      |
| VS Code         | Development environment                       |

# System Features

The system includes the following features:

### 1. Login System

The application begins with a login screen to provide basic security. Only authorized users can access the system.

### 2. Add Student

Users can add a new student with the following information:

* Roll Number
* Student Name
* Father's Name
* Subject
* Grade
* Email
* Phone Number

### 3. View All Students

Displays all student records stored in the database in a table format.

### 4. Search Student

Users can search for students using **Roll Number or Name**.

### 5. Update Student

Existing student information can be edited and updated.

### 6. Delete Student

Users can delete student records from the database with a confirmation message.

### 7. Export Data

The system can export all student data into a **CSV file**, which can be opened in Excel.

### 8. Total Students Counter

Displays the total number of students stored in the system.

### 9. Clear Form

Allows users to quickly reset all input fields.

### 10. Auto Table Refresh

The table automatically refreshes after any add, update, or delete operation.

# Database Design

The project uses a **MySQL database** named:

student_management

### Table Structure

Table Name: `student`

| Column | Data Type    | Description   |
| ------ | ------------ | ------------- |
| rollNo | INT          | Primary key   |
| name   | VARCHAR(50)  | Student name  |
| fname  | VARCHAR(50)  | Father name   |
| sub    | VARCHAR(50)  | Subject       |
| grade  | VARCHAR(10)  | Student grade |
| email  | VARCHAR(100) | Email address |
| phone  | VARCHAR(15)  | Phone number  |

### SQL Table Creation

```sql
CREATE DATABASE student_management;

USE student_management;

CREATE TABLE student(
rollNo INT PRIMARY KEY,
name VARCHAR(50),
fname VARCHAR(50),
sub VARCHAR(50),
grade VARCHAR(10),
email VARCHAR(100),
phone VARCHAR(15)
);
```

# System Architecture

The system follows a simple architecture:

```
User
 ↓
Tkinter GUI (Python)
 ↓
MySQL Connector
 ↓
MySQL Database
```

The GUI sends queries to the database and displays results to the user.

# Project Structure

```
Student-Management-System
│
├── main.py
├── login.py
├── database.py
├── students.csv
├── README.md
└── screenshots
      ├── login.png
      ├── dashboard.png
      ├── mysql_table.png
```


# How to Run the Project

Follow these steps to run the system:

### Step 1: Install Python

Download and install Python.

### Step 2: Install Required Library

Install MySQL connector:

```
pip install mysql-connector-python
```

### Step 3: Setup Database

Open MySQL Workbench and run the SQL commands provided above to create the database and table.

### Step 4: Configure Database Connection

Update the connection details in the Python code:

```
host = "localhost"
user = "root"
password = "your_password"
database = "student_management"
```

### Step 5: Run the Program

Run the Python file:

```
python main.py
```

The login window will appear.


## Login Window

Displays username and password fields for system access. <br>
Enter usernmae: admin <br>
password: 1234

## Main Dashboard

Allows users to perform all student management operations.

## MySQL Workbench Table

Shows student records stored in the database.


# Advantages of the System

* Easy to use graphical interface
* Fast data storage and retrieval
* Reduces manual record keeping
* Improves data organization
* Simple and extendable architecture

# Future Improvements

The following features can be added in future versions:

* Student photo upload
* PDF report generation
* Advanced search filters
* Web-based version using Flask or Django
* Role-based authentication system
* Dashboard analytics and charts

# Conclusion

The **Student Management System** successfully demonstrates how Python can be integrated with MySQL to build a practical database application.
The system provides a simple but effective solution for managing student information through an interactive graphical interface.

This project helped in understanding:

* Python GUI development
* Database connectivity
* CRUD operations
* Data management concepts

# Author

**Muhammad Ismail**
BS Computer Science Student

