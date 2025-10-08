# Cpp Solution:
#### Consider
```
                    Please Upvote If You Find It Helpful
```
#### Intuition
As we have to find the **Maximum Height of Tree**.
So, first we find the height of **Left Subtree and Right Subtree** of root node.
And we return the **maximum height** from **Left Subtree and Right Subtree** `+` `1`
<!-- Describe your first thoughts on how to solve this problem. -->

#### Approach : DFS
    Example : root = [3,9,20,null,8,15,7,null,null,null,null,10]


<!-- Describe your approach to solving the problem. -->

#### Complexity
- Time complexity: O(n) : As we are traversing each node of tree.
<!-- Add your time complexity here, e.g. $$O(n)$$ -->

- Space complexity: O(Height of tree) : Recursive stack space
<!-- Add your space complexity here, e.g. $$O(n)$$ -->

#### Code
#### cpp
```
class Solution {
public:
    int maxDepth(TreeNode* root) {
        if(root == NULL)
            return 0;
        int lh = maxDepth(root->left);
        int rh = maxDepth(root->right);
        return max(lh, rh) + 1;
    }
};
```
#### Python
```
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        leftSubtree = self.maxDepth(root.left)
        RightSubtree = self.maxDepth(root.right)
        return max(leftSubtree, RightSubtree) + 1
```
```
                            Give a . It motivates me alot
```
Let's Connect On [Linkedin](https://www.linkedin.com/in/naman-agarwal-0551aa1aa/)


# Python Solution:
**UPVOTE if you like (◠‿◠), If you have any question, feel free to ask.**

To calculate the maximum depth we can use the Depth-First Search. We call a helper function recursively and return the maximum depth between left and right branches. 

Time: **O(N)** - for DFS
Space: **O(N)** - for the recursive stack

Runtime: 40 ms, faster than **89.54%** of Python3 online submissions for Maximum Depth of Binary Tree.
Memory Usage: 16.3 MB, less than **18.15%** of Python3 online submissions for Maximum Depth of Binary Tree.

```
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        def dfs(root, depth):
            if not root: return depth
            return max(dfs(root.left, depth + 1), dfs(root.right, depth + 1))
                       
        return dfs(root, 0)
```

**UPVOTE if you like (◠‿◠), If you have any question, feel free to ask.**