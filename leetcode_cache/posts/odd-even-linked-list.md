# Cpp Solution:
**Firstly, thanks for refering to my solution :)**

**APPROACH :**
* The idea is to split the linked list into 2 : one containing all odd nodes and other containing all even nodes. And finally, attach the even node linked list at the end of the odd node linked list. 
* To split the linked list into even nodes & odd nodes, we traverse the linked list and keep connecting the consecutive odd nodes and even nodes (to maintain the order of nodes) and save the pointer to the first even node.
* Finally, we  insert all the even nodes at the end of the odd node list.




**Time Complexity :** O(n) - We traverse the linked list only once.

**Auxiliary Space :** O(1) - No extra space required

**Code :**
```
class Solution {
public:
    ListNode* oddEvenList(ListNode* head) {
        if(!head || !head->next || !head->next->next) return head;
        
        ListNode *odd = head;
        ListNode *even = head->next;
        ListNode *even_start = head->next;
        
        while(odd->next && even->next){
            odd->next = even->next; //Connect all odds
            even->next = odd->next->next;  //Connect all evens
            odd = odd->next;
            even = even->next;
        }
        odd->next = even_start;   //Place the first even node after the last odd node.
        return head; 
    }
};
```

**If you like my solution & explanation, PLEASE UPVOTE!!** 



# Python Solution:
#### ***Time : O(N) (Where N->length of LinkedList)***
#### ***Space : O(1)*** 






#### ***Hmm.... I Think you love this solution, Don't forget to upvote.*** 
#### Guys!!! UPVOTE is free of cost guys but matter alot for motivating me to post more valuable post.
#### if you don't want to upvote it's OK (No Problem)
#### **Thankyou:)** for both guys who ***upvote***   or ***downvote*** or ***novote***





