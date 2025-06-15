import sqlite3
from datetime import datetime

#Подключаемся к БД (или создаем новую)
conn = sqlite3.connect('diary.db')
cursor = conn.cursor()

# Создаём таблицу
cursor.execute('''
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    text TEXT NOT NULL,
    mood TEXT
)               
''')
conn.commit()

def add_entry(text, mood=None):
    """Добавляет запись в дневник."""
    cursor.execute(
        "INSERT INTO entries (date, text, mood) VALUES (?, ?, ?)",
        (datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), text, mood)
    )
    conn.commit()
    print("Запись добавлена!")

def get_entries():
    """Возвращает все записи"""
    cursor.execute("SELECT * FROM entries")
    return cursor.fetchall()

# Пример использования
if __name__ == "__main__":
    while True:
        print("\n1. Добавить запись")
        print("2. Показать все записи")
        print("3. Выход")
        choice = input("Выбери действие: ")

        if choice == "1":
            text = input("Текст записи: ")
            mood = input("Настроение (опционально): ")
            add_entry(text, mood if mood else None)
        elif choice == "2":
            entries = get_entries()
            for entry in entries:
                print(f"\n[{entry[1]}] {entry[2]}")
                if entry[3]:
                    print(f"Настроение: {entry[3]}")
        elif choice == "3":
            break

conn.close()
