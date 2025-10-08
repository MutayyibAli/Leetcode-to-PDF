# Cpp Solution:
#### Intuition
<!-- Describe your first thoughts on how to solve this problem. -->
We can solve this question using Multiple Approaches. (Here I have explained all the possible solutions of this problem).

1. Solved using Array(Two Nested Loops). Brute Force Approach.
2. Solved using Dynamic Programming Approach(tabulation).
3. Solved using Dynamic Programming Approach(Space Optimization). Optimized Approach.

#### Approach
<!-- Describe your approach to solving the problem. -->
We can easily understand the All the approaches by seeing the code which is easy to understand with comments.

#### Complexity
- Time complexity:
<!-- Add your time complexity here, e.g. $$O(n)$$ -->
Time complexity is given in code comment.

- Space complexity:
<!-- Add your space complexity here, e.g. $$O(n)$$ -->
Space complexity is given in code comment.

#### Code
```
/*

    Time Complexity : O(N^2), Where N is the size of the Array(nums). Here Two nested loop creates the time 
    complexity.

    Space complexity : O(1), Constant space. Extra space is only allocated for the Array(output), however the
    output does not count towards the space complexity.

    Solved using Array(Two Nested Loop). Brute Force Approach.

    Note : This will give TLE.

*/


/***************************************** Approach 1 *****************************************/

class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int n = nums.size();
        vector<int> output;
        for(int i=0; i<n; i++){
            int product = 1;
            for(int j=0; j<n; j++){
                if(i == j) continue;
                product *= nums[j];
            }
            output.push_back(product);
        }
        return output;
    }
};






/*

    Time Complexity : O(N), As we iterate the Array(nums) thrice. Where N = size of the array.

    Space complexity : O(N), Array(left_Product and right_Product) space. 

    Solved using Dynamic Programming Approach(tabulation).

*/


/***************************************** Approach 2 *****************************************/

class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int n = nums.size();
        vector<int> ans(n);
        vector<int> left_Product(n);
        vector<int> right_Product(n);
        left_Product[0] = 1;
        for(int i=1; i<n; i++){
            left_Product[i] = left_Product[i-1] * nums[i-1];
        }
        right_Product[n-1] = 1;
        for(int i=n-2; i>=0; i--){
            right_Product[i] = right_Product[i+1] * nums[i+1];
        }
        for(int i=0; i<n; i++){
            ans[i] = left_Product[i] * right_Product[i];
        }
        return ans;
    }
};






/*

    Time Complexity : O(N), As we iterate the Array(nums) twice. Where N = size of the array.

    Space complexity : O(1), Constant space. Extra space is only allocated for the Array(output), however the
    output does not count towards the space complexity.

    Solved using Dynamic Programming Approach(Space Optimization). Optimized Approach.

*/


/***************************************** Approach 3 *****************************************/

class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        int n = nums.size();
        vector<int> output(n);
        output[0] = 1;
        for(int i=1; i<n; i++){
            output[i] = output[i-1] * nums[i-1];
        }
        int right = 1;
        for(int i=n-1; i>=0; i--){
            output[i] *= right;
            right *= nums[i];
        }
        return output;
    }
};

```

***IF YOU LIKE THE SOLUTION THEN PLEASE UPVOTE MY SOLUTION BECAUSE IT GIVES ME MOTIVATION TO REGULARLY POST THE SOLUTION.***




# Python Solution:
#### Intuition
<!-- Describe your first thoughts on how to solve this problem. -->
Similar to finding Prefix Sum array, here the preblem intends us to find the Prefix Product Array and Suffix Product Array for our original array.
```
pre[i+1] = pre[i] * a[i]
suff[i-1] = suff[i] * a[i]
```

#### Complexity
- Time complexity: $$O(n)$$
Only 2 loops iterating $$n$$ times each without any nesting.
<!-- Add your time complexity here, e.g. $$O(n)$$ -->

- Space complexity: $$O(n)$$
We have taken prefix and suffixProduct as variables instead of arrays to further optimize space, even though the overall complexity remains the same.
<!-- Add your space complexity here, e.g. $$O(n)$$ -->

#### Code
```java
class Solution {
    public int[] productExceptSelf(int[] nums) {
        int numsLength = nums.length;
        int prefixProduct = 1;
        int suffixProduct = 1;
        int[] result = new int[numsLength];
        for(int i = 0; i < numsLength; i++) {
            result[i] = prefixProduct;
            prefixProduct *= nums[i];
        }
        for(int i = numsLength-1; i >= 0; i--) {
            result[i] *= suffixProduct;
            suffixProduct *= nums[i];
        }
        return result;
    }
}
```
```python3
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        prefix_product = 1
        postfix_product = 1
        result = [0]*n
        for i in range(n):
            result[i] = prefix_product
            prefix_product *= nums[i]
        for i in range(n-1,-1,-1):
            result[i] *= postfix_product
            postfix_product *= nums[i]
        return result
```
*Please upvote, if this helped you understand the solution in optimal time :)*
