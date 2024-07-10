from collections import UserDict #імпортуємо модуль
from datetime import datetime, date, timedelta

class Field:  #Клас що використовується для базовий клас для зберігання та обробки імя та номеру
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)
        

class Name(Field): # Клас що використовується для сберігання та обробки імені контакта
    def __init__(self, value):
        self.value = value
        super().__init__(value)


class Phone(Field): # Клас що використовується для сберігання та обробки номеру контакта
    def __init__(self, phone_number:str):
        if not phone_number.isdigit() or len(phone_number) != 10: # Перевірка на правельний запис номеру, викликає виняток 
            raise ValueError("Номер телефону має складатися з 10 цифр\nі містити лише цифри.")
        super().__init__(phone_number)


class Birthday(Field): # Клас для збереження дня народження
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date() 
            super().__init__(self.value.strftime("%d.%m.%Y"))
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record: # Клас що використовується для роботи з контактом
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        
    def add_phone(self, phone: str) -> None:  #Метод для додавання номеру контакта 
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone: str) -> None: #Метод для видалення номеру контакта
        try:
            self.phones.remove(Phone(phone))
        except ValueError:
            print(f"Phone number {phone} not found.")

    def edit_phone(self, phone: str, new_phone:str) -> None: # Метод для зміни номеру контакта
        for numer in self.phones: # Ітеруємось по списку номерів для контакту
            if numer.value == phone: # Якщо значення відповідає вказаному номеру то присвоюється новий номер
                numer.value = new_phone
                break

    def find_phone(self, phone: str) -> str: # Метод для пошуку контакта за номером
        for numer in self.phones:
            if numer.value == phone: # Якщо значення відповідає вказаному номеру то повертається номер
                return phone 
            else: # Або викликається вийняток який вказує що номер не знайжено
                raise ValueError(f'Номер контакту "{phone}" не знайдено.')

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict): # Клас для зберігання всіх контатів 
    def __init__(self):
        self.data = {}

    def add_record(self, contact: Record) -> None: # Метод що використовується для добавлення нового контакту
        self.data[contact.name.value] = contact

    def find(self, contact:str) -> Record: # Метод що використовується для знаходження контакта та повертає інформацію про його
        return self.data.get(contact)
    
    def delete(self, contact:str) -> None: # Метод для видалення контакту з контактонї книги
        if contact.name.value in self.data:
            del self.data[contact.name.value]
        else:
            raise ValueError('Contact not found')
    
    def __string_to_date(self, date_string):
        return datetime.strptime(date_string, "%d.%m.%Y").date()
    
    def __date_to_string(self, date): # Приватний метод для перетворення дати в строку
        return date.strftime("%d.%m.%Y")

    def __find_next_weekday(self, start_date, weekday): # Приватний метод для пошуку дня(Для прикладу наступного понеділка)
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    def __adjust_for_weekend(self, birthday): # Приватний метод для перевірки чи день випадає на суботу-неділю. Якщо так повертає наступний понеділок 
        if birthday.weekday() >= 5:
            return self.__find_next_weekday(birthday, 0)
        return birthday

    def get_upcoming_birthdays(self, days=7): # Метод для повернення списку з словників всіх контактів в кого день народження через тиждень
        upcoming_birthdays = []
        today = date.today()

        for contact in self.data.values():
            birthday_date = self.__string_to_date(contact.birthday.value)
            birthday = birthday_date.replace(year=today.year)
            birthday = self.__adjust_for_weekend(birthday)
            if birthday < today: 
                birthday = birthday.replace(year=birthday.year + 1)
                birthday = self.__adjust_for_weekend(birthday)
            delta_days = (birthday - today).days
            if 0 <= delta_days <= days:    
                congratulation_date_str = self.__date_to_string(birthday)
                upcoming_birthdays.append({"name": contact.name.value, "congratulation_date": congratulation_date_str})
                
        return upcoming_birthdays

    def __iter__(self): # Метод для можливості ітерації по класу
        return iter(self.data.values())

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
    
# ТЕСТ
if __name__ == "__main__":

    book = AddressBook()

    contact1 = Record("John Doe")
    contact1.add_phone("1234567890")
    contact1.add_birthday("1990.07.19")
    book.add_record(contact1)

    contact2 = Record("Alice Smith")
    contact2.add_phone("9876543210")
    contact2.add_birthday("1992.07.10")
    book.add_record(contact2)

    upcoming_birthdays = book.get_upcoming_birthdays(7)
    print("Upcoming birthdays:")
    for birthday in upcoming_birthdays:
        print(f"{birthday['name']}: {birthday['congratulation_date']}")