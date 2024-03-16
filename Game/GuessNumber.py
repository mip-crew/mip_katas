import tkinter as tk
from tkinter import messagebox
import random


class GuessNumber:
    def __init__(self, app):
        self.app = app  # Инициализируем приложение
        self.app.title('Угадай число')  # Называем приложение
        self.app.geometry('375x200')  # Задаем размеры окна
        # Фреймы
        self.f_left = tk.LabelFrame(text="Пользователь")
        self.f_right = tk.LabelFrame(text="Компьютер")
        self.f_left.pack(side='top')
        self.f_right.pack(side='bottom')
        # Базовые параметры игры
        self.list_upperBound = 101
        self.list_lowerBound = 1
        self.list_numbers = list(range(self.list_lowerBound, self.list_upperBound))  # Загадываем случайное число от 1 до 100. Достаточно 7 попыток
        self.secret_number = random.choice(self.list_numbers)
        # Параметры для игрока-человека
        self.attempts = 0  # Счетчик попыток
        self.upperBound = 0  # Нижняя граница, для подсказки
        self.lowerBound = 0  # Верхняя граница, для подсказки
        # Интерфейс для игрока-человека
        self.label_upperBound = tk.Label(self.f_left)  # Надпись подсказки
        self.label_lowerBound = tk.Label(self.f_left)  # Надпись подсказки
        self.label_upperBound.pack(side='top')  # Отображение подсказки
        self.label_lowerBound.pack(side='top')  # Отображение подсказки

        self.label = tk.Label(self.f_left, text='Введите число')  # Надпись
        self.label.pack(side='left')  # Отображаем надпись

        self.entry = tk.Entry(self.f_left)  # Поле для ввода пользователем
        self.entry.pack(side='left')  # Отображаем ввод числа

        self.button = tk.Button(self.f_left, text='Проверить', command=self.check_guess)  # Кнопка для проверки числа
        self.button.pack(side='left')  # Отображаем кнопку
        # Параметры для игрока-компьютера
        self.attempts_BinarySearch = 0  # Счетчик попыток для компьютера
        self.result = self.binary_search(self.list_numbers, 0, len(self.list_numbers) - 1, self.secret_number)
        # Интерфейс для игрока-компьютера
        self.label_BinarySearch = tk.Label(self.f_right, text=f'Число попыток алгоритма бинарного поиска: {self.attempts_BinarySearch}')  # Надпись
        self.label_BinarySearch.pack(side='right')  # Отображаем надпись

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

    def binary_search(self, arr, low, high, x):
        # Проверяем базовый вариант
        if high >= low:
            mid = (high + low) // 2
            # Загаданное число в середине массива
            if arr[mid] == x:
                self.attempts_BinarySearch += 1
                return mid
            # Если загаданное число меньше середины, то оно может быть только в левом подмножестве
            elif arr[mid] > x:
                self.attempts_BinarySearch += 1
                return self.binary_search(arr, low, mid - 1, x)
            # Если загаданное число больше середины, то оно может быть только в правом подмножестве
            else:
                self.attempts_BinarySearch += 1
                return self.binary_search(arr, mid + 1, high, x)
        else:
            # Обработка на случай ошибки
            return -1


if __name__ == '__main__':
    root = tk.Tk()
    game = GuessNumber(root)
    root.mainloop()
