import tkinter as tk
from adressbook import AddressBook, Record
from wrapper import input_error
from tkinter import messagebox
import pickle

class App:
    def __init__(self, root): # Ініціалізуємо додаток
        self.root = root
        self.book = self.load_book()
        self.window_param()
        self.start()

    def window_param(self):
        # очищуємо вікно
        for widget in self.root.winfo_children():
            widget.destroy()

        # Параметри вікна
        self.root.title('AddressBook')
        self.root.geometry("450x550")
        self.root.minsize(width=450, height=550)
        self.root.maxsize(width=450, height=550)
        self.root.configure(bg='white')

    def save_book(self, filename='adressbook.pkl'):
        with open(filename, "wb") as file:
            pickle.dump(self.book, file)

    def load_book(self, filename='adressbook.pkl'):
        try:
            with open(filename, "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return AddressBook()

    def start(self):
    # Стартове вікно
        self.window_param()

        welcm_label = tk.Label(self.root, text='Welcome to the assistant bot!', bg='white', fg='black', padx=5, pady=5, font=('Arial', 16))
        welcm_label.place(x=100, y=160)

        start_btn = tk.Button(self.root, text="Start", bg='white', fg='black', bd=0, highlightthickness=0, width=5, height=2, command= self.main)
        start_btn.place(x=170, y=210)

    def main(self):
        # Головне меню
        self.window_param()

        add_contact_btn = tk.Button(self.root, text='Add contact', bg='white', fg='black', bd=0, highlightthickness=0, width=12, height=2, command=self.add_contact_window)
        add_contact_btn.grid(row=1, column=0, padx=5, pady=5)
        change_btn = tk.Button(self.root, text='Change number', bg='white', fg='black', bd=0, highlightthickness=0, width=12, height=2, command=self.change_contact_window)
        change_btn.grid(row=2, column=0, padx=5, pady=5)
        birthday_btn = tk.Button(self.root, text='Add birthday', bg='white', fg='black', bd=0, highlightthickness=0, width=12, height=2, command=self.add_birthday_window)
        birthday_btn.grid(row=1, column=2, padx=5, pady=5)
        delete_btn = tk.Button(self.root, text='Delete contact', bg='white', fg='black', bd=0, highlightthickness=0, width=12, height=2, command=self.del_contact_window)
        delete_btn.grid(row=2, column=2, padx=5, pady=5)
        exit_btn = tk.Button(self.root, text='Upcoming birthdays', bg='white', fg='black', bd=0, highlightthickness=0, width=12, height=2, command=self.upcoming_birthdays)
        exit_btn.grid(row=1, column=3, padx=5, pady=5)
        exit_btn = tk.Button(self.root, text='Exit', bg='white', fg='black', bd=0, highlightthickness=0, width=12, height=2, command=self.exit_app)
        exit_btn.grid(row=2, column=3, padx=5, pady=5)

        # Створюємо Canvas для контактів з прокруткою
        self.canvas = tk.Canvas(self.root, bg='white')
        self.canvas.place(x=0, y=120, width=450, height=490)

        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.place(x=430, y=60, height=490)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.contact_frame = tk.Frame(self.canvas, bg='white')
        self.canvas.create_window((0, 0), window=self.contact_frame, anchor="nw")

        self.contact_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        # Виводимо всіх доданих контактів
        for index, contact in enumerate(self.book):
            contact_label = tk.Label(self.contact_frame, text=contact.name, bg='white', fg='black', font=('Arial', 16), bd=0, highlightthickness=0)
            contact_label.grid(row=index, column=0, padx=10, pady=5, sticky='w')
            numer_label = tk.Label(self.contact_frame, text=contact.phones, bg='white', fg='black', font=('Arial', 16), bd=0, highlightthickness=0)
            numer_label.grid(row=index, column=1, padx=10, pady=5, sticky='w')
            show_birt_btn = tk.Button(self.contact_frame, text='Show birthday', bg='white', fg='black', bd=0, highlightthickness=0, width=10, height=2, command=lambda: self.show_birthday(contact))
            show_birt_btn.grid(row=index, column=2, padx=10, pady=5)

    def add_contact_window(self):
        # Додаткове вікно з полями для вводу імені та номеру телефона
        acw = tk.Toplevel(root)
        acw.title('Add contact')
        acw.geometry("400x300")
        acw.minsize(width=400, height=300)
        acw.maxsize(width=400, height=300)
        acw.configure(bg='white')

        name_lbl = tk.Label(acw, text='Name', bg='white', fg='black', padx=5, pady=5, font=('Arial', 16), bd=0)
        phone_lbl = tk.Label(acw, text='Phone number', bg='white', fg='black', padx=5, pady=5, font=('Arial', 16), bd=0)

        x = 120
        name_lbl.place(x=x, y=20)
        phone_lbl.place(x=x, y=70)

        name_entry = tk.Entry(acw, bg='white', fg='black', bd=0, font=('Arial', 12))
        phone_entry = tk.Entry(acw, bg='white', fg='black', bd=0, font=('Arial', 12))

        name_entry.place(x=x, y=50)
        phone_entry.place(x=x, y=100)

        list_info = [name_entry, phone_entry]

        #Кнопка викликає функцію що відповідає за добавлення контакту в книгу
        add_btn = tk.Button(acw, text='Add contact', bg='white', fg='black', bd=0, highlightthickness=0, width=7, height=2, command= lambda: self.add_contact(list_info))
        add_btn.place(x=x, y= 130)

    @input_error
    def add_contact(self, args): # Функція для добавлення контактів
        name, numer = args
        name = name.get() # Отримуємо значення в вигляді строки з поля що ввів користувач
        numer = numer.get()
        record = self.book.find(name) # Шукаємо чи користувач вже існує
        if record is None: # Додаємо нового користувача якшо його не існує
            contact = Record(name)
            contact.add_phone(numer)
            self.book.add_record(contact)
            self.main() # в будь якому випадку повертаємось в головне меню
        else: # Додаємо номер телефону до вже існуючого контакту
            record.add_phone(numer)
            self.main() # +

    def change_contact_window(self):
        # Додаткове вікно з полями для вводу імені та номеру телефона
        acw = tk.Toplevel(root)
        acw.title('Change contact')
        acw.geometry("400x300")
        acw.minsize(width=400, height=300)
        acw.maxsize(width=400, height=300)
        acw.configure(bg='white')

        name_lbl = tk.Label(acw, text='Name', bg='white', fg='black', padx=5, pady=5, font=('Arial', 16), bd=0)
        phone_lbl = tk.Label(acw, text='Phone number', bg='white', fg='black', padx=5, pady=5, font=('Arial', 16), bd=0)
        new_phone = tk.Label(acw, text='New phone number', bg='white', fg='black', padx=5, pady=5, font=('Arial', 16), bd=0)

        x = 120
        name_lbl.place(x=x, y=20)
        phone_lbl.place(x=x, y=70)
        new_phone.place(x=x, y=120)

        name_entry = tk.Entry(acw, bg='white', fg='black', bd=0, font=('Arial', 12))
        phone_entry = tk.Entry(acw, bg='white', fg='black', bd=0, font=('Arial', 12))
        new_phone_entry = tk.Entry(acw, bg='white', fg='black', bd=0, font=('Arial', 12))

        name_entry.place(x=x, y=50)
        phone_entry.place(x=x, y=100)
        new_phone_entry.place(x=x, y=150)

        list_info = [name_entry, phone_entry, new_phone_entry]

        #Кнопка викликає функцію що відповідає за добавлення контакту в книгу
        add_btn = tk.Button(acw, text='Change number', bg='white', fg='black', bd=0, highlightthickness=0, width=10, height=2, command= lambda: self.change_contact(list_info))
        add_btn.place(x=x, y= 180)

    @input_error
    def change_contact(self, args): # Зміна номеру для контакта
        name, numer, new_number = args 
        name = name.get() # Отримуємо значення в вигляді строки з поля що ввів користувач
        numer = numer.get()
        new_number = new_number.get()
        contact = self.book.find(name)
        if contact:
            try:
                contact.edit_phone(numer, new_number)
                self.main()
            except ValueError:
                raise ValueError('Numer contact not found')
        else:
            raise ValueError('Contact not found')
    
    def add_birthday_window(self):
        # Додаткове вікно з полями для вводу імені та номеру телефона
        acw = tk.Toplevel(root)
        acw.title('Add birthday')
        acw.geometry("400x300")
        acw.minsize(width=400, height=300)
        acw.maxsize(width=400, height=300)
        acw.configure(bg='white')

        name_lbl = tk.Label(acw, text='Name', bg='white', fg='black', padx=5, pady=5, font=('Arial', 16), bd=0)
        birt_lbl = tk.Label(acw, text='Birthday', bg='white', fg='black', padx=5, pady=5, font=('Arial', 16), bd=0)

        x = 120
        name_lbl.place(x=x, y=20)
        birt_lbl.place(x=x, y=70)

        name_entry = tk.Entry(acw, bg='white', fg='black', bd=0, font=('Arial', 12))
        birt_entry = tk.Entry(acw, bg='white', fg='black', bd=0, font=('Arial', 12))

        name_entry.place(x=x, y=50)
        birt_entry.place(x=x, y=100)

        list_info = [name_entry, birt_entry]

        #Кнопка викликає функцію що відповідає за добавлення контакту в книгу
        add_btn = tk.Button(acw, text='Add contact', bg='white', fg='black', bd=0, highlightthickness=0, width=7, height=2, command= lambda: self.add_birtday(list_info))
        add_btn.place(x=x, y= 130)

    @input_error
    def add_birtday(self, args):
        # Функція для добавлення дня народження для контакту
        name, birt = args
        name = name.get() # Отримуємо значення в вигляді строки з поля що ввів користувач
        birt = birt.get()
        contact = self.book.find(name)
        if contact:
            contact.add_birthday(birt)
            self.main()
        else:
            raise ValueError('Contact not found')
    
    def show_birthday(self, contact):
        # Вікно для відображення дня народження кожного контакту
        acw = tk.Toplevel(root)
        acw.title('Birthday')
        acw.geometry("150x120")
        acw.minsize(width=150, height=120)
        acw.maxsize(width=150, height=120)
        acw.configure(bg='white')

        birt_lbl = tk.Label(acw, text=contact.birthday, bg='white', fg='black', padx=5, pady=5, font=('Arial', 16), bd=0)
        birt_lbl.place(x=20, y=20)

        ok_btn = tk.Button(acw, text='OK', command=acw.destroy, width=5, height=2, bd=0, highlightthickness=0)
        ok_btn.place(x=30, y=50)

        
    def del_contact_window(self):
        # Вікно для видалення контакту
        acw = tk.Toplevel(root)
        acw.title('Delete contact')
        acw.geometry("400x300")
        acw.minsize(width=400, height=300)
        acw.maxsize(width=400, height=300)
        acw.configure(bg='white')

        name_lbl = tk.Label(acw, text='Name', bg='white', fg='black', padx=5, pady=5, font=('Arial', 16), bd=0)

        x = 120
        name_lbl.place(x=x, y=20)

        name_entry = tk.Entry(acw, bg='white', fg='black', bd=0, font=('Arial', 12))

        name_entry.place(x=x, y=50)

        add_btn = tk.Button(acw, text='Delete contact', bg='white', fg='black', bd=0, highlightthickness=0, width=7, height=2, command= lambda: self.del_contact(name_entry))
        add_btn.place(x=x, y= 80)

    def upcoming_birthdays(self):
        # Вікно для відображення всіх днів народжння через 7 днів
        acw = tk.Toplevel(root)
        acw.title('Upcoming birthdays')
        acw.geometry("400x300")
        acw.minsize(width=400, height=300)
        acw.maxsize(width=400, height=300)
        acw.configure(bg='white')

        upcoming_birthdays = self.book.get_upcoming_birthdays(7)
        for birthday in upcoming_birthdays:
            birthdays_lbl = tk.Label(acw, text=f"{birthday['name']}: {birthday['congratulation_date']}", bg='white', fg='black', font=('Arial', 16), bd=0, highlightthickness=0)
            birthdays_lbl.pack()
        
        ok_btn = tk.Button(acw, text='OK', command=self.main, width=5, height=2, bd=0, highlightthickness=0)
        ok_btn.pack()

    def del_contact(self, name): # Функція для видалення контакту
        name = name.get()
        contact = self.book.find(name)
        if contact:
            self.book.delete(contact)
            self.main()

    def exit_app(self):
        # Функция для выхода из приложения
        self.save_book()
        messagebox.showinfo("Goodbye", "Goodbye")
        self.root.quit()

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()