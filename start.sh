#!/data/data/com.termux/files/usr/bin/bash
# Запуск: bash start.sh   (останавливать: pkill -f main.py; pkill -f alice_app.py)
termux-wake-lock
cd "$(dirname "$0")"
nohup python main.py > log.txt 2>&1 &
nohup python alice_app.py > alice_log.txt 2>&1 &
echo "запущено, логи: log.txt, alice_log.txt"
