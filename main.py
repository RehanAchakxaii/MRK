import os
import asyncio
import time
from dotenv import load_dotenv
from binance.client import Client
from telegram import Bot

# Load .env
load_dotenv()

# Environment variables
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
EXCHANGE_RATE_PKR = float(os.getenv("EXCHANGE_RATE_PKR"))

# Binance client
client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)

# Telegram Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Convert USD to PKR
def usd_to_pkr(usd):
    return round(usd * EXCHANGE_RATE_PKR, 2)

# Send Telegram message
async def send_telegram(message):
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

# Total fee tracker
total_fee_usd = 0.0

# Main task
async def track_trades():
    global total_fee_usd
    while True:
        try:
            symbol = "BTCUSDT"
            orders = client.get_all_orders(symbol=symbol, limit=50)
)
            for order in orders:
                if order["status"] == "FILLED":
                    price = float(order["price"])
                    qty = float(order["executedQty"])
                    side = order["side"]
                    fee = price * qty * 0.001  # 0.1% est. fee
                    total_fee_usd += fee

                    message = f"""📈 *Trade Alert*
Pair: {symbol}
Side: {side}
Qty: {qty}
Price: ${price}
Fee: ${round(fee, 4)} | PKR {usd_to_pkr(fee)}
Total: ${round(price * qty, 2)}
"""
                    await send_telegram(message)
                    await asyncio.sleep(2)  # Avoid rate limit

            print(f"🧾 Total Fee: ${total_fee_usd} | PKR {usd_to_pkr(total_fee_usd)}")

        except Exception as e:
            print("❌ Error:", e)
            await send_telegram(f"❌ Error: {str(e)}")

        await asyncio.sleep(15)

# Start bot
if __name__ == "__main__":
    asyncio.run(track_trades())
