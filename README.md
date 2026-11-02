# tg-mcp-phone (Termux)
1. `pkg install python git openssl libffi rust clang` ; `pkg install python-pillow`
2. `pip install -r requirements.txt`
3. `cp .env.example .env` и заполни (API_ID, API_HASH, SESSION_STRING, TICKTICK_TOKEN)
4. `bash start.sh`
Перед этим останови MCP на ноутбуке (иначе AuthKeyDuplicated).
ngrok: `ngrok http 8765` (MCP) и `ngrok http 5000` (Алиса).
