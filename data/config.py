import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
BOT_ID = str(os.getenv("BOT_ID"))
E_MAIL = str(os.getenv("E_MAIL"))
REG_URL = str(os.getenv("REG_URL"))
AUTH_URL = str(os.getenv("AUTH_URL"))
CHECK_URL = str(os.getenv("CHECK_URL"))
GET_BALANCE_URL = str(os.getenv("GET_BALANCE_URL"))
REFILL_URL = str(os.getenv("REFILL_URL"))
WITHDRAW_URL = str(os.getenv("WITHDRAW_URL"))

admins = [
]

ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}
