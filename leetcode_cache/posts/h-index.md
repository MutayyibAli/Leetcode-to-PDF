# Cpp Solution:
#### Intuition
- The problem is to find the h-index of a researcher based on their citation counts. The h-index is the maximum value h such that the researcher has published at least h papers that have each been cited at least h times.


#### Approach
- ***Two common approaches to solve this problem are:***
#### 1. Brute Force Approach: 
- Sort the array of citations in descending order and iterate through the sorted array. For each paper, check if its citation count is greater than or equal to its position in the sorted array. Keep track of the maximum h-index encountered. This approach has a time complexity of O(n log n) due to the sorting step.

#### 2. Binary Search Approach:
- Sort the array of citations and perform a binary search to find the h-index. Initialize a search range between 0 and the length of the citations array. In each iteration, calculate the mid-point and count the number of papers with citations greater than or equal to the mid-point. Adjust the search range based on this count. This approach has a time complexity of O(n log n) due to the sorting step.


#### Complexity
#### - Time complexity:
1. **Code 1 (Brute Force)**
- Time complexity: O(n log n) - Sorting the array takes O(n log n) time, and the subsequent iteration takes O(n) time.

2. **Code 2 (Binary Search)**
- Time complexity: O(n log n) - Sorting the array takes O(n log n) time, and the binary search takes O(log n) time.

#### - Space complexity:
1. **Code 1 (Brute Force)**
- Space complexity: O(1) - Constant space is used.

2. **Code 2 (Binary Search)**
- Space complexity: O(1) - Constant space is used.

#### Code 1.
```
class Solution {
public:

    int hIndexBruteForce(vector<int>& c) {
        sort(c.begin(), c.end());
        int n = c.size();
        int maxi = 0;
        for(int i = 0; i < n; i++) {
            if(c[i] >= n - i) {
                maxi = max(maxi, n - i);
            }
        }
        return maxi;
    }

    int hIndex(vector<int>& citations) {
        return hIndexBruteForce(citations);
    }
};
```

#### Code 2.
```
class Solution
{
public:
    int hIndex(vector<int> &citations)
    {
        sort(citations.begin(), citations.end());
        int n = citations.size();
        int start = 0, end = n - 1;
        int ans = 0;
        while (start <= end)
        {
            int mid = start + (end - start) / 2;
            if (citations[mid] >= n - mid)
            {
                ans = max(ans, n - mid);
                end = mid - 1;
            }
            else
            {
                start = mid + 1;
            }
        }
        return ans;
    }
};
```




# Python Solution:
####  IF YOU FIND THIS POST HELPFUL PLEASE UPVOTE 

#### Approach: 1  Sorting and Iteration


- **Sorting:** Sorts the `citations` list in ascending order.
- **Iterative Check:** Iterates through the sorted list.
For each citation `v` at index `i`:
    - If `n - i `(number of articles with at least `n - i` citations) is less than or equal to `v` itself (the current citation count), it means the h-index is `n - i`.
    - Returns `n - i` as the `h-index`.
- **Default Return:** If no valid `h-index` is found, returns `0`.

#### Code : 1
```
class Solution:
    def hIndex(self, citations: List[int]) -> int:
        n = len(citations)
        citations.sort()

        for i,v in enumerate(citations):
            if n - i <= v:
                return n - i
        return 0
```

#### Approach: 2 Counting Frequency and Backward Iteration


- **Frequency Array:** Creates a temporary array `temp` of size `n + 1` to store citation frequencies.
- **Counting Citations:** Iterates through the `citations` list:
    - If a citation `v` is greater than `n`, adds it to the highest frequency bucket (`temp[n]`).
    - Otherwise, increments the count in the corresponding bucket (`temp`[v]).
- **Calculating h-index:** Iterates backward through the `temp` array:
    - Accumulates the `total` number of citations up to each index `i`.
    - If the total count (total) is greater than or equal to `i` itself, it means `i` is the `h-index`.
    - Returns `i` as the `h-index`.
#### Code : 2
```
class Solution:
    def hIndex(self, citations: List[int]) -> int:
        n = len(citations)
        temp = [0 for _ in range(n + 1)]

        for i,v in enumerate(citations):
            if v > n :
                temp[n] += 1
            else:
                temp[v] += 1
        
        total = 0
        for i in range(n, -1, -1):
            total += temp[i]
            if total >= i:
                return i
```
#### Comparison Table:

Feature	| Code 1	| Code 2
---------|--------|-Approach	| Sorting and iteration	Frequency | counting and backward iteration
Time Complexity	| O(n log n) due to sorting	| O(n)
Space Complexity	| O(1)	| O(n) for temp array
Advantages	| Simpler to understand	| Linear time complexity
Disadvantages	| Slower for large inputs	| Requires extra space for temp array

######  If you found my solution and information helpful, I would greatly appreciate your upvote, as it would motivate me to continue sharing more solutions. 





