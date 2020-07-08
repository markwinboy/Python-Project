# Maximum chocolates
money = 15
price = 1
wrap = 3
count=0
i=0
while money!=0:
    if money<price:
        break
    count+=1
    money-=price
    wrap-=1
    if wrap==0:
        count+=1
        wrap=3
print(count)
