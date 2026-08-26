a = 10
b = -12
c = 0

if a and b and c:
    print("all the numbers have boolean value as true")
elif a or b or c:
    print("Atleast one number has boolean value as false")



a = 10
b = -10
c = 0

if a > 0 or b > 0:
    print("either of the numbers is greater than 0")
else:
    print("no numbers are greater than 0")

    if b > 0 or c > 0:
        print("either of the numbers is greater than 0")
    else:
        print("no number is greater than 0")