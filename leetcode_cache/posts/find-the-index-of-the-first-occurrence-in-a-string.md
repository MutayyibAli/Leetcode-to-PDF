# Cpp Solution:
Traverse all the possible starting points of `haystack` (from `0` to `haystack.length() - needle.length()`) and see if the following characters in `haystack` match those of `needle`.

```cpp
class Solution {
public:
    int strStr(string haystack, string needle) {
        int m = haystack.size(), n = needle.size();
        for (int i = 0; i <= m - n; i++) {
            int j = 0;
            for (; j < n; j++) {
                if (haystack[i + j] != needle[j]) {
                    break;
                }
            }
            if (j == n) {
                return i;
            }
        }
        return -1;
    }
};
```

The following is another implementation, shorter but harder to understand.

```cpp
class Solution {
public:
    int strStr(string haystack, string needle) {
        int m = haystack.size(), n = needle.size(), p = 0;
        while (p + n - 1 < m) {
            if (haystack.substr(p, n) == needle) {
                return p;
            }
            while (p++ + n - 1 < m && haystack[p] != needle[0]);
        }
        return -1;
    }
};
```

Finally comes the KMP algorithm. You may refer to [KMP on jBoxer's blog](http://jakeboxer.com/blog/2009/12/13/the-knuth-morris-pratt-algorithm-in-my-own-words/) and [KMP on geeksforgeeks](http://www.geeksforgeeks.org/searching-for-patterns-set-2-kmp-algorithm/) for some explanations. I rewrote the code from the second link.

```cpp
class Solution {
public:
    int strStr(string haystack, string needle) {
        int m = haystack.size(), n = needle.size();
        if (!n) {
            return 0;
        }
        vector<int> lps = kmpProcess(needle);
        for (int i = 0, j = 0; i < m;) {
            if (haystack[i] == needle[j]) { 
                i++, j++;
            }
            if (j == n) {
                return i - j;
            }
            if (i < m && haystack[i] != needle[j]) {
                j ? j = lps[j - 1] : i++;
            }
        }
        return -1;
    }
private:
    vector<int> kmpProcess(string needle) {
        int n = needle.size();
        vector<int> lps(n, 0);
        for (int i = 1, len = 0; i < n;) {
            if (needle[i] == needle[len]) {
                lps[i++] = ++len;
            } else if (len) {
                len = lps[len - 1];
            } else {
                lps[i++] = 0;
            }
        }
        return lps;
    }
};
```


# Python Solution:
#### Intuition
Slice a string of haystack.

#### Solution Video

https://youtu.be/lnTAVa8A7XI

###### ⭐️⭐️ Don't forget to subscribe to my channel! ⭐️⭐️

**■ Subscribe URL**
http://www.youtube.com/channel/UC9RMNwYTL3SXCP6ShLWVFww?sub_confirmation=1

Subscribers: 5,241
Thank you for your support!

#### Approach

Problem here is that we don't know where to start. That's why we iterate through all characters one by one.

```
haystack = "abcxyz", needle = "xyz"
```
We start from index `0`.

```
"abcxyz"
 i
```
My strategy is to check a part of string. Formula for the part is

⭐️ Points

```
sliced string = haystack[i: i+ length of needle] 
```

Why?

That's because we need to find a part of string which is length `3`, since length of needle is `3`.

One more important thing is that in Python ending number is not included. If current index is `0`, slicing range should be from index `0` to index  `2` in this case.

Let's see how it works!
```
 012345 → index
"abcxyz"
 i

slicing string: haystack[0:3] → "abc"

if "abc" == "xyz" → False, move next
```
```
 012345 → index
"abcxyz"
  i

slicing string: haystack[1:4] → "bcx"

if "bcx" == "xyz" → False, move next
```
```
 012345 → index
"abcxyz"
   i

slicing string: haystack[2:5] → "cxy"

if "cxy" == "xyz" → False, move next
```
```
 012345 → index
"abcxyz"
    i

slicing string: haystack[3:6] → "xyz"

if "xyz" == "xyz" → True
```
```
return 3
```

Easy!
Let's see solution codes and step by step algorithm!


#### Complexity
- Time complexity: $$O(n * m)$$
<!-- Add your time complexity here, e.g. $$O(n)$$ -->

- Space complexity: $$O(1)$$
<!-- Add your space complexity here, e.g. $$O(n)$$ -->


```python
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:

        if len(haystack) < len(needle):
            return -1

        for i in range(len(haystack)):
            if haystack[i:i+len(needle)] == needle:
                return i

        return -1 
```
```javascript
var strStr = function(haystack, needle) {
    if (haystack.length < needle.length) {
        return -1;
    }
    
    for (let i = 0; i <= haystack.length - needle.length; i++) {
        if (haystack.substring(i, i + needle.length) === needle) {
            return i;
        }
    }
    
    return -1;    
};
```
```java
class Solution {
    public int strStr(String haystack, String needle) {
        if (haystack.length() < needle.length()) {
            return -1;
        }
        
        for (int i = 0; i <= haystack.length() - needle.length(); i++) {
            if (haystack.substring(i, i + needle.length()).equals(needle)) {
                return i;
            }
        }
        
        return -1;        
    }
}
```
```cpp
class Solution {
public:
    int strStr(string haystack, string needle) {
        if (haystack.length() < needle.length()) {
            return -1;
        }
        
        for (int i = 0; i <= haystack.length() - needle.length(); i++) {
            if (haystack.substr(i, needle.length()) == needle) {
                return i;
            }
        }
        
        return -1;        
    }
};
```

#### Step by Step Algorithm

1. **Check Lengths**:
    - Before proceeding with the search, the function checks if the length of `haystack` is less than the length of `needle`.
    - If `haystack` is shorter, it's impossible for `needle` to be found within `haystack`, so the function returns `-1` immediately.

    ```python
    if len(haystack) < len(needle):
        return -1
    ```

2. **Loop Through `haystack`**:
    - The function uses a `for` loop to iterate through `haystack`.
    - The loop runs from the beginning of `haystack` to the point where the remaining substring is at least as long as `needle`.
    - This is achieved by setting the loop condition to `range(len(haystack) - len(needle) + 1)`, ensuring that we do not run out of characters to compare.

    ```python
    for i in range(len(haystack) - len(needle) + 1):
    ```

3. **Compare Substrings**:
    - Inside the loop, a substring of `haystack` starting at the current index `i` and of length equal to `needle` is extracted and compared to `needle`.
    - If they match, the function returns the current index `i`, which is the starting position of the first occurrence of `needle` in `haystack`.

    ```python
    if haystack[i:i+len(needle)] == needle:
        return i
    ```

4. **Return -1 if Not Found**:
    - If the loop completes without finding a match, the function returns `-1`.
    - This indicates that `needle` was not found in `haystack`.

    ```python
    return -1
    ```


Thank you for reading my post.

###### ⭐️ Subscribe URL
http://www.youtube.com/channel/UC9RMNwYTL3SXCP6ShLWVFww?sub_confirmation=1

###### ⭐️ Twitter
https://twitter.com/CodingNinjaAZ

###### ⭐️ My previous video
Remove Duplicates from Sorted List #83

https://youtu.be/uyd5vc0TZmA
