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
        # cursor.execute("SHOW TABLES")
        # global tablelist
        # tablelist = []
        # for x in cursor:
        #     tablename = str(x)
        #     #removing (,),' and , from the db name
        #     tablename = tablename.replace('(','')
        #     tablename = tablename.replace(')','')
        #     tablename = tablename.replace("'",'')
        #     tablename = tablename.replace(',','')
        #     tablelist.append(dbname)
        # print(tablelist)
        # if 'users' not in tablelist:
        #     cursor.execute("CREATE TABLE users(email VARCHAR(255) PRIMARY KEY, password VARCHAR(255), firstname VARCHAR(255), lastname VARCHAR(255), companyname VARCHAR(255));")
        #     mydb.commit()
    else:
        cursor.execute("CREATE DATABASE main;")
        cursor.execute("USE main")
        cursor.execute("CREATE TABLE users(email VARCHAR(255) PRIMARY KEY, password VARCHAR(255), firstname VARCHAR(255), lastname VARCHAR(255), companyname VARCHAR(255));")
        mydb.commit()
    print('config done')

def showall(table):
    global cursor
    cursor.execute("SELECT * FROM " + table)
    dblist = cursor.fetchall()
    return dblist

def signupInsert(tablename, email, password, firstname, lastname, companyname):
    sql = "INSERT INTO " + tablename + "(email, password, firstname, lastname, companyname)" + "VALUES (%s, %s, %s, %s, %s);"
    val = (email, password, firstname, lastname, companyname)
    cursor.execute(sql, val)
    mydb.commit()

def update(tablename, columnlist, valuelist, conditionfield, conditionvalue):
    length = len(columnlist)
    i = 0
    while i < length:
        sql = "UPDATE " + tablename + " SET " + columnlist[i] + "='" + str(valuelist[i]) + "' WHERE " + conditionfield + "='" + str(conditionvalue) + "';"
        print(sql)
        cursor.execute(sql)
        mydb.commit()
        i += 1