import math
try:
    number = float(input("Enter a number to find its square root: "))
    if number < 0:
        print("Square root of a negative number results in a complex number.")
        sqrt_value = math.sqrt(abs(number))
        print(f"The square root of {number} is {sqrt_value}i")
    else:
        sqrt_value = math.sqrt(number)
        print(f"The square root of {number} is {sqrt_value}")
except ValueError:
    print("Please enter a valid numerical value.")
