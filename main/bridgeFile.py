import mysql.connector
from qrgeneration import uuid_code
from main import field4
from uniqueCode import code_string
# establish a connection to the database
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='toor',
    database='qruserdb'
)

# prepare the update query
sql = "UPDATE testing SET secureid = %s, uuid = %s WHERE phonenumber = %s"
val = (code_string, uuid_code, field4)

# create a cursor object
mycursor = mydb.cursor()

# execute the update query
mycursor.execute(sql, val)

# commit the changes to the database
mydb.commit()

# print the number of rows affected by the query
print(mycursor.rowcount, "record(s) affected")
