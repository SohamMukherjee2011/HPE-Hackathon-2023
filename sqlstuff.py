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
    if 'main' in dblist:
        cursor.execute("USE main")
        cursor.execute("SHOW TABLES")
        tablelist = []
        for x in cursor:
            tablename = str(x)
            tablename = tablename.replace('(', '')
            tablename = tablename.replace(')', '')
            tablename = tablename.replace(',', '')
            tablename = tablename.replace("'", '')
            tablelist.append(tablename)
        if 'users' not in tablelist:
            cursor.execute("CREATE TABLE users(email VARCHAR(255) PRIMARY KEY, password BLOB, firstname VARCHAR(255), lastname VARCHAR(255), companyname VARCHAR(255), encryptionkey BLOB);")
            mydb.commit()


    else:
        cursor.execute("CREATE DATABASE main;")
        cursor.execute("USE main")
        cursor.execute("CREATE TABLE users(email VARCHAR(255) PRIMARY KEY, password BLOB, firstname VARCHAR(255), lastname VARCHAR(255), companyname VARCHAR(255), encryptionkey BLOB);")
        mydb.commit()
    print('config done')

def showall(table):
    global cursor
    cursor.execute("SELECT * FROM " + table)
    dblist = cursor.fetchall()
    return dblist

def showField(table, field, value):
    global cursor
    sql = "SELECT * FROM " + table + " WHERE " + field + "='" + value + "';"
    print(sql)
    cursor.execute(sql)
    dblist = cursor.fetchall()
    return dblist

def deleteSingleRow(table, field, value):
    cursor.execute("DELETE FROM " + table + " WHERE " + field + "='" + value + "';")
    mydb.commit()

def signupInsert(tablename, email, password, firstname, lastname, companyname, key):
    sql = "INSERT INTO " + tablename + "(email, password, firstname, lastname, companyname, encryptionkey)" + "VALUES (%s, %s, %s, %s, %s, %s);"
    val = (email, password, firstname, lastname, companyname, key)
    cursor.execute(sql, val)
    mydb.commit()

def update(tablename, column, value, conditionfield, conditionvalue):
        sql = "UPDATE " + tablename + " SET " + column + "='" + str(value) + "' WHERE " + conditionfield + "='" + str(conditionvalue) + "';"
        print(sql)
        cursor.execute(sql)
        mydb.commit()