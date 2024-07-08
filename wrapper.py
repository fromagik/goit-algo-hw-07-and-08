import sqlite3 #Імпортував модуль для роботи з БД

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError: # Якщо номер не передається то викликається виняток
            print("Give me name and phone please.")
        except IndexError: # Якщо передано більше аргументів ніж очікувалось
            print("Incorect number of arguments")
        except TypeError: # Перевірка на існування контакту або заповнення таблиці
            print('Contact not found')
        except sqlite3.IntegrityError: # Виняток що повертається коли контакт вже існує 
            print('Contact exist')


    return inner