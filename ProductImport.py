class Product_import_client:
    """Данный класс помогает сформировать словарь для добавления товара через метод Prodcut_Import, который принадлежит
       классу Ozon_Client. С помощью методов класса Product_import_client вы добавляете необходимые вам параметры, затем
       методом get_item_list получаете словарь с этими параметрами"""
    def __init__(self, items: dict):
        self.item = items

    def create_attribute_list(self, attribute_id: int, **opt_params):
        """Метод позволяет созать словарь с нужными параметрами характеристик

        :param attribute_id:    Идентификатор характеристики.
        :param opt_params:  complex_id = int - Идентификатор характеристики, которая поддерживает вложенные свойства.
                            values: словарь или массив словарей значений вложенных характеристик.
                                    Вид словаря: {"dictionary_value_id": 0, "value": "string"}, где
                                    dictionary_value_id:    Идентификатор справочника.
                                    value:  Значение из справочника.
        """
        # Массив вложенных значений характеристик
        values_list = []

        # Словарь для характеристик
        attributes_dict = {
            'id': attribute_id
        }
        # Добавляем необязательные параметры в список
        for param, value in opt_params.items():
            # Если values словарь, то добавляем его в массив и затем в словарь характеристик
            if param == 'values' and type(value) == dict:
                values_list.append(value)
                attributes_dict[param] = values_list
            # Если values массив словарей, то добавляем его сразу в словарь характеристик
            elif param == 'values' and type(value) == list:
                attributes_dict[param] = value
            # Добавляем все осатльные параметры
            else:
                attributes_dict[param] = value

        return attributes_dict

    def add_attributes(self, attributes):
        """Метод позволяет добавить характеристику к словарю

        :param attributes: словарь или массив словарей, которые были сформированы с помощью create_attribute_list
        """
        # параметр attributes либо словарь, либо массив словарей
        attributes_list = []
        if type(attributes) == dict:
            attributes_list.append(attributes)
            self.item['attributes'] = attributes_list
        elif type(attributes) == list:
            self.item['attributes'] = attributes

    def add_barcode(self, barcode: str):
        """Метод добавляет штрихкод к параметрам

        :param barcode: Штрихкод товара.
        """
        self.item['barcode'] = barcode

    def add_category_id(self, category_id: int):
        """Метод добавляет идентификатор категории к параметрам

        :param category_id: Идентификатор категории
        """
        self.item['category_id'] = category_id

    def add_complex_attribute(self, attributes):
        """Метод позволяет добавить комплексные характеристики в параметры

        :param attributes: словарь или массив словарей, сформированных с помощью create_attribute_list
        """
        # параметр attribute либо словарь, либо массив словарей
        attributes_list = []
        if type(attributes) == dict:
            attributes_list.append(attributes)
            self.item['complex_attributes'] = attributes_list
        elif type(attributes) == list:
            self.item['complex_attributes'] = attributes

    def add_depth(self, depth: int):
        """Метод добавляет глубину упаковки к параметрам

        :param depth: глубина
        """
        self.item['depth'] = depth

    def add_dimension(self, dimension_unit: str):
        """Метод добавляет единицу измерения габаритов к параметрам

        :param dimension_unit: Единица измерения габаритов.
                               Доступные варианты: mm (миллиметры), cm (сантиметры), in (дюймы).
        """
        # Доступные значения для dimension_unit: mm(миллиметры), cm(сантиметры), in(дюймы)
        self.item['dimension_unit'] = dimension_unit

    def add_height(self, height: int):
        """Метод добавляет высоту упаковки к параметрам

        :param height: высота
        """
        self.item['height'] = height

    def add_image_group_id(self, image_group_id: str):
        """Метод добавляет идентификатор для последующей пакетной загрузки изображений

        :param image_group_id: Идентификатор для последующей пакетной загрузки изображений.
        """
        self.item['image_group_id'] = image_group_id

    def add_images(self, images):
        """Метод добавляет массив с изображениями

        :param images: массив с изображениями, количеством не больше 10
        """
        self.item['images'] = images

    def add_images_360(self, images360):
        """Метод добавляет изобржания360 к параметрам

        :param images360: массив изображений 360
        """
        self.item['images360'] = images360

    def add_name_https(self, file_name):
        """Метод добавляет ссылку на изображение в формате https

        :param file_name:
        """
        self.item['name'] = file_name

    def add_offer_id(self, offer_id: int):
        """Метод добавляет идентификатор товара в системе продавца

        :param offer_id: идентификатор товара
        """
        self.item['offer_id'] = offer_id

    def add_old_price(self, old_price: str):
        """Метод добавляет цены до скидок

        :param old_price: цена до скидок. Разделитель дробной части "." До 2-х знаков после запятой
        """
        self.item['old_price'] = old_price

    def create_pdf_dict(self, index: int, name: str, src_url: str):
        """Метод позволяет сформировать словарь для добавления pdf-файла к параметрам

        :param index:   индекс
        :param name:    название
        :param src_url: URL для pdf-файла.
        """
        pdf_dict = {
            'index': index,
            'name': name,
            'src_url': src_url
        }
        return pdf_dict

    def add_pdf_list(self, pdf):
        """Метод добавляет список pdf-файлов к параметрам

        :param pdf: словарь или массив словарей, которые были сформированы с помощью create_pdf_dict
        :return:
        """
        pdf_list = []
        if type(pdf) == dict:
            pdf_list.append(pdf)
            self.item['pdf_list'] = pdf_list
        elif type(pdf) == list:
            self.item['pdf_list'] = pdf

    def add_premium_price(self, premium_price: str):
        """Метод добавляет цену для людей Ozon_Premium

        :param premium_price: цена
        :return:
        """
        self.item['premium_price'] = premium_price

    def add_price(self, price: str):
        """Метод добавляет цену с учетом скидок

        :param price: цена
        """
        self.item['price'] = price

    # Функция добавления ставки НДС
    def add_vat(self, vat: str):
        """Метод добавляет ставку НДС к параметрам

        :param vat: Ставка НДС для товара:  0 — не облагается НДС;
                                            0.1 — 10%;
                                            0.2 — 20%.
        """
        self.item['vat'] = vat

    def add_weight(self, weight: int):
        """Метод добавляет вес товара в упаковке к параметрам.

        :param weight: вес
        """
        self.item['weight'] = weight

    def add_weight_unit(self, unit: str):
        """Метод добавляет единицу измерения веса.

        :param unit: единица измерения веса. Доступные значение unit - 'g', 'kg', 'lb'
        """
        self.item['weight_unit'] = unit

    def add_width(self, width: int):
        """Метод добавляет ширину упаковки

        :param width: ширина упакови
        """
        self.item['width'] = width

    # Функция для получения словаря товаров
    def get_item_list(self):
        """Метод возвращает готовый словарь с настройками для добавления товара"""
        return self.item
