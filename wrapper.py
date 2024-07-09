import tkinter as tk

def input_error(func): #Декоратор вводу
    def inner(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except ValueError as e: # Якщо номер не передається то викликається виняток
            show_error_message(self.root, str(e))
        except AttributeError as e:
            show_error_message(self.root, str(e))
    return inner

def show_error_message(root, error: str): # Вікно помилки, приймає активне вікно та помилку як параметри
    error_window = tk.Toplevel(root)
    error_window.title("Ошибка ввода")
    error_window.configure(bg='white')

    # Встановлюєио розмір вікна
    error_window.geometry("300x105")

    # Добавляємо віджети для відображення помилки 
    label = tk.Label(error_window, text=error, fg="red", bg='white')
    label.pack(pady=10)

    button = tk.Button(error_window, text="Закрыть", bg='white', fg='black', command=error_window.destroy, bd=0, highlightthickness=0, width=5, height=2)
    button.pack(pady=10)
