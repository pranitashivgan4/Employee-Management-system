Employee Management System (EMS)

A simple and efficient Employee Management System built using HTML, CSS, JavaScript, Python (Backend), and MySQL Database.
This project allows organizations to manage employees, departments, and attendance in an organized and user-friendly way.

🚀 Project Overview

The Employee Management System helps administrators to:

✔ Add new employees
✔ View all employees
✔ Edit employee details
✔ Delete employee records
✔ Manage departments
✔ Track attendance
✔ View a dashboard with quick information

The system is built with a clean UI and smooth navigation between pages.

🖥️ Tech Stack
Frontend
HTML
CSS
JavaScript

Backend
Python (Flask / Custom Python logic)

Database
MySQL
phpMyAdmin for database management

📂 Project Structure

/ems-project
│── /static        → CSS, JS, images  
│── /templates     → HTML pages  
│── app.py         → Python backend  
│── database.sql   → Database tables  
│── README.md      → Project documentation

📌 Features

1. Dashboard
Displays total employees
Shows departments
Shows active / inactive status
Quick links to important pages

2. Employees Page
List of all employees
Columns: ID, Name, Email, Phone, Position, Salary, Joining Date
Edit & Delete buttons for each employee

3. Add Employee
Form to add new employee
Validation using JavaScript
Data stored in MySQL table

4. Departments
List of departments
Add / Edit / Delete departments

5. Attendance
Attendance records
Simple tracking module

Can be extended in the future

Database Structure:

1️⃣ employees Table
Stores all employee information.
Column	Type	Description
id	INT (PK)	Unique Employee ID
name	VARCHAR	Employee full name
email	VARCHAR	Email ID
phone	VARCHAR	Contact number
position	VARCHAR	Job title / designation
salary	INT	Monthly salary
join_date	DATE	Employee joining date
status	VARCHAR	Active / Inactive

2️⃣ attendance Table
Stores daily attendance of each employee.
Column	Type	Description
id	INT (PK)	Unique Attendance Record ID
emp_id	INT (FK)	Employee ID (same as id from employees table)
name	VARCHAR	Employee name (same as employees table)
date	DATE	Attendance date
status	VARCHAR	Present / Absent
Foreign Key:
emp_id → employees.id

3️⃣ department Table
Stores department information.
Column	Type	Description
dept_id	INT (PK)	Unique Department ID
dept_name	VARCHAR	Department Name
manager	VARCHAR	Department Manager

🔗 Relationship Summary

employees → attendance
One employee can have multiple attendance records.
Linked through emp_id.

department → employees
(If implemented later) each employee can belong to one department.
