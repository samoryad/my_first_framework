from wsgiref.simple_server import make_server

from my_first_framework.main import DebugApplication
from urls import fronts
from views import routes

# создание приложения
application = DebugApplication(routes, fronts)

# и запуск через wsgiref
with make_server('', 8010, application) as httpd:
    print("Запуск на порту 8010...")
    httpd.serve_forever()
