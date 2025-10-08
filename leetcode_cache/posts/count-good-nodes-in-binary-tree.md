# Cpp Solution:
**UPVOTE IF HELPFuuL**

**APPROACH**

Any sort of traversal would work here.
While traversing the tree, keep a variable that stores the maximum value till now in the path.
Compare it with node value to decide whether it is a ood node or not.


**BASE CASE**
* Return ```0```, whenever ```root == NULL```

**RECURSIVE CALL**
* Call the funtion for both ```root->left``` and ```root->right``` and changing the max value to ```max(max_till_now,root->val)```

**SELF-WORK**
* Get answer recursively for next nodes.
* If ```root->val > max_value_till_now``` increment the answer by one.

**UPVOTE IF HELPFuuL**

**cpp**
```
class Solution {
public:
    
    int solve(TreeNode* root,int hi){
        if (root){
            int k=solve(root->left, max(hi,root->val)) + solve(root->right, max(hi,root->val));
            if (root->val>=hi){
                k++;
            }
            return k;
        }
        return 0;
    }
    int goodNodes(TreeNode* root) {
        return solve(root,-10001);
    }
};
```
**PYTHON**
```
class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        def solve(root,val):
            if root:
                k = solve(root.left, max(val,root.val)) + solve(root.right, max(val,root.val))
                if root.val >= val:
                    k+=1
                return k
            return 0
        return solve(root,root.val)
```




# Python Solution:
**Idea:**
1. DFS through every path, and keep tracking of biggest value(curMax) in the path.
2. If current node is `>=` the biggest value in the path, we add the answer by one.

Here's an example to show how the code works:

(In **Python**, we use list as a global valuable)
<iframe src="https://leetcode.com/playground/EunmHB7o/shared" frameBorder="0" width="1000" height="400"></iframe>

**Please UPVOTE if you LIKE!!!**

