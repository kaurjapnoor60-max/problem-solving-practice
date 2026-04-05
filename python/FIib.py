# print the nth term of fibonacci series  
def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n-1) + fib(n-2)

n = int(input("Enter the term number: "))
print(fib(n))