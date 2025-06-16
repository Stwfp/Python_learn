from flask import Flask, request, render_template, redirect
from main import add_entry, get_entries, init_db

import sqlite3

app = Flask(__name__)

# инициализируем БД при старте приложения
with app.app_context():
    init_db()

@app.route("/")
def home():
    entries = get_entries()
    return render_template("index.html", entries=entries)

@app.route("/add", methods=["POST"])
def add():
    text = request.form.get("text")
    mood = request.form.get("mood")
    dream = request.form.get("dream")

    if dream: # это сон
        add_entry("🌌 Dream", mood, dream)
    else:     # обычная запись  
        add_entry(text, mood)
    
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True) # разрешаем подключение из локальной сети