# Cpp Solution:
#### Video Solution (`Aryan Mittal`) - Link in LeetCode Profile
`Maximum Twin Sum of a Linked List` by `Aryan Mittal`



#### Approach & Intution












#### Code
```cpp
class Solution {
    public:
     int pairSum(ListNode* head) {
        ListNode* slow = head;
        ListNode* fast = head;
        int maxVal = 0;

        while(fast && fast -> next)
        {
            slow = slow -> next;
            fast = fast -> next -> next;
        }

        ListNode *nextNode, *prev = NULL;
        while (slow) {
            nextNode = slow->next;
            slow->next = prev;
            prev = slow;
            slow = nextNode;
        }

        while(prev)
        {
            maxVal = max(maxVal, head -> val + prev -> val);
            prev = prev -> next;
            head = head -> next;
        }

        return maxVal;
    }
};
```
```Java
class Solution {
    public int pairSum(ListNode head) {
        ListNode slow = head;
        ListNode fast = head;
        int maxVal = 0;

        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }

        ListNode nextNode, prev = null;
        while (slow != null) {
            nextNode = slow.next;
            slow.next = prev;
            prev = slow;
            slow = nextNode;
        }

        while (prev != null) {
            maxVal = Math.max(maxVal, head.val + prev.val);
            prev = prev.next;
            head = head.next;
        }

        return maxVal;
    }
}
```
```Python
class Solution:
    def pairSum(self, head):
        slow = head
        fast = head
        maxVal = 0

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        nextNode, prev = None, None
        while slow:
            nextNode = slow.next
            slow.next = prev
            prev = slow
            slow = nextNode

        while prev:
            maxVal = max(maxVal, head.val + prev.val)
            prev = prev.next
            head = head.next

        return maxVal
```


# Python Solution:
**cpp :**

```
int pairSum(ListNode* head) {
	ListNode* slow = head;
	ListNode* fast = head;
	int maxVal = 0;

	// Get middle of linked list
	while(fast && fast -> next)
	{
		fast = fast -> next -> next;
		slow = slow -> next;
	}

	// Reverse second part of linked list
	ListNode *nextNode, *prev = NULL;
	while (slow) {
		nextNode = slow->next;
		slow->next = prev;
		prev = slow;
		slow = nextNode;
	}

	// Get max sum of pairs
	while(prev)
	{
		maxVal = max(maxVal, head -> val + prev -> val);
		prev = prev -> next;
		head = head -> next;
	}

	return maxVal;
}
```


**Python :**

```
def pairSum(self, head: Optional[ListNode]) -> int:
	slow, fast = head, head
	maxVal = 0

	#### Get middle of linked list
	while fast and fast.next:
		fast = fast.next.next
		slow = slow.next

	#### Reverse second part of linked list
	curr, prev = slow, None

	while curr:       
		curr.next, prev, curr = prev, curr, curr.next   

	#### Get max sum of pairs
	while prev:
		maxVal = max(maxVal, head.val + prev.val)
		prev = prev.next
		head = head.next

	return maxVal
```

**Like it ? please upvote !**