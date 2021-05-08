import jsonpickle as jsonpickle


# поведенческий паттерн - наблюдатель
# Курс
from my_first_framework.templator import render


class Observer:
    """Класс наблюдатель"""
    def update(self, subject):
        pass


class Subject:
    """Класс конкретных наблюдателей"""
    def __init__(self):
        self.observers = set()

    def notify(self):
        # print(f'наблюдатели {self.observers}')
        obs_copy = self.observers.copy()
        student = obs_copy.pop()
        sms_notifier = SmsNotifier()
        email_notifier = EmailNotifier()
        # print(f'студент {student}')
        for el in self.observers:
            print(f'message to {el.name}')
            sms_notifier.update(student)
            email_notifier.update(student)


class SmsNotifier(Observer):
    """Класс смс уведомления"""
    def update(self, subject):
        chosen_course = subject.__dict__['courses']
        print(f'SMS -> {subject.name} присоединился на курс {chosen_course}')


class EmailNotifier(Observer):
    """Класс e-mail уведомления"""
    def update(self, subject):
        chosen_course = subject.__dict__['courses']
        print(f'EMAIL -> {subject.name} присоединился на курс {chosen_course}')


class BaseSerializer:
    """Класс сериализации"""
    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return jsonpickle.dumps(self.obj)

    @staticmethod
    def load(data):
        return jsonpickle.loads(data)


# поведенческий паттерн - Шаблонный метод
class TemplateView:
    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        # print(f'get_queryset --> {self.queryset}')
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = self.get_request_data(request)
            # print(data)
            self.create_obj(data)

            return self.render_template_with_context()
        else:
            return super().__call__(request)


# поведенческий паттерн - Стратегия
class ConsoleWriter:

    def write(self, text):
        print(f'ConsoleWriter {text}')


class FileWriter:

    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')
