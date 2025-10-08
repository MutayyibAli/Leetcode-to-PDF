# Cpp Solution:
#### Intuition
The problem aims to find the maximum profit that can be obtained by buying and selling a stock. The given solution seems to follow a simple approach of iterating through the prices, keeping track of the minimum buying price, and updating the profit whenever a higher selling price is encountered.



#### Approach
1. Initialize variables `buy` with the first element of the prices array and `profit` as 0.
2. Iterate through the prices starting from the second element.
3. Update the `buy` variable if the current price is lower than the current buying price.
4. Update the `profit` if the difference between the current price and the buying price is greater than the current profit.
5. Return the final profit.
#### Kadane's Algorithm

Kadane's Algorithm is a dynamic programming technique used to find the maximum subarray sum in an array of numbers. The algorithm maintains two variables: `max_current` represents the maximum sum ending at the current position, and `max_global` represents the maximum subarray sum encountered so far. At each iteration, it updates `max_current` to include the current element or start a new subarray if the current element is larger than the accumulated sum. The `max_global` is updated if `max_current` surpasses its value.

#### Relating with the Approach

In the provided approach for finding the maximum profit in stock prices, the algorithm can be seen as a variation of Kadane's Algorithm. Instead of finding the maximum subarray sum directly, it focuses on finding the maximum positive difference between consecutive elements (prices) in the array. 

Here's how the approach relates to Kadane's Algorithm:

1. **Initialization:**
   - In Kadane's Algorithm, `max_current` and `max_global` are initialized to the first element of the array.
   - In the stock profit approach, `buy` is initialized with the first element of the prices array, and `profit` is initialized to 0.

2. **Iteration:**
   - Kadane's Algorithm iterates through the array, updating `max_current` based on the current element's value and deciding whether to start a new subarray.
   - The stock profit approach iterates through the prices array, updating `buy` when a lower price is encountered and treating the difference between the current price and `buy` as a potential profit.

3. **Comparison and Update:**
   - Kadane's Algorithm compares and updates `max_current` and `max_global` at each iteration.
   - The stock profit approach compares and updates `profit` whenever a positive difference between the current price and `buy` exceeds the current profit.
#### Complexity
- Time complexity: $$O(n)$$, where $$n$$ is the length of the prices array. The algorithm iterates through the array once.
- Space complexity: $$O(1)$$, as only a constant amount of extra space is used.

#### Code
```java
class Solution {
    public int maxProfit(int[] prices) {
        int buy = prices[0];
        int profit = 0;
        for (int i = 1; i < prices.length; i++) {
            if (prices[i] < buy) {
                buy = prices[i];
            } else if (prices[i] - buy > profit) {
                profit = prices[i] - buy;
            }
        }
        return profit;
    }
}
```
```c++
class Solution {
public:
    int maxProfit(std::vector<int>& prices) {
        int buy = prices[0];
        int profit = 0;
        for (int i = 1; i < prices.size(); i++) {
            if (prices[i] < buy) {
                buy = prices[i];
            } else if (prices[i] - buy > profit) {
                profit = prices[i] - buy;
            }
        }
        return profit;
    }
};
```
```python
class Solution:
    def maxProfit(self, prices):
        buy = prices[0]
        profit = 0
        for i in range(1, len(prices)):
            if prices[i] < buy:
                buy = prices[i]
            elif prices[i] - buy > profit:
                profit = prices[i] - buy
        return profit
```
```rust
impl Solution {
    pub fn max_profit(prices: Vec<i32>) -> i32 {
        let mut buy = prices[0];
        let mut profit = 0;
        for i in 1..prices.len() {
            if prices[i] < buy {
                buy = prices[i];
            } else if prices[i] - buy > profit {
                profit = prices[i] - buy;
            }
        }
        profit
    }
}
```
```javascript
class Solution {
    maxProfit(prices) {
        let buy = prices[0];
        let profit = 0;
        for (let i = 1; i < prices.length; i++) {
            if (prices[i] < buy) {
                buy = prices[i];
            } else if (prices[i] - buy > profit) {
                profit = prices[i] - buy;
            }
        }
        return profit;
    }
}
```





# Python Solution:
**The question is saying us to find the best day to buy and sell stock, so we will get maiximum profit.**

**Some body might think that we can find min and max number from the array so that we can get the max profit. But here is one catch
For Example:
prices=[3,4,1,6]
min=1
max=6
profit=max-min=5 which is correct
in this Example:
```
prices = [7,6,4,3,1]
```
min = 1 price at day 6
max = 7 price at day 1
max_profit = 7-1 = 6 u can think like this but you can't buy the stock at day 6 and sell it at day 1.**

**So what is the best way to find the max profit lets see 
<ins>Explanation:</ins>
let use initialize Left and Right pointer to first and second position of array
Here Left is to buy stock and Right is to sell stock**


`   Then we initialize our max_profit as 0.    `

####### Now we will start our while loop and we will run till our 

**Right pointer less then length of array 
<ins>For Example: </ins>
prices=[7,1,5,3,6,4]
Note:
prices[left] --> buy stock
prices[right] --> sell stock
now we will check price at right and left pointer**


**step 1:** <br>
price[left]=7 price[right]=1 profit=-6
here price[left] is greater than price[right] so we will move left pointer to the right position and increment our right pointer by 1. We always want our left point to be minimum

**step 2:** <br>
price[left]=1 price[right]=5 profit=4
here price[left] is less than price[right] which means we will get profit so we will update our max_profit and move our right pointer alone

**step 3:** <br>
price[left]=1 price[right]=3 profit=2
here price[left] is less than price[right] which means we will get profit so we will check our max_profit previously it

was 4 now our current profit is 2 so we will check which is maximum and update our max_profit and move our right pointer alone

**step 4:** <br>
price[left]=1 price[right]=6 profit=5
here price[left] is less than price[right] which means we will get profit so we will check our max_profit previously it was 4 now our current profit is 5 so we will check which is maximum and update our max_profit and move our right pointer alone

**step 5:** <br>
price[left]=1 price[right]=4 profit=3
same logic as above


```
Big O :
n--> length of array
Time Complexity: O(n)
Space Complexity: O(1)
```

**My Hand Writting will not be good ,please adjust it **




##### lets go to the solution:

python:
```python
class Solution:
    def maxProfit(self,prices):
        left = 0 #Buy
        right = 1 #Sell
        max_profit = 0
        while right < len(prices):
            currentProfit = prices[right] - prices[left] #our current Profit
            if prices[left] < prices[right]:
                max_profit =max(currentProfit,max_profit)
            else:
                left = right
            right += 1
        return max_profit
```

javascript:
```javascript
const maxProfit = (prices) => {
  let left = 0; // Buy
  let right = 1; // sell
  let max_profit = 0;
  while (right < prices.length) {
    if (prices[left] < prices[right]) {
      let profit = prices[right] - prices[left]; // our current profit

      max_profit = Math.max(max_profit, profit);
    } else {
      left = right;
    }
    right++;
  }
  return max_profit;
};
```
`UPVOTE if you like  , If you have any question, feel free to ask.`
