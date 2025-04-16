import sqlite3

## Connect to sqlite
connection = sqlite3.connect("student.db")

## create a cursor object to insert record, create
cursor = connection.cursor()

## Create the table
table_info = """
create table STUDENT (NAME TEXT, CLASS TEXT, 
SECTION TEXT, MARKS INTEGER)
"""

cursor.execute(table_info)

## Insert some more records

cursor.execute(""" Insert Into STUDENT values('Sadeeq', 'Data Science', 'A', 90)""")
cursor.execute(""" Insert Into STUDENT values('Buhari', 'Data Science', 'B', 35)""")
cursor.execute(""" Insert Into STUDENT values('Muhammad', 'Data Science', 'A', 85)""")
cursor.execute(""" Insert Into STUDENT values('Ameerah', 'DevOps', 'A', 100)""")
cursor.execute(""" Insert Into STUDENT values('Zainab', 'Machine Learning', 'A', 90)""")


## Display all the records
print("The Inserted Records Are")
data = cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)
    
## Commit your changes in the database
connection.commit()
connection.close()