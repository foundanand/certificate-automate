from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os
from dotenv import load_dotenv
load_dotenv()



def send_mail(EMAIL_ID, PER_NAME, EVENT_NAME, CERTIFICATE_FOLDER, CERTIFICATE):

    PER_NAME = ' '.join(word.capitalize() for word in PER_NAME.split())

    # Import from .env file
    admin_email = os.getenv("AUTH_EMAIL")
    admin_password = os.getenv("AUTH_PASS")

    # Create a message container
    msg = MIMEMultipart()
    msg['From'] = admin_email
    msg['To'] = EMAIL_ID
    msg['Subject'] = "Certificate of Participation"

    # Add HTML text to the email body
    html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 0;
                    font: 12px Arial, sans-serif; 
                }}
                p {{
                    margin-bottom: 20px;
                }}
            </style>
        </head>
        <body>
            <p>Dear {PER_NAME},<br><br>
            Add your message here.
            </p>
        </body>
        </html>
    """

    # Alternative way is to add external html file
    # with open('path/to/html/file.html', 'r') as file: 
    #     html = file.read()

    msg.attach(MIMEText(html, 'html'))

    # Add QR code attachment to the email
    certificate_path = (os.path.join(CERTIFICATE_FOLDER, f"{PER_NAME}_{EVENT_NAME}.pdf"))
    with open(certificate_path, 'rb') as f:
        participant_certificate = MIMEApplication(f.read(), _subtype='png')
    participant_certificate.add_header('content-disposition', 'attachment', filename=os.path.basename(certificate_path))
    msg.attach(participant_certificate)

    # Create the SMTP server and send the email
    # SMTP server details are stored in the .env file
    try:
        server = smtplib.SMTP_SSL(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT")))
        server.login(admin_email, admin_password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("An error occurred:", e)