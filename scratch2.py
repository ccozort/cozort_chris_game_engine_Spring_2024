# This file was created by: Chris Cozort

'''
Write a function that takes two arguments and multiplies them together 
Use a return statement
Print result

Write another function that converts the return from the 
first to a string an prints it out in a statement with concatenation
Pass the first function as an argument

Write a while loop that uses both functions 10 times

Write a for loop that uses both functions 10 times

Write a Class that wraps this all together

 '''

def f1(a,b):
    return a * b

print(f1(5,5))

def f2(f):
    print("answer is" + str(f))
# count = 0
count = 0

while True:
    print("keep going...")
    count+=1
    if count == 10:
        break