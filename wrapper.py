def input_error(func): #Декоратор вводу
    def inner(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except ValueError as e: # Якщо номер не передається то викликається виняток
            print(str(e))
        except AttributeError as e:
            print(str(e))
    return inner

