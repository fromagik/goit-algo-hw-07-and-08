import tkinter as tk
from adressbook import AddressBook, Record
from wrapper import input_error

class App:
    def __init__(self, root):
        self.root = root
        self.book = AddressBook()
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
    
    def start(self):
    # Главное окно 
        self.window_param()

        # Ініціалізація тексту 
        welcm_label = tk.Label(self.root, text='Welcome to the assistant bot!', bg='white', fg='black', padx=5, pady=5, font=('Arial', 16))
        welcm_label.place(x=100, y=160)

        start_btn = tk.Button(self.root, text="Start", bg='white', fg='black', bd=0, highlightthickness=0, width=5, height=2, command= self.main)
        start_btn.place(x=170, y=210)

    def main(self):
        self.window_param()

        add_contact_btn = tk.Button(self.root, text='Add contact', bg='white', fg='black', bd=0, highlightthickness=0, width=7, height=2, command= self.add_contact_window)
        add_contact_btn.place(x=20, y=20)
        y_position = 160
        for contact in self.book:
            contact_label = tk.Label(self.root, text=contact, bg='#8c6e00', font=('Arial', 14), bd=0, highlightthickness=0, width=5, height=2)
            contact_label.place(x=20, y=y_position)
            y_position += 40

    def add_contact_window(self):

        acw = tk.Toplevel(root)
        acw.title('Add contact')
        acw.geometry("400x300")
        acw.minsize(width=400, height=300)
        acw.maxsize(width=400, height=300)
        acw.configure(bg='white')
        
        name_lbl = tk.Label(acw, text='Name', bg='white', fg='black', padx=5, pady=5, font=('Arial', 16), bd=0)
        phone_lbl = tk.Label(acw, text='Phone number', bg='white', fg='black', padx=5, pady=5, font=('Arial', 16), bd=0)
        birthday_lbl = tk.Label(acw, text='Birthday', bg='white', fg='black', padx=5, pady=5, font=('Arial', 16), bd=0)
        
        x = 120
        name_lbl.place(x=x, y=20)
        phone_lbl.place(x=x, y=70)
        birthday_lbl.place(x=x, y=120)

        name_entry = tk.Entry(acw, bg='white', fg='black', bd=0, font=('Arial', 12))
        phone_entry = tk.Entry(acw, bg='white', fg='black', bd=0, font=('Arial', 12))
        birthday_entry = tk.Entry(acw, bg='white', fg='black', bd=0, font=('Arial', 12))

        name_entry.place(x=x, y=50)
        phone_entry.place(x=x, y=100)
        birthday_entry.place(x=x, y=150)

        list_info = [name_entry, phone_entry, birthday_entry]

        add_btn = tk.Button(acw, text='Add contact', bg='white', fg='black', bd=0, highlightthickness=0, width=7, height=2, command= lambda: self.add_contact(self.book, list_info))
        add_btn.place(x=x, y= 190)

    @input_error
    def add_contact(self, book, args): # Функція для добавлення контактів
        if len(args) == 1:
            raise ValueError 
        elif len(args) == 2:
            name, numer = args
            contact = Record(name)
            contact.add_phone(numer)
            book.add_record(contact)
        elif len(args) == 3:
            name, numer, birt = args
            contact = Record(name)
            contact.add_phone(numer)
            contact.add_birthday(birt)
            book.add_record(contact)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()