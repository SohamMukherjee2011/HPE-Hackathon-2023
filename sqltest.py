import sqlstuff
sqlstuff.config()

table = sqlstuff.showall('users')
for x in table:
    print(x[0])
sqlstuff.update('users', ['password'], ['1234'], 'email', 'iamsoham2011@gmail.com')