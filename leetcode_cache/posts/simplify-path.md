# Cpp Solution:
#### 71. Simplify Path
**KNOCKCAT**

Please ALso have a look to my Leetcode Repository Link Given Below :)
```
1. Easy cpp
2. Line by Line Explanation with Comments.
3. Detailed Explanation ✅
4. Stack Problem with Initution.
5. Please Upvote if it helps⬆️
6. Link to my Github Profile contains a repository of Leetcode with all my Solutions. ⬇️
	// If you Like the repository don't foget to star & fork the repository
```
``` ```
[LeetCode](https://github.com/knockcat/Leetcode)     **LINK TO LEETCODE REPOSITORY**

Please upvote my comment so that i get to win the 2022 giveaway and motivate to make such discussion post.
**Happy new Year 2023 to all of you**
**keep solving keep improving**
Link To comment
[Leetcode Give away comment](https://leetcode.com/discuss/general-discussion/2946993/2022-Annual-Badge-and-the-Giveaway/1734919)
``` ```

**EXPLANATION**
* Create a **Stack of String** with following condition.
	* **Iterate the loop till you doesn't reaches the end of string.**
	* If you **encounter a  "/" then ignore it.**
	* **Create a temp String** & **Iterate the while loop** till you **doesn't find  "/"** and **append it to temp**.
	* Now check if **temp  == "."** , t**hen ignore it**.
	* If **temp == ".."** then **pop the element from the stack if it exists.**
	* If **no of the above 2 matches** **push temp to stack** as you find a valid path.
	* **Check out temp** string on **basis of above conditions till you doesn't find "/".**
* 	Now **add all stack elements** to result as **res = "/" + st.top() + res**
* 	If **res.size() is 0** then **return "/"**  if no directory or file is present.
* 	At last **return res**.

```
Input: path = "/../"
Output: "/"
Input: path = "/home//foo/"
Output: "/home/foo"
```

**ALGORITHM**
* By looking at examples we can see that the above **simplification process** just **behaves like a stack**.
* **Whenever we encounter any file’s name**, **we simply push it into the stack**.
* when we come across **” . ”** **we do nothing**
* When **we find “..”** in our path, **we simply pop the topmost element** as we **have to jump back to parent’s directory.**
* When we **see multiple “////”** we **just ignore them** as **they are equivalent to one single “/”.** 
* After **iterating through the whole string** the **elements remaining in the stack** is our **simplified absolute path.**


``` ```
**CODE WITH EXPLANATION**
```
					// Please upvote if it helps 
class Solution {
public:
    string simplifyPath(string path) {
        
        stack<string> st;
        string res;
        
        for(int i = 0;  i<path.size(); ++i)
        {
            if(path[i] == '/')    
                continue;
            string temp;
			// iterate till we doesn't traverse the whole string and doesn't encounter the last /
            while(i < path.size() && path[i] != '/')
            {
				// add path to temp string
                temp += path[i];
                ++i;
            }
            if(temp == ".")
                continue;
			// pop the top element from stack if exists
            else if(temp == "..")
            {
                if(!st.empty())
                    st.pop();
            }
            else
			// push the directory file name to stack
                st.push(temp);
        }
        
		// adding all the stack elements to res
        while(!st.empty())
        {
            res = "/" + st.top() + res;
            st.pop();
        }
        
		// if no directory or file is present
        if(res.size() == 0)
            return "/";
        
        return res;
    }
};
```


# Python Solution:
#### Intuition
<!-- Describe your first thoughts on how to solve this problem. -->
The problem requires to convert a given absolute path to a simplified canonical path. The simplified canonical path should have the following format:
- The path starts with a single slash '/'.

- Any two directories are separated by a single slash '/'.

- The path does not end with a trailing '/'.

- The path only contains the directories on the path from the root directory to the target file or directory (i.e., no period '.' or double period '..').
#### Approach
<!-- Describe your approach to solving the problem. -->
The problem can be solved using a stack to keep track of the directories in the path. We split the input path by slash '/', iterate over the directories, and perform the following operations:

- Ignore the current directory '.' and empty directories.
- Go one level up for double period '..' by popping the top element from the stack if it is not empty.
- For any other directory, push it to the stack.
- Finally, we join the directories in the stack with slash '/' and add a slash at the beginning to form the simplified canonical path.

#### Complexity
- Time complexity:
<!-- Add your time complexity here, e.g. $$O(n)$$ -->
The time complexity of the algorithm is $$O(n)$$, where n is the length of the input path. This is because we iterate over each directory in the path only once.

- Space complexity:
<!-- Add your space complexity here, e.g. $$O(n)$$ -->
 The space complexity of the algorithm is $$O(n)$$ where n is the length of

 



#### Please Upvote
```
Thanks for visiting my solution. Keep Learning
Please give my solution an upvote! 
It's a simple way to show your appreciation and
keep me motivated. Thank you! 
```
#### Code
``` Java
class Solution {
    public String simplifyPath(String path) {
        Stack<String> stack = new Stack<>(); // create a stack to keep track of directories
        String[] directories = path.split("/"); // split the path by slash '/'
        for (String dir : directories) { // iterate over the directories
            if (dir.equals(".") || dir.isEmpty()) { // ignore the current directory '.' and empty directories
                continue;
            } else if (dir.equals("..")) { // go one level up for double period '..'
                if (!stack.isEmpty()) { // if stack is not empty, pop the top element
                    stack.pop();
                }
            } else { // for any other directory, push it to the stack
                stack.push(dir);
            }
        }
        return "/" + String.join("/", stack); // join the directories in the stack with slash '/' and add a slash at the beginning
    }
}
```
```JavaScript
/**
 * @param {string} path
 * @return {string}
 */
var simplifyPath = function(path) {
    const stack = [];
    const directories = path.split("/");
    for (const dir of directories) {
        if (dir === "." || !dir) {
            continue;
        } else if (dir === "..") {
            if (stack.length > 0) {
                stack.pop();
            }
        } else {
            stack.push(dir);
        }
    }
    return "/" + stack.join("/");
};

```
```cpp
class Solution {
public:
    string simplifyPath(string path) {
        stack<string> s;
        stringstream ss(path);
        string dir;
        while (getline(ss, dir, '/')) {
            if (dir.empty() || dir == ".") {
                continue;
            } else if (dir == "..") {
                if (!s.empty()) {
                    s.pop();
                }
            } else {
                s.push(dir);
            }
        }
        string res;
        while (!s.empty()) {
            res = "/" + s.top() + res;
            s.pop();
        }
        return res.empty() ? "/" : res;
    }
};

```
``` Python
class Solution(object):
    def simplifyPath(self, path):
        stack = []
        directories = path.split("/")
        for dir in directories:
            if dir == "." or not dir:
                continue
            elif dir == "..":
                if stack:
                    stack.pop()
            else:
                stack.append(dir)
        return "/" + "/".join(stack)

```
#### Please Comment
```
Thanks for visiting my solution comment below if you like it.
```