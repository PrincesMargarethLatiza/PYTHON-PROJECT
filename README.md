## Shop Management System

# Overview

This Shop Management System is a Python-based application that uses Tkinter for the graphical user interface (GUI) and MySQL for data storage. It provides functionalities for customers to view items and place orders, and for administrators to manage items and view orders.

## Features

# Customer Features

* View Menu: Browse available items and their prices.

* Place Orders: Select items and specify quantities for purchase.

# Admin Features

* Login System: Authenticate with a username and password.

* Manage Items:

* Add new items to the menu.

* Delete items from the menu.

* View all items in the menu.

# Manage Orders:

* View all customer orders.

* See order details, including total cost.

## Prerequisites

* Python 3.7 or above

* MySQL Database Server

# Required Python libraries:

`mysql-connector-python`

# Install depencies using:

`pip install -r requirements.txt`

# Run the application

`Python_project.py`


# Database Setup

```
CREATE DATABASE keykishop;

CREATE TABLE items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
    type varchar(100)
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    item_id INT,
    quantity INT
);

CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username varcha (50),
    password varchar(100)
);

CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    customer_phone VARCHAR(20),
    order_type VARCHAR(50),
    total_bill DECIMAL(10, 2)
);

```
# Directory Structure

```
|PYTHON PROJECT\
|
├── Python_project.py # Main application
├── Readme.md # This file
```

# License

This project is licensed under the MIT License - see the LICENSE file for details.
