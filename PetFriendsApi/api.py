import requests
import config


class PetFriendsApi:
    def __init__(self):
        self.base_url = config.base_url

    def get_api_key(self, email: str, password: str) -> tuple:
        """
        This method allows to get API key which should be used for other API methods.
        Этот метод позволяет получить ключ API, который следует использовать для других методов API.
        """
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + '/api/key', headers=headers)
        status_code = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status_code, result

    def get_api_pets(self, auth_key: str, filter: str = '') -> tuple:
        """
        This method allows to get the list of pets.
        Этот метод позволяет получить список питомцев.
        """
        headers = {'auth_key': auth_key}
        params = {'filter': filter}
        res = requests.get(self.base_url + '/api/pets', headers=headers, params=params)
        status_code = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status_code, result

    def post_api_pets(self, auth_key: str, name: str, animal_type: str, age: int, pet_photo) -> tuple:
        """
        This method allows to add information about new pet.
        Этот метод позволяет добавить информацию о новом питомце.
        """
        headers = {'auth_key': auth_key}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        files = {'pet_photo': pet_photo}
        res = requests.post(self.base_url + '/api/pets', headers=headers, data=data, files=files)
        status_code = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status_code, result

    def post_api_create_pet_simple(self, auth_key: str, name: str, animal_type: str, age: int):
        """
        This method allows to add information about new pet.
        Этот метод позволяет добавить информацию о новом питомце.
        """
        headers = {'auth_key': auth_key}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        res = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)
        status_code = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status_code, result

    def post_api_pets_set_photo(self, auth_key: str, pet_id: str, pet_photo) -> tuple:
        """
        This method allows to add photo of a pet.
        Этот метод позволяет добавить фотографию питомца.
        """
        headers = {'auth_key': auth_key}
        files = {'pet_photo': pet_photo}
        res = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=headers, files=files)
        status_code = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status_code, result

    def delete_api_pets(self, auth_key: str, pet_id: str) -> tuple:
        """
        This method allows to delete information about pet from database.
        Этот метод позволяет удалить информацию о питомце из базы данных.
        """
        headers = {'auth_key': auth_key}
        res = requests.delete(self.base_url + '/api/pets/' + pet_id, headers=headers)
        status_code = res.status_code
        result = res.text
        return status_code, result

    def put_api_pets(self, auth_key: str, pet_id: str, name: str, animal_type: str, age: int) -> tuple:
        """
        This method allows to update information about pet.
        Этот метод позволяет обновить информацию о питомце.
        """
        headers = {'auth_key': auth_key}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        res = requests.put(self.base_url + '/api/pets/' + pet_id, headers=headers, data=data)
        status_code = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status_code, result
