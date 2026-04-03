// Given a signed 32-bit integer x, return x with its digits reversed. If reversing x causes the value to go outside the signed 32-bit integer range [-231, 231 - 1], then return 0.

// Example 1:
// Input: x = -123
// Output: -321

// Example 2:
// Input: x = 120
// Output: 21
#include <iostream>
#include <climits>
using namespace std;

int reverse(int x) {
    int rev = 0;

    for(int temp = x; temp != 0; temp /= 10) {
        int digit = temp % 10;
          rev = rev * 10 + digit;
        if (rev > INT_MAX / 10 || rev < INT_MIN / 10)
            return 0;
    }

    return rev;
}

int main() {
    int x;
    cin >> x;
    cout << reverse(x);
    return 0;
}