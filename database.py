import sqlite3
import calendar_project

# Create a database connection
connectdb = sqlite3.connect('students.db')

# Create cursor to be able to navigate the database
cursor = connectdb.cursor()

# Create database table
cursor.execute("""CREATE TABLE students (
        first_name text,
        last_name text,
        date_available text
        )""")

# Commit changes to the database
connectdb.commit()

# Colose connection
connectdb.close()
