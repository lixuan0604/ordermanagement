from django.test import TestCase

# Create your tests here.


def test(left,right):
    l = []
    for num in range(left,right+1):
        numStr = str(num)
        numList = list(numStr)
        res = True
        for item in numList:
            itemNum = int(item)
            if itemNum==0:
                res = False
                break
            if num % itemNum !=0:
                res = False
        if res:
            l.append(num)
    return l

print(test(1,22))
