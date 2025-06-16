import sqlite3
from datetime import datetime

# Функция для получения соединения с БД (создает новое для каждого потока)
def get_db_connection():
    conn = sqlite3.connect('diary.db', check_same_thread=False) # отключаем проверку потоков
    conn.row_factory = sqlite3.Row # Чтобы результаты возвращались как словари
    return conn

# Инициализация БД ( вызывается один раз при старте)
def init_db():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            text TEXT NOT NULL,
            mood TEXT,
            dream TEXT  
        )''')
        
        # Добавялем столбец для снов (если его еще нет)
        try: 
            cursor.execute("ALTER TABLE entries ADD COLUMN dream TEXT")
            conn.commit()
            print("Столбец 'dream' добавлен!")
        except sqlite3.OperationalError as e:
            if "duplicate column name" not in str(e):
                raise e
            print("Столбец уже есть. Идем дальше.")

        conn.commit()
    finally:
        conn.close()

    

def add_entry(text, mood=None, dream=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
INSERT INTO entries (date, text, mood, dream)
VALUES (?, ?, ?, ?)
''', (datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), text, mood, dream))
    conn.commit()

"""Добавляет запись в дневник."""
def add_entry(text, mood=None, dream=None):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO entries (date, text, mood, dream) VALUES (?, ?, ?, ?)",
            (datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), text, mood, dream)
        )
        conn.commit()
        print("Запись добавлена!")
    finally:
        conn.close()

    """Возвращает все записи"""
def get_entries():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM entries ORDER BY date DESC")
        return cursor.fetchall()
    finally:
        conn.close()
    


# Пример использования
if __name__ == "__main__":
    init_db()
"""while True:
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

conn.close()"""
