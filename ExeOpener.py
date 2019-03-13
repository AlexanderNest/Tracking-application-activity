import os
import tkinter as tk
from tkinter import filedialog
import subprocess
import datetime
import time


class MyTime:  # время в формате чч:мм:сс.мс
    def __init__(self, time: str):
        self.hours = int(time[:time.index(':')])
        self.minutes = int(time[time.index(':')+1:time.rindex(':')])
        self.seconds = int(time[time.rindex(':')+1:time.index('.')])
        self.microseconds = int(time[time.index('.')+1:])

    def __str__(self):
        return str(self.hours) + ':' + str(self.minutes) + ':' + str(self.seconds) + '.' + str(self.microseconds)

    def __add__(self, other):
        hours = self.hours + other.hours
        minutes = self.minutes + other.minutes
        seconds = self.seconds + other.seconds
        if seconds >= 60:
            minutes += seconds//60
            seconds -= seconds//60 * 60
        if minutes//60 > 0:
            hours += minutes//60
            minutes -= minutes//60 * 60

        microseconds = self.microseconds + other.microseconds

        return MyTime(str(hours) + ':' + str(minutes) + ':' + str(seconds) + '.' + str(microseconds))


class Graphics:
    def __init__(self):
        self.path = ''  # путь к директории
        self.files = []

        # создание элементов окна
        self.root = tk.Tk()
        self.list = tk.Listbox()
        self.open_btn = tk.Button(text='Открыть', command=self.openfile)
        self.path_button = tk.Button(text='Выбрать директорию', command=self.selectdirectory)

        # размещение элементов на окне

        self.path_button.grid(column=2, row=0, ipadx=10, ipady=6, padx=10, pady=10)
        self.open_btn.grid(column=1, row=0, ipadx=10, ipady=6, padx=10, pady=10)
        self.list.grid(column=0, row=0, ipadx=10, ipady=6, padx=10, pady=10)

        self.root.mainloop()

    # выбор пути к директории
    def selectdirectory(self):

        self.path = tk.filedialog.askdirectory()

        if self.list.size() > 0:
            self.list.delete(0, tk.END)

        allfiles = os.listdir(self.path)

        for i in allfiles:
            if i.endswith('exe'):
                self.files.append(i)

        for i in self.files:
            self.list.insert(tk.END, i)

    # получить список активных .exe файлов
    def getactiveprocesses(self):
        a = str([line.split() for line in subprocess.check_output("tasklist").splitlines()]).split('\'')
        b = []
        for i in a:
            if i.endswith('.exe'):
                b.append(i)
        return b

    def openfile(self):  #открытие файла

        currentfile = self.list.get(self.list.curselection())
        print(self.path)
        os.startfile(r''+self.path+'/'+currentfile)

        ftime = datetime.datetime.now()  # время запуска программы

        while self.inprocess(currentfile):
            time.sleep(3)

        stime = datetime.datetime.now()  # время закрытия программы

        stime = MyTime(str(stime-ftime))
        print(currentfile, 'текущий файл')
        self.sessionwriter(currentfile, stime)

    def inprocess(self, name):  # проверяет, находится ли файл в списке активных приложений

        if name in self.getactiveprocesses():
            return True

    def sessionwriter(self, name, time):  # записывает информацию об использовании приложения в текстовый файл

            data = open('data.txt')

            buffer = data.read().rstrip('\n')

            data.close()

            if len(buffer) == 0:
                data = open('data.txt', 'w')
                data.write(name + ' ' + str(time))
                data.close()
            else:
                buffer = buffer.split('\n')

                content = []

                for i in buffer:
                    content.append(i.split())

                found = False

                for i in range(len(content)-1):
                    if content[i][0] == name:
                        t = MyTime(content[i][1])
                        t += time
                        content[i][1] = str(t)
                        found = True
                        break
                if not found:
                    content.append([name, str(time)])

                data = open('data.txt', 'w')

                for i in range(len(content)):
                    if i == len(content):
                        data.write(content[i][0] + ' ' + content[i][1])
                    else:
                        data.write(content[i][0] + ' ' + content[i][1] + '\n')

                data.close()


g = Graphics()





