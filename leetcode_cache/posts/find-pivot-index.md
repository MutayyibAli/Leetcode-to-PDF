# Cpp Solution:
[Tutorial video in Chinese 中文解題影片](https://www.youtube.com/watch?v=hK9gdtn2zq0)

[中文詳解 解題文章](https://vocus.cc/article/655b6d6ffd89780001b34a15)

[用Python來實現Prefix Sum](https://vocus.cc/article/66d59867fd897800014586cd)

[從"前綴和"查表高速計算"區間和"的教學專欄](https://vocus.cc/article/660402f4fd8978000101b7b4)

O(n) sol. by Balance scale.
#### Animation of Balance scale algorithm




**Hint**:

#1.
Think of the **Balance scale** in laboratory or traditional markets.


#2.
Imagine each **number** from input list as a **weight**.





#3
Turn the finding of pivot index with left hand sum = right hand sum into the **procedure of reaching the balance on boths sides**.


**Algorithm**:

Step_#1:

Let 
**Left hand side be empty**, and
**Right hand side holds all weights**.

Step_#2:

Iterate weight_*i* from 0 to (n-1)

During each iteration, **take away weight_#i from right hand side**, **check whether balance is met** or not.

**If yes**, then the **index *i*** is the **pivot index**.

If no, **put weight_#*i* on the left hand side**, and **repeat the process** until balance is met or all weights are exchanged.

Step_#3:

Finally, if all weights are exchanged and no balance is met, then pivot index does not exist, return -1.


```python
class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        
        #### Initialization:
        #### Left hand side be empty, and
        #### Right hand side holds all weights.
        total_weight_on_left, total_weight_on_right = 0, sum(nums)

        for idx, current_weight in enumerate(nums):

            total_weight_on_right -= current_weight

            if total_weight_on_left == total_weight_on_right:
                #### balance is met on both sides
                #### i.e., sum( nums[ :idx] ) == sum( nums[idx+1: ] )
                return idx

            total_weight_on_left += current_weight

        return -1
```
```javascript
function Accumulation(arr){
    return arr.reduce((a,b)=>a+b);  
}

var pivotIndex = function(nums) {
    

    // Initialization:
    // Left hand side be empty, and
    // Right hand side holds all weights.
    
    let totalWeightOnLeft = 0;
    let totalWeightOnRight = Accumulation(nums);
    
    for( let i = 0 ; i < nums.length ; i++ ){
        
        let currentWeight = nums[i];
        
        totalWeightOnRight -= currentWeight;
        
        if( totalWeightOnLeft == totalWeightOnRight ){
            // balance is met on both sides
            return i;
        }
        
        totalWeightOnLeft += currentWeight
        
        
    }
    
    return -1;
    
};
```
```java
class Solution {
    public int pivotIndex(int[] nums) {
        
        // Initialization:
        // Left hand side be empty, and
        // Right hand side holds all weights.
        int totalWeightOnLeft = 0;
        int totalWeightOnRight = IntStream.of( nums ).sum();
        
        for( int i = 0 ; i < nums.length ; i++ ){
            
            int curWeight = nums[i];
            
            totalWeightOnRight -= curWeight;
            
            if( totalWeightOnLeft == totalWeightOnRight ){
                // balance is met on both sides
                return i;
            }
            
            totalWeightOnLeft  += curWeight;
        }
        
        return -1;
    }
}
```
```Go
func accumulation(nums []int) int{
    
    summation := 0
    
    for _, num := range nums{
        summation += num    
    }
    
    return summation
}


func pivotIndex(nums []int) int {
    
    // Initialization
    // Left hand side be empty
    // Right hand side holds all weights
    totalWeightOnLeft := 0
    totalWeightOnRight := accumulation( nums )
    
    for idx, currentWeight := range nums{
        
        totalWeightOnRight -= currentWeight
        
        if totalWeightOnLeft == totalWeightOnRight{
            // balance is met on both sides
            return idx
        }
        
        totalWeightOnLeft += currentWeight
    }
    
    return -1
    
}
```
```cpp
class Solution {
public:
    int pivotIndex(vector<int>& nums) {
        
        // Initialization:
        // Left hand side be empty, and
        // Right hand side holds all weights.
        
        int totalWeightOnLeft = 0;
        int totalWeightOnRight = std::accumulate( nums.begin(), nums.end(), 0);
        
        
        for(std::size_t i = 0; i < nums.size() ; i++ ){
            
            int currentWeight = nums[i];
            
            totalWeightOnRight -= currentWeight;
            
            if( totalWeightOnLeft == totalWeightOnRight ){
                // balance is met on both sides
                return i;
            }
            
            totalWeightOnLeft += currentWeight;
        }
        
        
        return -1;
    }
};
```

Time Complexity: O(n) on for loop iteration, and summation of input array.

Sapce Complexity: O(1) on fixed size of temp variables.

Share traditional solution based on prefix sum

```python
class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        
        #### s = prefix sum of array
        #### s[i] = nums[0] + nums[1] + ... + nums[i]
        s = list( itertools.accumulate(nums) )
        total_sum = sum( nums )

        #### Linear scan on each index
        for i in range( len(nums) ):

            left_sum = s[i-1] if i >= 1 else 0
            right_sum = total_sum - s[i]

            #### Find pivot index from definition
            if left_sum == right_sum:
                return i

        return -1
```

Time complexity: O(n) on linear scan as well as prefix sum table

Space complexity: O( n ) on the size of prefix sum table 





# Python Solution:
#### **Java Solution:**
```
// Runtime: 1 ms, faster than 92.94% of Java online submissions for Find Pivot Index.
// Time Complexity : O(n)
class Solution {
    public int pivotIndex(int[] nums) {
        // Initialize total sum of the given array...
        int totalSum = 0;
        // Initialize 'leftsum' as sum of first i numbers, not including nums[i]...
        int leftsum = 0;
        // Traverse the elements and add them to store the totalSum...
        for (int ele : nums)
            totalSum += ele;
        // Again traverse all the elements through the for loop and store the sum of i numbers from left to right...
        for (int i = 0; i < nums.length; leftsum += nums[i++])
            // sum to the left == leftsum.
            // sum to the right === totalSum - leftsum - nums[i]..
            // check if leftsum == totalSum - leftsum - nums[i]...
            if (leftsum * 2 == totalSum - nums[i])
                return i;       // Return the pivot index...
        return -1;      // If there is no index that satisfies the conditions in the problem statement...
    }
}
```

#### **cpp Solution:**
```
// Time Complexity : O(n)
class Solution {
public:
    int pivotIndex(vector<int>& nums) {
        // Initialize rightSum to store the sum of all the numbers strictly to the index's right...
        int rightSum = accumulate(nums.begin(), nums.end(), 0);
        // Initialize leftSum to store the sum of all the numbers strictly to the index's left...
        int leftSum = 0;
        // Traverse all elements through the loop...
        for (int idx = 0; idx < nums.size(); idx++) {
            // subtract current elements with from rightSum...
            rightSum -= nums[idx];
            // If the sum of all the numbers strictly to the left of the index is equal to the sum of all the numbers strictly to the index's right...
            if (leftSum == rightSum)
                return idx;     // Return the pivot index...
            // add current elements with leftSum...
            leftSum += nums[idx];
        }
        return -1;      // If there is no index that satisfies the conditions in the problem statement...
    }
};
```

#### **Python/Python3 Solution:**
```
#### Time Complexity : O(n)
#### Space Complexity : O(1)
class Solution(object):
    def pivotIndex(self, nums):
        #### Initialize leftSum & rightSum to store the sum of all the numbers strictly to the index's left & right respectively...
        leftSum, rightSum = 0, sum(nums)
        #### Traverse elements through the loop...
        for idx, ele in enumerate(nums):
            rightSum -= ele
            #### If the sum of all the numbers strictly to the left of the index is equal to the sum of all the numbers strictly to the index's right...
            if leftSum == rightSum:
                return idx      #### Return the pivot index...
            leftSum += ele
        return -1       #### If there is no index that satisfies the conditions in the problem statement...
```
#### **JavaScript Solution:**
```
// Time Complexity : O(n)
var pivotIndex = function(nums) {
    // Initialize total sum of the given array...
    let totalSum = 0
    // Traverse the elements and add them to store the totalSum...
    for(let i = 0; i < nums.length; i++) {
        totalSum += nums[i]
    }
    // Initialize 'leftsum' as sum of first i numbers, not including nums[i]...
    let leftSum = 0
    // Again traverse all the elements through the for loop and store the sum of i numbers from left to right...
    for (let i = 0; i < nums.length; i++) {
        // sum to the left == leftsum.
        // sum to the right === totalSum - leftsum - nums[i]..
        // check if leftsum == totalSum - leftsum - nums[i]...
        if (leftSum * 2 == totalSum - nums[i])
            return i;       // Return the pivot index...
        leftSum += nums[i]
    }
    return -1      // If there is no index that satisfies the conditions in the problem statement...
};
```
**I am working hard for you guys...
Please upvote if you found any help with this code...**