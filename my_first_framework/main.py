import quopri

from my_first_framework.requests import PostRequests, GetRequests
from views import PageNotFound404


class MyFirstFramework:
    """Класс MyFirstFramework - основа фреймворка"""

    def __init__(self, routes_objects, fronts_objects):
        self.routes_lst = routes_objects
        self.fronts_lst = fronts_objects

    def __call__(self, environ, start_response):
        # получаем адрес, по которому выполнен переход
        # print(environ)
        path = environ['PATH_INFO']
        # находим нужный контроллер
        # отработка паттерна page controller
        # добавляем слеш, если его забыли прописать
        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        # определяем тип запроса (GET, POST)
        method = environ['REQUEST_METHOD']
        # вносим данные в словарь запросов
        request['method'] = method
        # print(f'словарь типов запроса {request}')

        if method == 'POST':
            data = PostRequests().post_request_params(environ)
            request['data'] = data
            print(f'Данные из post-запроса: '
                  f'{MyFirstFramework.decode_value(data)}')
        if method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            request_params = MyFirstFramework.decode_value(request_params)
            request['request_params'] = request_params
            print(f'Нам пришли GET-параметры: {request_params}')

        # отработка паттерна page controller
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()

        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # отработка паттерна front controller
        for front in self.fronts_lst:
            front(request)
        # print(f'общий словарь с FC {request}')
        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        """метод, приводящий словарь с post параметрами к корректному виду"""
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data


# Новый вид WSGI-application.
# Первый — логирующий (такой же, как основной, только для каждого запроса
# выводит информацию (тип запроса и параметры) в консоль.
class DebugApplication(MyFirstFramework):
    """
    Класс DebugApplication - фреймворк с дополнением в
    виде словаря с параметрами
    """

    def __init__(self, routes_objects, fronts_objects):
        self.application = MyFirstFramework(routes_objects, fronts_objects)
        super().__init__(routes_objects, fronts_objects)

    def __call__(self, env, start_response):
        print('DEBUG MODE')
        print(env)
        return self.application(env, start_response)


# Новый вид WSGI-application.
# Второй — фейковый (на все запросы пользователя отвечает:
# 200 OK, Hello from Fake).
class FakeApplication(MyFirstFramework):
    """Класс FakeApplication - фиктивный фреймворк"""

    def __init__(self, routes_objects, fronts_objects):
        self.application = MyFirstFramework(routes_objects, fronts_objects)
        super().__init__(routes_objects, fronts_objects)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']
