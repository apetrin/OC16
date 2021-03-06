import datetime


class ControllerException(Exception):

    def header(self):
            return ""

    @staticmethod
    def ender():
        return ""

    def message(self):
        return self.info

    def __init__(self, message="", **kwargs):
        super().__init__(**kwargs)
        self.info = message

    @property
    def full_message(self):
        return self.header() + self.message() + self.ender()

    def __str__(self):
        return self.full_message


class CheckerException(ControllerException):
    pass


class CheckIsFalse(CheckerException):
    pass


class BadSeat(CheckerException):
    pass


class EndLoopException(CheckerException):
    pass


class NoFreeAuditory(CheckerException):
    pass


class UserErrorException(ControllerException):
    lg = "debug.txt"
    situation = "Основное исключение"

    def __init__(self, fact=None, req=None, name=None, aud=None):
        self.current = fact
        self.expected = req
        self.test_name = name
        self.audname = aud

    def header(self):
        line = """
{sit: ^40}
Дата: {date}

    Возникло при тесте: {where}
        На листе {aud}

""".format(date=datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"),
           sit=self.situation,
           where=self.test_name,
           aud=self.audname)
        return line

    def message(self):
        mes = "Возникло {0}".format(type(self).__name__)
        return mes

    @staticmethod
    def ender():
        return """
Без указанных требований выполнение программы невозможно


"""

    def log_error(self):
        with open(self.lg, "a") as log:
            log.write(self.header())
            log.write(self.message())
            log.write(self.ender())


class NotEnoughSettings(UserErrorException):
    def __init__(self, way=">=", **kwargs):
        super().__init__(**kwargs)
        self.way = way
    situation = "Недостаточно входных данных"

    def message(self):
        mes = """
Дополнительная информация

        Ожидается: {exp}
        Получено:  {cur}

        Разность между входными и ожидаемыми: {ce}
        Разность между ожидаемыми и входными: {ec}

Учитывая операции над множествами нужно добиться:
               Входные {way} Необходимые
""".format(exp=self.expected,
           cur=self.current,
           ce=self.current - self.expected,
           ec=self.expected - self.current,
           way=self.way)
        return mes


class ValuesConditionException(UserErrorException):
    situation = "Входные данные не допустимы"

    def message(self):
        mes = "{0: <16}{1: <8}{2: <25}{3:<10}\n".format("Переменная", "Значение", "Условие", "Выполнение")
        mes += "+" + "-"*16 + "+" + "-"*8 + "+" + "-"*25 + "+" + "-"*10 + "+\n"
        for f in self.current:
            mes += "{0: <16}{1: <8}{2: <25}{3: <10}\n".format(str(f),
                                                                   str(self.current[f]),
                                                                   str(self.expected.get(f)),
                                                                   str(self.expected.get(f)(self.current[f])))
            mes += "+" + "-"*16 + "+" + "-"*8 + "+" + "-"*25 + "+" + "-"*10 + "+\n"
        return mes


class WrongMatrixInputException(UserErrorException):
    situation = "Неправильный матричный ввод"
    problem = "Неправильное представление"

    def solution(self):
        return "Проверьте, все ли необходимые условия выполнены"

    def message(self):
        mes = """
Дополнительная информация

       Описание проблемы:
           {problem}

       Возможное решение:
           {solution}
""".format(problem=self.problem,
           solution=self.solution())
        return mes


class NansInMatrixException(WrongMatrixInputException):
    problem = "Есть отсутствующие значения"

    def solution(self):
        return "Проверьте, все ли ячейки заполнены"


class WrongShapeException(WrongMatrixInputException):
    problem = "Неправильная размерность матрицы"

    def solution(self):
        solv = """Поменяйте размерность матрицы
           Ожидаемая размерность: {exp}
           Текущая размерность:   {cur}
""".format(exp=self.expected,
            cur=self.current,
            problem=self.problem)
        return solv
