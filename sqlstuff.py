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
    if 'hackathon' in dblist:
        cursor.execute("USE hackathon;")
        cursor.execute("SHOW TABLES")
        tablelist = []
        for x in cursor:
            tablename = str(x)
            tablename = tablename.replace('(', '')
            tablename = tablename.replace(')', '')
            tablename = tablename.replace(',', '')
            tablename = tablename.replace("'", '')
            tablelist.append(tablename)
        if 'userlist' not in tablelist:
            cursor.execute("""CREATE TABLE userlist(
                            email VARCHAR(255),
                            password BLOB,
                            firstname VARCHAR(255),
                            lastname VARCHAR(255),
                            companyname VARCHAR(255),
                            encryptionkey BLOB);""")
        if 'quizresult' not in tablelist:
            cursor.execute("""CREATE TABLE quizresult(
                            email VARCHAR(255),
                            quizname VARCHAR(255),
                            score INT,
                            result INT);""")
        if 'bloglist' not in tablelist:
            cursor.execute("""CREATE TABLE bloglist(
                           title VARCHAR(255) ,
                           description VARCHAR(255),
                           link VARCHAR(255));""")
        if 'blogs' not in tablelist:
            cursor.execute("""CREATE TABLE blogs(
                            title VARCHAR(255),
                            content VARCHAR(255),
                            type VARCHAR(255),
                            indexno INT);""")
        if 'quizlist' not in tablelist:
            cursor.execute("""CREATE TABLE quizlist(
                            title VARCHAR(255),
                            link VARCHAR(255));""")
        if 'quizzes' not in tablelist:
            cursor.execute("""CREATE TABLE quizzes(
                            title VARCHAR(255),
                            description VARCHAR(255), 
                            link VARCHAR(255));""")
            
    else:
        cursor.execute("CREATE DATABASE hackathon;")
        cursor.execute("USE hackathon")
        cursor.execute("""CREATE TABLE userlist(
                            email VARCHAR(255),
                            password BLOB,
                            firstname VARCHAR(255),
                            lastname VARCHAR(255),
                            companyname VARCHAR(255),
                            encryptionkey BLOB);""")
        cursor.execute("""CREATE TABLE quizresult(
                            email VARCHAR(255),
                            quizname VARCHAR(255),
                            score INT,
                            result INT);""")
        cursor.execute("""CREATE TABLE bloglist(
                           title VARCHAR(255),
                           description VARCHAR(255),
                           link VARCHAR(255));""")
        cursor.execute("""CREATE TABLE blogs(
                            title VARCHAR(255),
                            content VARCHAR(255),
                            type VARCHAR(255),
                            index INT);""")
        cursor.execute("""CREATE TABLE quizlist(
                            title VARCHAR(255),
                            link VARCHAR(255));""")
        cursor.execute("""CREATE TABLE quizzes(
                            title VARCHAR(255),
                            description VARCHAR(255), 
                            link VARCHAR(255));""")

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
    cursor.execute(sql)
    valuelist = cursor.fetchall()
    return valuelist

def deleteSingleRow(table, field, value):
    cursor.execute("DELETE FROM " + table + " WHERE " + field + "='" + value + "';")
    mydb.commit()

def signupInsert(tablename, email, password, firstname, lastname, companyname, key):
    sql = "INSERT INTO " + tablename + "(email, password, firstname, lastname, companyname, encryptionkey)" + "VALUES (%s, %s, %s, %s, %s, %s);"
    val = (email, password, firstname, lastname, companyname, key)
    cursor.execute(sql, val)
    mydb.commit()

def quizresultinsert(tablename, email, quizname, score, result, attempted, link):
    sql = "INSERT INTO " + tablename + "(email, quizname, score, result, attempted, link)  VALUES(%s, %s, %s, %s, %s, %s);"
    val = (email, quizname, score, result, attempted,link)
    cursor.execute(sql, val)
    mydb.commit()

def update(tablename, column, value, conditionfield, conditionvalue):
        sql = "UPDATE " + tablename + " SET " + column + "='" + str(value) + "' WHERE " + conditionfield + "='" + str(conditionvalue) + "';"
        cursor.execute(sql)
        mydb.commit()