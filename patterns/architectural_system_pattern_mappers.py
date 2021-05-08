import sqlite3

from patterns.generative_patterns import Student


class StudentMapper:
    """Класс преобразователь данных для передачи данных между объектами
     (в частности студент) и БД"""

    def __init__(self, conn):
        self.connection = conn
        self.cursor = conn.cursor()
        self.table_name = 'student'

    def all(self):
        statement = f'SELECT * from {self.table_name}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            student = Student(name)
            student.id = id
            result.append(student)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.table_name} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.table_name} SET name=? WHERE id=?"
        # Где взять obj.id? Добавить в DomainModel? Или добавить когда берем
        # объект из базы
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


connection = sqlite3.connect('patterns.sqlite')


class MapperRegistry:
    """Фабричный метод создания мэпперов (пока студента)"""
    mappers = {
        'student': StudentMapper,
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


# исключение коммита
class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


# исключение обновления
class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


# исключение удаления
class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


# исключение отсутствия данных в БД
class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')
