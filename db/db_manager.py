import sqlite3


def create_db(db_path='db/concerts.db'):
    """
    Функция создает таблицу concerts в базе данных
    SQLite, если она не существует.
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
    Функция сохраняет список концертов в базу данных.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for concert in concerts:
        cursor.execute('''
        SELECT COUNT(*)
        FROM concerts
        WHERE title = ? AND date = ? AND location = ?
        ''', (concert['title'], concert['date'], concert['location']))
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
            INSERT INTO concerts (title, date, location)
            VALUES (?, ?, ?)
            ''', (concert['title'], concert['date'], concert['location']))

    conn.commit()
    conn.close()


def get_last_12_concerts(db_path='db/concerts.db'):
    """
    Функция возвращает последние 12 концертов из базы данных.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT id, title, date, location
    FROM concerts
    ORDER BY id DESC
    LIMIT 12
    ''')

    concerts = cursor.fetchall()
    conn.close()
    return concerts[::-1]
