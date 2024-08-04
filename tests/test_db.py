import os
import sqlite3
import unittest

from db.db_manager import create_db, get_last_12_concerts, save_to_db


class TestParsingConcerts(unittest.TestCase):
    """
    Класс для тестирования запросов к базе данных
    """

    def setUp(self):

        self.db_path = 'tests/concerts_test.db'

        self.concerts = [{'title': 'Пикник Афиши',
                          'date': '3 и 4 августа',
                          'location': 'СК «Лужники»'}] * 12

        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS concerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            location TEXT NOT NULL
        )
        ''')

        self.cursor.executemany('''
        INSERT INTO concerts (title, date, location)
        VALUES (:title, :date, :location)
        ''', self.concerts)

        self.conn.commit()

    def tearDown(self):
        self.conn.close()

        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_get_last_12_concerts(self):
        """
        Функция для тестирования get_last_12_concerts
        """

        concerts_db = get_last_12_concerts(self.db_path)
        concerts_db_dicts = [{
            'title': concert[1],
            'date': concert[2],
            'location': concert[3]} for concert in concerts_db]

        self.assertEqual(self.concerts, concerts_db_dicts)

    def test_save_to_db(self):
        """
        Функция для тестирования сохранения данных в бд
        """

        save_to_db(self.concerts, self.db_path)
        concerts_db = get_last_12_concerts(self.db_path)
        concerts_db_dicts = [{
            'title': concert[1],
            'date': concert[2],
            'location': concert[3]} for concert in concerts_db]

        self.assertEqual(self.concerts, concerts_db_dicts)

    def test_create_db(self):
        """
        Функция для тестирования создания БД
        """

        create_db(self.db_path)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(concerts)")
        columns = cursor.fetchall()
        conn.close()

        expected_columns = [
            (0, 'id', 'INTEGER', 0, None, 1),
            (1, 'title', 'TEXT', 1, None, 0),
            (2, 'date', 'TEXT', 1, None, 0),
            (3, 'location', 'TEXT', 1, None, 0)
        ]

        self.assertEqual(columns, expected_columns)


if __name__ == '__main__':
    unittest.main()
