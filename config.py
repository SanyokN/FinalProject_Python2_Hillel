import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = True

TOKEN_API = os.getenv("TOKEN_API")
EMAIL_USER = os.getenv("EMAIL_USER")
SMTP_SERVER = os.getenv("SMTP_SERVER")
IMAP_SERVER = os.getenv("IMAP_SERVER")
DB_PATH = os.getenv("DB_PATH") or ""
