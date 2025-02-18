# from flask_sqlalchemy import SQLAlchemy



# # We create a database instance
# db = SQLAlchemy()

### We can represent our database structure as classes => 
###  Those classes will be called models 

## => Each class is its own table in the database

import sqlite3

conn = sqlite3.connect('./instance/quiz.db')
print("Connected")

conn.execute("select * from user")

conn.execute("create table Employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, address TEXT NOT NULL)")  
  
print("Table created successfully")  
  
conn.close()  