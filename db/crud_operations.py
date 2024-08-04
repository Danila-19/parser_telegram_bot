import argparse
import os
import sqlite3


def create_connection(db_file):
    '''Создание подключения к SQLite базе данных.'''
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f'SQLite версия: {sqlite3.version}')
    except sqlite3.Error as e:
        print(e)
    return conn


def create_concert(conn, title, date, location):
    '''Добавление нового концерта в таблицу concerts.'''
    sql = ''' INSERT INTO concerts(title, date, location)
              VALUES(?,?,?) '''
    cursor = conn.cursor()
    cursor.execute(sql, (title, date, location))
    conn.commit()
    return cursor.lastrowid


def read_concerts(conn):
    '''Чтение всех записей из таблицы concerts.'''
    sql = ''' SELECT * FROM concerts '''
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def update_concert(conn, id, title, date, location):
    '''Обновление записи в таблице concerts.'''
    sql = ''' UPDATE concerts
              SET title = ? ,
                  date = ? ,
                  location = ?
              WHERE id = ?'''
    cursor = conn.cursor()
    cursor.execute(sql, (title, date, location, id))
    conn.commit()


def delete_concert(conn, id):
    '''Удаление записи из таблицы concerts по id.'''
    sql = 'DELETE FROM concerts WHERE id=?'
    cursor = conn.cursor()
    cursor.execute(sql, (id,))
    conn.commit()


def close_connection(conn):
    '''Закрытие соединения с SQLite базой данных.'''
    if conn:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description='Управление базой данных концертов.')
    parser.add_argument(
        'action',
        choices=['create', 'read', 'update', 'delete'],
        help='Действие: create, read, update, delete',
    )
    parser.add_argument('--id',
                        type=int,
                        help='ID концерта (для update и delete)')
    parser.add_argument('--title',
                        type=str,
                        help='Название исполнителя')
    parser.add_argument('--date',
                        type=str,
                        help='Дата концерта')
    parser.add_argument('--location',
                        type=str,
                        help='Место проведения концерта')
    parser.add_argument(
        '--db',
        type=str,
        default=os.path.abspath('concerts.db'),
        help='Путь к базе данных SQLite',
    )

    args = parser.parse_args()

    conn = create_connection(args.db)
    if not conn:
        return

    if args.action == 'create':
        if args.title and args.date and args.location:
            create_concert(conn, args.title, args.date, args.location)
        else:
            print('Для создания концерта необходимо'
                  'указать title, date и location.')
    elif args.action == 'read':
        read_concerts(conn)
    elif args.action == 'update':
        if args.id and args.title and args.date and args.location:
            update_concert(conn, args.id, args.title, args.date, args.location)
        else:
            print(
                'Для обновления концерта необходимо'
                'указать id, title, date и location.'
            )
    elif args.action == 'delete':
        if args.id:
            delete_concert(conn, args.id)
        else:
            print('Для удаления концерта необходимо указать id.')

    close_connection(conn)


if __name__ == '__main__':
    main()
