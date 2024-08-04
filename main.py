from db.db_manager import create_db, save_to_db
from parser_12.parser_12 import parsing_concerts


def main() -> None:
    try:
        # Создаём базу данных и таблицу
        create_db()
        # Извлекаем данные о концертах
        concerts = parsing_concerts()
        if not concerts:
            raise ValueError('Не удалось извлечь данные о концертах.')
        # Сохраняем данные в базу данных
        save_to_db(concerts)
    except Exception as e:
        raise RuntimeError(f'Произошла ошибка: {e}')


if __name__ == '__main__':
    main()
