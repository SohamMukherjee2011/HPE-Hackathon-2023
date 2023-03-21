import mysql.connector as mysql

def config():
    mydb = mysql.connect(
    host="localhost",
    user="root",
    password="Soham@12"
    )
    global cursor
    cursor = mydb.cursor()




