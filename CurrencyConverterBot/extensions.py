import requests
from config import URL, values


# Пользовательские исключения
class APIExceptions(Exception):
    pass


# пользовательские запросы
class UsersRequests:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            params = {'fsym': values[base], 'tsyms': values[quote]}
            r = requests.get(URL, params=params).json()
            result = r[values[quote]] * float(amount)
            return f'{base} = {amount}, это {quote} = {result}'
        except Exception:
            raise Exception(f'Ошибка выполнения функции get_price')
