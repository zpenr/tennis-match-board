class Errors(Exception):
    def __init__(self, message:str = 'Сервер столкнулся с непредвиденной внутренней ошибкой'):
        self.message = message
        self.code = 500
        self.status_code = '500 Internal Server Error'

class DBErrors(Errors):
    def __init__(self, message:str = 'Ошибка при работе с базой данных'):
        self.message = message
        self.code = 418
        self.status_code = "418 I'm a teapot"

class DBNotFound(DBErrors):
    def __init__(self, message:str = 'Запрашиваемый ресурс не найден'):
        self.message = message
        self.code = 404
        self.status_code = '404 Not Found'
        
class DBUnrecoverableError(DBErrors):
    def __init__(self, message:str = 'Ошибка в базе данных. Возможно запрос составлен некорректно'):
        self.message = message
        self.code = 456
        self.status_code = '456 Unrecoverable Error'
