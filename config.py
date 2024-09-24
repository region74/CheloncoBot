from dotenv import load_dotenv
import os

load_dotenv()

TOKEN_BOT = os.getenv('TOKEN_BOT')

DB_LITE_URL = os.getenv('DB_LITE_URL')
POSTGRES_URL = os.getenv('POSTGRES_URL')

approve_users_str = os.getenv('APPROVE_USERS')
APPROVE_USERS = list(map(int, approve_users_str.split(','))) if approve_users_str else []
