# Cpp Solution:
#### Intuition
If we thought that all elements of the vector is a number we need to increase it by 1. The input can be 100 digits so we must handle that through digits.

#### Approach
First we increment the first digit (last element) by 1, if it becomes 10 we make it 0 ans add 1 to the second digit.. until the last digit (first element), if it becoms 10 we make it 1 and push_back a leading zero.

#### Complexity
- Time complexity:
O(n)


#### Code
```
class Solution {
public:
    vector<int> plusOne(vector<int>& v) {
        int n = v.size();
        for(int i = n-1; i >= 0; i--){
            if(i == n-1)
                v[i]++;
            if(v[i] == 10){
                v[i] = 0;
                if(i != 0){
                    v[i-1]++;
                }
                else{
                    v.push_back(0);
                    v[i] = 1;
                }
            }
        }
        return v;
    }
};
```

Don't forget please :')





# Python Solution:
#### Intuition
Iterate through the array from the end

#### Solution Video

https://youtu.be/9Ea9RH7Dm-g

###### ⭐️⭐️ Don't forget to subscribe to my channel! ⭐️⭐️

**■ Subscribe URL**
http://www.youtube.com/channel/UC9RMNwYTL3SXCP6ShLWVFww?sub_confirmation=1

Subscribers: 6,990
Thank you for your support!

#### Approach

Let's think about this.

```
Input: digits = [1,2,3]
```
The description says "Increment the large integer by one and return the resulting array of digits", so we should add `1` to the last index then return the array.

```
[1,2,4]
```
But what if we have 
```
Input: digits = [9,9]
```
If we add `1` to the last index, the number at the last index will be `0` then we have `carry`. Again if we add the carry to the index `0`, the number at index `0` will be `0`, then we will get `another carry`.

Finally, add `1` and `1` will be the first index and return the array.

```
return [1,0,0]
``` 


⭐️ Points

When we add `1` then the number is not `10`, just add `1` to the last index and return the array.

If `10`, add `0` to the current index, add `0` to the current index then continue to loop until `we find a number except 10` or `reach index 0`.

If we reach index `0`, then add `1` to the first index and other all numbers should be `0`, **because we have `10` in each digit and have `carry` for the next digit.**

https://youtu.be/bU_dXCOWHls

#### Complexity
- Time complexity: $$O(n)$$
<!-- Add your time complexity here, e.g. $$O(n)$$ -->

- Space complexity: $$O(1)$$
<!-- Add your space complexity here, e.g. $$O(n)$$ -->

```python
class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:

        for i in range(len(digits) - 1, -1, -1):

            if digits[i] + 1 != 10:
                digits[i] += 1
                return digits
            
            digits[i] = 0

            if i == 0:
                return [1] + digits
```
```javascript
var plusOne = function(digits) {
    for (let i = digits.length - 1; i >= 0; i--) {
        if (digits[i] + 1 !== 10) {
            digits[i] += 1;
            return digits;
        }
        digits[i] = 0;
        if (i === 0) {
            digits.unshift(1);
            return digits;
        }
    }    
};
```
```java
class Solution {
    public int[] plusOne(int[] digits) {
        for (int i = digits.length - 1; i >= 0; i--) {
            if (digits[i] + 1 != 10) {
                digits[i] += 1;
                return digits;
            }
            digits[i] = 0;
        }
        
        int[] newDigits = new int[digits.length + 1];
        newDigits[0] = 1;
        return newDigits;        
    }
}
```
```cpp
class Solution {
public:
    vector<int> plusOne(vector<int>& digits) {
        for (int i = digits.size() - 1; i >= 0; i--) {
            if (digits[i] + 1 != 10) {
                digits[i] += 1;
                return digits;
            }
            digits[i] = 0;
            if (i == 0) {
                digits.insert(digits.begin(), 1);
                return digits;
            }
        }
        return digits;        
    }
};
```

Thank you for reading my post. Please upvote it and don't forget to subscribe to my channel!

###### ⭐️ Subscribe URL
http://www.youtube.com/channel/UC9RMNwYTL3SXCP6ShLWVFww?sub_confirmation=1

###### ⭐️ Twitter
https://twitter.com/CodingNinjaAZ

###### ⭐️ #189 - Rotate Array

https://youtu.be/fDRPdN0dlcs

