user_input = input("Enter a number: ")
clean_input = user_input.replace("-", "").replace(".", "")
if clean_input.isdigit():
    num_places = len(clean_input)
    print(f"The number of places in '{user_input}' is: {num_places}")
else:
    print("Invalid input. Please enter a valid number.")
