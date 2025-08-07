
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
BTCUSDT | 🔴 SHORT  
✅ PROFIT  
Waktu: 2025‑08‑04 13:22:41  
Leverage: 20x  
Size: 0.0020 | Harga: 29123.4500  
Margin Entry: 2.91 USDT  
Margin Total: 11.65 USDT  
PNL: ✅ PROFIT `4.58 USDT`  
📊 ROI (PNL%): `39.33%`  

🕒 Lama Trading: 2 jam 14 menit  
💰 Wallet Sekarang: `172.33 USDT`  
```

### Google Sheet: jurnal
| Tanggal            | Symbol  | Posisi | Qty    | Harga     | PnL     | Wallet   | Durasi         |
|--------------------|---------|--------|--------|-----------|---------|----------|----------------|
| 2025‑08‑04 13:22:41| BTCUSDT | SHORT  | 0.002  | 29123.45  | 4.58    | 172.33   | 2 jam 14 menit |

## ⚠️ Keamanan
Pastikan file `.env` dan `credentials.json` masuk ke `.gitignore` bila diupload ke repo GitHub.

## Lisensi
Open source project by [juni-kun](https://github.com/juni-kun)
