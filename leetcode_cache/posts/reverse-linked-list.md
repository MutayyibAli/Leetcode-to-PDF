# Cpp Solution:
Not sure how this problem is expecting me to use less memory than this, but here is the deal:
* we are going to use 3 variables: `prevNode`, `head` and `nextNode`, that you can easily guess what are meant to represent as we go;
* we will initialise `prevNode` to `NULL`, while `nextNode` can stay empty;
* we are then going to loop until our current main iterator (`head`) is truthy (ie: not `NULL`), which would imply we reached the end of the list;
* during the iteration, we first of all update `nextNode` so that it acquires its namesake value, the one of the next node indeed: `head->next`;
* we then proceeding "reversing" `head->next` and assigning it the value of `prevNode`, while `prevNode` will become take the current value of `head`;
* finally, we update `head` with the value we stored in `nextNode` and go on with the loop until we can. After the loop, we return `prevNode`.

I know it is complex, but I find this gif from another platform to make the whole logic much easier to understand (bear in mind we do not need `curr` and will just use `head` in its place):



The code:

```cpp
class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode *nextNode, *prevNode = NULL;
        while (head) {
            nextNode = head->next;
            head->next = prevNode;
            prevNode = head;
            head = nextNode;
        }
        return prevNode;
    }
};
```

Relatively trivial refactor (the function does basically the same) with recursion and comma operator to make it one-line:

```cpp
class Solution {
public:
    ListNode* reverseList(ListNode *head, ListNode *nextNode = NULL, ListNode *prevNode = NULL) {
        return head ? reverseList(head->next, (head->next = prevNode, nextNode), head) : prevNode;
    }
};
```


# Python Solution:
#### **Java Solution (Recursive Approach):**
Runtime: 0 ms, faster than 100.00% of Java online submissions for Reverse Linked List.
```
class Solution {
    public ListNode reverseList(ListNode head) {
        // Special case...
        if (head == null || head.next == null) return head;
        // Create a new node to call the function recursively and we get the reverse linked list...
        ListNode res = reverseList(head.next);
        // Set head node as head.next.next...
        head.next.next = head;
        //set head's next to be null...
        head.next = null;
        return res;     // Return the reverse linked list...
    }
}
```

#### **cpp Solution (Iterative Approach):**
```
class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        // Special case...
        if(head == NULL || head->next == NULL)  return head;
        // Initialize prev pointer as the head...
        ListNode* prev = head;
        // Initialize curr pointer as the next pointer of prev...
        ListNode* curr = prev->next;
        // Initialize next of head pointer as NULL...
        head->next = NULL;
        // Run a loop till curr and prev points to NULL...
        while(prev != NULL && curr != NULL){
            // Initialize next pointer as the next pointer of curr...
            ListNode* next = curr->next;
            // Now assign the prev pointer to curr’s next pointer.
            curr->next = prev;
            // Assign curr to prev, next to curr...
            prev = curr;
            curr = next;
        }
        return prev;    // Return the prev pointer to get the reverse linked list...
    }
};
```

#### **Python Solution (Iterative Approach):**
Runtime: 18 ms, faster than 97.75% of Python online submissions for Reverse Linked List.
```
class Solution(object):
    def reverseList(self, head):
        #### Initialize prev pointer as NULL...
        prev = None
        #### Initialize the curr pointer as the head...
        curr = head
        #### Run a loop till curr points to NULL...
        while curr:
            #### Initialize next pointer as the next pointer of curr...
            next = curr.next
            #### Now assign the prev pointer to curr’s next pointer.
            curr.next = prev
            #### Assign curr to prev, next to curr...
            prev = curr
            curr = next
        return prev       #### Return the prev pointer to get the reverse linked list...
```
                
#### **JavaScript Solution (Recursive Approach):**
```
var reverseList = function(head) {
    // Special case...
    if (head == null || head.next == null) return head;
    // Create a new node to call the function recursively and we get the reverse linked list...
    var res = reverseList(head.next);
    // Set head node as head.next.next...
    head.next.next = head;
    //set head's next to be null...
    head.next = null;
    return res;     // Return the reverse linked list...
};
```

#### **C Language (Iterative Approach):**
```
struct ListNode* reverseList(struct ListNode* head){
    // Special case...
    if(head == NULL || head->next == NULL)  return head;
    // Initialize prev pointer as the head...
    struct ListNode* prev = head;
    // Initialize curr pointer as the next pointer of prev...
    struct ListNode* curr = prev->next;
    // Initialize next of head pointer as NULL...
    head->next = NULL;
    // Run a loop till curr and prev points to NULL...
    while(prev != NULL && curr != NULL){
        // Initialize next pointer as the next pointer of curr...
        struct ListNode* next = curr->next;
        // Now assign the prev pointer to curr’s next pointer.
        curr->next = prev;
        // Assign curr to prev, next to curr...
        prev = curr;
        curr = next;
    }
    return prev;    // Return the prev pointer to get the reverse linked list...
}
```

#### **Python3 Solution (Iterative Approach):**
```
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        #### Initialize prev pointer as NULL...
        prev = None
        #### Initialize the curr pointer as the head...
        curr = head
        #### Run a loop till curr points to NULL...
        while curr:
            #### Initialize next pointer as the next pointer of curr...
            next = curr.next
            #### Now assign the prev pointer to curr’s next pointer.
            curr.next = prev
            #### Assign curr to prev, next to curr...
            prev = curr
            curr = next
        return prev       #### Return the prev pointer to get the reverse linked list...
```
**I am working hard for you guys...
Please upvote if you found any help with this code...**