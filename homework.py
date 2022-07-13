import logging
import os
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
console.setFormatter(formatter)
logging.getLogger('__name__').addHandler(console)

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    if bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message):
        pass
    else:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text='Сбой при отправке сообщения')
        logging.error('Сбой при отправке сообщения')


def get_api_answer(current_timestamp):
    """Запрос к эндпоинту и возвращение ответа API."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        homework_statuses = requests.get(ENDPOINT,
                                         headers=HEADERS,
                                         params=params
                                         )
    except Exception as error:
        message = f'Сбой запроса к API: {error}'
        logging.error(message)
    if homework_statuses.status_code != HTTPStatus.OK:
        raise logging.error('Статус страницы не равен 200')
    return homework_statuses.json()


def check_response(response):
    """Проверяет ответ API на корректность."""
    if response is None:
        assert logging.error('Словарь пуст')
    homework = response['homeworks']
    if homework is None:
        assert logging.error('Словарь пуст')
    if isinstance(homework, dict):
        raise TypeError('Ответ от API является словарём')
    return homework


def parse_status(homework):
    """Возвращает строку со статусом домашней работы."""
    homework_name = homework['homework_name']
    homework_status = homework['status']
    verdict = HOMEWORK_STATUSES[homework_status]
    if homework_status not in HOMEWORK_STATUSES:
        raise logging.error(f'Статус {homework_status} '
                            f'не возможно обработать :(')
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверяет доступность переменных окружения."""
    if PRACTICUM_TOKEN and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        return True
    else:
        logging.critical('Отсутствуют обязательные переменные окружения!!!')
        return False


def main():
    """Основная логика работы бота."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homework = check_response(response)
            message = parse_status(homework)
            send_message(bot, message)
            current_timestamp = int(time.time())
            time.sleep(RETRY_TIME)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message)
            time.sleep(RETRY_TIME)
        else:
            raise logging.info('Сообщение отправлено')


if __name__ == '__main__':
    main()
