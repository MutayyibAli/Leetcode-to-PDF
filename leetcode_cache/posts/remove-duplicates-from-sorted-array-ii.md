# Cpp Solution:
#### **PLEASE UPVOTE MY SOLUTION IF YOU LIKE IT**
#### **CONNECT WITH ME**
####### **[https://www.linkedin.com/in/pratay-nandy-9ba57b229/]()**
####### **[https://www.instagram.com/pratay_nandy/]()**
#### Approach
The goal of this function is to remove duplicates from the nums vector while keeping at most two occurrences of any element. The function returns the length of the modified vector after removing duplicates.

Here's the approach implemented in the code:

- Initialize an integer variable i to 0. This variable will keep track of the current position in the modified nums vector.

- Use a for loop to iterate through each element ele in the nums vector using the range-based for loop.

- Inside the loop, check the following conditions:


1. i == 0: This condition ensures that the first element is always included in the modified vector.
2. i == 1: This condition ensures that the second element is always included in the modified vector.
3. nums[i-2] != ele: This condition checks if the current element ele is not the same as the element two positions before the current position i. This ensures that only two occurrences of any element are included in the modified vector.-  If any of the above conditions are met, copy the current element ele to the nums[i] position in the modified vector, and increment i by 1 to move to the next position.


- Repeat this process for all elements in the nums vector.

- Finally, return the value of i, which represents the length of the modified vector with duplicates removed.

This approach effectively modifies the nums vector in place, removing duplicates while keeping at most two occurrences of each element. The function returns the length of the modified vector, which can be used to access the unique elements in the first i positions of the vector
<!-- Describe your approach to solving the problem. -->

#### Complexity
- Time complexity:**0(N)**
<!-- Add your time complexity here, e.g. $$O(n)$$ -->

- Space complexity:**0(1)**
<!-- Add your space complexity here, e.g. $$O(n)$$ -->



#### Code
```
class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        int i =0;
        // int ele= nums[0];
        for(auto ele : nums)
        {
            if(i==0 || i==1 || nums[i-2] != ele)
            {
                nums[i] = ele;
                i++;
            }
        }
    return i ;
    }
};
```


# Python Solution:
#### Intuition
The problem seems to involve removing duplicates from a sorted array, but with a constraint that allows at most two occurrences of each element. The use of a two-pointer approach is hinted by the iteration variable `j` in the code.



#### Approach
The approach employs a two-pointer strategy. The variable `j` is used to keep track of the current position in the modified array where elements are being stored without violating the constraint. The loop iterates through the array, and for each element, it checks whether it is the same as the element two positions behind the current `j`. If it is, it means there are already two occurrences of this element in the modified array, and we should skip adding another one to adhere to the constraint. Otherwise, the element is added to the modified array at position `j`, and `j` is incremented.

#### Complexity
- Time complexity: $$O(n)$$, where $$n$$ is the length of the input array. The algorithm iterates through the array once.
- Space complexity: $$O(1)$$, as the modification is done in-place without using any additional data structures.

#### Explanation of Two-Pointer Approach
The two-pointer approach in this scenario involves using two pointers, `i` and `j`, where `i` iterates through the array, and `j` keeps track of the position where elements satisfying the constraint are being stored.

- **Initialization:** Initialize `j` to 1 since the first element (at index 0) is always considered part of the modified array.
- **Iteration:** Loop through the array starting from index 1 (i.e., `i = 1`). Compare the current element at index `i` with the element two positions behind at index `j - 2`. If they are the same, it means there are already two occurrences of this element in the modified array, so skip adding another. If they are different, add the current element to the modified array at position `j` and increment `j`.
- **Final Result:** The final length of the modified array is equal to `j`, and the modified array contains elements adhering to the constraint.
#### Code
```Java
class Solution {
    public int removeDuplicates(int[] nums) {
        int j = 1;
        for (int i = 1; i < nums.length; i++) {
            if (j == 1 || nums[i] != nums[j - 2]) {
                nums[j++] = nums[i];
            }
        }
        return j;
    }
}
```
```cpp
class Solution {
public:
    int removeDuplicates(std::vector<int>& nums) {
        int j = 1;
        for (int i = 1; i < nums.size(); i++) {
            if (j == 1 || nums[i] != nums[j - 2]) {
                nums[j++] = nums[i];
            }
        }
        return j;
    }
};
```
```Python
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        j = 1
        for i in range(1, len(nums)):
            if j == 1 or nums[i] != nums[j - 2]:
                nums[j] = nums[i]
                j += 1
        return j
```
```Rust
impl Solution {
    pub fn remove_duplicates(nums: &mut Vec<i32>) -> i32 {
        let mut j = 1;
        for i in 1..nums.len() {
            if j == 1 || nums[i] != nums[j - 2] {
                nums[j] = nums[i];
                j += 1;
            }
        }
        j as i32
    }
}

```

