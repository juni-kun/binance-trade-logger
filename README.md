
# Binance Trade Logger

Skrip Python untuk mencatat trade Binance Futures ke Google Sheet dan mengirim laporan ke Telegram, lengkap dengan durasi trading.

## Fitur Utama
- Menyimpan trade otomatis ke Google Sheet
- Menghitung durasi trading dari buka hingga tutup
- Notifikasi Telegram setiap trade selesai
- Format tampilan profesional di Telegram & Google Sheets

## 
✅ STRUKTUR FILE YANG DIBUTUHKAN

project-folder/

- main.py  <- (isi skrip kamu)

- .env     <- (isi API keys)

- credentials.json <- (Google Service Account credentials)

- requirements.txt <- (daftar library Python)

## ✅ Cara Membuat Ini Jalan 24/7
Jadwalkan lewat cron di VPS (misalnya setiap 2 menit)
```
*/2 * * * * /usr/bin/python3 /home/user/binance-trade-logger/main.py
```

## 📦 Setup

1. Buat file `.env` dengan isi seperti:
    ```env
    BINANCE_API_KEY=isi_punya_kamu
    BINANCE_API_SECRET=isi_punya_kamu
    TELEGRAM_TOKEN=isi_punya_kamu
    TELEGRAM_CHAT_ID=isi_punya_kamu
    ```

2. Siapkan `credentials.json` dari Google API (Spreadsheet access).

3. Install dependensi:
    ```bash
    pip install python-binance python-telegram-bot gspread oauth2client
    ```

4. Jalankan dengan:
    ```bash
    python main.py
    ```

## 🔎 Contoh Output

### Telegram (Markdown)
```
📉 BTCUSDT | 🔴 SHORT
✅ PROFIT | 12.50 USDT
──────────────
🕒 Waktu: 2025-08-08 10:32:15
📈 Harga: 29250.50 | Qty: 0.0100
⚖️ Leverage: 20x
💰 Margin: 14.63 USDT
📊 ROI: 85.47%
🕓 Durasi: 2h 15m
💼 Wallet: 1250.40 USDT
```

## 📄 Contoh Output di Google Sheet

### 1. Sheet: `log`
| Trade ID  | Time                | Symbol   | Realized PNL |
|-----------|--------------------|----------|--------------|
| 123456789 | 2025-08-08 10:32:15 | BTCUSDT  | 12.50        |
| 123456790 | 2025-08-08 12:45:20 | ETHUSDT  | -5.25        |
| 123456791 | 2025-08-08 14:02:55 | BNBUSDT  | 0.00         |

---

### 2. Sheet: `jurnal`
| Time                | Symbol   | Posisi | Leverage | Qty     | Price    | Realized PNL | Wallet Balance | Durasi |
|--------------------|----------|--------|----------|---------|----------|--------------|----------------|--------|
| 2025-08-08 10:32:15 | BTCUSDT  | SHORT  | 20x      | 0.0100  | 29250.50 | 12.50        | 1250.40        | 2h 15m |
| 2025-08-08 12:45:20 | ETHUSDT  | LONG   | 10x      | 0.5000  | 1850.00  | -5.25        | 1245.15        | 45m    |
| 2025-08-08 14:02:55 | BNBUSDT  | SHORT  | 15x      | 1.0000  | 240.00   | 0.00         | 1245.15        | 10m    |

## ⚠️ Keamanan
Pastikan file `.env` dan `credentials.json` masuk ke `.gitignore` bila diupload ke repo GitHub.

## Lisensi
Open source project by [juni-kun](https://github.com/juni-kun)
