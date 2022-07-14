import logging
import os
import time
from http import HTTPStatus
import requests
import telegram
from dotenv import load_dotenv

from exceptions import EmptyResponseException, NotGettingListException, KeyMissingException

load_dotenv()

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
console.setFormatter(formatter)
logger = logging.getLogger('logger')
logger.addHandler(console)

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
    if not bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message):
        logger.exception('Сбой при отправке сообщения')
    logger.info('Сообщение доставлено')


def get_api_answer(current_timestamp):
    """Запрос к эндпоинту и возвращение ответа API."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    if response.status_code != HTTPStatus.OK:
        raise Exception(f'Ответ от API: {response.status_code}')
    return response.json()


def check_response(response):
    """Проверяет ответ API на корректность."""
    if response is None:
        error_message = 'Ответ от сервера пуст'
        logger.exception(error_message)
        raise EmptyResponseException(error_message)
    if 'homeworks' not in response:
        logger.exception('Ключ "homeworks" отсутствует в словаре')
    homework = response['homeworks']
    if not isinstance(homework, list):
        error_message = 'ДЗ должно приходить в виде списка'
        logger.exception(error_message)
        raise NotGettingListException(error_message)
    try:
        homework = homework[0]
    except IndexError:
        raise IndexError('Список работ пуст')
    return homework


def parse_status(homework):
    """Возвращает строку со статусом домашней работы."""
    try:
        homework_name = homework['homework_name']
        homework_status = homework['status']
    except KeyError:
        raise KeyError('Ключ "homework_name" или "status" отсутствуют.')
    verdict = HOMEWORK_STATUSES[homework_status]
    if homework_status not in HOMEWORK_STATUSES:
        logger.exception(f'Статус {homework_status} невозможно обработать')
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверяет доступность переменных окружения."""
    if PRACTICUM_TOKEN and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        return True
    logger.critical('Отсутствуют обязательные переменные окружения!!!')
    return False


def main():
    """Основная логика работы бота."""
    condition = check_tokens()
    logger.warning('Бот запушен')
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    while condition:
        try:
            response = get_api_answer(current_timestamp)
            homework = check_response(response)
            message = parse_status(homework)
            send_message(bot, message)
            current_timestamp = int(time.time())
            time.sleep(RETRY_TIME)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            send_message(bot, message)
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
