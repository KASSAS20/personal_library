from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")
DB = os.environ.get("DB")
USER = os.environ.get("USER")
PASSWORD = os.environ.get("PASSWORD")
