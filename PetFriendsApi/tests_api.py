import pytest
import config
from api import PetFriendsApi

pf = PetFriendsApi()


########################################################################################################################
#                                              Positive test                                                           #
########################################################################################################################

# KEY
def test_get_api_key_valid_email_and_password(email=config.valid_email, password=config.valid_password):
    """
    Тест - Получение key.
    """
    status_code, result = pf.get_api_key(email, password)
    assert status_code == 200
    assert len(result['key']) > 0


# CREATE
def test_post_api_pets(name=config.name_1, animal_type=config.animal_type_1, age=config.age_1,
                       pet_photo_url=config.pet_photo_url_1):
    """
    Тест - добавление нового питомца.
    """
    _, auth_key = pf.get_api_key(config.valid_email, config.valid_password)
    auth_key = auth_key['key']
    with open(pet_photo_url, 'rb') as pet_photo:
        status_code, result = pf.post_api_pets(auth_key, name, animal_type, age, pet_photo)
    assert status_code == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == str(age) \
           and result['pet_photo'] != ''


def test_post_api_create_pet_simple(email=config.valid_email, password=config.valid_password, name=config.name_2,
                                    animal_type=config.animal_type_2, age=config.age_2):
    """
    Тест - добавление нового питомца без фотографии.
    """
    _, auth_key = pf.get_api_key(email, password)
    auth_key = auth_key['key']
    status_code, result = pf.post_api_create_pet_simple(auth_key, name, animal_type, age)
    assert status_code == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age  # Тест провален.
    # API возвращает возраст как строку, по описанию должно быть число.


def test_post_api_pets_set_photo(email=config.valid_email, password=config.valid_password, name=config.name_2,
                                 animal_type=config.animal_type_2, age=config.age_2,
                                 pet_photo_url=config.pet_photo_url_2):
    """
    Тест - добавление фотографии выбранному питомцу.
    """
    _, auth_key = pf.get_api_key(email, password)
    auth_key = auth_key['key']
    _, result = pf.post_api_create_pet_simple(auth_key, name, animal_type, age)
    pet_id = result['id']
    with open(pet_photo_url, 'rb') as pet_photo:
        status_code, result = pf.post_api_pets_set_photo(auth_key, pet_id, pet_photo)
    assert status_code == 200
    assert result['name'] == name and result['animal_type'] == animal_type and result['age'] == age \
           and result['pet_photo'] != ''


# READ
def test_get_api_pets_all(email=config.valid_email, password=config.valid_password, name=config.name_2,
                          animal_type=config.animal_type_2, age=config.age_2):
    """
    Тест - Получение списка питомцев.
    """
    _, auth_key = pf.get_api_key(email, password)
    auth_key = auth_key['key']
    _, result = pf.post_api_create_pet_simple(auth_key, name, animal_type, age)
    status_code, result = pf.get_api_pets(auth_key)
    assert status_code == 200
    assert len(result['pets']) > 0


def test_get_api_pets_filter_my_pets(email=config.valid_email, password=config.valid_password, name=config.name_2,
                                     animal_type=config.animal_type_2, age=config.age_2):
    """
    Тест - Получение списка питомцев (фильтр 'my_pets').
    """
    _, auth_key = pf.get_api_key(email, password)
    auth_key = auth_key['key']
    status_code, result = pf.get_api_pets(auth_key, filter='my_pets')
    len_1 = len(result['pets'])
    _, result = pf.post_api_create_pet_simple(auth_key, name, animal_type, age)
    status_code, result = pf.get_api_pets(auth_key, filter='my_pets')
    len_2 = len(result['pets'])
    assert status_code == 200
    assert len_1 + 1 == len_2


# UPDATE
def test_put_api_pets(email=config.valid_email, password=config.valid_password, name_1=config.name_1,
                      animal_type_1=config.animal_type_1, age_1=config.age_1, name_2=config.name_2,
                      animal_type_2=config.animal_type_2, age_2=config.age_2):
    """
    Тест - изменить выбранного питомца.
    """
    _, auth_key = pf.get_api_key(email, password)
    auth_key = auth_key['key']
    _, result = pf.post_api_create_pet_simple(auth_key, name_1, animal_type_1, age_1)
    pet_id = result['id']
    status_code, result = pf.put_api_pets(auth_key, pet_id, name_2, animal_type_2, age_2)
    assert status_code == 200
    assert result['name'] == name_2 and result['animal_type'] == animal_type_2 and result['age'] == str(age_2)


# DELETE
def test_delete_api_pets(email=config.valid_email, password=config.valid_password, name=config.name_1,
                         animal_type=config.animal_type_1, age=config.age_1):
    """
    Тест - Удаление выбранного питомца.
    """
    _, auth_key = pf.get_api_key(email, password)
    auth_key = auth_key['key']
    _, result = pf.post_api_create_pet_simple(auth_key, name, animal_type, age)
    pet_id = result['id']A
    status_code, _ = pf.delete_api_pets(auth_key, pet_id)
    assert status_code == 200
    _, result = pf.get_api_pets(auth_key, filter='my_pets')
    assert pet_id not in result['pets'][0]['id']


########################################################################################################################
#                                              Negative test                                                           #
########################################################################################################################

# KEY
def test_get_api_not_valid_email(email=config.not_valid_email, password=config.valid_password):
    """
    Тест - Получение key. Не верное значение email.
    """
    status_code, result = pf.get_api_key(email, password)
    assert status_code == 403
    assert "This user wasn't found in database" in result


def test_get_api_not_valid_password(email=config.valid_email, password=config.not_valid_password):
    """
    Тест - Получение key. Не верное значение password.
    """
    status_code, result = pf.get_api_key(email, password)
    assert status_code == 403
    assert "This user wasn't found in database" in result


def test_get_api_key_zero_email(email='', password=config.valid_password):
    """
    Тест - Получение key. Пустое значение email.
    """
    status_code, result = pf.get_api_key(email, password)
    assert status_code == 403
    assert "This user wasn't found in database" in result


def test_get_api_key_zero_password(email=config.valid_email, password=''):
    """
    Тест - Получение key. Пустое значение password.
    """
    status_code, result = pf.get_api_key(email, password)
    assert status_code == 403
    assert "This user wasn't found in database" in result


# CREATE
def test_post_api_pets_not_valid_auth_key(name=config.name_1, animal_type=config.animal_type_1, age=config.age_1,
                                          pet_photo_url=config.pet_photo_url_1):
    """
    Тест - добавление нового питомца. Не верный key.
    """
    auth_key = ''
    with open(pet_photo_url, 'rb') as pet_photo:
        status_code, result = pf.post_api_pets(auth_key, name, animal_type, age, pet_photo)
    assert status_code == 403
    assert "Please provide 'auth_key' Header" in result


def test_post_api_pets_not_valid_animal_type(email=config.valid_email, password=config.valid_password,
                                             name=config.name_1, animal_type=config.animal_type_3, age=config.age_1,
                                             pet_photo_url=config.pet_photo_url_1):
    """
    Тест - добавление нового питомца. Не верный тип входных данных: Тип животного - число.
    """
    _, auth_key = pf.get_api_key(email, password)
    auth_key = auth_key['key']
    with open(pet_photo_url, 'rb') as pet_photo:
        status_code, result = pf.post_api_pets(auth_key, name, animal_type, age, pet_photo)
    assert status_code == 400  # Тест провален. Предоставляю данные неверного формата, ожидаю увидеть код 400,
    # по факту код 200, сервер не проверяет тип данных в полях: Имя, Возраст, Тип


def test_post_api_pets_not_valid_age(email=config.valid_email, password=config.valid_password, name=config.name_1,
                                     animal_type=config.animal_type_1, age=config.age_3,
                                     pet_photo_url=config.pet_photo_url_1):
    """
    Тест - добавление нового питомца. Не верный тип входных данных: Возраст - отрицательное число.
    """
    _, auth_key = pf.get_api_key(email, password)
    auth_key = auth_key['key']
    with open(pet_photo_url, 'rb') as pet_photo:
        status_code, result = pf.post_api_pets(auth_key, name, animal_type, age, pet_photo)
    assert status_code == 400  # Тест провален. Предоставляю данные неверного формата, ожидаю увидеть код 400,
    # по факту код 200, сервер не проверяет тип данных в полях: Имя, Возраст, Тип


def test_post_api_pets_not_pet_photo(email=config.valid_email, password=config.valid_password, name=config.name_1,
                                     animal_type=config.animal_type_1, age=config.age_1,
                                     pet_photo_url=config.pet_photo_url_3):
    """
    Тест - добавление нового питомца. Не верный тип входных данных: Фотография - текстовый документ.
    """
    _, auth_key = pf.get_api_key(email, password)
    auth_key = auth_key['key']
    with open(pet_photo_url, 'rb') as pet_photo:
        status_code, result = pf.post_api_pets(auth_key, name, animal_type, age, pet_photo)
    assert status_code == 400  # Тест провален. Предоставляю данные неверного формата, ожидаю увидеть код 400,
    # по факту код 500


# READ
def test_get_api_pets_all_not_valid_auth_key():
    """
    Тест - Получение списка питомцев. Не верный key.
    """
    auth_key = ''
    status_code, result = pf.get_api_pets(auth_key)
    assert status_code == 403
    assert "Please provide 'auth_key' Header" in result


def test_get_api_pets_not_valid_filter(email=config.valid_email, password=config.valid_password):
    """
    Тест - Получение списка питомцев. Не верный filter.
    """
    _, auth_key = pf.get_api_key(email, password)
    auth_key = auth_key['key']
    status_code, result = pf.get_api_pets(auth_key, filter='filter')
    assert status_code == 400  # Тест провален. Ожидаю 400 Bad Request, приходит 500 Internal Server Error
    assert 'Filter value is incorrect' in result


# DELETE
def test_delete_api_pets_not_valid_auth_key(email=config.valid_email, password=config.valid_password,
                                            name=config.name_1, animal_type=config.animal_type_1, age=config.age_1):
    """
    Тест - Удаление выбранного питомца. Не верный key.
    """
    _, auth_key = pf.get_api_key(email, password)
    auth_key = auth_key['key']
    _, result = pf.post_api_create_pet_simple(auth_key, name, animal_type, age)
    pet_id = result['id']
    auth_key = ''
    status_code, result = pf.delete_api_pets(auth_key, pet_id)
    assert status_code == 403
    assert "Please provide 'auth_key' Header" in result


def test_delete_api_pets_not_valid_pet_id(email=config.valid_email, password=config.valid_password):
    """
    Тест - Удаление выбранного питомца. Выбран не существующий питомец.
    """
    _, auth_key = pf.get_api_key(email, password)
    auth_key = auth_key['key']
    pet_id = ''
    status_code, result = pf.delete_api_pets(auth_key, pet_id)
    assert status_code == 404
    assert 'The requested URL was not found on the server. If you entered the URL manually please check your ' \
           'spelling and try again.' in result
