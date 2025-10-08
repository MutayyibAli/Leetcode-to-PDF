# Cpp Solution:
```cpp
class Solution {
public:
    vector<int> rightSideView(TreeNode* root) {
        vector<int>ans;
        queue<TreeNode*> q;
        if(root==NULL)
        return ans;
        q.push(root);
        while(1)
        {
            int size=q.size();
            if(size==0)
            return ans;
            vector<int> data;
            while(size--)
            {
                TreeNode* temp=q.front();
                q.pop();
                data.push_back(temp->val);
                if(temp->left!=NULL)
                q.push(temp->left);
                if(temp->right!=NULL)
                q.push(temp->right);
            }
            ans.push_back(data.back());
        }
    }
};
```

```Python3
from collections import deque
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        queue = deque()
        if root is None:
            return []
        
        if root.left is None and root.right is None:
            return [root.val]
        
        result = []
        queue.append(root)
        while queue:
            child_queue = deque()
            prev = -1
            while queue:
                curr = queue.popleft()

                if curr.left is not None:
                    child_queue.append(curr.left)

                if curr.right is not None:
                    child_queue.append(curr.right)
                
                prev = curr
            
            result.append(prev.val)
            queue = child_queue
        
        return result
```

```Java
class Solution {
    int maxlevel = 0;
    public List<Integer> rightSideView(TreeNode root) {
        List<Integer> list  = new ArrayList<>();
        right(root,1,list);
        return list ;
    }
    void right(TreeNode root,int level,List<Integer> list){
        if(root==null){
            return ;
        }
        if(maxlevel<level){
            list.add(root.val);
            maxlevel=level;
        }
        right(root.right,level+1,list);
        right(root.left,level+1,list);
        
    }
}
```



# Python Solution:
Solution 1: **Recursive, combine right and left:** 5 lines, 56 ms

Compute the right view of both right and left left subtree, then combine them. For very unbalanced trees, this can be O(n^2), though.

    def rightSideView(self, root):
        if not root:
            return []
        right = self.rightSideView(root.right)
        left = self.rightSideView(root.left)
        return [root.val] + right + left[len(right):]

Solution 2: **Recursive, first come first serve:** 9 lines, 48 ms

DFS-traverse the tree right-to-left, add values to the view whenever we first reach a new record depth. This is O(n).

    def rightSideView(self, root):
        def collect(node, depth):
            if node:
                if depth == len(view):
                    view.append(node.val)
                collect(node.right, depth+1)
                collect(node.left, depth+1)
        view = []
        collect(root, 0)
        return view

Solution 3: **Iterative, level-by-level:** 7 lines, 48 ms

Traverse the tree level by level and add the last value of each level to the view. This is O(n).

    def rightSideView(self, root):
        view = []
        if root:
            level = [root]
            while level:
                view += level[-1].val,
                level = [kid for node in level for kid in (node.left, node.right) if kid]
        return view