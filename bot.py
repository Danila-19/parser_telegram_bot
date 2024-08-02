import asyncio
import logging
import sqlite3

from aiogram import Bot, Dispatcher, html, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.command import Command, CommandObject
from aiogram.types import Message

from db.db_manager import get_last_12_concerts

logging.basicConfig(level=logging.INFO)
token = '7110758526:AAF9fcSMwP-NExpu3Z9hF4NL6n4BupBlcqk'
bot = Bot(
    token=token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Функция получает сообщения с командой '/start'.
    """
    await message.answer(
        f'Привет, {html.bold(message.from_user.full_name)}!\n'
        f'Этот бот предназначен для просмотра\n'
        f'самых ожидаемых концертов в Москве.'
        )


@dp.message(Command('latest'))
async def send_latest_concerts(message: types.Message) -> None:
    """
    Функция  функиция для работы с командой '/latest'.
    """
    concerts = get_last_12_concerts()
    if concerts:
        concerts_text = "\n\n".join(
            [f"{concert[1]} - {concert[2]} - {concert[3]}"
             for concert in concerts]
        )
    else:
        concerts_text = 'Нет доступных концертов.'

    await message.reply(concerts_text)


@dp.message(Command('search'))
async def search_concert(message: types.Message,
                         command: CommandObject):
    """
    Функция получает сообщения с командой '/search + <ключевое слово>'.
    """
    args = command.args
    db_path = 'db/concerts.db'

    if args:
        keyword = args
        await message.answer(f'Ищем по ключевому слову: {keyword}')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
            SELECT *
            FROM concerts
            WHERE title = ?
            ''', (keyword,))

            result = cursor.fetchone()

            if result:
                result_str = ' - '.join([str(field) for field in result[1:]])
                await message.answer(f'Найдено:\n{result_str}')
            else:
                await message.answer('По вашему запросу ничего не найдено.')
        except sqlite3.Error as e:
            await message.answer(
                f'Произошла ошибка при выполнении запроса: {e}')
        finally:
            conn.close()
    else:
        await message.answer('Пожалуйста, укажите название группы '
                             'для поиска.\nПример: /search ЛСП')


async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
