# -*- coding: utf-8 -*-
"""
"Balance" version 0.0.5

author: a.bezzubov
data: 26/09/2020 year

balance.py -  файл запуска консольного приложения для просмотра и редактирования базы данных записей изменений в счетах балансовых ресурсов.

1 - Информация - чтение файла info.txt;
2 - БД - база данных на экран;
3 - Добавить - добавить запись в базу данных;
4 - Удалить - удалить запись и добавить в файл archive.txt;
5 - Подробнее - чтение файла journal.txt;
6 - Архив - чтение файла archive.txt;
"""

# Реализация:
# Интерфейс командной строки с помощью инструментов интроспекции Python.
# Структура - смотри паттерн MVVM.
# Смотри по коду комментарий #NEW Commands для добавления новых команд

import sys
import os
import time
import locale # модуль для выхода на локаль
from abc import ABC, abstractmethod
import shelve
from prettytable import PrettyTable, from_csv

class Intro(object):
    """
    Класс "О приложении" с возможностью вывода текущей даты и времени
    "О приложении" с наименованием версии
    a = Intro()
    print(a.today_time())
    """
    def __init__(self, version ='Альфа версия приложения "balance v.0.0.5"\n'):
        self.version = version

    def __str__(self):
        return self.version

    def today_time(self):
        locale.setlocale(locale.LC_ALL, "Russian_Russia.1251")
        self._s = "Сегодня:\n%A %d %b %Y %H:%M:%S\n%d.%m.%Y"
        return time.strftime(self._s)

class Active_030A_(object):
    """
    Реализация класса счёта -030A- с данными
    """
    def __init__(self, score='', name='', course=0, amount=0, criterion=0, data = '', remark=None):
        self.score = score
        self.name = name
        self.course = course
        self.amount = amount
        self.criterion = criterion
        self.data = data
        self.remark = remark

    def __repr__(self):
        return ('{},\t{},\t{},\t{},\t{},\t{},\t{}'.format(self.score, self.name, self.course, self.amount, self.criterion, self.data, self.remark))

class New_object(object):  # new_object = New_object()
    """
    Обычно метакласс переопределяет метод __new__ или __init__ класса type,
    с целью взять на себя управление созданием или инициализацией нового
    объекта класса. Как и при использовании декораторов классов,
    суть состоит в том, чтобы определить программный код, который будет
    вызываться автоматически на этапе создания класса. Оба способа позволяют
    расширять классы или возвращать произвольные объекты
    для его замены – протокол с практически неограниченными возможностями.
    """
    obj = None
    items = None

    @classmethod
    def __new__(cls, *args):
        if cls.obj is None:
            cls.obj = object.__new__(cls)
            cls.items = []
        return cls.obj

class BaseCommand(ABC):
    """
    Абстрактным базовым классом (Abstract Base Class, ABC) называется
    класс, который не может использоваться для создания объектов.
    Назначение таких классов состоит в определении интерфейсов, то есть
    в том, чтобы перечислить методы и свойства, которые должны быть
    реализованы в классах, наследующих абстрактный базовый класс. Это
    удобно, так как можно использовать абстрактный базовый класс как
    своего рода договоренность - договоренность о том, что любые
    порожденные классы обеспечат реализацию методов и свойств, объявленных
    в абстрактном базовом.
    """
    @abstractmethod
    def label()->str:
        """
        Наименование команды
        :return: str
        """
        pass

    def perform(self, object, *args, **kwargs):
        """
        Выполняемые инструкции
        """
        pass

class Interface_cmd(object):
    """
    Класс запуска интерфейса командной строки
    Пример:
    run = Interface()
    run.main()
    """
    def user_input(self):
        """
        Пользовательский ввод input()
        # Наименование команд из класса 'dict_keys'
        :return: str
        """
        message = '\n{}: '.format('|'.join(
            {
                HelpCommand.label(): HelpCommand,
                InfoCommand.label(): InfoCommand,
                ScoreCommand.label(): ScoreCommand,
                AddCommand.label(): AddCommand,
                DelCommand.label(): DelCommand,
                NoteCommand.label(): NoteCommand,
                ArchiveCommand.label(): ArchiveCommand,
                ExitCommand.label(): ExitCommand,
                #NEW Commands

            }.keys()
        ))
        return input(message)

    def lst_commands(self):
        """
        Определение команд
        :return: словарь со значением {input_function(message) : class}
        """
        return {
            'help': HelpCommand,
            '1': InfoCommand,
            '2': ScoreCommand,
            '3': AddCommand,
            '4': DelCommand,
            '5': NoteCommand,
            '6': ArchiveCommand,
            'exit': ExitCommand,
            #NEW Commands
        }

    def perform_command(self, command):
        """
        Выполнение команды по наименованию.
        Сохраняет результат в 'New_object()'.
        """
        try:
            command = command.lower()
            routes = self.lst_commands()
            command_class = routes[command]
            command_inst = command_class()
            new_object = New_object()
            command_inst.perform(new_object.items)
        except KeyError:
            print('Неправильная команда, попробуйте снова!!!')

    def main(self):
        """
        Запуск
        """
        while True:
            try:
                command = self.user_input()
                assert command != ''
                self.perform_command(command)
            except KeyboardInterrupt:
                print('Выход...')
                break
            except UserExitException:
                print('Выход...')
                break
            except AssertionError:
                pass
            except Exception:
                print('Здесь пока ничего, проверьте файл log.txt на отсутствие записей о вызовах исключений')
                """
                Дополнительная информация об исключении
                """
                print(time.ctime(), sys.exc_info()[:2], file=open('log.txt', 'a'))

class UserExitException(Exception): pass

###############################################################################
# NEW_COMMANDs
###############################################################################

class InfoCommand(BaseCommand):
    """
    Класс команды "1"
    """

    file = open('info.txt', 'a')
    file.close()

    def label()->str:
        """
        Функция с наименованием команды
        :return: str
        """
        return 'Информация-"1"'

    def perform(self, objects, *args, **kwargs):
        """
        Чтение файла формата .txt с общей информацией
        """
        file = 'info.txt'
        numlines = 30
        text = open(file, encoding='utf-8').read()
        lines = text.splitlines() # подобно split('\n'), но без '' в конце
        while lines:
            chunk = lines[:numlines]
            lines = lines[numlines:]
            for line in chunk: print(line)
            if lines and input('Далее-->') not in ['']: break

class ScoreCommand(BaseCommand):
    """
    Класс команды "2"
    """
    def label()->str:
        """
        Функция с наименованием команды
        :return: str
        """
        return 'БД - "2"'

    def perform(self, objects, *args, **kwargs):
        """
        База данных на экран
        """
        file = 'temp.csv'
        field_names = ['Ключ,', 'Счёт,', 'Наименование,', 'Курс,', 'Кол-во,', 'Критерий,', 'Дата,', 'Примечание\n']
        db = shelve.open('vlt_shelve')
        fp = open(file, 'w+')
        fp.writelines(field_names)
        for key in db:
            fp.writelines(str(key) + ',' + str(db[key].score) + ',' + str(db[key].name) +
                    ',' + str(db[key].course) + ',' + str(db[key].amount)  +
                    ',' + str(db[key].criterion) + ',' + str(db[key].data) + ',' + str(db[key].remark) + '\n')
        fp.close()
        db.close()
        with open(file, 'r') as f:
            x = from_csv(f)
            print(x)
        os.remove(file)

class AddCommand(BaseCommand):
    """
    Класс команды "3"
    """
    def label()->str:
        """
        Функция с наименованием команды
        :return: str
        """
        return 'Добавить-"3"'

    def perform(self, objects, *args, **kwargs):
        """
        Добавление и редактирование записей БД
        """
        fieldnames = ('score', 'name', 'course', 'amount', 'criterion', 'data', 'remark')
        maxfield = max(len(f) for f in fieldnames)
        db = shelve.open('vlt_shelve')
        while True:
            try:
                key = input('\nНаименование ключа? -> ') # ключ или пустая строка
                if not key: break
                if key in db:
                    print('Внимание!!!Замена существующей записи!!!')
                    if input('\nВы действительно хотите продолжить?(y/n)') == 'y':
                        record = db[key] # изменить существующую запись
                    else:
                        break
                else: # или создать новую запись
                    record = Active_030A_(score = ' Номер счёта', name = ' Наименование актива', course = ' Курс покупки', amount = ' Кол-во', criterion = ' Критерий продажи', data = ' Дата покупки', remark = ' Примечание')
                for field in fieldnames:
                    currval = getattr(record, field)
                    newtext = input('\t[%s] = %s\n\t\tНовая запись-> ' % (field, currval))
                    if newtext:
                        setattr(record, field, eval(newtext))
                    db[key] = record

            except (NameError, TypeError, SyntaxError):
                print('Используйте кавычки при вводе строковых данных ...попробуйте еще раз...')
                continue
                db.close()

class DelCommand(BaseCommand):
    """
    Класс команды "4"
    """

    file = open('archive.txt', 'a')
    file.close()

    def label()->str:
        """
        Функция с наименованием команды
        :return: str
        """
        return 'Удалить-"4"'

    def perform(self, objects, *args, **kwargs):
        """
        Удаление записи по ключу
        """
        db = shelve.open('vlt_shelve')
        if input('\nВы действительно хотите удалить запись?(y/n): ') == 'y':
            n = input("Введите ключ для удаления: ")
            for key in db:
                if n in db:
                    print(db[n], file=open('archive.txt', 'a'))
                    del db[n]
                    print("Протокол итерации ... Запись удалена")
                else:
                    print("Протокол итерации ... ключа {} не существует".format(str(n)))
        db.close()

class NoteCommand(BaseCommand):
    """
    Класс команды "5"
    """

    file = open('journal.txt', 'a')
    file.close()

    def label()->str:
        """
        Функция с наименованием команды
        :return: str
        """
        return 'Подробнее-"5"'

    def perform(self, objects, *args, **kwargs):
        """
        Чтение файла журнала формата .txt
        """
        file = 'journal.txt'
        numlines = 30
        text = open(file, encoding='utf-8').read()
        lines = text.splitlines() # подобно split('\n'), но без '' в конце
        while lines:
            chunk = lines[:numlines]
            lines = lines[numlines:]
            for line in chunk: print(line)
            if lines and input('Далее-->') not in ['']: break

class ArchiveCommand(BaseCommand):
    """
    Класс команды "6"
    """

    def label()->str:
        """
        Функция с наименованием команды
        :return: str
        """
        return 'Архив-"6"'

    def perform(self, objects, *args, **kwargs):
        """
        Чтение файла журнала формата .txt
        """
        file = 'archive.txt'
        numlines = 30
        text = open(file).read()
        lines = text.splitlines() # подобно split('\n'), но без '' в конце
        while lines:
            chunk = lines[:numlines]
            lines = lines[numlines:]
            for line in chunk: print(line)
            if lines and input('Далее-->') not in ['']: break

class ExitCommand(BaseCommand):
    def label():
        """
        Функция с наименованием команды
        :return: str
        """
        return 'exit'

    def perform(self, object, *args, **kwargs):
        raise UserExitException

class HelpCommand(BaseCommand):

    file = open('help.txt', 'a')
    file.close()

    def label()->str:
        """
        Функция с наименованием команды
        :return: str
        """
        return 'help'

    def perform(self, object, *args, **kwargs):
        """
        Чтение файла помощи формата .txt
        """
        file = 'help.txt'
        numlines = 30
        text = open(file).read()
        lines = text.splitlines() # подобно split('\n'), но без '' в конце
        while lines:
            chunk = lines[:numlines]
            lines = lines[numlines:]
            for line in chunk: print(line)
            if lines and input('Далее-->') not in ['']: break

#NEW Commands
###############################################################################
# END NEW_COMMANDs
###############################################################################

if __name__=='__main__':
    print(Intro().today_time()) # Дата и время
    print(__doc__) # Общая информация
    run = Interface_cmd() # экземпляр класса запуска
    run.main() # запуск
