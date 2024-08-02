import requests
from bs4 import BeautifulSoup


def parsing_concerts() -> dict:
    """
    Функция для извлечения данных о концертах с веб-страницы.
    """
    filtered_concerts = []
    url = 'https://afisha.yandex.ru/moscow/selections/hot'

    page = requests.get(url)
    if page.status_code != 200:
        raise RuntimeError(f'Ошибка загрузки страницы: {page.status_code}')

    # Парсим страницу Яндекс Афиши
    soup = BeautifulSoup(page.text, 'html.parser')

    # Находим все полные блоки концертов
    all_concerts = soup.findAll('div', class_='Root-fq4hbj-4 iFrhLC')
    if not all_concerts:
        raise ValueError('Не удалось найти ни одного блока концертов.')

    for items in all_concerts:
        title = items.find('h2', class_='Title-fq4hbj-3 hponhw')
        details = items.find('ul', class_='Details-fq4hbj-0 jznoEj')
        date = (
            details.find_all(
                'li', class_='DetailsItem-fq4hbj-1 ZwxkD')[0].text.strip()
            if details
            else None
        )
        location = (
            details.find_all(
                'li', class_='DetailsItem-fq4hbj-1 ZwxkD')[1].text.strip()
            if details
            else None
        )

        # Проверяем, что все найдено
        if title and date and location:
            concert_info = {
                'title': title.text.strip(),
                'date': date,
                'location': location,
            }
            filtered_concerts.append(concert_info)
    return filtered_concerts
