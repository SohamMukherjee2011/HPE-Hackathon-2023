import mysql.connector as mysql

mydb = mysql.connect(
        host="localhost",
        user="root",
        password="Soham@12"
    )
global cursor
cursor = mydb.cursor()
def config():

    #project-specific db checking if exists
    cursor.execute("SHOW DATABASES")
    i = 0
    global dblist
    dblist = []
    for x in cursor:
        global dbname
        dbname = str(x)
        #removing (,),' and , from the db name
        dbname = dbname.replace('(', '')
        dbname = dbname.replace(')', '')
        dbname = dbname.replace(',', '')
        dbname = dbname.replace("'", '')
        dblist.append(dbname)
        i = i + 1
    if 'main' in dblist:
        cursor.execute("USE main")
    else:
        cursor.execute("CREATE DATABASE main;")
        cursor.execute("USE main")
        cursor.execute("CREATE TABLE user(username VARCHAR(255) PRIMARY KEY, email VARCHAR(255), password VARCHAR(255), firstname VARCHAR(255), lastname VARCHAR(255), companyname VARCHAR(255));")
    print('config done')

def showall(table):
    global cursor
    cursor.execute("SELECT * FROM " + table)
    dblist = cursor.fetchall()
    return dblist

def signupInsert(tablename, username, password, firstname, lastname, email, companyname):
    sql = "INSERT INTO " + tablename + "(username, email, password, firstname, lastname, companyname)" + "VALUES (%s, %s, %s, %s, %s, %s);"
    val = (username, email, password, firstname, lastname, companyname)
    cursor.execute(sql, val)
    mydb.commit()

