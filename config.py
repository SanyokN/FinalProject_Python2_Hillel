import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = True
DB_PATH = os.getenv("DB_PATH") or ''
