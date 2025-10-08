# Cpp Solution:
This is a typical DP problem. Suppose the minimum path sum of arriving at point `(i, j)` is `S[i][j]`, then the state equation is `S[i][j] = min(S[i - 1][j], S[i][j - 1]) + grid[i][j]`.

Well, some boundary conditions need to be handled. The boundary conditions happen on the topmost row (`S[i - 1][j]` does not exist) and the leftmost column (`S[i][j - 1]` does not exist). Suppose `grid` is like `[1, 1, 1, 1]`, then the minimum sum to arrive at each point is simply an accumulation of previous points and the result is `[1, 2, 3, 4]`.

Now we can write down the following (unoptimized) code.

    class Solution {
    public:
        int minPathSum(vector<vector<int>>& grid) {
            int m = grid.size();
            int n = grid[0].size(); 
            vector<vector<int> > sum(m, vector<int>(n, grid[0][0]));
            for (int i = 1; i < m; i++)
                sum[i][0] = sum[i - 1][0] + grid[i][0];
            for (int j = 1; j < n; j++)
                sum[0][j] = sum[0][j - 1] + grid[0][j];
            for (int i = 1; i < m; i++)
                for (int j = 1; j < n; j++)
                    sum[i][j]  = min(sum[i - 1][j], sum[i][j - 1]) + grid[i][j];
            return sum[m - 1][n - 1];
        }
    };

As can be seen, each time when we update `sum[i][j]`, we only need `sum[i - 1][j]` (at the current column) and `sum[i][j - 1]` (at the left column). So we need not maintain the full `m*n` matrix. Maintaining two columns is enough and now we have the following code.

    class Solution {
    public:
        int minPathSum(vector<vector<int>>& grid) {
            int m = grid.size();
            int n = grid[0].size();
            vector<int> pre(m, grid[0][0]);
            vector<int> cur(m, 0);
            for (int i = 1; i < m; i++)
                pre[i] = pre[i - 1] + grid[i][0];
            for (int j = 1; j < n; j++) { 
                cur[0] = pre[0] + grid[0][j]; 
                for (int i = 1; i < m; i++)
                    cur[i] = min(cur[i - 1], pre[i]) + grid[i][j];
                swap(pre, cur); 
            }
            return pre[m - 1];
        }
    };

Further inspecting the above code, it can be seen that maintaining `pre` is for recovering `pre[i]`, which is simply `cur[i]` before its update. So it is enough to use only one vector. Now the space is further optimized and the code also gets shorter.

    class Solution {
    public:
        int minPathSum(vector<vector<int>>& grid) {
            int m = grid.size();
            int n = grid[0].size();
            vector<int> cur(m, grid[0][0]);
            for (int i = 1; i < m; i++)
                cur[i] = cur[i - 1] + grid[i][0]; 
            for (int j = 1; j < n; j++) {
                cur[0] += grid[0][j]; 
                for (int i = 1; i < m; i++)
                    cur[i] = min(cur[i - 1], cur[i]) + grid[i][j];
            }
            return cur[m - 1];
        }
    };


# Python Solution:
#### Please UPVOTE 

**!! BIG ANNOUNCEMENT !!**
I am currently Giving away my premium content well-structured assignments and study materials to clear interviews at top companies related to computer science and data science to my current Subscribers this week. I planned to give for next 10,000 Subscribers as well. So **DON'T FORGET** to Subscribe

**Search `Tech Wired leetcode` on YouTube to Subscribe**

#### Video Solution
**Search  `Minimum Path Sum by Tech Wired` on YouTube**




Happy Learning, Cheers Guys 

#### Approach:

- The code implements a dynamic programming approach to find the minimum path sum in a grid.

- The algorithm uses a 2D array to store the minimum path sum to reach each position (i, j) in the grid, where i represents the row and j represents the column.

- The minimum path sum to reach each position (i, j) is computed by taking the minimum of the path sum to reach the position above (i-1, j) and the position to the left (i, j-1), and adding the cost of the current position (i, j).

- The minimum path sum to reach the bottom-right corner of the grid is stored in the last element of the array (grid[m-1][n-1]), where m is the number of rows and n is the number of columns in the grid.

#### Intuition:

- The intuition behind the dynamic programming approach is that the minimum path sum to reach a position (i, j) in the grid can be computed by considering the minimum path sum to reach the positions (i-1, j) and (i, j-1).

- This is because the only two possible ways to reach the position (i, j) are either by moving down from (i-1, j) or moving right from (i, j-1).

- By computing the minimum path sum to reach each position in the grid, the algorithm can find the minimum path sum to reach the bottom-right corner of the grid by simply looking at the last element of the array (grid[m-1][n-1]).


```Python
class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
            
        
        m, n = len(grid), len(grid[0])
        
        for i in range(1, m):
            grid[i][0] += grid[i-1][0]
        
        for i in range(1, n):
            grid[0][i] += grid[0][i-1]
        
        for i in range(1, m):
            for j in range(1, n):
                grid[i][j] += min(grid[i-1][j], grid[i][j-1])
        
        return grid[-1][-1]
    
        #### An Upvote will be encouraging

```
```Java
class Solution {
    public int minPathSum(int[][] grid) {
        int m = grid.length;
        int n = grid[0].length;
        
        for (int i = 1; i < m; i++) {
            grid[i][0] += grid[i-1][0];
        }
        
        for (int j = 1; j < n; j++) {
            grid[0][j] += grid[0][j-1];
        }
        
        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                grid[i][j] += Math.min(grid[i-1][j], grid[i][j-1]);
            }
        }
        
        return grid[m-1][n-1];
    }
}


```
```cpp
class Solution {
public:
    int minPathSum(vector<vector<int>>& grid) {
        int m = grid.size();
        int n = grid[0].size();
        
        for (int i = 1; i < m; i++) {
            grid[i][0] += grid[i-1][0];
        }
        
        for (int j = 1; j < n; j++) {
            grid[0][j] += grid[0][j-1];
        }
        
        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                grid[i][j] += min(grid[i-1][j], grid[i][j-1]);
            }
        }
        
        return grid[m-1][n-1];
    }
};


```



#### Please UPVOTE 