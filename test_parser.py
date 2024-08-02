import unittest
from parser.parser import parsing_concerts
from unittest.mock import patch


class TestParsingConcerts(unittest.TestCase):
    """
    Класс для тестирования парсера
    """

    @patch('requests.get')
    def test_parsing_concerts_success(self, mock_get):
        """
        Функция для тестирования удачного сбора данных
        """

        html_content = '''
        <div class="Root-fq4hbj-4 iFrhLC">
            <h2 class="Title-fq4hbj-3 hponhw">ЛСП</h2>
            <ul class="Details-fq4hbj-0 jznoEj">
                <li class="DetailsItem-fq4hbj-1 ZwxkD">8 Августа</li>
                <li class="DetailsItem-fq4hbj-1 ZwxkD">Лужники</li>
            </ul>
        </div>
        '''
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = html_content

        expected_result = [{
            'title': 'ЛСП',
            'date': '8 Августа',
            'location': 'Лужники'
        }]

        self.assertEqual(parsing_concerts(), expected_result)

    @patch('requests.get')
    def test_parsing_concerts_no_concerts(self, mock_get):
        """
        Функция для тестирования, когда
        спаршенная страница пустая
        """

        html_content = '<html></html>'
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = html_content

        with self.assertRaises(ValueError) as context:
            parsing_concerts()
        self.assertEqual(str(context.exception),
                         'Не удалось найти ни одного блока концертов.')

    @patch('requests.get')
    def test_parsing_concerts_http_error(self, mock_get):
        """
        Функция для тестирования, когда
        не удалось сделать запрос к сайте
        """

        mock_get.return_value.status_code = 404

        with self.assertRaises(RuntimeError) as context:
            parsing_concerts()
        self.assertEqual(str(context.exception),
                         'Ошибка загрузки страницы: 404')


if __name__ == '__main__':
    unittest.main()
