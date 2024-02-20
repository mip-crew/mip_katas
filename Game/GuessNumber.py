import tkinter as tk
from tkinter import messagebox
import random


class GuessNumber:
    def __init__(self, app):
        self.app = app  # Инициализируем приложение
        self.app.title('Угадай число')  # Называем приложение
        self.app.geometry('200x200')  # Задаем размеры окна

        self.secret_number = random.randint(1, 100)  # Загадываем случайное число от 1 до 100. Достаточно 7 попыток
        self.attempts = 0  # Счетчик попыток

        self.upperBound = 0  # Нижняя граница, для подсказки
        self.lowerBound = 0  # Верхняя граница, для подсказки
        self.label_upperBound = tk.Label(self.app)  # Надпись подсказки
        self.label_lowerBound = tk.Label(self.app)  # Надпись подсказки
        self.label_upperBound.pack()  # Отображение подсказки
        self.label_lowerBound.pack()  # Отображение подсказки

        self.label = tk.Label(self.app, text='Введите число')  # Надпись
        self.label.pack()  # Отображаем надпись

        self.entry = tk.Entry(self.app)  # Поле для ввода пользователем
        self.entry.pack()  # Отображаем ввод числа

        self.button = tk.Button(self.app, text='Проверить', command=self.check_guess)  # Кнопка для проверки числа
        self.button.pack()  # Отображаем кнопку

    def check_guess(self):
        try:
            guess = int(self.entry.get())  # Получаем введенное значение
            self.attempts += 1  # Увеличиваем счетчик попыток на единицу

            if guess == self.secret_number:
                messagebox.showinfo(title='Победа', message=f'Вы угадали число за {self.attempts} попыток')  # Сообщение о победе
                self.app.destroy()  # Закрываем все приложение после закрытия сообщения о победе
            elif guess < self.secret_number:
                messagebox.showinfo(title='Подсказка', message='Загаданное число больше введенного')
                self.lowerBound = guess
                self.label_lowerBound.config(text=f'Нижняя граница = {guess}')
            elif guess > self.secret_number:
                messagebox.showinfo(title='Подсказка', message='Загаданное число меньше введенного')
                self.upperBound = guess
                self.label_upperBound.config(text=f'Верхняя граница = {guess}')
        except ValueError:  # Ошибка типа данных
            tk.messagebox.showerror(title='Ошибка типа данных', icon='error', message='Должно быть целое число')


if __name__ == '__main__':
    root = tk.Tk()
    game = GuessNumber(root)
    root.mainloop()
