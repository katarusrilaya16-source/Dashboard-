import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234"
    )
    print("Connected Successfully")
except Exception as e:
    print(e)