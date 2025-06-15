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

# Добавялем столбекц для снов (если его еще нет)
try: 
    cursor.execute("ALTER TABLE entries ADD COLUMN dream TEXT")
    conn.commit()
    print("Столбец 'dream' добавлен!")
except sqlite3.OperationalError:
    print("Столбец уже есть. Идем дальше.")

def add_entry(text, mood=None, dream=None):
    cursor.execute('''
INSERT INTO entries (date, text, mood, dream)
VALUES (?, ?, ?, ?)
''', (datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), text, mood, dream))
    conn.commit()


def add_entry(text, mood=None, dream=None):
    """Добавляет запись в дневник."""
    cursor.execute(
        "INSERT INTO entries (date, text, mood, dream) VALUES (?, ?, ?, ?)",
        (datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), text, mood, dream))
    conn.commit()
    print("Запись добавлена!")

def get_entries():
    """Возвращает все записи"""
    cursor.execute("SELECT * FROM entries")
    return cursor.fetchall()

# Пример использования
if __name__ == "__main__":
    while True:
        print("\n1. Добавить обычную запись")
        print("2. Добавить сон")
        print("3. Показать все записи")
        print("4. Выход")
        choice = input("Выбери действие: ")

        if choice == "1":
            text = input("Текст записи: ")
            mood = input("Настроение (опционально): ")
            add_entry(text, mood if mood else None)
        elif choice == "2":
            dream = input("Опиши сон: ")
            mood =input("Настроение после сна (опционально): ")
            add_entry("🌌 Сон", mood if mood else None, dream) #запись сна.    
        elif choice == "3":
            entries = get_entries()
            for entry in entries:
                print(f"\n[{entry[1]}] {entry[2]}")
                if entry[3]:  #mood
                    print(f"Настроение: {entry[3]}")
                if entry[4]:  #dream
                    print(f"Сон: {entry[4]}")
        elif choice == "4":
            break

conn.close()
