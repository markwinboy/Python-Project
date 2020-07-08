# Задание: переместить все нули в конец списка сохраняя относительно порядок ненулевых элементов
# a = list(map(int, input().split()))
a=[0,1,0,0,14,0,0,4,3,12]
i=0
while i<len(a):
    if a[i]==0:
        a.remove(0)
        a.append(0)
    elif a[i]!=0:
        i+=1
    if a.count(0)==(len(a)-i):
        break
print(a)
