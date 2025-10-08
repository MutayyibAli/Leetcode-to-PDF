# Cpp Solution:
    class Solution {
    public:
        int evalRPN(vector<string>& tokens) {
            unordered_map<string, function<int (int, int) > > map = {
                { "+" , [] (int a, int b) { return a + b; } },
                { "-" , [] (int a, int b) { return a - b; } },
                { "*" , [] (int a, int b) { return a * b; } },
                { "/" , [] (int a, int b) { return a / b; } }
            };
            std::stack<int> stack;
            for (string& s : tokens) {
                if (!map.count(s)) {
                    stack.push(stoi(s));
                } else {
                    int op1 = stack.top();
                    stack.pop();
                    int op2 = stack.top();
                    stack.pop();
                    stack.push(map[s](op2, op1));
                }
            }
            return stack.top();
        }
    };


# Python Solution:
```
class Solution(object):
    def evalRPN(self, tokens):
        stack = []
        for t in tokens:
            if t not in "+-*/":
                stack.append(int(t))
            else:
                r, l = stack.pop(), stack.pop()
                if t == "+":
                    stack.append(l+r)
                elif t == "-":
                    stack.append(l-r)
                elif t == "*":
                    stack.append(l*r)
                else:
                    stack.append(int(float(l)/r))
        return stack.pop()
```