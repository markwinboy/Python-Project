
from math import  *

#Функция, которая оценивает значение e^x по формуле Тейлора
def get_exp(x,c):
    sum=1
    for i in range(1,c+1):
        sum+=(x**i)/factorial(i)
    return sum

#Реализация функции факториал
def factorial(n):
    count=1
    for i in range(n):
        count*=(i+1)
    return count

def main():
    x = int(input("Введите x: "))
    c =int( input("Введите кол-во членов в ряду: "))
    print(get_exp(x,c))
    x1=20
    y = exp(20)
    c=1
    while True:
        if y/get_exp(x1,c)-1<0.1:
            print(c)
            break
        c+=1
if __name__ == '__main__':
    main()