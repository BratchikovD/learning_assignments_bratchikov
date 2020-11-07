from Reqclient import Request_client
import datetime
from dateutil.parser import parse
import json


class Ozon_Client:
    # добавляем в сериализацию json возможность обрабатывать datetime тип данных
    json.JSONEncoder.default = lambda self, obj: (obj.isoformat() if isinstance(obj, datetime.datetime) else None)

    def __init__(self, host, client_id, apikey):
        self.host = host
        self.client_id = client_id
        self.apikey = apikey

    # Блок "Атрибуты и категории товаров".
    def categories_tree(self, **opt_params):
        """Метод позволяет получить категории в виде дерева

        :param opt_params: category_id = int - идентификатор товара
                           language = str - язык, на котором вернётся результат. Допустимые значени: "RU", "EN"
        :return: ответ на запрос в формате json
        """
        # https://api-seller.ozon.ru/apiref/ru/#t-title_get_categories_tree
        # создаём объект клсса Request_Client для вызова его функций.
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v1/category/tree'
        # Формируем словарь для запроса.
        data = {}
        # Через цикл добавляем дополнительные параметры в словарь data
        for param, value in opt_params.items():
            data[param] = value

        response = r.post_request(path, data)
        return response.json()

    def category_attribute(self, category_id: int, **opt_params):
        """Метод позволяет получить список характеристик категории

        :param category_id: Идентификатор категории
        :param opt_params:  attribute_type = str - фильтр по характеристикам.
                                                   Допустимые значения для строки 'required' и 'optional'
                            language = str - язык, на котором вернётся результат. Допустимые значени: "RU", "EN"
        """
        # https://api-seller.ozon.ru/apiref/ru/#t-title_category_attribute
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v2/category/attribute'

        # Формируем словарь для запроса.
        data = {
            'category_id': category_id,
        }
        # Через цикл добавляем необязательные параметры к data
        for param, value in opt_params.items():
            data[param] = value

        response = r.post_request(path, data)
        # Возвращаем ответ запроса в формате json
        return response.json()

    def attribute_value_by_option(self, language: str, options):
        """ Метод позволяет узнать новые идентификаторы характеристик

        :param language: язык, на котором вернётся результат. Допустимые значени: "RU", "EN"
        :param options: словарь или массив словарей с идентификаторами.
                        Сам словарь должен иметь вид {'attribute_id': int, 'option_id': int}.
                        attribute_id - старый идентификатор характеристики.
                        option_id - старый идентификатор справочника
        """
        # https://api-seller.ozon.ru/apiref/ru/#t-title_attribute-_value-_byoption
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v2/category/attribute/value/by-option'

        # Формируем словарь для запроса.
        data = {
            'language': language,
            'options': options
        }

        response = r.post_request(path, data)
        # Возвращаем ответ запроса в формате json
        return response.json()

    def categories_attribute_values(self, category_id: int, attribute_id: int, limit: int, **opt_params):
        """Метод возвращает справочник для категории или характеристики товара.

        :param category_id: идентификатор категории
        :param attribute_id: идентификатор характеристики
        :param limit: количество отправлений в ответе. Максимум - 50, минимум - 1
        :param opt_params: last_value_id = int - Идентификатор с которого начать ответ. Пример: id=345, ответ с id=346.
                           language = str - язык, на котором вернётся результат. Допустимые значени: "RU", "EN"
        """
        # opt_params: last_value_id = int, language = 'RU' или 'EN'
        # https://api-seller.ozon.ru/apiref/ru/#t-title_attribute-_values
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v2/category/attribute/values'
        # Формируем словарь для запроса.
        data = {
            'category_id': category_id,
            'attribute_id': attribute_id,
            'limit': limit
        }
        # Через цикл обавляем необязательные параметры к data
        for method, key in opt_params.values():
            data[method] = key

        response = r.post_request(path, data)
        # Возвращаем ответ запроса в формате json
        return response.json()

    # Блок "Управление товарами и ценами"
    def product_import(self, items):
        """Метод позваляет добавить товары

        :param items: одиночный словарь или массив словарей. Словарь с необходимыми настройками формируется с помощью
                      вспомогательного класса Product_Import
        """
        # https://api-seller.ozon.ru/apiref/ru/#t-title_product_import
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v2/product/import'
        items_list = []
        # Формируем словарь для запроса
        data = {}
        if type(items) == dict:
            items_list.append(items)
            data['items'] = items_list
        elif type(items) == list:
            data['items'] = items

        return r.post_request(path, data).json()

    def product_update(self, product_card: dict):
        """Метод позволяет обновить карточку товара

        :param product_card: словарь с необходимыми параметрами для обновления карточки товара.
                             Формируется с помощью методов класса Product_Card_Client
        """
        # https://api-seller.ozon.ru/apiref/ru/#t-title_post_products_update
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v1/product/update'

        return r.post_request(path, product_card)

    def product_info(self, **opt_params):
        """Метод позволяет получить информацию о товаре по его идентификатору

        :param opt_params: offer_id = str - Идентификатор товара в системе продавец - артикул.
                           product_id = int - Идентификатор товара.
                           sku = int - Идентификатор товара в системе OZON-SKU
        """
        # opt_params: offer_id = str, product_id = int, sku = int
        # https://api-seller.ozon.ru/apiref/ru/#t-title_products_info
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v2/product/info'
        # Словарь для запроса
        data = {}
        # В цикле добавляем необязательные параметры в data
        for param, value in opt_params.items():
            data[param] = value

        response = r.post_request(path, data)
        # Возвращаем ответ в формате json
        return response.json()

    def products_attributes(self, **opt_params):
        """Метод позволяет получить описание характеристик товара по его идентификатору

        :param opt_params: offer_id = list - массив артикулов(идентификаторов товара в системе продавец).
                           product_id = list - массив идентификаторов товара.
                           page = int - Номер страницы, возвращаемой в запросе.
                           page_size = int - Количество элементов на странице
        """
        # opt_params: offer_id = list, product_id = list, page = int, page_size = int
        # https://api-seller.ozon.ru/apiref/ru/#t-title_products_info_attributes
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v2/products/info/attributes'

        # Создаём словарь для filter:
        flt = {}
        # Создаём словарь для запроса и добавляем туда сразу filter
        data = {
            'filter': flt
        }
        # В цикле добавляем необязательные параметры в data
        for param, value in opt_params.items():
            # Если параметр offer_id или product_id, то добавляем в словарь flt
            if param == "offer_id" or param == "product_id":
                flt[param] = value
            # Другие параметры добавляем сразу в data
            else:
                data[param] = value
        response = r.post_request(path, data)
        # Возвращаем ответ в формате json()
        return response.json()

    def prices_for_import(self, offer_id: str, price: str, **opt_params):
        """Этот метод позволяет сформировать словарь для обновления цены на товар

        :param offer_id: Идентификатор товара в системе продавца
        :param price:   Цена товара с учетом скидок.
        :param opt_params: product_id = int - идентификатор товара.
                           old_price = str - Цена до скидок (будет зачеркнута на карточке товара).
                                             Указывается в рублях. Разделитель дробной части—точка, до двух знаков после
                           premium_price = str - Цена для клиентов с подпиской Ozon Premium.
        """
        # Формируем словарь для обновления цены. Сразу добавляем обязательные параметры.
        price_list = {
            'offer_id': offer_id,
            'price': price
        }
        # В цикле добавляем необязательные параметры к price_list
        for param, value in opt_params.items():
            price_list[param] = value
        # Возвращаем словарь со всеми необходимыми данными для обновления цены
        return price_list

    def product_import_prices(self, prices):
        """Метод позволяет обновить цену одного или нескольких товаров.

        :param prices: словарь или массив словрей. Словарь формируется с помощью метода prices_for_import
        """
        # https://api-seller.ozon.ru/apiref/ru/#t-title_post_products_prices
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v1/product/import/prices'
        # В этот массив будем добавлять товары, цены которых хотим обновить
        prices_list = []
        # Словарь для запроса
        data = {}

        # Если передаём массив товаров, то сразу добавляем их к запросу
        if type(prices) == list:
            data['prices'] = prices
        # Если товар один и отправлен в виде словаря, то добавляем словарь к массиву и затем отправляем массив в data
        else:
            prices_list.append(prices)
            data['prices'] = prices_list

        # Возвращаем ответ в формате json
        return r.post_request(path, data).json()

    def stocks_for_import(self, offer_id: str, stock: int, **opt_params):
        """Метод позволяет добавить необходимые параметры в словарь для обновления остатков товара.

        :param offer_id: Идентификатор товара в системе продавца.
        :param stock: Количество товара в наличии.
        :param opt_params: product_id = int - Идентификатор товара.
        """
        # Формируем словарь для обновления остатка товара. Сразу добавляем обязательные параметры.
        stocks_list = {
            'offer_id': offer_id,
            'stock': stock
        }
        # В цикле добавляем необязательные параметры к stocks_list
        for param, value in opt_params.items():
            stocks_list[param] = value

        # Возвращаем сформированный словарь остатков.
        return stocks_list

    def product_import_stocks(self, stocks):
        """Метод позволяет обновить цену одного или нескольких товаров.

        :param stocks: словарь или массив словрей. Словарь формируется с помощью метода stocks_for_import
        """
        # https://api-seller.ozon.ru/apiref/ru/#t-title_post_products_stocks
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v1/product/import/stocks'
        # В этот массив будем добавлять товары, остатки которых хотим обновить
        stocks_list = []
        # Словарь для запроса
        data = {}
        # Если передаём массив товаров, то сразу добавляем их к запросу
        if type(stocks) == list:
            data['prices'] = stocks
        # Если товар один и отправлен в виде словаря, то добавляем словарь к массиву и затем отправляем массив в data
        else:
            stocks_list.append(stocks)
            data['prices'] = stocks_list

        # Возвращаем ответ в формате json()
        return r.post_request(path, data).json()

    def product_list(self, **opt_params):
        """Метод позволяет получить список товаров.

        :param opt_params:  offer_id = list - массив идентификаторов в системе продавец.
                            product_id = list - массив идентификаторов товара.
                            visibility = str - видимость товара.
                                        Возможные значения: ALL: все товары
                                                            VISIBLE: товары, которые видны покупателям
                                                            INVISIBLE: товары, которые по какой-то из причин не видны
                                                            EMPTY_STOCK: товары, у которых не указано наличие
                                                            READY_TO_SUPPLY: товары, которым можно установить наличие
                                                            STATE_FAILED: товары, создание которых завершилось ошибкой
                            page = int - Количество страниц в ответе.
                            page_size = int - Количество товаров на странице. По умолчанию значение 20. Макс: 1000
        """
        # https://api-seller.ozon.ru/apiref/ru/#t-title_get_products_list
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v1/product/list'
        # Создаём словарь для 'filter'
        fltdict = {}
        # Создаём словарь для запроса
        data = {}
        # В цикле добавляем необязательные параметры
        for param, value in opt_params.items():
            # В IF добавляем параметры для фильтра
            if param == 'offer_id' or param == 'product_id' or param == 'visibility':
                fltdict[param] = value
            # Добавляем все остальные параметр уже в data
            else:
                data[param] = value

        # Возвращаем ответ в формате json
        return r.post_request(path, data).json()

    def product_info_stocks(self, **opt_params):
        """Метод позволяет получиьт информацию о стоках товара

        :param opt_params: page = int - Количество страниц в ответе.
                           page_size = int - Количество товаров на странице. По умолчанию значение 20. Макс: 1000
        """
        # https://api-seller.ozon.ru/apiref/ru/#t-title_get_product_info_stocks
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v1/product/info/stocks'

        # Формируем словарь для запроса
        data = {}
        # В цикле добавляем необязательные параметры к data
        for param, value in opt_params.items():
            data[param] = value

        response = r.post_request(path, data)
        # Возвращаем ответ в формате json
        return response.json()

    def product_info_prices(self, **opt_params):
        """Метод позволяет получиьт информацию о ценах товара

        :param opt_params: page = int - Количество страниц в ответе.
                           page_size = int - Количество товаров на странице. По умолчанию значение 20. Макс: 1000
        """
        # opt_params: page = int, page_size = int
        # https://api-seller.ozon.ru/apiref/ru/#t-title_get_product_info_prices
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v1/product/info/prices'

        # Формируем словарь для запроса
        data = {}
        # В цикле добавляем необязательные параметры к data
        for param, value in opt_params.items():
            data[param] = value

        # Возвращаем ответ в формате json
        return r.post_request(path, data).json()

    # Блок "Акции"
    def actions_list(self):
        """Метод позволяет получить список акций, доступных для партнёра"""
        # https://api-seller.ozon.ru/apiref/ru/#t-title_action_available
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v1/actions'
        # Возвращаем ответ в формате json
        return r.get_request(path)

    def actions_candidates(self, action_id: int, **opt_params):
        """Метод позволяет получить список товаров, доступных для акции

        :param action_id: Идентификатор акции
        :param opt_params:  limit = int - Количество товаров в ответе.
                            offset = int - Количество элементов, которое будет пропущено в ответе.
                                           Если offset = 10, то ответ начнётся с 11 элемента
        """
        # https://api-seller.ozon.ru/apiref/ru/#t-title_action_available_products
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v1/actions/candidates'
        # Формируем словарь для запроса
        data = {
            'action_id': action_id
        }
        # В цикле добавляем все необязательные параметры к data
        for param, value in opt_params.items():
            data[param] = value

        # Возвращаем ответ в формате json
        return r.post_request(path, data).json()

    def action_products(self, action_id: int, **opt_params):
        """Метод позволяет получить список товаров, учавствующих в акции

        :param action_id:   Идентификатор акции
        :param opt_params:  limit = int - Количество товаров в ответе.
                            offset = int - Количество элементов, которое будет пропущено в ответе.
                                           Если offset = 10, то ответ начнётся с 11 элемента
        """
        # https://api-seller.ozon.ru/apiref/ru/#t-title_action_products
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v1/actions/products'

        # Формируем словарь для запроса
        data = {
            'action_id': action_id
        }
        # В цикле добавляем необязательные параметры к data
        for param, value in opt_params.items():
            data[param] = value

        # Возвращаем ответ в формате json
        return r.post_request(path, data).json()

    def action_add_product(self, action_id: int, products):
        """Метод позволяет добавить товары в доступную для партнера акцию
        :param action_id:   Идентификатор акции
        :param products:    Словарь или массив словарей вида {'product_id': int, 'action_price': float}, где
                            product_id: Идентификатор товара
                            action_price: Цена товара по акции. В рублях и с округлением до сотых.
        """
        # products передаётся либо в виде словаря вида {'product_id': int, 'action_price': float}.
        # Либо в виде массива таких словарей.
        # https://api-seller.ozon.ru/apiref/ru/#t-title_action_add_products
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v1/actions/products/activate'
        # Массив для акциозных продуктов
        products_list = []
        # Формируем словарь для запроса
        data = {
            'action_id': action_id,
        }
        # Если передали массив продуктов, то сразу добавляем в data
        if type(products) == list:
            data['products'] = products
        # Если дали один продукт (словарь), то добавляем его к массиву products_list, а затем в data
        else:
            products_list.append(products)
            data['products'] = products_list

        # Возвращаем ответ в формате json
        return r.post_request(path, data).json()

    def action_delete_products(self, action_id: int, products: list):
        """Метод позволяет удалить указанные товары из акции

        :param action_id: Идентификатор акции
        :param products: Список товаров, которые нужно удалить из акции.
        """
        # https://api-seller.ozon.ru/apiref/ru/#t-title_action_delete_products
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v1/actions/products/deactivate'
        # Формируем словарь для запроса
        data = {
            'action_id': action_id,
            'product_ids': products
        }

        # Возвращаем ответ в формате json
        return r.post_request(path, data).json()

    # Блок "Чат с покупателем"
    def chat_start(self, posting_number: str):
        """Метод позволяет начать чат с покупателем по отправлению.

        :param posting_number: Номер отправления
        """
        # https://api-seller.ozon.ru/apiref/ru/#t-title_post_chatstart
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v1/chat/start'

        # Формируем словарь для запроса
        data = {
            'posting_number': posting_number
        }
        # Отправляем запрос
        response = r.post_request(path, data)
        # Преобразовываем json в словарь
        answer = json.loads(response.text)
        # Если запрос успешен возвращаем идентификатор чата
        if response.status_code == 200:
            return answer['result']['chat_id']
        else:
            return response.json()

    def chat_list(self, **opt_params):
        """Метод позволяет получить информацию о чатах с указанными идентификаторами

        :param opt_params:  chat_id_list = list - Массив с идентификаторами чатов, для которых нужно вывести информацию.
                            page = int - Количество страниц в ответе.
                            page_size = int - Количество заказов на странице. Значение по умолчанию: 100. Макс: 1000
        """
        # https://api-seller.ozon.ru/apiref/ru/#t-title_post_chatlist
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v1/chat/list'
        # Формируем словарь для запроса
        data = {}
        # В цикле добавляем необязательные параметры к data
        for param, value in opt_params.items():
            data[param] = value

        # Возвращаем ответ в формате json
        return r.post_request(path, data).json()

    def chat_history(self, chat_id: str, **opt_params):
        """Метод позволяет получить историю сообщений в чате

        :param chat_id: Идентификатор чата.
        :param opt_params:  from_message_id = str - Идентификатор сообщения, с которого начать вывод истории чата.
                            limit = int - Количество сообщений в ответе.
        :return:
        """
        # https://api-seller.ozon.ru/apiref/ru/#t-title_get_chathistory
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v1/chat/history'

        # Формируем словарь для запроса
        data = {
            'chat_id': chat_id
        }
        # В цикле добавляем необязательные параметры к data
        for param, value in opt_params.items():
            data[param] = value

        # Возвращаем ответ в формате json
        return r.post_request(path, data).json()

    def chat_send_message(self, chat_id: str, text: str):
        """Метод позволяет отправить сообщение в чат по его идентификатору.

        :param chat_id: Идентификатор чата.
        :param text: Текст сообщения в формате plain text.
        :return:
        """
        # https://api-seller.ozon.ru/apiref/ru/#t-title_post_sendmessage
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v1/chat/send/message'

        # Формируем словарь для запроса
        data = {
            'chat_id': chat_id,
            'text': text
        }

        # Возвращаем ответ в формате json
        return r.post_request(path, data).json()

    def chat_send_file(self, chat_id: str, base64_content: str, name: str):
        """Метод позволяет отправить файл в чат по его идентификатору

        :param chat_id: Идентификатор чата
        :param base64_content:  Файл в виде строки base64.
        :param name:    Название файла с расширением.
        """
        # https://api-seller.ozon.ru/apiref/ru/#t-title_post_sendfile
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v1/chat/send/file'

        # Формируем словарь для запроса
        data = {
            'chat_id': chat_id,
            'base64_content': base64_content,
            'name': name
        }

        # Возвращаем ответ в формате json
        return r.post_request(path, data).json()

    # Блок "Отчёты"
    def transactions_list(self, date_from: str, date_to: str, transaction_type: str,
                          page: int, page_size: int, **posting_number):
        """Метод позволяет получить информацию о транзакциях за указанный период, по конкретным отправлениям

        :param date_from:   Начало периода в виде строки. Строка должна иметь вид: ""2020-03-01T07:14:11.897Z"
        :param date_to:     Конец периода в виде строки. Строка должна иметь вид: ""2020-03-01T07:14:11.897Z"
        :param transaction_type:    Тип транзакции. Допустимые значения: all — все,
                                                                         orders — заказы,
                                                                         returns — возвраты,
                                                                         services — сервисные сборы.
        :param page:    Номер страницы, возвращаемой в запросе.
        :param page_size: Количество элементов на странице.
        :param posting_number: Номер отправления.
        :return:
        """
        # https://api-seller.ozon.ru/apiref/ru/#t-title_transactions
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v2/finance/transaction/list'
        # Словарь для параметра 'date'
        from_to = {
            # парсим обе строки дат в формат datetime
            'from': parse(date_from, fuzzy=True),
            'to': parse(date_to, fuzzy=True)
        }
        # Формируем словарь для фильтра
        flt_dict = {
            'date': from_to,
            'transaction_type': transaction_type
        }
        # В цикле добавляем необязатыельный параметр в фильтр
        for param, value in posting_number.items():
            flt_dict[param] = value

        # Формируем словарь для запроса
        data = {
            'filter': flt_dict,
            'page_size': page_size,
            'page': page
        }

        # Возвращаем ответ в виде json
        return r.post_request(path, data).json()

    def report_list(self, **opt_params):
        """Метод позволяет вернуть список отчётов, которые были сформированы раньше.

        :param opt_params:  page = int - Количество страниц в ответе.
                            page_size = int - Количество заказов на странице. Значение по умолчанию: 100. Макс: 1000
                            report_type = str -Тип отчёта. Допустимые значения: SELLER_PRODUCTS — отчет по товарам,
                                                                                SELLER_TRANSACTIONS — отчет по транзакц.
        """
        # https://api-seller.ozon.ru/apiref/ru/#t-title_post_reportlist
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v1/report/list'

        # Формируем словарь для запроса
        data = {}
        # В цикле добавляем необязательные параметры к data
        for param, value in opt_params.items():
            data[param] = value

        # Возвращаем ответ в формате json
        return r.post_request(path, data).json()

    def report_info(self, code: str):
        """Метод позволяет вернуть информацию о запрошенном отчете по его уникальному ID

        :param code:    Уникальный ID отчета
        """
        # https://api-seller.ozon.ru/apiref/ru/#t-title_post_reportinfo
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v1/report/info'

        # Формируем словарь для запроса
        data = {
            'code': code
        }

        # Возвращаем ответ в формате json
        return r.post_request(path, data).json()

    def report_products(self, offer_id: list, *sku: list, **opt_params):
        """Метод позволяет вернуть отчёт по товарам

        :param offer_id: Список типа str идентификаторов товара в системе продавца.
        :param sku: Список типа int идентификаторов товара в системе Ozon.
        :param opt_params:  search = str - Поиск по содержанию записи, проверяет наличие
                            visibility = str - Фильтр по видимости товара.
                            Допустимые значения: ALL: все товары
                                                 VISIBLE: товары, которые видны покупателям
                                                 INVISIBLE: товары, которые по какой-то из причин не видны покупателям
                                                 EMPTY_STOCK: товары, у которых не указано наличие
                                                 READY_TO_SUPPLY: товары, которым можно установить наличие
                                                 STATE_FAILED: товары, создание которых завершилось ошибкой
        """
        # https://api-seller.ozon.ru/apiref/ru/#t-title_post_reportproducts
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавялется к хосту для запроса
        path = '/v1/report/products/create'

        # Формируем словарь для запроса
        data = {
            'offer_id': offer_id,
            'sku': sku
        }
        for param, value in opt_params:
            data[param] = value

        # Возвращаем ответ в формате json
        return r.post_request(path, data).json()

    def report_transactions(self, date_from: str, date_to: str, **opt_params):
        """Метод позволяет вернуть отчёт по транзакциям

        :param date_from: Дата с которой рассчитывается отчет по транзакциям. Формат YYYY-MM-DD
        :param date_to: Дата по которую рассчитывается отчет по транзакциям. Формат YYYY-MM-DD
        :param opt_params:  search = str - Поиск по содержанию записи, проверяет наличие
                            transaction_type = str - Фильтр по типу транзакции.
                            Возможные варианты: "ALL", "ORDERS", "RETURNS", "SERVICES", "OTHER", "DEPOSIT"
        """
        # opt_params: search = str, transaction_type = str
        # https://api-seller.ozon.ru/apiref/ru/#t-title_post_reporttransactions
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v1/report/transactions/create'

        # Формируем словарь для запроса
        data = {
            'date_from': date_from,
            'date_to': date_to
        }
        # В цикле добавляем необязательные параметры к data
        for param, value in opt_params.items():
            data[param] = value

        # Возвращаем ответ в формате json
        return r.post_request(path, data).json()

    # Блок "Отправления со склада продавцы"
    def fbs_list(self, sort: str, since: str, to: str, limit: int, barcodes: bool, **opt_params):
        """Метод позволяет вернуть список отправлений за указанный период

        :param sort: направление сортировки. asc — по возрастанию, desc — по убыванию.
        :param since: 	Начало периода. Строка вида "2020-03-01T07:14:11.897Z"
        :param to:      Конец периода. Строка вида "2020-03-01T07:14:11.897Z"
        :param limit:   Количество отправлений в ответе. Максимум — 50, минимум — 1.
        :param barcodes:   Штрихкоды отправления.
        :param opt_params:  status = str - Статус отправления.
                            Возможные значения для статуса: awaiting_packaging — ожидает упаковки,
                                                            not_accepted — не принят в сортировочном центре,
                                                            arbitration — ожидает решения спора,
                                                            awaiting_deliver — ожидает отгрузки,
                                                            delivering — доставляется,
                                                            driver_pickup — у водителя,
                                                            delivered — доставлено,
                                                            cancelled — отменено.
                            offset = int - Количество элементов, которое будет пропущено в ответе.
        """
        # opt_params: status = str, offset = int
        # https://api-seller.ozon.ru/apiref/ru/#t-fbs_list
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v2/posting/fbs/lis'
        # Формируем словарь для фильтра
        flt_list = {
            # Парсим дату из строки в тип datetime
            'since': parse(since, fuzzy=True),
            'to': parse(to, fuzzy=True)
        }
        # Формируем словарь для параметра 'with'
        with_list = {
            'barcodes': barcodes
        }
        # Формируем словарь для запроса
        data = {
            'dir': sort,
            'filter': flt_list,
            'limit': limit,
            'with': with_list
        }
        # В цикле добавляем необязательные параметры в flt_list и в data
        for param, value in opt_params.items():
            if param == 'status':
                flt_list[param] = value
            elif param == 'offset':
                data[param] = value

        # Возвращаем овтет в формате json
        return r.post_request(path, data).json()

    def fbs_get(self, posting_number: str):
        """Метод позволяет получить информацию об отправлении по его идентификатору.

        :param posting_number: 	Номер отправления.
        """
        # https://api-seller.ozon.ru/apiref/ru/#t-fbs_get
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v2/posting/fbs/get'

        # Формируем словарь для запроса
        data = {
            'posting_number': posting_number
        }

        # Возвращаем ответ в формате json
        return r.post_request(path, data).json()

    def fbs_unfulfilled_list(self, sort: str, limit: int, status: list, barcodes: bool, **opt_params):
        """Метод позволяет вернуть список необработанных отправлений

        :param sort: Направление сортировки: asc — по возрастанию, desc — по убыванию.
        :param limit: Количество отправлений в ответе. Максимум — 50, минимум — 1.
        :param status: Массив статусов отправлений: awaiting_packaging — ожидает упаковки,
                                                    not_accepted — не принят в сортировочном центре,
                                                    awaiting_deliver — ожидает отгрузки.
        :param barcodes: Штрихкоды отправления.
        :param opt_params: offset = int - Количество элементов, которое будет пропущено в ответе.
        """
        # opt_params: offset = int
        # http://api-seller.ozon.ru/apiref/ru/#t-fbs_unfulfilled_list
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v2/posting/fbs/unfulfilled/list'
        # Формируем словарь для параметра 'with'
        with_list = {
            'barcodes': barcodes
        }
        # Формируем словарь для запроса
        data = {
            'dir': sort,
            'limit': limit,
            'status': status,
            'with': with_list
        }
        # Добавляем необязательные параметры к data
        for param, value in opt_params.items():
            if param == 'offset':
                data[param] = value

        # Возвращаем ответ в формате json
        return r.post_request(path, data)

    def posting_fbs_ship(self, posting_number: str, items):
        """Метод делит заказ на отправления и переводит его в статус awaiting_deliver.

        :param posting_number: Номер отправления.
        :param items:   список товаров для отправления. Массив словарей вида: {"quantity": 3, "sku": 123065}, где
                        quantity: количество товара, sku: Идентификатор товара.
        """
        # http://api-seller.ozon.ru/apiref/ru/#t-fbs_ship
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v2/posting/fbs/ship'

        # Формируем массив items для параметра 'packages'
        packages = [{'items': items}]
        # Формируем словарь для запроса
        data = {
            'packages': packages,
            'posting_number': posting_number
        }

        # Возвращаем ответ в формате json
        return r.post_request(path, data).json()

    def fbs_act_create(self):
        """Метод позволяет получить предаточные документы"""
        # Акт создаётся в 3 запроса
        # http://api-seller.ozon.ru/apiref/ru/#t-section_postings_fbs_act_title
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь для отправки запроса на формирование акта
        path1 = '/v2/posting/fbs/act/create'
        # Путь для отправки запроса на проверку статуса готовности
        path2 = '/v2/posting/fbs/act/check-status'
        # Путь для получения pdf-документа с актом
        path3 = 'v2/posting/fbs/act/get-pdf'

        # Отправляем запрос для формирования акта
        create_response = r.post_request(path1, {})
        # Десериализируем json в словарь
        create_answer = json.loads(create_response.text)

        # Если ответ успешен, то добавляем в дату номер задания
        if create_response.status_code == 200:
            data = {
                'id': create_answer['result']['id']
            }
            print('Документ сформирован успешно.')
            # Отправлем запрос на проверку статуса
            check_response = r.post_request(path2, data)
            check_answer = json.loads(check_response.text)
        else:
            return create_answer
        # Если запрос на проверку успешен и документы готовы к скачиванию, то отправляем запрос на скачивание pdf
        if check_response.status_code == 200 and check_answer['result']['status'].key == 'ready':
            print('Документы сформированы и готовы для скачивания.')
            print('Номера отправлений, попавших в акт: ', check_answer['result']['added_to_act'])
            print('Номера отправлений не попавших в акт: ', check_answer['result']['removed_from_act'])
            get_pdf_response = r.post_request(path3, data)
            with open("act.pdf", "wb") as code:
                code.write(get_pdf_response.content)
        else:
            return check_answer

    def fbs_package_label(self, posting_number):
        """Метод позволяет сгенерировать pdf-файл с маркировкой.

        :param posting_number:  Номер отправления или массив номеров.
        :return: pdf-файл
        Возможная ошибка: POSTINGS_NOT_READY — отправление не готово к маркировке, повторите попытку позже.
        """
        # http://api-seller.ozon.ru/apiref/ru/#t-fbs_package_label
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v2/posting/fbs/package-label'
        # Массив для номеров отправлений
        posting_list = []
        # Формируем словарь для запроса
        data = {}
        # Если отправили 1 номер, то отправляем его к массиву. Добавляем массив к data
        if type(posting_number) == str:
            posting_list.append(posting_number)
            data['posting_number'] = posting_list
        # Иначе: Сразу добавляем полученный массив к data
        else:
            data['posting_number'] = posting_number

        # Отправляем запрос на сервер
        response = r.post_request(path, data)
        # Если запрос успешен, скачиваем файл
        if response.status_code == 200:
            with open("fbs_label.pdf", "wb") as code:
                code.write(response.content)
            return 'Файл с маркировкой получен'
        # Иначе: Возвращаем код ошибки
        else:
            answer = json.loads(response.text)
            return answer['error']['code']

    def fbs_arbitration(self, posting_number):
        """Метод позволяет открыть спор

        :param posting_number: Номер отправления или массив номеров.
        """
        # http://api-seller.ozon.ru/apiref/ru/#t-fbs_package_label
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v2/posting/fbs/arbitration'
        # Массив номеров отправлений
        posting_list = []

        # Формируем словарь для запроса
        data = {}
        # Если послали один номер, добавляем его к массиву номеро. Затем добавляем posting_list к data
        if type(posting_number) == str:
            posting_list.append(posting_number)
            data['posting_number'] = posting_list
        # Иначе: Сразу добавляем полученный массив к data
        else:
            data['posting_number'] = posting_number

        # Отправляем запрос
        response = r.post_request(path, data)
        # Десириализуем ответ
        answer = json.loads(response.text)

        return answer['result']

    def fbs_awaiting_delivery(self, posting_number):
        """Метод позволяет передать спорные отправление к отгрузке.

        :param posting_number: Номер отправления или массив номеров.
        """
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v2/posting/fbs/awaiting-delivery'
        # Массив номеров отправлений
        posting_list = []
        # Формируем словарь для запроса
        data = {}
        # Если дали 1 номер, то добавляем его в posting_list. Затем Posting_list добавляем к Data
        if type(posting_number) == str:
            posting_list.append(posting_number)
            data['posting_number'] = posting_number
        # Иначе, сразу добавляем полученный массив к data
        else:
            data['posting_number'] = posting_number

        # Отправляем запрос
        response = r.post_request(path, data)
        # Десириализуем ответ
        answer = json.loads(response.text)

        return answer['result']

    def fbs_cancel(self, cancel_reason_id: int, posting_number: str, cancel_reason_message=''):
        """Метод позволяет отменить отправление

        :param cancel_reason_id:    Идентификатор причины отмены:   352 — товар закончился,
                                                                    400 — остался только товар с недостатками,
                                                                    402 — другая прична.
        :param posting_number: Номер отправления
        :param cancel_reason_message: Дополнительная информация по отмене.
        """
        # http://api-seller.ozon.ru/apiref/ru/#t-fbs_cancel_title
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляетс к хосту для запроса
        path = '/v2/posting/fbs/cancel'

        # Формируем словарь для запроса
        data = {
            'cancel_reason_id': cancel_reason_id,
            'posting_number': posting_number
        }
        # Добавляем необязательный параметр
        if not cancel_reason_message:
            data['cancel_reason_message'] = cancel_reason_message

        # Отправляем запрос
        response = r.post_request(path, data)
        # Десириализуем ответ
        answer = json.loads(response.text)

        return answer['result']

    def fbs_cancel_reason(self):
        """Метод позволяет вернуть список причин отмены отправлений"""
        # http://api-seller.ozon.ru/apiref/ru/#t-fbs_cancel_title
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v2/posting/fbs/cancel-reason/list'
        data = {}
        # Возвращаем ответ в формате json
        return r.post_request(path, data).json()

    #  Блок "Отправления со склада OZON
    def fbo_list(self, sort: str, since: str, to: str, limit: int, **opt_params):
        """Метод позволяет получить список отправлений со склада Ozon за указанные период.

        :param sort:    Направление сортировки: asc — по возрастанию, desc — по убыванию.
        :param since:   Начало периода. Строка вида "2020-03-01T07:14:11.897Z"
        :param to:      Конец периода. Строка вида "2020-03-01T07:14:11.897Z"
        :param limit:   Количество отправлений в ответе. Максимум — 50, минимум — 1.
        :param opt_params:  status = str - Статус отправления:  awaiting_approve — ожидает подтверждения,
                                                                awaiting_packaging — ожидает упаковки,
                                                                awaiting_deliver — ожидает отгрузки,
                                                                delivering — доставляется,
                                                                driver_pickup — у водителя,
                                                                delivered — доставлено,
                                                                cancelled — отменено.
                            offset = int - Количество элементов, которое будет пропущено в ответе.
        """
        # http://api-seller.ozon.ru/apiref/ru/#t-fbo_list_title
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v2/posting/fbo/list'

        # Формируем словарь для параметра 'filter'
        filter_list = {
            # Парсим обе даты из str в datetime
            'since': parse(since, fuzzy=True),
            'to': parse(to, fuzzy=True)
        }
        # Формируем словарь для запроса
        data = {
            'dir': sort,
            'filter': filter_list,
            'limit': limit
        }
        # В цикле добавляем необязательные параметры к data
        for param, value in opt_params.items():
            data[param] = value

        # Возвращаем ответ в формате json
        return r.post_request(path, data).json()

    def fbo_get(self, posting_number: str):
        """Метод позволяет получить информацию об отправлении со склада Ozon по его идентификатору.

        :param posting_number:  Номер отправления.
        """
        # http://api-seller.ozon.ru/apiref/ru/#t-fbo_list_title
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v2/posting/fbo/get'

        # Формируем словарь для запроса
        data = {
            'posting_number': posting_number
        }

        # Возвращаем ответ в формате json
        return r.post_request(path, data).json()

    # Блок "Отправления из-за рубежа
    def crossborder_list(self, sort: str, since: str, to: str, limit: int, status='', **offset):
        """Метод позволяет получить список отправлений из-за рубежа за указанные период.

        :param sort:    Направление сортировки: asc — по возрастанию, desc — по убыванию.
        :param since:   Начало периода. Строка вида "2020-03-01T07:14:11.897Z"
        :param to:      Конец периода. Строка вида "2020-03-01T07:14:11.897Z"
        :param limit:   Количество отправлений в ответе. Максимум — 50, минимум — 1.
        :param status:  Статус отправления:  awaiting_approve — ожидает подтверждения,
                                             awaiting_packaging — ожидает упаковки,
                                             awaiting_deliver — ожидает отгрузки,
                                             delivering — доставляется,
                                             driver_pickup — у водителя,
                                             delivered — доставлено,
                                             cancelled — отменено.
        :param offset = int - Количество элементов, которое будет пропущено в ответе.
        """
        # даты отправляются строкой вида: "2020-03-01T07:14:11.897Z"
        # http://api-seller.ozon.ru/apiref/ru/#t-cb_list
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v2/posting/crossborder/list'

        # Формируем словарь для параметра 'filter'
        filter_list = {
            # Парсим строки в формат datetime
            'since': parse(since, fuzzy=True),
            'to': parse(to, fuzzy=True)
        }
        # Добавляем необязательный параметр к filter_list
        if not status:
            filter_list['status'] = status
        # Формируем словарь для запроса
        data = {
            'dir': sort,
            'filter': filter_list,
            'limit': limit,
        }
        # В цикле добавляем необязательные параметры к data
        for param, value in offset.items():
            data[param] = value

        # Посылаем запрос
        response = r.post_request(path, data)
        # Десириализуем ответ
        answer = json.loads(response.text)
        # Если запрос успешен, то возвращаем ответ в формате json
        if response.status_code == 200:
            return response.json()
        # Иначе, отправляем код http ошибки и код ошибки в ответе
        else:
            return_answer = str(response.status_code) + ' ' + answer['error']['code']
            return return_answer

    def crossborder_get(self, posting_number: str):
        """Метод позволяет вернуть информаци об отправлении из-за рубежа.

        :param posting_number:  Номер отправления.
        """
        # http://api-seller.ozon.ru/apiref/ru/#t-cb_get
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v2/posting/crossborder/get'

        # Формируем словарь для запроса
        data = {
            'posting_number': posting_number
        }
        # Отправляем запрос
        response = r.post_request(path, data)
        # Если запрос успешен, то возвращаем ответ в формате json
        if response.status_code == 200:
            return response.json()
        # Иначе, возвращаем код http ошибки и код ошибки в ответе
        else:
            answer = json.loads(response.text)
            return_answer = str(response.status_code) + ' ' + answer['error']['code']
            return return_answer

    def crossborder_unfulfilled_list(self, sort: str, limit: int, offset: int, status):
        """Возвращает список отправлений из-за рубежа, которые готовы к сборке.

        :param sort:    Направление сортировки: asc — по возрастанию, desc — по убыванию.
        :param limit:   Количество отправлений в ответе. Максимум — 50, минимум — 1.
        :param offset:  Количество элементов, которое будет пропущено в ответе.
        :param status:  Статус отправления:  awaiting_approve — ожидает подтверждения,
                                             awaiting_packaging — ожидает упаковки,
                                             awaiting_deliver — ожидает отгрузки,
                                             delivering — доставляется,
                                             driver_pickup — у водителя,
                                             delivered — доставлено,
                                             cancelled — отменено.
        """
        # http://api-seller.ozon.ru/apiref/ru/#t-cb_unfulfilled_list
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавялется к хосту для запроса
        path = '/v2/posting/crossborder/unfulfilled/list'
        # Массив для списка статусов отправлений
        status_list = []
        # Формируем словарь для запроса
        data = {
            'dir': sort,
            'limit': limit,
            'offset': offset
        }
        # Если параметр статус одиночный, то добавляем его в массив. Затем добавляем массив к data
        if type(status) == str:
            status_list.append(status)
            data['status'] = status_list
        # Иначе, сразу добавляем массив статусов к data
        else:
            data['status'] = status

        # Возвращаем ответ в формате json
        return r.post_request(path, data).json()

    def crossborder_ship(self, items, posting_number: str, shipping_provider_id: int, track_number=str):
        """Метод позволяет собрать заказ для отправления из-за рубежа.

        :param items: список товаров для отправления. Массив словарей вида: {"quantity": 3, "sku": 123065}, где
                      quantity: количество товара, sku: Идентификатор товара.
        :param posting_number:  Номер отправления.
        :param shipping_provider_id:    Идентификатор службы доставки.
        :param track_number:    Трек-номер отправления.
        :return:
        """
        # http://api-seller.ozon.ru/apiref/ru/#t-cb_ship
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v2/posting/crossborder/ship'
        # массив товаров
        items_list = []
        # Формируем словарь для запроса
        data = {
            'posting_number': posting_number,
            'shipping_provider_id': shipping_provider_id,
            'tracking_number': track_number
        }
        # Если товары переданы в виде словаря, добавляем словарь в массив. Затем, добавляем массив к data
        if type(items) == dict:
            items_list.append(items)
            data['items'] = items_list
        # Иначе, добавляем полученный массив items к data
        else:
            data['items'] = items

        # Отправляем запрос
        response = r.post_request(path, data)
        # Десириализуем ответ
        answer = json.loads(response.text)
        # Если запрос успешен, возвращаем значение package_number
        if response.status_code == 200:
            return answer['result']['package_number']
        # Иначе: Возвращаем код ошибки
        else:
            return answer['error']['code']

    def crossborder_approve(self, posting_number: str):
        """Метод переводит отправление в статус awaiting_for_packaging — подтверждено и ожидает упаковку.

        :param posting_number: Номер отправления
        """
        # http://api-seller.ozon.ru/apiref/ru/#t-cb_approve
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавялется к хосту для запроса
        path = '/v2/posting/crossborder/approve'

        # Формируем словарь для запроса
        data = {
            'posting_number': posting_number
        }

        # Посылаем запрос
        response = r.post_request(path, data)
        # Десириализуем ответ
        answer = json.loads(response.text)
        # Если запрос успешен, возвращаем значение результата ('true', 'false')
        if response.status_code == 200:
            return answer['result']
        # Иначе: Возвращаем код ошибки
        else:
            return answer['error']['code']

    def crossborder_cancel(self, cancel_reason_id: int, posting_number: str, cancel_message='', **sku):
        """Метод позволяет отменить весь заказ или отдельные товары по их идентификатору.

        :param cancel_reason_id:    Идентификатор причины отмены:   352 — товар закончился,
                                                                    400 — остался только товар с недостатками,
                                                                    402 — другая прична.
        :param posting_number:  Номер отправления.
        :param cancel_message:  Дополнительная информация по отмене. Если cancel_reason_id=402, параметр обязательный.
        :param sku: Список идентификаторов товаров в отправлении.
        :return:
        """
        # http://api-seller.ozon.ru/apiref/ru/#t-cb_cancel
        r = Request_client(self.host, self.client_id, self.apikey)
        # Путь, который добавляется к хосту для запроса
        path = '/v2/posting/crossborder/cancel'

        # массив идентификаторов товаров для отправления
        sku_list = []
        # Формируем словарь для запроса
        data = {
            'cancel_reason_id': cancel_reason_id,
            'posting_number': posting_number
        }
        # Добавляем необязательные параметры к data
        if not cancel_message:
            data['cancel_reason_message'] = cancel_message
        for param, value in sku.items():
            # Если идентификатор sku один, то добавляем его в массив. Затем массив добавляем в data.
            if type(value) == int:
                sku_list.append(value)
                data[param] = sku_list
            # Если передали sku, как массив, то добавляем его сразу в data.
            else:
                data[param] = value

        # Отправляем запрос
        response = r.post_request(path, data)
        # Десириализуем ответ
        answer = json.loads(response.text)
        # Если запрос успешный, возвращаем значение результата
        if response.status_code == 200:
            return answer['result']
        # Иначе, возвращаем код ошибки
        else:
            return answer['error']['code']
