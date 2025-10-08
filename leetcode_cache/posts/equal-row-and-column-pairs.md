# Cpp Solution:
```
class Solution {
public:
    int equalPairs(vector<vector<int>>& grid) 
    {
        // Number to store the count of equal pairs.
        int ans = 0;
        map<vector<int>, int> mp;
        // Storing each row int he map
        for (int i = 0; i < grid.size(); i++)
            mp[grid[i]]++;
        
        for (int i = 0; i < grid[0].size(); i++)
        {
            vector<int> v;
            // extracting column in a vector.
            for (int j = 0; j < grid.size(); j++)
                v.push_back(grid[j][i]);
            // Add the number of times that column appeared as a row.
            ans += mp[v];
        }
        // Return the number of count
        return ans;
    }
};
```
Hope you like it.


# Python Solution:

Consider this grid for an example:
```
           grid = [[1,2,1,9]
                   [2,8,9,2]
                   [1,2,1,9]
                   [9,2,6,3]]
```    
Here's the plan:
- Determine`tpse`, the transpose of`grid`(using`zip(*grid)`):
```
           tspe = [[1,2,1,9] 
                   [2,8,2,2]
                   [1,9,1,6]
                   [9,2,9,3]]
```
- The problem now is to determine the pairs of identical rows, one row in `tpse`and the other in` grid`. We hash`grid`and`tspe`:
```
          Counter(tuple(grid)):
               {(1,2,1,9): 2, (2,8,9,2): 1, (9,2,6,3): 1}
 
           Counter(zip(*grid)):
            {(1,2,1,9): 1, (2,8,2,2): 1, (1,9,1,6): 1, (9,2,9,3): 1}
```            
   • Finally, we determine the number of pairs:
```
       (1,2,1,9): 2 and (1,2,1,9): 1    => 2x1 = 2
```
Here's the code:
```
class Solution:                                
    def equalPairs(self, grid: List[List[int]]) -> int:

        tpse = Counter(zip(*grid))                  #### <-- determine the transpose
                                                    ####     and hash the rows

        grid = Counter(map(tuple,grid))             #### <-- hash the rows of grid. (Note the tuple-map, so
                                                    ####     we can compare apples w/ apples in next step.)

        return  sum(tpse[t]*grid[t] for t in tpse)  #### <-- compute the number of identical pairs
```
[https://leetcode.com/problems/equal-row-and-column-pairs/submissions/1287382373/](https://leetcode.com/problems/equal-row-and-column-pairs/submissions/1287382373/)

I could be wrong, but I think that time complexity is *O*(*N*) and space complexity is *O*(*N*), in which *N* ~ the count of elements in `grid`.