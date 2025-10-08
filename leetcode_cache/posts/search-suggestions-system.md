# Cpp Solution:
**✅APPROACH : 1**
#### VERY EASY SOLUTION -> NO THINKING NEEDED JUST DO WHAT IS SAID IN QUESTION-->
* ***sort the string list***
* ***create a temp vector to store the answer in each stage and then push it back***

```
vector<vector<string>> suggestedProducts(vector<string>& products, string searchWord) {
        int n=products.size();
        sort(products.begin(),products.end());
        vector<vector<string>>ans;
        vector<string>temp;
        string curr="";
        for(auto c:searchWord){
            curr+=c;                // adding character, like -> m-->mo-->mou-->mous--->mouse
            temp.clear();         //reusing the same vector
            for(int i=0;i<n;i++){
                string s=products[i];
                if(s.substr(0,curr.length())==curr){              //finding the prefix containing words in the list
                    temp.push_back(s);
                }
                if(temp.size()==3)break;         //question asked for 3 words so we break at 3
            }
            ans.push_back(temp);
        }
        return ans;
    }
```

#### ✔ THIS WAS A VERY EASY SOLUTION BUT IT TAKES A LOT OF TIME ---> SO WE NEED TO OPTIMIZE IT

#### ✔ FOR OPTIMIZING WE USE BINARY SEARCH 

#### ✔ WHY BINARY SEARCH?? WHERE AND HOW??

**LETS SEE---->**

* **When the list is sorted the we know they are in increasing order(lexographically)**
* **if we find 'mou' first at the index 3 then we are sure that we can not find any word containing 'mou' before index 3-->Why?? --> as before index 3 the words are smaller and in the sorted list we find it for the first time at index 3**
* **How to find the index 3(as example) then?? --> we will use lower_bound() -> it returns the first occurance of searched element**
* **lower_bound() gives us the index in a binary search manner---> you can use lower_bound() stl or write a function for yourself**

```
vector<vector<string>> suggestedProducts(vector<string>& products, string searchWord) {
        auto start=products.begin();
        sort(start,products.end());
        vector<vector<string>>ans;
        vector<string>temp;
        string curr="";
        for(auto c:searchWord){
            curr+=c;
            temp.clear();                       //upto this same as previous code
            start=lower_bound(start,products.end(),curr);      // providing first occurance
            for(int i=0;i<3 && start+i!=products.end();i++){         //question asked 3 times so i<3 and start+i!=products.end() -> checks if we are out of index or not
                string s=*(start+i);        //(start+i) gives the pointer and *(start+i) gives the value at the pointer->here string
                if(s.find(curr))break;         //if we dont find the curr then we are sure that we are not going to find it in the upcoming words as they are in sorted manner
                temp.push_back(s);
            }
            ans.push_back(temp);
        }
        return ans;
    }
```
####  ✅ Hope this helped a little bit--> if so please upvote it.



✅ Happy Coding 




# Python Solution:
*(Note: This is part of a series of Leetcode solution explanations. If you like this solution or find it useful,* ***please upvote*** *this post.)*

####### ***Idea:***

Despite the fact that the clues suggest a **binary search** and a **trie**, the optimal solution to this problem needs neither. The substrings formed by adding one letter at a time from the search word (**S**) are naturally already in lexicographical order, as are the results that we're instructed to push into our answer array (**ans**).

So if we sort the products array (**P**), we should only ever need to iterate through **P** once during the entire remaining process of the solution with a **time complexity** of **O(N)**. A single binary search would only require **log(N) time**, but we'd have to perform **M = S.length** binary searches, so in total they would take **O(M * log(N)) time**, compared to the **O(N)** time of a simple iteration.

With constraints of **1000** on both **M** and **N**, the binary search route would max out at a worse time complexity than iteration. Regardless, the sort itself, which is required for both, requires **O(N * log(N))** time already, so neither option can decrease the overall time complexity required.

So in order to only require a single pass through **P**, we should keep track of the current bounds for the range of matches (**left, right**), then we'll iterate through the characters (**c**) of **S**. At each iteration, we'll first want to move **left** forward and **right** back to narrow the range of matches based on the new value of **c**.

Then we can add the next three elements of **P** to our result array (**res**), as long as they fall inside the range **[left, right]**. Once that's done, we can add **res** to **ans** and move to the next iteration.

Once we've finished iterating through **S**, we can **return ans**.

 - _**Time Complexity: O(N * log(N))** where **N** is the length of **P**_
 - _**Space Complexity: O(1)** excluding output space required for **ans**_

####### ***Javascript Code:***

The best result for the code below is **108ms / 49.5MB** (beats 100% / 99%).
```javascript
var suggestedProducts = function(P, S) {
    P.sort()
    let ans = [], left = 0, right = P.length - 1
    for (let i = 0; i < S.length; i++) {
        let c = S.charAt(i), res = []
        while (P[left]?.charAt(i) < c) left++
        while (P[right]?.charAt(i) > c) right--
        for (let j = 0; j < 3 && left + j <= right; j++)
            res.push(P[left+j])
        ans.push(res)
    }
    return ans
};
```

####### ***Python Code:***

The best result for the code below is **60ms / 16.8MB** (beats 99% / 99%).
```python
class Solution:
    def suggestedProducts(self, P: List[str], S: str) -> List[List[str]]:
        P.sort()
        ans, left, right = [], 0, len(P) - 1
        for i in range(len(S)):
            c, res = S[i], []
            while left <= right and (len(P[left]) == i or P[left][i] < c): left += 1
            while left <= right and (len(P[right]) == i or P[right][i] > c): right -= 1
            for j in range(3):
                if left + j > right: break
                else: res.append(P[left+j])
            ans.append(res)
        return ans
```

####### ***Java Code:***

The best result for the code below is **6ms / 44.5MB** (beats 100% / 68%).
```java
class Solution {
    public List<List<String>> suggestedProducts(String[] P, String S) {
        Arrays.sort(P);
        List<List<String>> ans = new ArrayList<>();
        int left = 0, right = P.length - 1;
        for (int i = 0; i < S.length(); i++) {
            List<String> res = new ArrayList<>();
            char c = S.charAt(i);
            while (left <= right && (P[left].length() == i || P[left].charAt(i) < c)) left++;
            while (left <= right && (P[right].length() == i || P[right].charAt(i) > c)) right--;
            for (int j = 0; j < 3 && left + j <= right; j++)
                res.add(P[left+j]);
            ans.add(res);
        }
        return ans;
    }
}
```

####### ***cpp Code:***

The best result for the code below is **32ms / 26.2MB** (beats 96% / 86%).
```c++
class Solution {
public:
    vector<vector<string>> suggestedProducts(vector<string>& P, string S) {
        sort(P.begin(), P.end());
        vector<vector<string>> ans;
        int left = 0, right = P.size() - 1;
        for (int i = 0; i < S.length(); i++) {
            vector<string> res;
            char c = S[i];
            while (left <= right && (P[left].length() == i || P[left][i] < c)) left++;
            while (left <= right && (P[right].length() == i || P[right][i] > c)) right--;
            for (int j = 0; j < 3 && left + j <= right; j++)
                res.push_back(P[left+j]);
            ans.push_back(res);
        }
        return ans;
    }
};
```