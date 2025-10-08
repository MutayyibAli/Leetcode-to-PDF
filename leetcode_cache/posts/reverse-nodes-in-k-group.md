# Cpp Solution:
#### Recursive solution

Recursive solution has `O(n)` space complexity because of call stacks.

```c++
	ListNode* reverseKGroup(ListNode* head, int k) {
        ListNode* cursor = head;
        for(int i = 0; i < k; i++){
            if(cursor == nullptr) return head;
            cursor = cursor->next;
        }
        ListNode* curr = head;
        ListNode* prev = nullptr;
        ListNode* nxt = nullptr;
        for(int i = 0; i < k; i++){
            nxt = curr->next;
            curr->next = prev;
            prev = curr;
            curr = nxt;
        }
        head->next = reverseKGroup(curr, k);
        return prev;
    }
```


******************************************************************************************


#### Iterative solution

Iterative solution has `O(1)` space complexity.

```c++
	ListNode* reverseKGroup(ListNode* head, int k) {
        ListNode* dummy = new ListNode(0);
        dummy->next = head;
        ListNode* before = dummy;
        ListNode* after = head;
        ListNode* curr = nullptr;
        ListNode* prev = nullptr;
        ListNode* nxt = nullptr;
        while(true){
            ListNode* cursor = after;
            for(int i = 0; i < k; i++){
                if(cursor == nullptr) return dummy->next;
                cursor = cursor->next;
            }
            curr = after;
            prev = before;
            for(int i = 0; i < k; i++){
                nxt = curr->next;
                curr->next = prev;
                prev = curr;
                curr = nxt;
            }
            after->next = curr;
            before->next = prev;
            before = after;
            after = curr;
        }
    }
```


# Python Solution:
Use a dummy head, and

l, r :          define reversing range

pre, cur :  used in reversing, standard reverse linked linked list method

jump :      used to connect last node in previous k-group to first node in following k-group

    def reverseKGroup(self, head, k):
        dummy = jump = ListNode(0)
        dummy.next = l = r = head
        
        while True:
            count = 0
            while r and count < k:   #### use r to locate the range
                r = r.next
                count += 1
            if count == k:  #### if size k satisfied, reverse the inner linked list
                pre, cur = r, l
                for _ in range(k):
                    cur.next, cur, pre = pre, cur.next, cur  #### standard reversing
                jump.next, jump, l = pre, l, r  #### connect two k-groups
            else:
                return dummy.next