import qrcode
import mysql.connector
import emailimage

def conn_retrieve(email, password):
    user_email = email
    user_password = password
    try:
        # Connect to the database
        mydb = mysql.connector.connect(
            host='localhost', 
            password='toor', 
            user='root',
            database='qrusersdb'
        )
        mycursor = mydb.cursor()

        # Define the SQL query with conditions
        sql = "SELECT * FROM testing WHERE email = %s AND userpassword = %s"
        # Define the values for the conditions
        val = (user_email, user_password)
        # Execute the SQL query with the conditions
        mycursor.execute(sql, val)
        # Fetch the results
        records = mycursor.fetchone()
        if records:
            # Call the qrGeneration function with the UUID code
            qrGeneration(records[-2], email)
        else:
            print("No record found for the given email and phone number.")
    except mysql.connector.Error as error:
        print("Failed to retrieve data from the database: {}".format(error))
    finally:
        # Close the database connection
        if mydb.is_connected():
            mydb.close()

def qrGeneration(uuid_code, email):
    try:
        qr = qrcode.QRCode(version=1, box_size=7, border=2)
        qr.add_data(uuid_code)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        image_path = 'E:\\RevisedEAuthenticationSystem\\qrcodes\\code.png'
        img.save(image_path)
        # os.system('python emailimage.py')
        emailimage.send_verification_email(email, password='abcnzzjjqibhevrx',image_path='E:\\RevisedEAuthenticationSystem\\qrcodes\\code.png')

        # connection and updation of UUID
        mydb = mysql.connector.connect(
        host='localhost', 
        password='toor', 
        user='root',
        database='qrusersdb'
        )
        mycursor = mydb.cursor()

        # Define the SQL query with conditions
        sql = "UPDATE testing SET uuid = %s WHERE email = %s"

        # Define the new value and conditions
        val = (uuid_code, email)

        # Execute the SQL query with the new value and conditions
        mycursor.execute(sql, val)

        # Commit the changes to the database
        mydb.commit()

    except Exception as e:
        print("Failed to generate QR code: {}".format(e))
