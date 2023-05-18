import mysql.connector
from flask import Flask, render_template, request, redirect, url_for
import time
import uuid
import otp_auth
import qrgeneration
import realTimeAuthentication
import voiceRecording
import voiceRecognition

# Connect to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="toor",
    database="qrusersdb"
)

if db.is_connected():
    print("Successfully Connected")
else:
    print("Not success")

# Create a cursor object to execute SQL queries
cursor = db.cursor()
# Initialize the Flask app
app = Flask(__name__, template_folder='')

# Define a route for the form page


@app.route('/')
def form():
    return render_template('index.html')

# Define a route for submitting the form


@app.route('/submit', methods=['POST'])
def submit():
    # Get the form data
    field1 = request.form['firstname']
    field2 = request.form['lastname']
    field3 = request.form['email']
    field4 = request.form['phonenumber']
    field5 = request.form['address']
    field6 = request.form['userpassword']
    # field7 = str(random.randint(100000, 999999))
    # code = uuid.uuid4()
    # field8 = str(code)
    try:
        # Execute an INSERT query to add a new record
        sql = "INSERT INTO testing (firstname, lastname, email, phonenumber, address, userpassword) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (field1, field2, field3, field4, field5, field6)
        cursor.execute(sql, values)

        # Commit the transaction
        db.commit()
        print(cursor.rowcount, "record inserted.")
        return "Record inserted successfully!"
    except mysql.connector.Error as error:
        print("Failed to insert record into table: {}".format(error))
        return "Error inserting record into table."

# Define a route for the sign-in page


@app.route('/signin')
def signin():
    return render_template('index.html')

# Define a route for submitting the sign-in form


@app.route('/signin_submit', methods=['POST'])
def signin_submit():
    # Get the form data
    email = request.form['email']
    password = request.form['password']
    try:
        # Execute a SELECT query to check if the email and password exist in the database
        sql = "SELECT * FROM testing WHERE email=%s AND userpassword=%s"
        values = (email, password)
        cursor.execute(sql, values)

        # Check if the query returned any rows
        row = cursor.fetchone()
        if row:
            # If the email and password are correct, redirect to the success page
            # os.system('python E:\\RevisedEAuthenticationSystem\\main\\uniqueCode.py')
            # generating QR and sending it
            code = uuid.uuid4()
            qrgeneration.qrGeneration(str(code), email)
            time.sleep(1)
            # generating OTP and sending it
            otp_auth.sending_otp(email, password)
            time.sleep(1)
            realTimeAuthentication.conn_retreive(
                email, password)  # verfication of QR
            time.sleep(1)
            voiceRecording.recording_voice()  # recording the voice of the user
            time.sleep(1)
            voiceRecognition.main(email, password)     # voice recognition

            # os.system('python E:\\RevisedEAuthenticationSystem\\main\\qrgeneration.py')
            # os.system('python bridgeFile.py')
            # os.system("python E:\\RevisedEAuthenticationSystem\\main\\realTimeAuthentication.py")
            # os.system("python E:\\RevisedEAuthenticationSystem\\main\\otpsendingVonage.py")
            # os.system("python E:\\RevisedEAuthenticationSystem\\main\\otpVerification.py")
            return ("QR and OTP is sended on your registered email address and phone number")
        else:
            # If the email and password are incorrect, display an error message
            return "Invalid email or password."
    except mysql.connector.Error as error:
        print("Failed to execute query: {}".format(error))
        return "Error executing query."


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
