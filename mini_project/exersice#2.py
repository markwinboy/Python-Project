#Дан список слов. Найти, имеет ли второе слово вхождение подстроки, которая является анаграммой первого слова
a = list(map(str, input().split()))
b = input()
main_lst = []
for i in range(len(b)):
    main_lst.append(b[i:len(a)+i+1])
    if (len(a)+i)==len(b):
        break
print(main_lst)
for j in a:
    boll = False
    for i in main_lst:
        count=0
        for k in j:
            if k in i:
                count+=1
        if count==len(j):
            boll=True
    print(boll)