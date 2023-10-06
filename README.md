# Бот-ассистент

### Описание проекта

Telegram-бот, который обращается к API сервиса Практикум.Домашка и узнаёт статус вашей домашней работы: взята ли ваша домашка в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.

Бот может:
- раз в 10 минут опрашивать API сервиса Практикум.Домашка и проверять статус отправленной на ревью домашней работы;
- при обновлении статуса анализировать ответ API и отправлять вам соответствующее уведомление в Telegram;
- логировать свою работу и сообщать вам о важных проблемах сообщением в Telegram.

### Стек технологий
<div>
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/>
</div>

### Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:
```
git clone <project_url>
```
```
cd homework_bot
```

Создать и активировать виртуальную среду:
```
python -m venv venv
```
```
source venv/Scripts/activate
```

Установить зависимости из файла `requirements.txt`:
```
pip install -r requirements.txt
```

Запустить файл `homework.py`:
```
python homework.py
```

# Об авторе
Лошкарев Ярослав Эдуардович \
Python-разработчик (Backend) \
Россия, г. Москва \
E-mail: real-man228@yandex.ru 

[![VK](https://img.shields.io/badge/Вконтакте-%232E87FB.svg?&style=for-the-badge&logo=vk&logoColor=white)](https://vk.com/yalluv)
[![TG](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/yallluv)
