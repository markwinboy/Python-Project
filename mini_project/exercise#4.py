#Умножить без оператора умножения
#
a=5
b=6
def rec(a,b):
    if b==0:
        return 0
    else:
        return rec(a,b-1)+a
print(rec(a,b))