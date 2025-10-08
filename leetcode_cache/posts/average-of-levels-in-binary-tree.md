# Cpp Solution:
**Approach #1 :** ***Depth First Search*** 
This can be done by applying dfs and keeping track of the current depth . We will keep a sum of elements at a particular depth and will also store the no. of elements encounter for a  depth.
.
.

.
.

```
 vector<pair<long,int>> count;       //  stores ( sum of a level , no of elements in that level)
    void dfs(TreeNode* root,int depth){     
        if(!root)return;
        int a = root->val;
        if(count.size()<=depth){             // to check if we have any entry corresponding to current depth 
            count.push_back({a,1});           //  if  we are at depth 1 and only depth 0 is completed then count.size()=1
        }
        else{
            count[depth].first += a;
            count[depth].second++;
        }
        dfs(root->left,depth+1);
        dfs(root->right,depth+1);    
    }
	
    vector<double> averageOfLevels(TreeNode* root) {  
        count.clear();
        dfs(root,0);
        vector<double> ans;
        for(int i=0;i<count.size();i++){
            ans.push_back((double)count[i].first/count[i].second);    // pushing in averages
        }
        return ans;
        
    }
```
.
.
.
**Approach #2 :** ***Breadth First Search/Level Order Traversal*** 
This can also be done by traversing level by level , we again need to store the sum and count of a level .As soon as a level ends, (which we get to know by encountering `NULL`) we push in the average and initialize sum and count of elements again for next level.
.
.

.
.

```
        vector<double> ans;
        queue<TreeNode*> q;
        q.push(root);
        q.push(NULL);                  // to mark end of a level 
        long long sum =0,count = 0;
        while(q.size()){
            TreeNode* cur = q.front();
            q.pop();
            if(!cur){
                ans.push_back((double)sum/count);     //  pushing in averages
                sum = 0,count = 0;
                q.push(NULL);
                if(!q.front())break;
            }
            else{
                count++;
                sum += cur->val;
                if(cur->left)q.push(cur->left);
                if(cur->right)q.push(cur->right);
            }
        }
 
        return ans;
```

.
.
***Thanks!***


# Python Solution:
*(Note: This is part of a series of Leetcode solution explanations. If you like this solution or find it useful,* ***please upvote*** *this post.)*

####### ***Idea:***

A problem talking about levels in a binary tree should immediately bring to mind a **breadth-first search** (**BFS**) approach. The classic BFS approach for a binary tree is to use a **queue** and push each queue entry's children onto the end of the queue. This way, the queue will run to the end of the row/level before moving onto the next level.

When a problem requires you to isolate a level, you can simply take the length of the queue at the start of the row and then once you've processed that many nodes from the queue, you'll know that you're ready to start the next row.

So as long as the queue exists, we'll take each row, sum the row's values (**row**), then divide by the length of the row (**qlen**) to find the average, pushing each average into our answer array (**ans**).


####### ***Implementation:***

The code for all four languages is almost identical.

####### ***Javascript Code:***

The best result for the code below is **84ms / 43.2MB** (beats 98% / 73%).
```javascript
var averageOfLevels = function(root) {
    let q = [root], ans = []
    while (q.length) {
        let qlen = q.length, row = 0
        for (let i = 0; i < qlen; i++) {
            let curr = q.shift()
            row += curr.val
            if (curr.left) q.push(curr.left)
            if (curr.right) q.push(curr.right)
        }
        ans.push(row/qlen)
    }
    return ans
};
```

####### ***Python Code:***

The best result for the code below is **44ms / 16.3MB** (beats 92% / 100%).
```python
class Solution:
    def averageOfLevels(self, root: TreeNode) -> List[float]:
        q, ans = [root], []
        while len(q):
            qlen, row = len(q), 0
            for i in range(qlen):
                curr = q.pop(0)
                row += curr.val
                if curr.left: q.append(curr.left)
                if curr.right: q.append(curr.right)
            ans.append(row/qlen)
        return ans
```

####### ***Java Code:***

The best result for the code below is **2ms / 40.5MB** (beats 82% / 97%).
```java
class Solution {
    public List<Double> averageOfLevels(TreeNode root) {
        Queue<TreeNode> q = new LinkedList<>(List.of(root));
        List<Double> ans = new ArrayList<>();
        while (q.size() > 0) {
            double qlen = q.size(), row = 0;
            for (int i = 0; i < qlen; i++) {
                TreeNode curr = q.poll();
                row += curr.val;
                if (curr.left != null) q.offer(curr.left);
                if (curr.right != null) q.offer(curr.right);
            }
            ans.add(row/qlen);
        }
        return ans;
    }
}
```

####### ***cpp Code:***

The best result for the code below is **8ms / 22.3MB** (beats 99% / 99%).
```c++
class Solution {
public:
    vector<double> averageOfLevels(TreeNode* root) {
        queue<TreeNode*> q;
        q.push(root);
        vector<double> ans;
        while (q.size()) {
            double qlen = q.size(), row = 0;
            for (int i = 0; i < qlen; i++) {
                TreeNode* curr = q.front(); q.pop();
                row += curr->val;
                if (curr->left) q.push(curr->left);
                if (curr->right) q.push(curr->right);
            }
            ans.push_back(row/qlen);
        }
        return ans;
    }
};
```