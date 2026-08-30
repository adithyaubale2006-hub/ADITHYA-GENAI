#intersection Two arrays 
def Intersect(num1, num2):
    set1 = set(num1)
    set2 = set(num2)

    return list(set1&set2)

num1 = [1,1,2,2,1]
num2 = [2,2,2]
print(Intersect(num1, num2))