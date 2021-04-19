class GetRequests:
    """класс обработки GET запросов"""

    @staticmethod
    def parse_input_data(data: str):
        """метод парсинга входящих данных - на выходе получаем словарь"""
        # данные соберём в словарь
        result = {}
        if data:
            # делим параметры через &
            params = data.split('&')
            for item in params:
                # делим ключ и значение через =
                k, v = item.split('=')
                # и записываем данные в словарь
                result[k] = v
        return result

    @staticmethod
    def get_request_params(environ):
        """
        метод получающий на вход параметры запроса
        и возвращающий словарь с параметрами запроса
        """
        # получаем параметры запроса
        query_string = environ['QUERY_STRING']
        # превращаем параметры в словарь
        request_params = GetRequests.parse_input_data(query_string)
        return request_params


class PostRequests:
    """класс обработки POST запросов"""

    @staticmethod
    def parse_input_data(data: str):
        """метод парсинга входящих данных - на выходе получаем словарь"""
        # данные соберём в словарь
        result = {}
        if data:
            # делим параметры через &
            params = data.split('&')
            for item in params:
                # делим ключ и значение через =
                k, v = item.split('=')
                # и записываем данные в словарь
                result[k] = v
        return result

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        """
        метод получающий на вход данные из формы (POST)
        и возвращающий байты
        """
        # получаем длину тела
        content_length_data = env.get('CONTENT_LENGTH')
        # приводим к int
        content_length = int(content_length_data) if content_length_data else 0
        # считываем данные, если они есть
        data = env['wsgi.input'].read(
            content_length) if content_length > 0 else b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        """
        метод декодирующий данные из байт (в post запросах данные в байтах)
        и возвращающий словарь параметров запроса
        """
        result = {}
        if data:
            # декодируем данные
            data_str = data.decode(encoding='utf-8')
            # собираем их в словарь
            result = self.parse_input_data(data_str)
        return result

    def post_request_params(self, environ):
        """
        метод, возвращающий словарь с параметрами POST запроса
        """
        # получаем данные
        data = self.get_wsgi_input_data(environ)
        # превращаем данные в словарь
        data = self.parse_wsgi_input_data(data)
        return data
