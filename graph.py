import astropy.io.fits as pyfits
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from tkinter import ttk
from matplotlib import cm
from matplotlib.ticker import LinearLocator


# функция, считающая энергию фона
def E_back(x, y, rbig, rsmall, exp, scidata):
    E_backgr = 0
    pxs = 0
    for i in range(x - rbig, x + rbig + 1):
        for j in range(y - rbig, y + rbig + 1):
            if ((i - x) ** 2 + (j - y) ** 2 <= rbig ** 2) and ((i - x) ** 2 + (
                    j - y) ** 2 > rsmall ** 2):  # проверяем, чтоб данная точка была в пределах кольца фона
                E_backgr += scidata[j - 1][i - 1]
                pxs += 1
    E_backgr = E_backgr / pxs
    E_backgr = E_backgr / exp
    return (E_backgr)


# функция, считающая энергию звезды
def Estar():
    file = inp1.get()  # путь к файлу
    x = int(inp2.get())
    y = int(inp3.get())
    r = int(inp4.get())  # радиус звезды
    rbig = int(inp5.get())  # внеш радиус фона
    rsmall = int(inp6.get())  # внутр радиус фона
    hdulist = pyfits.open(file)
    exp = hdulist[0].header['exptime']
    scidata = hdulist[0].data
    scidata = np.array(scidata)

    E_star = 0
    pxs = 0
    for i in range(x - r, x + r + 1):
        for j in range(y - r, y + r + 1):
            if ((i - x) ** 2 + (j - y) ** 2 <= r ** 2):  # проверяем, что данная точка лежит внутри радиуса звезды
                E_star += scidata[j - 1][i - 1]  # -1 из-за нумерации пикселей и элем массива
                pxs += 1
    E_star = E_star / exp
    E_star -= E_back(x, y, rbig, rsmall, exp, scidata) * pxs
    cap8['text'] = E_star


# создаём графики
def plot():
    if plotnum.get() == 1:
        x = int(inp2.get())
        y = int(inp3.get())
        r = int(inp4.get())
        file = inp1.get()
        hdulist = pyfits.open(file)
        scidata = hdulist[0].data
        scidata = np.array(scidata)
        hdulist.close()
        val_x = []
        x_axis = []
        for i in range(x - r, x + r + 1):
            val_x.append(scidata[y - 1][i - 1])  # -1 из-за разной нумерации пикселей и элем массива
            x_axis.append(i)
        plt.plot(x_axis, val_x)
        plt.xlabel('x')
        plt.ylabel('Value')
        plt.title(f'Value(x) при y={y}')
        plt.show()
    elif plotnum.get() == 2:
        file = inp1.get()
        x = int(inp2.get())
        y = int(inp3.get())
        r = int(inp4.get())
        hdulist = pyfits.open(file)
        scidata = hdulist[0].data
        scidata = np.array(scidata)
        val_y = []
        y_axis = []
        for i in range(y - r, y + r + 1):
            val_y.append(scidata[i - 1][x - 1])
            y_axis.append(i)
        plt.plot(y_axis, val_y)
        plt.xlabel('y')
        plt.ylabel('Value')
        plt.title(f'Value(y) при x={x}')
        plt.show()
    elif plotnum.get() == 3:
        file = inp1.get()
        x = int(inp2.get())
        y = int(inp3.get())
        r = int(inp4.get())
        hdulist = pyfits.open(file)
        scidata = hdulist[0].data
        scidata = np.array(scidata)
        x_axis = []
        y_axis = []
        for i in range(x - r, x + r + 1):
            x_axis.append(i)
        for i in range(y - r, y + r + 1):
            y_axis.append(i)
        val_3d = np.zeros((len(x_axis), len(y_axis)))
        val_max = 0
        val_min = 20000
        for i in range(len(x_axis)):
            for j in range(len(y_axis)):
                val_3d[j][i] = scidata[y_axis[j] - 1][x_axis[i] - 1]
                if val_3d[j][i] < val_min:
                    val_min = val_3d[j][i]
                elif val_3d[j][i] > val_max:
                    val_max = val_3d[j][i]
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        x_axis, y_axis = np.meshgrid(x_axis, y_axis)  # переводим x и y в квадратные массивы для построения 3д графика
        surf = ax.plot_surface(x_axis, y_axis, val_3d, cmap=cm.ocean)
        ax.set_zlim(val_min, val_max)
        ax.zaxis.set_major_locator(LinearLocator(5))  # устанавливаем положения делений
        fig.colorbar(surf, shrink=0.5, aspect=3)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(f'val 3d')
        plt.show()


# создаём окно
wind = Tk()
wind.title("Новое окно")
wind.geometry("800x400")

# разлиновываем окно
for c in range(4):
    wind.columnconfigure(index=c)
for r in range(9):
    wind.rowconfigure(index=r)

# создаём элементы окна
cap1 = ttk.Label(text='Путь к файлу:')
cap1.grid(row=0, column=0)
inp1 = ttk.Entry()
inp1.grid(row=0, column=1)
cap2 = ttk.Label(text='Данные звезды:')
cap2.grid(row=1, column=0)
cap3 = ttk.Label(text='Координата центра звезды по оси x:')
cap3.grid(row=2, column=0)
inp2 = ttk.Entry()
inp2.grid(row=2, column=1)
cap4 = ttk.Label(text='Координата центра звезды по оси y:')
cap4.grid(row=3, column=0)
inp3 = ttk.Entry()
inp3.grid(row=3, column=1)
cap5 = ttk.Label(text='Радиус звезды в пикселях:')
cap5.grid(row=4, column=0)
inp4 = ttk.Entry()
inp4.grid(row=4, column=1)
cap6 = ttk.Label(text='Внешний радиус фона:')
cap6.grid(row=5, column=0)
inp5 = ttk.Entry()
inp5.grid(row=5, column=1)
cap7 = ttk.Label(text='Внутренний радиус фона:')
cap7.grid(row=6, column=0)
inp6 = ttk.Entry()
inp6.grid(row=6, column=1)
cap8 = ttk.Label(text='0')
cap8.grid(row=7, column=1)
but1 = ttk.Button(text='Энергия звезды', command=Estar)
but1.grid(row=7, column=0)
cap9 = ttk.Label(text='Выберите график, который нужно построить:')
cap9.grid(row=0, column=3)
plotnum = IntVar(value=0)
rbut1 = ttk.Radiobutton(text='Профиль по y', variable=plotnum, value=1)
rbut1.grid(row=0, column=4)
rbut2 = ttk.Radiobutton(text='Профиль по x', variable=plotnum, value=2)
rbut2.grid(row=1, column=4)
rbun3 = ttk.Radiobutton(text='3D график', variable=plotnum, value=3)
rbun3.grid(row=2, column=4)
but2 = ttk.Button(text='Построить график', command=plot)
but2.grid(row=3, column=4)
wind.mainloop()
