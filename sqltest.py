import sqlstuff
import encryption
sqlstuff.config()
sqlstuff.update('users', 'firstname', 'Rohan', 'email', 'iamsoham2011@gmail.com')
print("update done")