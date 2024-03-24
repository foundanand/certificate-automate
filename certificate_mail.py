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
    gmail_user = os.getenv("AUTH_EMAIL")
    gmail_password = os.getenv("AUTH_PASS")

    # Create a message container
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = EMAIL_ID
    msg['Subject'] = f"Certificate of Participation | FINGENAI Hackathon 💡 | 16th Feburary"

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
            We hope this email finds you well. As we wrap up an exhilarating journey of innovation and collaboration at the FinGenAI Hackathon, we wanted to take a moment to extend our heartfelt gratitude for your enthusiastic participation and contribution.<br><br>
            Your dedication, creativity, and willingness to tackle challenging financial-based problems have truly enriched the experience for everyone involved. The diverse array of ideas and solutions presented has been truly inspiring, showcasing the incredible talent and potential within our community.<br>
            In recognition of your valuable participation, we are pleased to attach your Certificate of Participation here. This certificate is a token of our appreciation for your commitment and efforts, and we hope it serves as a fond reminder of your accomplishments and the exciting time we spent together.<br><br>
            In addition to this, we are thrilled to extend our warmest congratulations to our winning team:<br>
            Team Name: Team 404<br>
            for their outstanding victory by their exceptional performance, dedication and innovative solution.<br>
            You will receive the hard copy of your winning certificates in this upcoming week.<br><br>
            Once again, thank you all for making the FinGenAI Hackathon a remarkable event. We wish you all the best in your future endeavors and hope to cross paths again in the journey of Fintech exploration and advancement.<br><br>
            <p>Additionally, for those interested in reliving the moments from the event, please find the link to the event photos <a href="https://drive.google.com/drive/folders/1FEYYHELjAaDmHIgB07rm9oKF1VkW4F7L">here</a>.</p> <br><br>

            Warmest Regards,<br>
            FinTech Club,<br>
            VIT Bhopal University<br>
            </p>
        </body>
        </html>
    """

    msg.attach(MIMEText(html, 'html'))

    # Add QR code attachment to the email
    qr_code_path = (os.path.join(CERTIFICATE_FOLDER, f"{PER_NAME}_{EVENT_NAME}.pdf"))
    with open(qr_code_path, 'rb') as f:
        qr_code = MIMEApplication(f.read(), _subtype='png')
    qr_code.add_header('content-disposition', 'attachment', filename=os.path.basename(qr_code_path))
    msg.attach(qr_code)

    # Create the SMTP server and send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_user, gmail_password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()