# Given an input string, containing upper-case and lower-case letters, digits, and spaces( ' ' ). A word is defined as a sequence of non-space characters. The words in s are separated by at least one space.
# Return a string with the words in reverse order, concatenated by a single space.
# Example 1
# Input: s = "welcome to the jungle"
# Output: "jungle the to welcome"
# Explanation: The words in the input string are "welcome", "to", "the", and "jungle". Reversing the order of these words gives "jungle", "the", "to", and "welcome". The output string should have exactly one space between each word.

# Example 2
# Input: s = " amazing coding skills "
# Output: "skills coding amazing"
def reverseString(s):
    result = " "
    word = s.split()
    for i in range (len(word)-1, -1, -1):
        result = result + word[i] + " "
    return result.strip()
s = input("Enter a string : ")
print(reverseString(s))
