a = int(input("Enter a number: "))
b = int(input("Enter a second number to be added or subtracted to the first number: "))
c = input("Enter + or - if you want to add or subtract the numbers: ")

if c == "+":
  print("The sum of the two numbers is " + str(a + b))

elif c == "-":
  print("The difference of the two numbers is " + str(a - b))

else:
  print("Unknown operator")
