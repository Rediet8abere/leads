import os
import logging
from dotenv import load_dotenv

# Load the .env file
load_dotenv(override=True)
EMAIL_SENDER_PASSWORD = os.getenv('EMAIL_SENDER_PASSWORD')
SECRET_KEY = os.getenv('SECRET_KEY')