import os
import time
from binance.client import Client
from telegram import Bot
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)
bot = Bot(token=TELEGRAM_TOKEN)

# === GOOGLE SHEETS SETUP ===
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
CREDS = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPE)
gc = gspread.authorize(CREDS)
SHEET = gc.open('TradeLog').worksheet('log')  # Pastikan nama spreadsheet & tab sesuai

def is_trade_logged(trade_id):
    try:
        last_rows = SHEET.get_all_values()[-100:]
        trade_ids = {row[0].strip() for row in last_rows if len(row) > 0}
        return str(trade_id) in trade_ids
    except Exception as e:
        print(f"ERROR checking trade_id in sheet: {e}")
        return False

def log_trade_to_sheet(trade):
    if is_trade_logged(trade["id"]):
        return
    try:
        SHEET.append_row([
            str(trade["id"]),
            format_timestamp(trade["time"]),
            trade["symbol"],
            trade.get("realizedPnl", "0")
        ])
    except Exception as e:
        print(f"ERROR logging trade to sheet: {e}")

# === DURASI TRADING ===
def calculate_trade_duration(open_time, close_time):
    duration_sec = (close_time - open_time) / 1000
    seconds = int(duration_sec)
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24

    if days >= 1:
        return f"{days}d {hours % 24:02d}h"
    elif hours >= 1:
        return f"{hours:02d}h {minutes % 60:02d}m"
    elif minutes >= 1:
        return f"{minutes:02d}m {seconds % 60:02d}s"
    else:
        return f"{seconds}s"

# === FIX: Cari open_time walaupun qty beda (untuk grid/DCA) ===
def get_trade_open_time(trade):
    try:
        symbol = trade["symbol"]
        side = trade["side"].upper()
        trades = client.futures_account_trades(symbol=symbol)

        # Cari eksekusi berlawanan arah sebelum trade ini
        opposite = "SELL" if side == "BUY" else "BUY"
        for t in reversed(trades):
            if t["time"] < trade["time"] and t["side"].upper() == opposite:
                return t["time"]

        # Fallback: ambil trade pertama untuk simbol ini
        if trades:
            return min(t["time"] for t in trades)
    except:
        pass
    return None

# === JURNAL TAMBAHAN ===
def log_journal_entry(trade):
    try:
        jurnal_sheet = gc.open('TradeLog').worksheet('jurnal')

        side = trade["side"].upper()
        position = "SHORT" if side == "BUY" else "LONG"
        close_time = trade["time"]
        open_time = get_trade_open_time(trade)
        duration = calculate_trade_duration(open_time, close_time) if open_time else "?"

        # Ambil leverage
        symbol = trade["symbol"]
        account_data = client.futures_account()
        positions = account_data.get("positions", [])
        position_data = next((p for p in positions if p["symbol"] == symbol), None)
        leverage = position_data.get("leverage", "-") if position_data else "-"
        if leverage != "-":
            leverage = f"{leverage}x"

        jurnal_sheet.append_row([
            format_timestamp(close_time),
            trade["symbol"],
            position,
            leverage,
            trade["qty"],
            trade["price"],
            trade.get("realizedPnl", "0"),
            get_wallet_balance(),
            duration
        ])
    except Exception as e:
        print(f"ERROR logging to jurnal sheet: {e}")

def format_timestamp(ms):
    try:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ms / 1000))
    except:
        return "-"

def get_wallet_balance():
    try:
        account = client.futures_account()
        for a in account.get("assets", []):
            if a["asset"] == "USDT":
                return float(a["walletBalance"])
    except:
        return 0.0

def format_closed_trade_message(trade):
    symbol = trade["symbol"]
    side = trade["side"].upper()
    qty = float(trade["qty"])
    price = float(trade["price"])
    realized_pnl = float(trade.get("realizedPnl", 0))
    timestamp = trade["time"]

    position_emoji = "🔴 SHORT" if side == "BUY" else "🟢 LONG"
    if realized_pnl > 0:
        pnl_label = "✅ PROFIT"
    elif realized_pnl < 0:
        pnl_label = "❌ LOSS"
    else:
        pnl_label = "⚪ BREAK EVEN"

    try:
        account_data = client.futures_account()
        positions = account_data.get("positions", [])
        position = next((p for p in positions if p["symbol"] == symbol), None)
        leverage = position.get("leverage", "-") if position else "-"
    except:
        leverage = "-"

    try:
        leverage_float = float(leverage)
        margin_used = (price * qty) / leverage_float
        pnl_percent = (realized_pnl / margin_used) * 100 if margin_used != 0 else 0
    except:
        pnl_percent = 0

    wallet = get_wallet_balance()
    time_str = format_timestamp(timestamp)
    open_time = get_trade_open_time(trade)
    duration = calculate_trade_duration(open_time, timestamp) if open_time else "?"

    message = (
        f"📉 *{symbol}* | {position_emoji}\n"
        f"{pnl_label} | *{realized_pnl:.2f} USDT*\n"
        f"──────────────\n"
        f"🕒 *Waktu*: {time_str}\n"
        f"📈 *Harga*: `{price:.2f}` | *Qty*: `{qty:.4f}`\n"
        f"⚖️ *Leverage*: `{leverage}x`\n"
        f"💰 *Margin*: `{(price * qty / float(leverage)):.2f} USDT`\n"
        f"📊 *ROI*: `{pnl_percent:.2f}%`\n"
        f"🕓 *Durasi*: {duration}\n"
        f"💼 *Wallet*: `{wallet:.2f} USDT`\n"
    )
    return message

def get_closed_trades(limit=100):
    try:
        trades = client.futures_account_trades(limit=limit)
        trades = sorted(trades, key=lambda x: x["time"])

        for trade in trades:
            trade_id = int(trade["id"])
            pnl = float(trade.get("realizedPnl", 0))

            if pnl == 0 or is_trade_logged(trade_id):
                continue

            msg = format_closed_trade_message(trade)
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg, parse_mode="Markdown")
            log_trade_to_sheet(trade)
            log_journal_entry(trade)

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    get_closed_trades()
