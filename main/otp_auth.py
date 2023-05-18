import vonage
import random
import os
import mysql.connector

def sending_otp(email, password):
    usermail = email
    userpassword = password
    # Get Vonage credentials from environment variables
    VONAGE_API_KEY = os.environ.get('VONAGE_API_KEY')
    VONAGE_API_SECRET = os.environ.get('VONAGE_API_SECRET')

    # Generate a random 6-digit number
    random_number = random.randint(100000, 999999)
    # connection and updation in database
    mydb = mysql.connector.connect(
        host='localhost', 
        password='toor', 
        user='root',
        database='qrusersdb'
    )
    mycursor = mydb.cursor()

    # Define the SQL query with conditions
    sql = "UPDATE testing SET secureid = %s WHERE email = %s"

    # Define the new value and conditions
    val = (random_number, email)

    # Execute the SQL query with the new value and conditions
    mycursor.execute(sql, val)

    # Commit the changes to the database
    mydb.commit()


    # Create a Vonage client and send an SMS message
    client = vonage.Client(key=66286356, secret="Nb0GVOURQO1Ztvy0")
    sms = vonage.Sms(client)

    to_number = '918894646869'
    message = f'Your verification code is: {random_number}\n'

    try:
        responseData = sms.send_message({
            "from": "Vonage APIs",
            "to": to_number,
            "text": message,
        })

        if responseData["messages"][0]["status"] == "0":
            print("Message sent successfully.")
        else:
            print(f"Message failed with error: {responseData['messages'][0]['error-text']}") 

    except vonage.VonageError as e:
        print(f"Message failed with error: {e}")
    verify_otp(random_number, usermail, userpassword)

def verify_otp(otp_number, email, password):
    try:
        with mysql.connector.connect(
            host='localhost', 
            password='toor', 
            user='root',
            database='qrusersdb'
        ) as connection:
            cursor = connection.cursor()
            sql = "SELECT * FROM testing WHERE email = %s AND userpassword = %s"
            val = (email, password)
            cursor.execute(sql, val)
            records = cursor.fetchone()
            if int(records[-3]) == otp_number:
                print("OTP verified")
            else:
                print("Wrong OTP")
    except mysql.connector.Error as error:
        print(f"Error: {error}")
