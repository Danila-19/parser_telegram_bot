import sqlite3


def create_db(db_path='db/concerts.db'):
    """
    Создает таблицу concerts в базе данных SQLite, если она не существует.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS concerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        date TEXT NOT NULL,
        location TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()


def save_to_db(concerts, db_path='db/concerts.db'):
    """
    Сохраняет список концертов в базу данных SQLite.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for concert in concerts:
        cursor.execute('''
        INSERT INTO concerts (title, date, location)
        VALUES (?, ?, ?)
        ''', (concert['title'], concert['date'], concert['location']))

    conn.commit()
    conn.close()
