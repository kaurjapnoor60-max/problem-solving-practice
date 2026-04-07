# You are given an m x n integer grid accounts where accounts[i][j] is the amount of money the i​​​​​​​​​​​th​​​​ customer has in the j​​​​​​​​​​​th​​​​ bank. Return the wealth that the richest customer has.
# A customer's wealth is the amount of money they have in all their bank accounts. The richest customer is the customer that has the maximum wealth.
# Example 1:
# Input: accounts = [[1,2,3],[3,2,1]]
# Output: 6
# Explanation:
# 1st customer has wealth = 1 + 2 + 3 = 6
# 2nd customer has wealth = 3 + 2 + 1 = 6
# Both customers are considered the richest with a wealth of 6 each, so return 6.
# Example 2:
# Input: accounts = [[1,5],[7,3],[3,5]]
# Output: 10
def maximumWealth(accounts):
    maxwealth = 0
    m=len(accounts)
    n=len(accounts[0])
    for i in range(m):
        sum = 0
        for j in range(n):
            sum = sum + accounts[i][j]
        if sum > maxwealth:
            maxwealth = sum
    return maxwealth

print("Enter the number of customers ")
m = int(input())
print("Enter the number of banks ")
n = int(input())
accounts = []
print("Enter the account details ")
for i in range(m):
    row = []
    for j in range(n):

        x = int(input())
        row.append(x)
    accounts.append(row)

print("The maximum wealth is:", maximumWealth(accounts))