# Cpp Solution:
**Intuition:** Since we are asked to calculate all the possible combinations , hence we have to use backtracking

**Concept:** In every backtracking problem , there are two things to keep in mind , which we will explore here as well :
*  Base Case: Every problem of backtracking has some base case which tells us at which point we have to stop with the recursion process. In our case, when the size of our array `current` equals to `k` i.e. `current.size()=k`, we stop with the recursion and add it to our final result `ans`.

*   Conditions: There is just one thing to keep in mind here:
   After generating combinations corresponding to a particular number `i` , proceed to the next element by popping the element from the temporary array `current`, as we used that already. 
 
We basically consider a number `i`, generate the combinations corresponding to it by recursively calling it again, and then we pop that element as we are done with it and proceed to the next!!
		
And thats it!! We are done!! Keeping this in mind, here is the code

**Code:**
```
class Solution {
public:
    vector<vector<int>> ans;
    
    void helper(int idx, int k,vector<int>&current,int n)
    {
        if(current.size()==k)    // base case
        {
            ans.push_back(current);
            return;
        }
        
        for(int i=idx;i<n+1;i++)
        {
            current.push_back(i);  //consider the current element i
            helper(i+1,k,current,n); // generate combinations
            current.pop_back(); //proceed to next element
        }
    }
    
    vector<vector<int>> combine(int n, int k) {
        vector<int>current;
        helper(1,k,current,n);
        return ans; //return answer
    }
};
```
**For similar problems: [Backtracking Collection](https://leetcode.com/discuss/interview-question/1141947/backtracking-study-and-analysis)**

If you like, please **UPVOTE**


# Python Solution:
###### Backtracking
Backtracking is a general algorithm for finding all (or some) solutions to some computational problems which incrementally builds candidates to the solution and abandons a candidate ("backtracks") as soon as it determines that the candidate cannot lead to a valid solution. 

It is due to this backtracking behaviour, the backtracking algorithms are often much faster than the brute-force search algorithm, since it eliminates many unnecessary exploration. 

```
def backtrack(candidate):
    if find_solution(candidate):
        output(candidate)
        return
    
    #### iterate all possible candidates.
    for next_candidate in list_of_candidates:
        if is_valid(next_candidate):
            #### try this partial candidate solution
            place(next_candidate)
            #### given the candidate, explore further.
            backtrack(next_candidate)
            #### backtrack
            remove(next_candidate)
```

Overall, the enumeration of candidates is done in two levels: 
1) at the first level, the function is implemented as recursion. At each occurrence of recursion, the function is one step further to the final solution.  
2) as the second level, within the recursion, we have an iteration that allows us to explore all the candidates that are of the same progress to the final solution.  

###### Code
Here we have to explore all combinations of numbers from 1 to n of length k. Indeed, we could solve the problem with the paradigm of backtracking.

Problem - combinations
Decision space- numbers from 1 to n without repetation
Output- all combinatins of numbers from 1 to n of size k

**Python 3**
```
def combine(self, n, k):   
		sol=[]
        def backtrack(remain,comb,nex):
			#### solution found
            if remain==0:
                sol.append(comb.copy())
            else:
				#### iterate through all possible candidates
                for i in range(nex,n+1):
					#### add candidate
                    comb.append(i)
					#backtrack
                    backtrack(remain-1,comb,i+1)
					#### remove candidate
                    comb.pop()
            
        backtrack(k,[],1)
        return sol
```
- Given an empty array, the task is to add numbers between 1 to n to the array upto size of k. We could model the each step to add a number as a recursion function (i.e. backtrack() function).

- At each step, technically we have 9 candidates at hand to add to the array. Yet, we want to consider solutions that lead to a valid case (i.e. is_valid(candidate)). Here the validity is determined by whether the number is repeated or not. Since in the loop, we iterate from nex to n+1, the numbers before nex are already visited and cannot be added to the array. Hence, we dont arrive at an invalid case.

- Then, among all the suitable candidates, we add different numbers using `comb.append(i)` i.e. place(next_candidate). Later we can revert our decision with `comb.pop()` i.e.  remove(next_candidate), so that we could try out the other candidates.

- The backtracking would be triggered at the points where the decision space is complete i.e. `nex` is 9 or when the size of the` comb `array becomes` k`. At the end of the backtracking, we would enumerate all the possible combinations.

###### Practice problems on backtracking
*Easy*

[Binary watch](http://)

*Medium*

[Permutations](http://)
[Permutations II](http://)
[Combination sum III](http://)

*Hard*

[N Queens](http://)
[N Queen II](http://)
[Sudoku solver](http://)

**Notes**
* For more examples and detailed explanation refer [Recursion II](http://)
* Any suggestions are welcome.
