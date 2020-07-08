import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_data(sample_name):
    lst_of_concentration = []#я не стал запариваться и просто создал список в котором будут храниться списки(можно скахать массив)
    path = sample_name
    dirs = os.listdir(path)#открываю директорию папки sample_name
    for i in dirs:#перебираю эту директорию по папкам, условие для того чтобы в случае hromos отсортировать файлы
        #вначале сработает условие flows, так как эта папка первая по счет, а потом уже hromos
        if i == "hromos":
            lst = sorted(os.listdir(path+ "/" + i), key=lambda x: int(x.split(".")[0]))# сортировка файлов по возрастанию(от1 до 10)
            count = 0#просто счетчик
            for file in lst:#Перебираю файлы из папки hromos
                with open(path + "/" + i + "/" + file, "r") as f:#открываю файлы и начинаю с ними работать
                    potok_vyhod = f.readlines()#список из всех строк файла
                    time = potok_vyhod[3].split("_")[5].split(".")[0]#выделяю время в 4 строчке
                    time_second = int(time[:2]) * 60 * 60 + int(time[2:4]) * 60 + int(time[4:])#Перевожу время в секунды
                    if count == 0:#а вот и счетчик, если нулевое значение то значит стартовое время которое должно равняться 0
                        start_time = time_second
                    lst_of_concentration[count].append(time_second - start_time)#добавляем в список значение времени в секундах
                    lst_of_concentration[count].append(float(potok_vyhod[10].split(",")[4]))#добавляем С3
                    lst_of_concentration[count].append(float(potok_vyhod[11].split(",")[4]))#добавляем С4
                    count += 1
        elif i == "flows":
            lst_2 = []#создаем пустой список
            lst = os.listdir(path+ "/" + i)#заходим в директорию папки flows
            for file in lst:#проходимся по всем файлам, хотя там всего один
                with open(path + "/" + i + "/" + file, "r") as f:#открываю файлы и начинаю с ними работать
                    potok_vyhod = f.readlines()#список из всех строк файла
                    for i in potok_vyhod:#Перебираю строки из сиска potok_vyhod
                        lst_2.append(float(i.split("\t")[1].replace("\n", "")))#добавляю значение Fout в список
                        lst_of_concentration.append(lst_2)#добавляю список в скисок
                        lst_2 = []#очищаю чтобы использовать повторно
    lst_second = []#создаю новый список для секундных значений
    lst_selection = []#создаю список для значений селекции
    lst_convertion = []#ну и анологично для конверсии
    for i in lst_of_concentration:#перебираю списки значений от 1 до 10
        X = (30-(i[2]*i[0]/100))*100/30#Подсчет конверсии
        lst_convertion.append(X)#добавляю в список
        S = (i[3]*i[0])/(30-(i[2]*i[0]/100))#подсчет селекции
        lst_selection.append(S)#добавляю в список
        lst_second.append(i[1])#добавляю в список секунды
    d = dict(Second=lst_second, Selection=lst_selection, Convertion=lst_convertion)#создаю словарь
    df = pd.DataFrame(d)#перевожу в табличку(массив) для удобства построения графиков и визуально таблица выглядит лучше
    df = df.set_index("Second")#перевожу столбец секунды в индексную часть, тоже для удобства построения
    print(df)
    plt.plot(df["Selection"])#даю данные для посроения по оси y селекция( по оси x по умолчанию стоят секунды)
    plt.ylabel('Селекция', fontsize=14)#название yоси
    plt.xlabel('Время эксперимента', fontsize=14)#название xоси
    plt.show()#рисует сам график
    #далее то же самое
    plt.plot(df["Convertion"])
    plt.ylabel('Конверсия', fontsize=14)
    plt.xlabel('Время эксперимента', fontsize=14)
    plt.show()

sample_name = "C:/Users/Марк/PycharmProjects/project1/Pt-Sn-Al2O3-02-2018"
plot_data(sample_name)
