import inline as inline
import yfinance as yf
import xlwt
import matplotlib.pyplot as plt
import pandas as pd

#Создание списка интересющих нас котировок
data_list_yahoo=['^GSPC','BTC-USD']
name_list = ["S&P500", "BITCOIN"]

#Получение при помощи пакета yfinance цену закрытия S&P500 с 1 января 2017 года по 1 января 2020 года
data = yf.download('^GSPC','2017-01-01','2020-01-01')
#Парсинг цены закрытии Биткоина
data1 = yf.download('BTC-USD','2017-01-01','2020-01-01')
#Функция которая собирает котировки из списка с 2016 года по 2020
def yahoo_parse_clone(lst_data_yahoo):
    ticker = pd.DataFrame(columns=lst_data_yahoo)
    for j in lst_data_yahoo:
        ticker[j]=yf.download(j, '2016-01-01', '2020-02-01')["Adj Close"]
    return ticker
#Запись данных в файл Excel-формата
def parses(data):
    book = xlwt.Workbook()
    sheet1 = book.add_sheet("Sheet1")
    i1=0
    for _ in ["number"]+data_list_yahoo:
        row = sheet1.row(0)
        row.write(i1,_)
        i1+=1
    for num in range(data["BTC-USD"].__len__()):
        row = sheet1.row(num+1)
        # value = list_of_line[num][0]
        row.write(0, data.index[num])
        count=0
        for index in data_list_yahoo:
            value = data[index][num]
            row.write(count+1, value)
            count+=1
    book.save("yahoo.xls")

#построение графика
def graphics(data):
    count = 0
    for i in data_list_yahoo:
        data[i].plot(figsize=(10, 7))
        plt.legend()
        plt.title(name_list[count], fontsize=16)
        plt.ylabel('Price', fontsize=14)
        plt.xlabel('Year', fontsize=14)
        plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
        plt.show()
        count+=1

def graphics1(data):
    # Подготавливаем таблицу переменных для построения
    ((data.pct_change() + 1).cumprod()).plot(figsize=(10, 7))

    #Легенда
    plt.legend()

    # Наименование для оси Y и для оси X
    plt.ylabel('Log Wages: Standard Deviation', fontsize=14)
    plt.xlabel('AGE', fontsize=14)

    # Посроение графиков
    plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
    plt.show()

#Запуск программы
def main():
    data = yahoo_parse_clone(data_list_yahoo)
    print(name_list[1])
    graphics(data)
    graphics1(data)
    parses(data)

if __name__ == '__main__':
    main()