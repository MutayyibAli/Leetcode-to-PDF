# Cpp Solution:
```
The way to think of a solution to this is that when we are looking a path in a tree its unidirectional and cannot retrace back what i mean by that is:
    _
  / 1 \ 
 / / \ \ <-----path that goes like a depth first search without backtracking
/ 2   3 v  

So a way to solve this is that if i am at a node i can choose a left or right subtree but if i choose both this is the only subtree that will contain my maximum

I first set my max_sum to INT_MIN.
I can do either either of the options presented:
1.I can choose to take up the left subtree or drop it.
2.I can either choose to take up the right subtree or drop it.
3.I check for a possibility whether if i were to take both left subtree and right subtree would that beat my current max_sum?
Lets consider
   -10
   / \
  9  20
    /  \
   15   7
I do my postorder traversal with a bit of variation:-

int l=max(max_gain(root->left),0);
int r=max(max_gain(root->right),0);
But why?
This is because I have the option to choose the left or right subtree or whether i will just settle with my root value.

So I do my regular postorder traversal and do the above steps
I hit 9

    9
   / \
NULL  NULL

int l=0,r=0(Base condition)
i store the value of 9+0+0 in a variable
Then check if this is greater than maxsum or not is so i update it.
As my max_sum was INT_MIN it gets updated to 9

Now we explore the right tree of root which reaches 15

    15
   / \
NULL  NULL

int l=0,r=0(Base condition)
i store the value of 9+0+0 in a variable
Then check if this is greater than maxsum or not is so i update it.
As my max_sum was 9 it gets updated to 15

Similarly with 7 but 7 doesnt beat the max_sum so nothing happens.

Now we backtrack 20
here int r=7(as 7>0)
     int l=15(as 15>0)
 now i check whether 20+15+7(considering this subtree to be my maximum)
 as 42>15 max_sum=42
 Now what if we dont consider this subtree?

 Then we choose 20 and maximum of its left or right subtree
 so we send return root->val+max(l,r) to our recursion stack
 so when i reach the root it would be like this
           -10
           /  \    <----I considered 15 and 20 because its along a path and is greater than 20+7
          9    35
  int l=9
      r=35
      check whether 9+35+-10=34 beats max_sum
      34<42 so nothing happens and we return -10+max(9,35)=25 to the caller after which we break out of the helper function and we get max_sum as 42.

    int max_sum=INT_MIN;
    int max_gain(TreeNode* root)
    {
        if(!root)return 0;
        int l=max(max_gain(root->left),0);
        int r=max(max_gain(root->right),0);
        int new_price=root->val+l+r;
        max_sum=max(max_sum,new_price);
        return root->val+max(l,r);
    }
    int maxPathSum(TreeNode* root) {
        max_gain(root);
        return max_sum;
    }
```


# Python Solution:
This problem requires quite a bit of quirky thinking steps. Take it slow until you fully grasp it.

#### **Basics**



#### **Base cases**



#### **Important Observations**
* These important observations are very important to understand `Line 9` and `Line 10` in the code.
	* For example, in the code (`Line 9`), we do something like `max(get_max_gain(node.left), 0)`. The important part is: why do we take maximum value between 0 and maximum gain we can get from left branch? Why 0?
	* Check the two images below first.



* The important thing is "We can only get any sort of gain IF our branches are not below zero. If they are below zero, why do we even bother considering them? Just pick 0 in that case. Therefore, we do `max(<some gain we might get or not>, 0)`.

#### **Going down the recursion stack for one example**




* Because of this, we do `Line 12` and `Line 13`. It is important to understand the different between looking for the maximum path INVOLVING the current node in process and what we return for the node which starts the recursion stack. `Line 12` and `Line 13` takes care of the former issue and `Line 15` (and the image below) takes care of the latter issue.



* Because of this fact, we have to return like `Line 15`. For our example, for node 1, which is the recursion call that node 3 does for `max(get_max_gain(node.left), 0)`, node 1 cannot include both node 6 and node 7 for a path to include node 3. Therefore, we can only pick the max gain from left path or right path of node 1.


**Python**
``` python
1. class Solution:
2.     def maxPathSum(self, root: TreeNode) -> int:
3. 		max_path = float("-inf") #### placeholder to be updated
4. 		def get_max_gain(node):
5. 			nonlocal max_path #### This tells that max_path is not a local variable
6. 			if node is None:
7. 				return 0
8. 				
9. 			gain_on_left = max(get_max_gain(node.left), 0) #### Read the part important observations
10. 		gain_on_right = max(get_max_gain(node.right), 0)  #### Read the part important observations
11. 			
12. 		current_max_path = node.val + gain_on_left + gain_on_right #### Read first three images of going down the recursion stack
13. 		max_path = max(max_path, current_max_path) #### Read first three images of going down the recursion stack
14. 			
15. 		return node.val + max(gain_on_left, gain_on_right) #### Read the last image of going down the recursion stack
16. 			
17. 			
18. 	get_max_gain(root) #### Starts the recursion chain
19. 	return max_path		
```