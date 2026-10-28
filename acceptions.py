try:
    num1 = int(input("Enter the first number: "))
    num2 = int(input("Enter the second number: "))
    result = num1 / num2
    print("The result is ", result)
except ZeroDivisionError:
    print("Division by zero is an error")
except ValueError:
    print("Please enter valid whole numbers")
except:
    print("wrong input")
else:
    print("no exceptions ")
finally: 
    print("this will print no matter what")   