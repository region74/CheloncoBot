from dotenv import load_dotenv
import os

load_dotenv()

TOKEN_BOT = os.getenv('TOKEN_BOT')

DB_LITE_URL = os.getenv('DB_LITE_URL')
POSTGRES_URL = os.getenv('POSTGRES_URL')
