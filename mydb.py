import mysql.connector

database = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'admin123'
)

# prepare a cursor object
cursorObject = database.cursor()

#create a database
cursorObject.execute("CREATE DATABASE CRM_DB")

print("ALL DONE")

# django administration credentials
#username: admin123
#password: admin123