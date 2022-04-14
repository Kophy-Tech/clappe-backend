import smtplib, ssl
from decouple import config

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os


SENDER_MAIL = os.environ.get("EMAIL_HOST_USER")
PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

if PASSWORD is None or SENDER_MAIL is None:
    PASSWORD = config("EMAIL_HOST_PASSWORD")
    SENDER_MAIL = config("EMAIL_HOST_USER")

# sauce ocde: 152583


def send_my_email(receiver_email, body, subject, filename=None):
    
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = SENDER_MAIL
    message["To"] = receiver_email
    message["Subject"] = subject
    # message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    if filename:
        # Open file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(SENDER_MAIL, PASSWORD)
        server.sendmail(SENDER_MAIL, receiver_email, text)