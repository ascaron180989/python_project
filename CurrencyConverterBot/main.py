import telebot
from config import TOKEN, values
from extensions import APIExceptions, UsersRequests

bot = telebot.TeleBot(TOKEN)


def check_validation(text_message):
    if len(text_message) != 3:
        raise APIExceptions('Не верное количество параметров (см. /help).')
    else:
        base, quote, amount = text_message
        if base not in values.keys():
            raise APIExceptions(f'Неизвестное значение параметра <валюта 1>: "{base}"\n(см. /values)')
        elif quote not in values.keys():
            raise APIExceptions(f'Неизвестное значение параметра <валюта 2>: "{quote}"\n(см. /values)')
        elif base == quote:
            raise APIExceptions(f'Невозможно конвертировать одинаковые валюты')
        try:
            float(amount)
        except ValueError:
            raise APIExceptions(f'Недопустимое значение параметра <количество>: параметр должен быть числом')


@bot.message_handler(commands=['start', 'help', 'values'])
def answer_command(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, f'Я бот🤖 который поможет вам конвертировать валюты.\n'
                                          f'Введите: <валюта 1> <валюта 2> <количество>\n'
                                          f'Для получения подробной справки введите /help\n'
                                          f'Для получения списка доступных валют /values\n')
    elif message.text == '/help':
        bot.send_message(message.chat.id, f'Вам необходимо отправить сообщение боту в виде <имя валюты цену которой '
                                          f'вы хотите узнать> <имя валюты в которой надо узнать цену первой валюты> '
                                          f'<количество первой валюты>. Доступные для конвертации валюты можно '
                                          f'увидеть нажав /values')
    elif message.text == '/values':
        bot.send_message(message.chat.id, f"Допустимые валюты: {', '.join(list(values.keys()))}")


@bot.message_handler(content_types='text')
def execute_convert(message):
    try:
        text_message = str(message.text).lower().split()
        check_validation(text_message)
        base, quote, amount = text_message
        result_convert = UsersRequests.get_price(base, quote, amount)
    except APIExceptions as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Ошибка приложения.\n{e}')
    else:
        bot.reply_to(message, result_convert)


bot.infinity_polling()
