# factorial of a given number using tail recursion
def factorial(n, fact):
    if n == 0:
        return fact
    else:
        return factorial(n-1, n * fact)

n=int(input("Enter a number: "))
fact=1
print("Factorial of", n, "is", factorial(n, fact))