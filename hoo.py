user_input = input("Enter your age: ")

try:
    
    print(f"Valid age: {int(user_input)}")
except ValueError:
    
    length = len(user_input)
    status = "even" if length % 2 == 0 else "odd"
    print(f"Error! The input length ({length}) is {status}.")
