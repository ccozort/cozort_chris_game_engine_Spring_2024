# This file was created by: Chris Cozort

print("hello world!")

x = "awesome"

def myFunc():
    # global x
    x  = "fantastic"
    print("Python is " + x)

myFunc()
print("Python is " + x)

x = 2
y = 5

print(x**5)

i = 1


while i < 6:
    print(i)
    i += 1