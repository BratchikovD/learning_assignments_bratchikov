class Product_Card_Client:
    """Данный класс помогает сформировать словарь для добавления товара через метод Prodcut_Update, который принадлежит
       классу Ozon_Client. С помощью методов класса Product_Card_client вы добавляете необходимые вам параметры, затем
       методом get_product_card получаете словарь с этими параметрами"""
    def __init__(self, card: dict):
        self.product_card = card

    def add_product_id(self, product_id: int):
        """Метод добавления ID продукта"""
        self.product_card['product_id'] = product_id


    def add_barcode(self, barcode: str):
        """Метод добавления Штрихкода товара"""
        self.product_card['barcode'] = barcode


    def add_description(self, description: str):
        """Метод добавления описания товара"""
        self.product_card['description'] = description

    def add_name(self, name: str):
        """Метод добавления названия товара"""
        self.product_card['name'] = name

    def add_vendor(self, vendor: str):
        """Метод добавления производителя"""
        self.product_card['vendor'] = vendor


    def add_vendor_code(self, vendor_code: str):
        """Метод добавления кода производителя"""
        self.product_card['vendor_code'] = vendor_code


    def add_height(self, height: int):
        """Метод добавления высоты упаковки"""
        self.product_card['height'] = height


    def add_depth(self, depth: int):
        """Метод добавления глубины упаковки"""
        self.product_card['height'] = depth


    def add_width(self, width: int):
        """Метод добавления ширины упаковки"""
        self.product_card['height'] = width


    def add_dimension_unit(self, unit: str):
        """Метод добавления единицы измерения габаритов"""
        self.product_card['dimension_unit'] = unit

    def add_weight(self, weight: int):
        """Метод добавления веса"""
        self.product_card['weight'] = weight

    def add_weight_unit(self, unit: str):
        """Метод добавления единицы измерения веса"""
        self.product_card['weight_unit'] = unit

    def create_image_dict(self, file_name: str, default: bool):
        """Метод создания словаря с настройками для изображения

        :param file_name: ссылка на изображение формата http:// или https://. До 1000 знаков, форматы изображения JPEG или PNG
        :param default: Признак, позволяющий установить изображение основным.
        """
        image_dict = {
            'file_name': file_name,
            'default': default
        }

        return image_dict

    def add_images(self, images):
        """Метод добавления массива изображений(не больше 10)

        :param images: словарь или массив словарей, сформированных с помощью create_image_dict
        """
        images_list = []
        if type(images) == dict:
            images_list.append(images)
            self.product_card['images'] = images_list
        elif type(images) == list:
            self.product_card['images'] = images

    def create_single_attribute(self, attribute_id: int, value: str):
        """Метод создания словаря характеристики товара с единичным значением характеристики

        :param attribute_id: Идентификатор характеристики.
        :param value: Значение характеристики
        """
        attribute_dict = {
            'id': attribute_id,
            'value': value
        }

        return attribute_dict

    def create_collection_attribute(self, attribute_id: int, collection: list):
        """Метод создания словаря характеристики товара с массивом значений

        :param attribute_id: Идентификатор характеристики
        :param collection:  Массив значений характеристики
        """
        attribute_dict = {
            'id': attribute_id,
            'collection': collection
        }

        return attribute_dict

    def create_complex_attribute(self, attribute_id: int, complex_list: list):
        """Метод создания словаря характеристики, которая поддерживает вложенные свойства

        :param attribute_id: Идентификатор характеристики
        :param complex_list: массив, состоящий из словарей, которые можно получить с помощью create_single_attribute
        :return:
        """
        attribute_dict = {
            'id': attribute_id,
            'complex': complex_list
        }

        return attribute_dict

    def create_complex_collection(self, attribute_id: int, complex_collection: list):
        """Метод создания словаря характеристики, имеющая массив характеристик с одинаковым названием, но разными знач.

        :param attribute_id: Идентификатор характеристики
        :param complex_collection: массив, состоящий из словарей характеристик с вложенными характеристиками
        """
        # Здесь complex_collection - это массив, состоящий из словарей характеристик с вложенными характеристиками
        attribute_dict = {
            'id': attribute_id,
            'complex_collection': complex_collection
        }

        return attribute_dict

    # Функция добавления характеристик в исходный словарь
    def add_attributes(self, attributes_list: list):
        """Метод добавления характеристик в исходный словарь

        :param attributes_list: массив различным словарей, полученных методами: create_single_attribute
                                                                                create_collection_attribute
                                                                                create_complex_attribute
                                                                                create_complex_collection
        """
        self.product_card['attributes'] = attributes_list


    def get_product_card(self):
        """Метод возвращает словарь с добавленными параметрами для обновления карточки товара"""
        return self.product_card
