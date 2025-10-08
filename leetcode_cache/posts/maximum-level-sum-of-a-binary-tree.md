# Cpp Solution:
#### An Upvote will be encouraging 


#### Video Solution

#### Search ` Maximum Level Sum of a Binary Tree By Tech Wired`
#### or
#### Click the Link in my Profile


```Python
class Solution:
    def maxLevelSum(self, root):
        if not root:
            return 0

        queue = [root]
        max_level = 1
        max_sum = float('-inf')
        level = 1

        while queue:
            level_sum = 0
            next_level = []

            for node in queue:
                level_sum += node.val

                if node.left:
                    next_level.append(node.left)
                if node.right:
                    next_level.append(node.right)

            if level_sum > max_sum:
                max_sum = level_sum
                max_level = level

            queue = next_level
            level += 1

        return max_level

```
```Java
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;

    TreeNode(int val) {
        this.val = val;
        this.left = null;
        this.right = null;
    }
}

class Solution {
    public int maxLevelSum(TreeNode root) {
        if (root == null) {
            return 0;
        }

        Queue<TreeNode> queue = new LinkedList<>();
        queue.add(root);
        int maxLevel = 1;
        int maxSum = Integer.MIN_VALUE;
        int level = 1;

        while (!queue.isEmpty()) {
            int levelSum = 0;
            int levelSize = queue.size();

            for (int i = 0; i < levelSize; i++) {
                TreeNode node = queue.poll();
                levelSum += node.val;

                if (node.left != null) {
                    queue.add(node.left);
                }
                if (node.right != null) {
                    queue.add(node.right);
                }
            }

            if (levelSum > maxSum) {
                maxSum = levelSum;
                maxLevel = level;
            }

            level++;
        }

        return maxLevel;
    }
}

```
```cpp
class Solution {
public:
    int maxLevelSum(TreeNode* root) {
        if (root == nullptr) {
            return 0;
        }

        std::queue<TreeNode*> queue;
        queue.push(root);
        int maxLevel = 1;
        int maxSum = INT_MIN;
        int level = 1;

        while (!queue.empty()) {
            int levelSum = 0;
            int levelSize = queue.size();

            for (int i = 0; i < levelSize; i++) {
                TreeNode* node = queue.front();
                queue.pop();
                levelSum += node->val;

                if (node->left != nullptr) {
                    queue.push(node->left);
                }
                if (node->right != nullptr) {
                    queue.push(node->right);
                }
            }

            if (levelSum > maxSum) {
                maxSum = levelSum;
                maxLevel = level;
            }

            level++;
        }

        return maxLevel;
    }
};

```
#### An Upvote will be encouraging 


# Python Solution:
**Method 1: BFS**

Use BFS to find the sum of each level, then locate the level with largest sum.


```java
    public int maxLevelSum(TreeNode root) {
        int max = Integer.MIN_VALUE, maxLevel = 1;
        Queue<TreeNode> q = new LinkedList<>();
        q.offer(root);
        for (int level = 1; !q.isEmpty(); ++level) {
            int sum = 0;
            for (int sz = q.size(); sz > 0; --sz) {
                TreeNode n = q.poll();
                sum += n.val;
                if (n.left != null) { 
                    q.offer(n.left);
                }
                if (n.right != null) {
                    q.offer(n.right);
                }
            }
            if (max < sum) {
                max = sum;
                maxLevel = level;
            }
        }
        return maxLevel;
    }
```
```python
    def maxLevelSum(self, root: TreeNode) -> int:
        max, level, maxLevel = -float('inf'), 0, 0
        q = collections.deque()
        q.append(root)
        while q:
            level += 1
            sum = 0
            for _ in range(len(q)):
                node = q.popleft()
                sum += node.val
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            if max < sum:
                max, maxLevel = sum, level        
        return maxLevel
```

Python 3 BFS code - credit to **@leihao1313**
```python
    def maxLevelSum(self, root: TreeNode) -> int:
        ans, q, depth = (-math.inf, 0), [root], -1
        while q:
            ans = max(ans, (sum(node.val for node in q), depth))
            q = [kid for node in q for kid in (node.left, node.right) if kid]
            depth -= 1
        return -ans[1]
```		

------------------
**Method 2: DFS**
Use DFS to compute and store the sum of each level in an ArrayList, then locate the level with largest sum.
1. Recurse down from root, level of which is 0, increase level by 1 for each recursion down;
2. Use the level as the index of an ArrayList to store the sum of the correspoinding level;
3. Find the index of the max sum, then plus 1.

**Java**

```
    public int maxLevelSum(TreeNode root) {
        List<Integer> list = new ArrayList<>();
        dfs(root, list, 0);
        return 1 + IntStream.range(0, list.size()).reduce(0, (a, b) -> list.get(a) < list.get(b) ? b : a);
    }
    private void dfs(TreeNode n, List<Integer> l, int level) {
        if (n == null) { return; } 
        if (l.size() == level) { l.add(n.val); } // never reach this level before, add first value.
        else { l.set(level, l.get(level) + n.val); } // reached the level before, accumulate current value to old value.
        dfs(n.left, l, level + 1);
        dfs(n.right, l, level + 1);
    }
```
In case you are NOT comfortable with the Java 8 stream in the return statement, it can be written as:
```
        int maxLevel = 0;
        for (int i = 0; i < list.size(); ++i) {
            if (list.get(maxLevel) < list.get(i)) {
                maxLevel = i;
            }
        }
        return maxLevel + 1;
```

-
**Python 3**

```
    def maxLevelSum(self, root: TreeNode) -> int:
        def dfs(node: TreeNode, list: List, level: int) -> None:
            if not node:
                return
            if len(list) == level:
                list.append(node.val)
            else:
                list[level] += node.val
            dfs(node.left, list, level + 1)
            dfs(node.right, list, level + 1)
        list = []    
        dfs(root, list, 0)
        return 1 + list.index(max(list))
```

-
**Analysis:**

Time & space: `O(n), n` is the number of total nodes.