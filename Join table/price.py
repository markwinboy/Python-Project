import pandas as pd
import numpy as np
import os
import datetime
import math
from cmd import Cmd
from dateutil.relativedelta import relativedelta

columns = {
    'Название': 'name',
    'Тип квартир': 'type',
    'Цена за кв.м., руб./кв.м.': 'price'
}
d = [{
    'Объект': None,
    'Тип квартир': None
}]
df_main = pd.DataFrame(columns=['Объект', 'Тип квартир'])


# Создание столбца для основного файла
def create_new_date(name):
    global df_main
    df = pd.read_csv(name, sep=',', encoding='cp1251')
    date = name.split('.')[0].split('/')[1].split("-")
    date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
    df = df.rename(columns={
        'Название': 'Объект',
        'Цена за кв.м., руб./кв.м.': date
    })
    df1 = df[['Объект', 'Тип квартир', date]]
    df1 = df1.astype(object).replace({0: np.nan, '—': np.nan, '-': np.nan})
    df1.iloc[:, 2] = pd.to_numeric(df1.iloc[:, 2])
    grouped = df1.groupby(['Объект', 'Тип квартир'], sort=False).mean()
    return grouped


# Проверка на
def check_columns(df):
    global df_main
    lst_index = list(df_main)
    if df_main.empty:
        df_main = df.copy()
    elif list(df)[-1] in lst_index:
        return ""
    else:
        if isinstance(lst_index[-1], datetime.datetime):
            if ((lst_index[-1].month - list(df)[-1].month) == -1) and ((lst_index[-1].year - list(df)[-1].year) == 0):
                add_column_to_main(df)
                average_columns()
                return df
            elif ((lst_index[-1].month - list(df)[-1].month) == 0) and ((lst_index[-1].year - list(df)[-1].year) == 0):
                return add_column_to_main(df)
            else:
                df_main[lst_index[-1] + relativedelta(months=+1)] = np.nan
                return check_columns(df)
        else:
            return add_column_to_main(df)

#усреднение значений по месячно
def average_columns():
    global df_main
    data = df_main.loc[:, :"Тип квартир"].copy()
    df_main.drop(["Объект", "Тип квартир"], axis="columns", inplace=True)
    df_main.columns = pd.Series(df_main.columns).apply(lambda x: x.to_period('M').to_timestamp())
    df_main = df_main.groupby(df_main.columns, axis=1).mean()
    is_nan(df_main)
    df_main = data.join(df_main)

# Добавление столбца к основному
def add_column_to_main(df):
    global df_main
    result = pd.merge(df_main, df, how='outer', on=['Объект', 'Тип квартир'])
    result = change_for_average(result)
    df_main = result.copy()

#Замена nan-значений
def is_nan(df):
    for index, row in df.iterrows():
        if math.isnan(row[-1]) == False:
            count = list(row.isnull()).index(False)
            while count<len(row):
                if math.isnan(row[count]):
                    row[count] = row[count-1]+(row[-1]-row[count-1])/(len(row)-count+1)
                count+=1

# Работа с основной таблицей
def work_pd_main(name):
    global df_main
    xl = pd.ExcelFile(name)
    df1 = xl.parse('Цены')
    df_main = change_for_average(df1)

# Парсинг из excel в csv
def excel_to_csv(name):
    if len(name.split('.')) == 1:
        os.mkdir(name+"_csv")
        dirs = os.listdir(name)
        lst_csv = sorted(dirs, key=lambda x: str(x.split(".")[0]))
        for file in lst_csv:
            xl = pd.ExcelFile(name + "/" + file)
            df1 = xl.parse('Цены')
            df1.to_csv(name+"_csv/" + file.split(".")[0] + '.csv', index=False, sep=',', encoding='cp1251')
    else:
        xl = pd.ExcelFile(name)
        df1 = xl.parse('Цены')
        df1.to_csv(name.split('.')[0].split('/')[-1] + '.csv', index=False, sep=',', encoding='cp1251')


# Парсинг из csv в excel
def csv_to_excel(name):
    if len(name.split('.')) == 1:
        os.mkdir(name + "_excel")
        dirs = os.listdir(name)
        lst_csv = sorted(dirs, key=lambda x: str(x.split(".")[0]))
        for file in lst_csv:
            df = pd.read_csv(name + "/" + file, sep=',', encoding='cp1251')
            writer = pd.ExcelWriter(name+"_excel/" + file.split(".")[0] + ".xlsx", engine='xlsxwriter')
            df.to_excel(writer, 'Цены')
            writer.save()
    else:
        writer = pd.ExcelWriter(name.split('.')[0].split('/')[-1]+ ".xlsx", engine='xlsxwriter')
        df = pd.read_csv(name, sep=',', encoding='cp1251')
        df.to_excel(writer, 'Цены')
        writer.save()


# Запись таблицы в Excel
def write_to_excel(df):
    writer = pd.ExcelWriter("Result.xlsx")
    df.to_excel(writer, 'Цены',index=False)
    writer.save()


# перебор файлов в папке
def pars_folder_csv(name):
    global df_main
    try:
        if len(name.split('.')) == 1:
            dirs = os.listdir(name)
            lst_csv = sorted(dirs, key=lambda x: str(x.split(".")[0]))
            for file in lst_csv:
                df1 = create_new_date(name + "/" + file)
                check_columns(df1)
        else:
            df1 = create_new_date(name)
            check_columns(df1)
        average_columns()
        write_to_excel(df_main)
    except FileNotFoundError:
        print("Указан несуществующий путь")


# Замена значений NaN на средние значения
def change_for_average(df):
    df = df.astype(object).replace({0: np.nan, '—': np.nan, '-': np.nan})
    df.iloc[:, 2:].apply(pd.to_numeric, errors='ignore')
    return df

 # Класс команд для управления файлом
class MyPrompt(Cmd):
    prompt = 'pb>'
    intro = 'Welcome! Type ? to list commands'

    def do_exit(self, inp):
        print('Bye')
        return True

    def help_exit(self):
        print('exit the application. Shorthand: x q Ctrl-D')

    def do_csv_to_excel(self, inp):
        csv_to_excel(inp)

    def help_csv_to_excel(self):
        print("Перевод значений из csv-файла в Excel")

    def do_excel_to_csv(self, inp):
        excel_to_csv(inp)

    def help_excel_to_csv(self):
        print("Перевод значений из Excel в csv")

    def do_add_csv(self, inp):
        pars_folder_csv(inp)

    def help_add_csv(self):
        print("Добавить csv-файл или папку csv файлов к основной таблице")

    def do_main_df(self, inp):
        global df_main
        work_pd_main(str(inp))

    def help_main_df(self):
        print("Создать основную таблицу для ее дальнейшего заполнения")

    def default(self, inp):
        pass


if __name__ == '__main__':
    MyPrompt().cmdloop()