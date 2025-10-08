# Cpp Solution:
    class MinStack {
    private:
	    stack<int> s1;
	    stack<int> s2;
    public:
	    void push(int x) {
		    s1.push(x);
		    if (s2.empty() || x <= getMin())  s2.push(x);	    
        }
        void pop() {
		    if (s1.top() == getMin())  s2.pop();
		    s1.pop();
	    }
        int top() {
		    return s1.top();
	    }
        int getMin() {
		    return s2.top();
	    }
    };


# Python Solution:
```cpp
class MinStack {
public:
    typedef struct node{
        int v;
        int minUntilNow;
        node* next;
    }node;

    MinStack() : topN(nullptr){
        
    }
    
    void push(int val) {
        node* n = new node;
        n->v = n->minUntilNow = val;
        n->next = nullptr;
        
        if(topN == nullptr){
            topN = n;
        }

        else{
            n->minUntilNow = min(n->v,topN->minUntilNow);
            n->next = topN;
            topN = n;
        }
    }
    
    void pop() {
        topN = topN->next;
    }
    
    int top() {
        return topN->v;
    }
    
    int getMin() {
        return topN->minUntilNow;
    }

    private:
    node* topN;
};
```

```Python3
class MinStack:

    def __init__(self):
        self.stack = []
        self.minStack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if self.minStack:
            val = min(self.minStack[-1],val)
        self.minStack.append(val)

    def pop(self) -> None:
        self.stack.pop()
        self.minStack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.minStack[-1]
```

```Java
class MinStack {
    LinkedList<TplusMin> stack;
    private class TplusMin {
        int val;
        int min;
        public TplusMin(int val, int min) {
            this.val = val;
            this.min = min;
        }
    }

    public MinStack() {
        stack = new LinkedList<>();
    }
    
    public void push(int val) {
        int newMin;
        if (stack.size() == 0){
            newMin = val;
        }
        else {
            int currentMin = stack.getFirst().min;
            newMin = val < currentMin ? val : currentMin;
        }
        stack.addFirst(new TplusMin(val, newMin));
    }
    
    public void pop() {
        stack.removeFirst();
    }
    
    public int top() {
        return stack.peekFirst().val;
    }
    
    public int getMin() {
        return stack.peekFirst().min;
    }
}
```
