import os
import logging
from fastapi import HTTPException
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from secrets import EMAIL_SENDER_PASSWORD

# # Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Create a logger instance
logger = logging.getLogger(__name__)

def send_email(subject: str, body: str, to_email: str):
    logger.info(f"GET request received - subject={subject} body={body} to_email={to_email} EMAIL_SENDER_PASSWORD={EMAIL_SENDER_PASSWORD}")
    # SMTP server configuration
    smtp_host = "smtp.gmail.com"  # Gmail SMTP server
    smtp_port = 587  # SMTP port for Gmail
    sender_email = "redietaberegesesse@gmail.com"
    sender_password = EMAIL_SENDER_PASSWORD

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Add email body
    msg.attach(MIMEText(body, 'plain'))
    if sender_password is None:
        raise HTTPException(status_code=401, detail="Invalid sender_password")
    try:
        # Establish a connection to the SMTP server
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)  # Log in to the SMTP server

        # Send the email
        server.sendmail(sender_email, to_email, msg.as_string())
        logger.info("Email sent successfully!")

    except Exception as e:
        logger.info(f"Error: {e}")

    finally:
        # Close the server connection
        server.quit()



