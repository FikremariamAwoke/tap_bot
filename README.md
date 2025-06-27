# 🤖 Tap Bot

A hybrid **Python + Node.js Telegram bot** that automates tapping in the [TapTap crypto game](https://t.me/TapTapGameBot) using headless Chrome. Add the bot to a Telegram group, send a session link, and let it auto-tap all day using a custom JS override.

---

## 🚀 Features

- ✅ Listens to Telegram group messages for TapTap session links
- ✅ Uses Puppeteer (headless Chrome) to simulate taps
- ✅ Replaces the original tap script (`main.b930ae92.js`) with a custom one
- ✅ Reloads game page every 10 minutes
- ✅ Runs in a Docker container with auto-restart and sandboxed Chrome support

---

## 🧱 Tech Stack

- **Python**: `python-telegram-bot`, `watchdog`
- **Node.js**: `puppeteer`
- **Docker**: for containerization
- **Headless Chrome**: for in-browser automation

---
