from urls import routes, fronts
from views import PageNotFound404


class MyFirstFramework:
    """Класс MyFirstFramework - основа фреймворка"""

    def __init__(self, routes_objects, fronts_objects):
        self.routes_lst = routes_objects
        self.fronts_lst = fronts_objects

    def __call__(self, environ, start_response):
        # получаем адрес, по которому выполнен переход
        path = environ['PATH_INFO']
        # находим нужный контроллер
        # отработка паттерна page controller
        # добавляем слеш, если его забыли прописать
        if path[-1] != '/':
            path = path + '/'
        # отработка паттерна page controller
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()

        request = {}
        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # отработка паттерна front controller
        for front in self.fronts_lst:
            front(request)
        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]


application = MyFirstFramework(routes, fronts)
