# Cpp Solution:
The `O(n)` solution is to use two pointers: `l` and `r`. First we move `r` until we get a `sum  >= s`, then we move `l` to the right until `sum < s`. In this process, store the minimum length between `l` and `r`. Since each element in `nums` will be visited by `l` and `r` for at most once. This algorithm is of `O(n)` time.

```cpp
class Solution {
public:
    int minSubArrayLen(int s, vector<int>& nums) {
        int l = 0, r = 0, n = nums.size(), sum = 0, len = INT_MAX;
        while (r < n) {
            sum += nums[r++];
            while (sum >= s) {
                len = min(len, r - l);
                sum -= nums[l++];
            }
        }
        return len == INT_MAX ? 0 : len;
    }
};
```

Then comes the `O(nlogn)` solution. This less efficient one turns out to be more difficult to come up with.

First, we maintain an array of accumulated sums of elements in `nums` according to the following two equations.

1. `sums[0] = 0`
2. `sums[i] = nums[0] + ... + nums[i - 1]` for `i > 0`

Then, for each `sums[i] >= s`, we search for the first `sums[j] > sums[i] - s (j < i)` using binary search. In this case, we also have `sums[j - 1] <= sums[i] - s`. If we plug in the definition for `sums`, we have

* `nums[0] + ... + nums[j - 1] > nums[0] + ... + nums[j - 1] + nums[j] + ... + nums[i - 1] - s`
* `nums[0] + ... + nums[j - 2] <= nums[0] + ... + nums[j - 2] + nums[j - 1] + ... + nums[i - 1] - s`

If we minus the left-hand side from both inequalities, we have

* `0 > nums[j] + ... + nums[i - 1] - s`
* `0 <= nums[j - 1] + ... + nums[i - 1] - s`

So, we have `nums[j - 1] + ... + nums[i - 1] >= s` but `nums[j] + ... + nums[i - 1] < s`. So `nums[j-1..i-1]` is the shortest subarray with sum not less than `s` **ending at `i - 1`**. After traversing all possible `i`, we will find out the shortest subarray with sum not less than `s`.

By the way, a `0` is added to the head of `sums` to account for cases like `nums = [3], s = 3`.

```cpp
class Solution {
public:
    int minSubArrayLen(int s, vector<int>& nums) {
        int n = nums.size(), len = INT_MAX;
        vector<int> sums(n + 1, 0);
        for (int i = 1; i <= n; i++) {
            sums[i] = sums[i - 1] + nums[i - 1];
        }
        for (int i = n; i >= 0 && sums[i] >= s; i--) {
            int j = upper_bound(sums.begin(), sums.end(), sums[i] - s) - sums.begin();
            len = min(len, i - j + 1);
        }
        return len == INT_MAX ? 0 : len;
    }
};
```


# Python Solution:
#### Approach

For detailed explanation you can refer to my youtube channel (Hindi Language)
https://youtu.be/0tZ-9dIAY_Q
 or link in my profile.Here,you can find any solution in playlists monthwise from june 2023 with detailed explanation.i upload daily leetcode solution video with short and precise explanation (5-10) minutes.
or
search `Minimum size subarray sum by Let's Code Together` on youtube

#### Sliding Window Approach

1. Initialize two pointers, `i` and `j`, to track the start and end of the current subarray, respectively. Set `i` and `j` to 0 initially.
2. Initialize a variable `sum` to keep track of the current sum of elements in the subarray.
3. Initialize a variable `mn` to store the minimum length found so far. Set it to the maximum possible integer value (`INT_MAX`).
4. Start a while loop that continues until the `j` pointer reaches the end of the array `nums`.
5. Inside the loop, add the element at index `j` to the `sum` variable.
6. Check if the `sum` is greater than or equal to the target value.
7. If the condition is true, enter another while loop. This loop will handle the case where the current subarray sum is equal to or greater than the target.
   a. Decrement the `sum` by subtracting the element at index `i`.
   b. Update `mn` with the minimum length found so far (`j - i + 1`).
   c. Increment the `i` pointer to move the window to the right.
   d. Repeat steps a-c until the `sum` is no longer greater than or equal to the target value.
8. Increment the `j` pointer to move the window to the right.
9. Repeat steps 5-8 until the `j` pointer reaches the end of the array.
10. After the loop, check if the value of `mn` is still `INT_MAX`, indicating that no subarray was found. In this case, return 0.
11. Otherwise, return the value of `mn`, which represents the minimum length of a subarray whose sum is greater than or equal to the target.

The sliding window technique allows us to efficiently search for the minimum length subarray that satisfies the given condition. By maintaining two pointers and adjusting the window based on the sum of elements, we can avoid unnecessary computations and achieve a time complexity of O(N), where N is the size of the input array `nums`.

#### Code1 Sliding Window
```
class Solution {
public:
    int minSubArrayLen(int target, vector<int>& nums) {
        int i=0;
        int j=0;
        int sum=0;
        int mn=INT_MAX;
        while(j<nums.size()){
            sum+=nums[j];
            while(sum>=target){
                sum-=nums[i];
                mn=min(j-i+1,mn);
                i++;
            }
            j++;
        }
        if(mn==INT_MAX){
            return 0;
        }
        return mn;
    }
};
```
#### Complexity
- Time complexity: $$O(n)$$  
- Space complexity: O(1)
#### Code2 Binary Search

#### Binary Search Approach

1. The `windowfind` function checks if there exists a subarray of a given size whose sum is greater than or equal to the target.
2. It uses the sliding window technique to iterate through the array and maintain a window of the specified size.
3. If the sum of the elements in the window is greater than or equal to the target, it returns `true`.
4. Otherwise, it returns `false`.

The `minSubArrayLen` function finds the minimum length of a subarray whose sum is greater than or equal to the target using binary search.
1. It initializes a range from 1 to the size of the input array.
2. It repeatedly divides the range in half and checks if a subarray of the mid-point length satisfies the condition using the `windowfind` function.
3. If a valid subarray is found, it updates the upper bound of the range to mid-1 and stores the mid-point length as the minimum length found so far.
4. If a valid subarray is not found, it updates the lower bound of the range to mid+1.
5. The search continues until the lower bound is no longer less than or equal to the upper bound.
6. Finally, it returns the minimum length of the subarray.

The code efficiently utilizes the sliding window technique and binary search to find the minimum length subarray satisfying the given condition.
```
class Solution {
public:
      bool windowfind(int size, vector<int>&nums, int target) {
        int sum = 0;
        int i=0;
        int j=0;
        int mx=INT_MIN;
        int n=nums.size();
        while(j<n){
            sum+=nums[j];
            if(j-i+1==size){
              mx=max(sum,mx);
              sum-=nums[i];
              i++;
            }
            j++;
        }
        if(mx>=target)
        return true;
        return false;
    }

    int minSubArrayLen(int target, vector<int>& nums) {
        int low = 1, high = nums.size(), mn = 0;
        while (low <= high) {
            int mid = (low + high) / 2;
            if (windowfind(mid, nums, target)) {
                high = mid-1;
                mn = mid;
            } else low = mid + 1;
        }
        return mn;
    }
};
```
#### Complexity
- Time complexity: $$O(n logn)$$ 
- Space complexity: O(1)



Please Upvote 
