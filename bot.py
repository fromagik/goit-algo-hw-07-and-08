from wrapper import *
import time
from adressbook import AddressBook, Record
import pickle

def main(): # Основна функція

    book = load_book()

    print("Welcome to the assistant bot!")
    time.sleep(2)
    print("How can I help you?")
    while True: # Основний цикл
        user_command = input('Enter you command (help to display all commands): ')
        cmd, *args = parse_input(user_command)
        if cmd in ['exit', 'close']:
            save_book(book)
            print('Goodbay!!!')
            break
        elif cmd == 'add': # Додавання контакту
            add_contact(book, args)
        elif cmd == 'change': # Зміна номеру для контакта
            change_contact(book, args)
        elif cmd == 'phone':
            get_phone(book, args) # Номер контакта
        elif cmd == 'all':
            print(get_all_contact(book))
        elif cmd == 'del':
            del_contact(book, args)
        elif cmd == 'birthday':
            add_birthday(book, args)
        elif cmd == 'show':
            get_birthday(book, args)
        elif cmd == 'upcoming':
            upcoming_birthdays(book)
        elif cmd == 'help': # Список можливих функцій
            help()
        else:
            print('Invalid command.')


def load_book(filename='adressbook.pkl'):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()
    
def save_book(book, filename='adressbook.pkl'):
    with open(filename, "wb") as file:
        pickle.dump(book, file)


def parse_input(user_input): # Парсинг введених команд користувачем
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args # Повертає команду як перший агрумент і список як решту аргументів 


@input_error
def add_contact(book, args): # Функція для добавлення контактів
    if len(args) != 2:
        raise ValueError 
    else:
        name, numer = args
        record = book.find(name)
        if record is None:
            contact = Record(name)
            contact.add_phone(numer)
            book.add_record(contact)
            print("Contact added.")
        else:
            contact.add_phone(numer)
            print('Contact updated')


@input_error
def change_contact(book, args): # Зміна номеру для контакта
    if len(args) != 3:
        raise ValueError
    if not book:
        raise ValueError
    else:
        name, number, new_number = args 
        contact = book.find(name)
        if contact:
            try:
                contact.edit_phone(number, new_number)
                print('Contact updated')
            except ValueError:
                raise ValueError('Numer contact not found')
        else:
            raise ValueError('Contact not found')

@input_error
def get_phone(book, args): # Функція для повернення номеру телефону 
    if len(args) != 1:
        raise ValueError
    else:
        numer = args[0]
        for contact in book:
            found_phone = contact.find_phone(numer)
            if found_phone:
                print(f"{contact.name}:{found_phone}")


def del_contact(book, args): # Функція для видалення контакту
    if len(args) != 1:
        raise ValueError
    name = args[0]
    contact = book.find(name)
    if contact:
        book.delete(contact)


@input_error
def add_birthday(book, args):
    # Функція для добавлення дня народження для контакту
    name, birt = args
  
    contact = book.find(name)
    if contact:
        contact.add_birthday(birt)
        print("Birthday added.")
    else:
        raise ValueError('Contact not found')
    
def get_birthday(book, args):
    name = args[0]
    contact = book.find(name)
    if contact:
        print(contact.birthday)
    

def upcoming_birthdays(book):
    # Вікно для відображення всіх днів народжння через 7 днів
    upcoming_birthdays = book.get_upcoming_birthdays(7)
    for birthday in upcoming_birthdays:
        print(f"{birthday['name']}: {birthday['congratulation_date']}")
    
@input_error
def get_all_contact(book): # Повернення всіх контактів 
    return str(book)

def help(): # Меню допомоги
    commands = """
    Commands:
    add <name> <phone> - Add a new contact
    change <name> <old_phone> <new_phone> - Change phone number for a contact
    phone <name> - Get phone numbers for a contact
    del <name> - for delete contact
    birthday <name><date birthday> - To add birthday for contact (in DD.MM.YYYY format)
    show <name> - for show birthday contact 
    upcoming - To show upcoming birthday
    all - Show all contacts
    exit, close - Exit the assistant
    """
    print(commands)


if __name__ == '__main__': #Виклик основної функції якщо імя файлу основне 
    main()