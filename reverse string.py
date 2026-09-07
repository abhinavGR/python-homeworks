string = input("please enter a word: ")
string2 = ('')

for i in string:
    string2 = i + string2

print("\nthe original string first = ", string)
print("the reversed string = ", string2)