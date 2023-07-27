import os
import dotenv
from telethon import TelegramClient
from pymongo import MongoClient


dotenv.load_dotenv('.env')

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('BOT_TOKEN')
db_url = os.environ.get('MONGO_DB_URL')
database_name = os.environ.get('DATABASE_NAME')
database_channel = int(os.environ.get('TARGET_CHANNEL'))

client = MongoClient(db_url, tls=True)

bot = TelegramClient(
        'bot', 
        api_id, 
        api_hash,
    ).start(bot_token=bot_token)