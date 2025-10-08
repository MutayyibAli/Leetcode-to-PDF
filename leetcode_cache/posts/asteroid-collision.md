# Cpp Solution:
**Intuition**

According to the question, positive values are moving to the right and negative values are moving to the left. We can apply the concept of relative velocity and make positive values as fixed and negative values now moving with double velocity in the negative direction. But, magnitude of velocity does not matter only the direction matters.

**Idea**

Lets consider an example:-

```[8, 9, 6, -7, -9, 12, 50, -34]```

Start iterating from the beginning. Whenever we encounter a positive value, we don't have to do anything. Since they are fixed, they won't attack anyone. But the moment we sees a negative value, we are sure it is going to attack positive values.

Imagine ```[8, 9, 6]``` are happily sitting inside the array. The moment ```-7``` enters, it will start knocking out positive values. This gives an idea we can use a stack to solve this problem.

**Explanation**

Lets see how to use this idea to code.

Consider the same example ```[8, 9, 6, -7, -9, 12, 50, -34]```
Initially ```i = 0```.

1. Whenever we encounter a positive value, we will simply push it to the stack.
2. The moment we encounter a negative value, we know some or all or zero positive values will be knocked out of the stack. The negative value may itself be knocked out or it may enter the stack.
We will keep on poping the elements from the stack while the ```asteroids[i] > s.top()```. But remember, negative asteroids can never pop another negative asteroids, since they will never meet them. So, the final condition is ```while(!s.empty() and s.top() > 0 and s.top() < abs(ast[i]))```, we will pop the elements.
3. We have to take care of the case when ```s.top() == asteroids[i]```. In this case one positive element will pop out and negative asteroid won't enter the stack.
4. If after knocking out elements stack becomes empty() or s.top() becomes negative, that means the current asteroids[i] will enter the stack.

**Code**
```
class Solution {
public:
    vector<int> asteroidCollision(vector<int>& ast) {
        int n = ast.size();
        stack<int> s;
        for(int i = 0; i < n; i++) {
            if(ast[i] > 0 || s.empty()) {
                s.push(ast[i]);
            }
            else {
                while(!s.empty() and s.top() > 0 and s.top() < abs(ast[i])) {
                    s.pop();
                }
                if(!s.empty() and s.top() == abs(ast[i])) {
                    s.pop();
                }
                else {
                    if(s.empty() || s.top() < 0) {
                        s.push(ast[i]);
                    }
                }
            }
        }
		// finally we are returning the elements which remains in the stack.
		// we have to return them in reverse order.
        vector<int> res(s.size());
        for(int i = (int)s.size() - 1; i >= 0; i--) {
            res[i] = s.top();
            s.pop();
        }
        return res;
    }
};
```

**Do upvote if this post is helpful to you**

**Edit** - Thanks for the upvote and comments, do follow me on twitter https://twitter.com/DevTalesShrey where I regularly post coding articles.


# Python Solution:
###### Explanation
- Intuition, when adding a new asteroid, there are 2 situation (collision or no collsion)
	- Collision (left meaning previous asteroid, right meaning current asteroid)
		- Left destroyed right, e.g. `3, -1`
		- Right destroyed left, e.g. `1, -3`
		- Both destroyed, e.g. `2, -2`
	- No collision
- It seems like scenarios can be analyzed linearly with some condition check on neighbors, intuitively, `stack` is a good tool to use
- So let's focus on 3 collision situation, for each new `right` asteroid
	- If left destroyed right, then no more to destroy, break
	- If both destroyed, no more to destroy, break
	- If right destroyed left, then there is a chance it could destroy more on the left, thus
		- pop out left from stack, repeat check again
	- If stack becomes empty, meaning right destroyed all left asteroids, append right to stack
- Time Complexity: `O(N)`
###### Implementation
<iframe src="https://leetcode.com/playground/ee8uH7fr/shared" frameBorder="0" width="500" height="250"></iframe>