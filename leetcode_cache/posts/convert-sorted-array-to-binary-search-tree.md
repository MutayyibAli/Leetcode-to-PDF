# Cpp Solution:

    class Solution {
        TreeNode* sortedArrayToBST(vector<int>& nums, int start, int end){
            if(end<=start) return NULL; 
            int midIdx=(end+start)/2;
            TreeNode* root=new TreeNode(nums[midIdx]);
            root->left=sortedArrayToBST(nums, start, midIdx);
            root->right=sortedArrayToBST(nums, midIdx+1,end);
            return root;
        }
    public:
        TreeNode* sortedArrayToBST(vector<int>& nums) {
            return sortedArrayToBST(nums, 0,nums.size());
        }
    };


# Python Solution:
The idea is to find the root first, then recursively build each left and right subtree

    #### Definition for a  binary tree node
    #### class TreeNode:
    ####     def __init__(self, x):
    ####         self.val = x
    ####         self.left = None
    ####         self.right = None
    
    class Solution:
        #### @param num, a list of integers
        #### @return a tree node
        #### 12:37
        def sortedArrayToBST(self, num):
            if not num:
                return None
    
            mid = len(num) // 2
    
            root = TreeNode(num[mid])
            root.left = self.sortedArrayToBST(num[:mid])
            root.right = self.sortedArrayToBST(num[mid+1:])
    
            return root