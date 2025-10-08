# Cpp Solution:
#### Intuition
<!-- Describe your first thoughts on how to solve this problem. -->
We can Solved this question using multiple approach. (Here I have explained all the possible solutions of this problem).

1. Solved using Linear Search. Brute Force Approach
2. Solved using Binary Search (Recursive Approach).
3. Solved using Binary Search (Iterative Approach). Optimized Approach.

#### Approach
<!-- Describe your approach to solving the problem. -->
We can easily understand the all the approaches by seeing the code which is easy to understand with comments.

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

    Time Complexity : O(N), because in the worst case we traverse the <= N element. Where N is the size of the
    Array(nums).
                    
    Space Complexity : O(1), the space complexity is constant.

    Solved using Linear Search.

*/


/***************************************** Approach 1 First Code *****************************************/

class Solution {
public:
    int findPeakElement(vector<int>& nums) {
        int n = nums.size();
        for(int i=0; i<n-1; i++){
            if(nums[i] > nums[i+1]){
                return i;
            }
        }
        return n-1;
    }
};






/***************************************** Approach 1 Second Code *****************************************/

class Solution {
public:
    int findPeakElement(vector<int>& nums) {
        return max_element(nums.begin(), nums.end()) - nums.begin();
    }
};






/*

    Time Complexity : O(log N), since we have used binary search to find the target element. The time complexity
    is logarithmic.

    Space Complexity : O(logN), Recursion stack space.

    Solved using Binary Search (Recursive Approach).

*/


/***************************************** Approach 2 First Code *****************************************/

class Solution {
private: 
    int recursive_binary_search(vector<int>& nums, int low, int high){
        if(low == high){
            return low;
        }
        int mid = (low + high) >> 1;
        if(nums[mid] > nums[mid+1]){
            return recursive_binary_search(nums, low, mid);
        }
        else{
            return recursive_binary_search(nums, mid+1, high);
        }
    }
public:
    int findPeakElement(vector<int>& nums) {
        return recursive_binary_search(nums, 0, nums.size()-1);
    }
};






/*

    Time Complexity : O(log N), since we have used binary search to find the target element. The time complexity
    is logarithmic.

    Space Complexity : O(1), since we stored only some constant number of elements, the space complexity is
    constant.

    Solved using Binary Search (Iterative Approach).

*/


/***************************************** Approach 3 First Code *****************************************/

class Solution {
public:
    int findPeakElement(vector<int>& nums) {
        int n = nums.size();
        int low = 0;
        int high = nums.size()-1;
        while(low < high){
            int mid = (low + high) >> 1;
            if(nums[mid] > nums[mid+1]){
                high = mid;
            }
            else{
                low = mid + 1;
            }
        }
        return low;
    }
};

```

***IF YOU LIKE THE SOLUTION THEN PLEASE UPVOTE MY SOLUTION BECAUSE IT GIVES ME MOTIVATION TO REGULARLY POST THE SOLUTION.***




# Python Solution:
    Basic Idea: Binary search

    Elaboration: 
     if an element(not the right-most one) is smaller than its right neighbor, then there must be a peak element on its right, because the elements on its right is either 
       1. always increasing  -> the right-most element is the peak
       2. always decreasing  -> the left-most element is the peak
       3. first increasing then decreasing -> the pivot point is the peak
       4. first decreasing then increasing -> the left-most element is the peak  

       Therefore, we can find the peak only on its right elements( cut the array to half)

       The same idea applies to that an element(not the left-most one) is smaller than its left neighbor.



    Conditions:
         1. array length is 1  -> return the only index 
         2. array length is 2  -> return the bigger number's index 
         3. array length is bigger than 2 -> 
               (1) find mid, compare it with its left and right neighbors  
               (2) return mid if nums[mid] greater than both neighbors
               (3) take the right half array if nums[mid] smaller than right neighbor
               (4) otherwise, take the left half
    
    Run time: O(logn)
    Memory: constant
    Test cases: 
         [1]
         [1,2]
         [2,1]
         [1,2,3]
         [3,2,1]
         [2,1,3]
    
    
    def findPeakElement(self, nums):
        left = 0
        right = len(nums)-1
    
        #### handle condition 3
        while left < right-1:
            mid = (left+right)/2
            if nums[mid] > nums[mid+1] and nums[mid] > nums[mid-1]:
                return mid
                
            if nums[mid] < nums[mid+1]:
                left = mid+1
            else:
                right = mid-1
                
        #handle condition 1 and 2
        return left if nums[left] >= nums[right] else right