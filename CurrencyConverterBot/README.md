# telegram bot CurrencyConverterBot

Найти бота можно перейдя по ссылке: https://t.me/mycurconvrbot/

Бот поддерживает следующие команды:
1) /start # Приветственное сообщение и краткая инструкция
2) /help # Подробная инструкция
3) /values # Допустимые валюты
4) <валюта 1> <валюта 2> <количество> # формат команды

Репозиторий содержит все необходимое для запуска бота на своем ПК. Для работы потребуются библиотеки: PyTelegramBotAPI и requests.

Для использования кода со своим ботом, достаточно изменить TOKEN в файле config.py

Для добавления новых конвертируемых валют, достаточно добавить валюты в словарь values в файле config.py
