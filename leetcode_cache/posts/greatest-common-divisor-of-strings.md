# Cpp Solution:
Let's Connect on ****[LINKDIN](https://www.linkedin.com/in/mahesh-vishnoi-a4a47a193)****
#### Approach

 - str1+str2 == str2+str1 if and only if str1 and str2 have a gcd . 
- E.g. str1=abcabc, str2=abc, then str1+str2 = abcabcabc = str2+str1
This(str1+str2==str2+str1) is a requirement for the strings to **have a gcd**. If one of them is NOT a common part then  gcd is "".It means we will return **empty string**
**Proof**:-`str1 = mGCD, str2 = nGCD, str1 + str2 = (m + n)GCD = str2 + str1`
- Both the strings are made of same substring added multiple times.
- Since they are multiples, next step is simply to find the gcd of the lengths of 2 strings e.g. gcd(6,3) = 3, (we can use gcd function to find that)and get the substring of length 3 from either str1 or str2.
In c++ it will be **str1.substr(0, gcd)**


#### Code
```
class Solution {
public:
    string gcdOfStrings(string str1, string str2) {
        return (str1 + str2 == str2 + str1)? 
        str1.substr(0, gcd(size(str1),size(str2))): "";
    }
};
```
If you really found my solution helpful **please upvote it**, as it motivates me to post such kind of codes.
**Let me know in comment if i can do better.**
Let's Connect on **[LINKDIN](https://www.linkedin.com/in/mahesh-vishnoi-a4a47a193)**





# Python Solution:
#### Consider
```
                    Please Upvote If You Find It Helpful
```
#### Intuition
<!-- Describe your first thoughts on how to solve this problem. -->
    First we check if str1 + str2 == str2 + str1
    If it is equal than if find the longest common substring.
    Otherwise we return "".
#### Approach
<!-- Describe your approach to solving the problem. -->
    Suppose str1 = "ABCABC" and str2 = "ABC"
    str1 + str2 = ABCABCABC
    str2 + str1 = ABCABCABC
    str1 + str2 == str2 + str1
    return str.substr(0, gcd(size(str1), gcd(size(str2))))
    where gcd(3, 6) = 3
    So, answer is "ABC"

    Also str1 = "LEET", str2 = "CODE"
    str1 + str2 = "LEETCODE"
    str2 + str1 = "CODELEET"
    So, return ""
#### Complexity
- Time complexity: O(n)
<!-- Add your time complexity here, e.g. $$O(n)$$ -->

- Space complexity: O(n)
<!-- Add your space complexity here, e.g. $$O(n)$$ -->

#### Code
```cpp
class Solution {
public:
    string gcdOfStrings(string str1, string str2) {
        // Check if concatenated strings are equal or not, if not return ""
        if(str1 + str2 != str2 + str1)
            return "";
        // If strings are equal than return the substring from 0 to gcd of size(str1), size(str2)
        return str1.substr(0, gcd(str1.size(), str2.size()));
    }
};
```
```python
class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        #### Check if concatenated strings are equal or not, if not return ""
        if str1 + str2 != str2 + str1:
            return ""
        #### If strings are equal than return the substring from 0 to gcd of size(str1), size(str2)
        from math import gcd
        return str1[:gcd(len(str1), len(str2))]

```
```Java
class Solution {
    public String gcdOfStrings(String str1, String str2) {
        // Check if concatenated strings are equal or not, if not return ""
        if (!(str1 + str2).equals(str2 + str1))
            return "";
        // If strings are equal than return the substring from 0 to gcd of size(str1), size(str2)
        int gcd = gcd(str1.length(), str2.length());
        return str1.substring(0, gcd);
    }

    private int gcd(int a, int b) {
        return b == 0 ? a : gcd(b, a % b);
    }
}

```
```
                            Give a . It motivates me alot
```
Let's Connect On [Linkedin](https://www.linkedin.com/in/naman-agarwal-0551aa1aa/)