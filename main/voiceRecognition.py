from scipy.io import wavfile
import mysql.connector

def conn_retrieve(audio_shape, email, password):
    mydb = mysql.connector.connect(
        host='localhost', 
        password='toor', 
        user='root',
        database='qrusersdb'
    )
    
    mycursor = mydb.cursor()
    sql = "UPDATE testing SET audio_shape = %s WHERE email = %s"
    val = (audio_shape, email)
    mycursor.execute(sql, val)
    mydb.commit()
    
    sql = "SELECT * FROM testing WHERE phonenumber = %s AND firstname = %s"
    val = (email, password)
    mycursor.execute(sql, val)
    records = mycursor.fetchone()

    if int(records[-1]) == audio_shape:
        print("Access Granted")
    else:
        print("Access Denied")

def main(email, password):
    frequency_sampling, audio_signal = wavfile.read("E:\\RevisedEAuthenticationSystem\\recordedVoices\\recording.wav")
    useremail = email
    userpassword =  password
    conn_retrieve(audio_signal.shape[0], useremail, userpassword)
