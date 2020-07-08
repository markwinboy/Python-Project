#Функция которая проверяет является ли строка палиндромом
def polindrom(text):
    if text==text[::-1]:
        return True
    else:
        return False
def main():
    a = input("ВВедите бля текст: ")
    print(polindrom(a))
if __name__ == '__main__':
    main()