import numpy as np
from pyzbar.pyzbar import decode
import cv2
import mysql.connector


def conn_retreive(email, password):
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
    val = (email, password)

    # Execute the SQL query with the conditions
    mycursor.execute(sql, val)

    # Fetch all the matching records from the result set
    records = mycursor.fetchone()

    # Print the matching records

    print(records[-2])
    # # Close the database connection
    mydb.close()
    qr_authenticaiton(records[-2])
    # return records[-2]


def qr_authenticaiton(writing_file):
    # setting up camera feed
    video = cv2.VideoCapture(0)
    video.set(3, 640)
    video.set(4, 740)

    with open("E:\\RevisedEAuthenticationSystem\\authorisedUsers\\users.txt", 'a') as writingfile:
        writingfile.write('\n'+writing_file)
    with open("E:\\RevisedEAuthenticationSystem\\authorisedUsers\\users.txt", 'r') as file:
        authorised_list = file.read().strip()

    while True:
        success, image = video.read()
        for barcode in decode(image):
            qr_text = barcode.data.decode('utf-8')
            qr_text = str(qr_text)
            if qr_text not in authorised_list:
                color = (0, 0, 255)
                display_message = "Denied Access"
            else:
                color = (0, 255, 0)
                display_message = "Access Granted"
            polygon_points = np.array([barcode.polygon], np.int32)
            polygon_points = polygon_points.reshape(-1, 1, 2)
            rect_points = barcode.rect
            cv2.polylines(image, [polygon_points], True, color, 3)
            cv2.putText(image, display_message,
                        (rect_points[0], rect_points[1]), cv2.FONT_HERSHEY_PLAIN, 0.9, color, 2)
        cv2.imshow("Video", image)
        cv2.waitKey(1)
