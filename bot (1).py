import requests
import pandas as pd
import time
from telegram import Bot

# Telegram bilgilerin
BOT_TOKEN = "7625815250:AAED-goW-7qu2dzpPdQTrXUr9Mdt4un2uo8"
CHAT_ID = "1245892653"

bot = Bot(token=BOT_TOKEN)

# RSI hesaplama fonksiyonu
def rsi(data, period=14):
    delta = data.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# MEXC'den fiyat verisi çekme
def get_klines(symbol="BTCUSDT", interval="1m", limit=100):
    url = f"https://api.mexc.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url).json()
    closes = [float(item[4]) for item in response]  # Kapanış fiyatları
    return pd.Series(closes)

# Sinyal kontrol fonksiyonu
def check_rsi_and_signal(symbol="BTCUSDT"):
    try:
        closes = get_klines(symbol)
        rsi_series = rsi(closes)
        latest_rsi = rsi_series.iloc[-1]
        print(f"{symbol} RSI: {latest_rsi:.2f}")
        if latest_rsi > 90:
            bot.send_message(chat_id=CHAT_ID, text=f"{symbol} RSI: {latest_rsi:.2f} → SHORT sinyali")
        elif latest_rsi < 15:
            bot.send_message(chat_id=CHAT_ID, text=f"{symbol} RSI: {latest_rsi:.2f} → LONG sinyali")
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    while True:
        check_rsi_and_signal("BTCUSDT")
        time.sleep(60)
