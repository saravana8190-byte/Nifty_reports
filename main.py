import time
import threading
import datetime
import os
import requests
import yfinance as yf
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Nifty 50 Bot is running 24/7!"

TELEGRAM_BOT_TOKEN = "8845571222:AAHUU8J1kn_Uk_c_d3sT80mLaSZxSCEuZXo"
TELEGRAM_CHAT_ID = "5125988102"

NIFTY_50_TICKERS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS",
    "BHARTIARTL.NS", "SBIN.NS", "LTIM.NS", "ITC.NS", "HINDUNILVR.NS",
    "LT.NS", "BAJFINANCE.NS", "HCLTECH.NS", "MARUTI.NS", "SUNPHARMA.NS",
    "ADANIENT.NS", "TATAMOTORS.NS", "NTPC.NS", "KOTAKBANK.NS", "TITAN.NS",
    "ONGC.NS", "POWERGRID.NS", "ADANIPORTS.NS", "COALINDIA.NS", "BAJAJFINSV.NS",
    "M&M.NS", "ULTRACEMCO.NS", "AXISBANK.NS", "ASIANPAINT.NS", "TATASTEEL.NS",
    "JSWSTEEL.NS", "GRASIM.NS", "TECHM.NS", "HDFCLIFE.NS", "BRITANNIA.NS",
    "HINDALCO.NS", "SBILIFE.NS", "DIVISLAB.NS", "EICHERMOT.NS", "NESTLEIND.NS",
    "DRREDDY.NS", "CIPLA.NS", "BPCL.NS", "TATACONSUM.NS", "APOLLOHOSP.NS",
    "HEROMOTOCO.NS", "BEL.NS", "TRENT.NS", "SHRIRAMFIN.NS", "WIPRO.NS"
]

def send_telegram_alert(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram API Error: {e}")

def run_bot():
    send_telegram_alert("🟢 *Render Bot Initialized & Running 24/7!*")
    while True:
        now = datetime.datetime.now()
        print(f"[{now.strftime('%H:%M:%S')}] Scanning strict 52-week lows...")
        try:
            data = yf.download(NIFTY_50_TICKERS, period="1y", interval="1d", progress=False)
            for ticker in NIFTY_50_TICKERS:
                try:
                    stock_close = data['Close'][ticker].dropna()
                    if stock_close.empty:
                        continue
                    current_price = stock_close.iloc[-1]
                    low_52w = stock_close.min()

                    if current_price <= low_52w:
                        symbol = ticker.replace(".NS", "")
                        alert_msg = (
                            f"🚨 *NEW 52-WEEK LOW BREAKOUT!*\n\n"
                            f"📈 *Stock:* `{symbol}`\n"
                            f"💰 *Current Price:* ₹{current_price:.2f}\n"
                            f"📉 *52-Week Low Hit:* ₹{low_52w:.2f}"
                        )
                        send_telegram_alert(alert_msg)
                except Exception:
                    continue
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(300)

if __name__ == "__main__":
    # Start the background trading bot thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Run Flask app to satisfy Render's web service health check requirement
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
                      
