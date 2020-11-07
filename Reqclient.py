import requests

""" Класс содержит функции для обработки GET и POST запросов """


class Request_client:
    def __init__(self, host, client_id, apikey):
        self.host = host
        self.ClientID = client_id
        self.Apikey = apikey

    def post_request(self, path: str, data: dict):
        """"Метод отправляет post запрос к Ozon
                Аргументы:
                    path: str - путь для запроса
                    data: dict - словарь, содержащий параметры для body post запроса
        """
        # создаём словарь хэдеров для передачи
        headers = {
            'Client-ID': str(self.ClientID),
            'Api-Key': str(self.Apikey)
        }
        # формируем url для запроса host+путь метода, который мы хотим использовать
        url = self.host + path

        return requests.post(url, headers=headers, json=data)

    # функия get запроса. Path - путь к методу.
    def get_request(self, path: str):
        """Метод отправляет get запрос к Ozon
            Аргументы:
                path: str - путь для запроса
        """
        # Формируем url для запроса
        url = self.host + path

        # Формируем словарь header'ов
        headers = {
            'Client-ID': str(self.ClientID),
            'Api-Key': str(self.Apikey)
        }
        return requests.get(url, headers=headers)
