"""Навык Алисы -> TickTick. Flask в Termux, наружу через ngrok на ALICE_PORT."""
import os

import httpx
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()
app = Flask(__name__)
TOKEN = os.getenv("TICKTICK_TOKEN", "")
API = "https://api.ticktick.com/open/v1"
H = {"Authorization": f"Bearer {TOKEN}"}


def reply(req, text, end=False):
    return jsonify({"version": req.get("version", "1.0"), "session": req["session"],
                    "response": {"text": text, "end_session": end}})


def add_task(title):
    r = httpx.post(f"{API}/task", headers=H, json={"title": title}, timeout=10)
    r.raise_for_status()


def list_tasks():
    projects = httpx.get(f"{API}/project", headers=H, timeout=10).json()
    out = []
    for p in projects[:5]:
        data = httpx.get(f"{API}/project/{p['id']}/data", headers=H, timeout=10).json()
        out += [t["title"] for t in data.get("tasks", []) if t.get("status") == 0]
    return out


@app.post("/alice")
def alice():
    req = request.get_json()
    cmd = req["request"].get("command", "").lower().strip()
    try:
        if cmd.startswith(("добавь", "запиши", "создай")):
            title = cmd.split(" ", 1)[1] if " " in cmd else ""
            title = title.removeprefix("задачу").strip()
            if not title:
                return reply(req, "Какую задачу добавить?")
            add_task(title)
            return reply(req, f"Добавила: {title}")
        if "задач" in cmd or "список" in cmd:
            tasks = list_tasks()[:7]
            return reply(req, "; ".join(tasks) if tasks else "Задач нет")
    except Exception as e:  # noqa: BLE001
        return reply(req, f"Ошибка TickTick: {e}")
    return reply(req, "Скажи: добавь задачу, или: какие у меня задачи")


if __name__ == "__main__":
    app.run("127.0.0.1", int(os.getenv("ALICE_PORT", "5000")))
