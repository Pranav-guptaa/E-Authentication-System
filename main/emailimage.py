import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def send_verification_email(to_email, password, image_path):
    from_email = 'buildingsite4@gmail.com'
    subject = 'User Verification'

    msg = MIMEMultipart()

    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    body = f"Hi {to_email.split('@')[0]}, \
        \n\nThis is a verification email. Please scan the below QR code for further processing."
    msg.attach(MIMEText(body, "plain"))

    with open(image_path, 'rb') as f:
        img_data = f.read()
    image = MIMEImage(img_data, name='code.png')
    msg.attach(image)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        print("Email sent successfully.")
    except Exception as e:
        print("Failed to send email:", e)
    finally:
        server.quit()

# # Example usage
# if __name__ == '__main__':
#     to_email = field3
#     password = 'abcnzzjjqibhevrx'
#     image_path = 'E:\\RevisedEAuthenticationSystem\\qrcodes\\code.png'
#     send_verification_email(to_email, password, image_path)
