# Cpp Solution:
To apply DP, we define the state `dp[i][j]` to be the minimum number of operations to convert `word1[0..i)` to `word2[0..j)`.

For the base case, that is, to convert a string to an empty string, the mininum number of operations (deletions) is just the length of the string. So we have `dp[i][0] = i` and `dp[0][j] = j`.

For the general case to convert `word1[0..i)` to `word2[0..j)`, we break this problem down into sub-problems. Suppose we have already known how to convert `word1[0..i - 1)` to `word2[0..j - 1)` (`dp[i - 1][j - 1]`), if  `word1[i - 1] == word2[j - 1]`, then no more operation is needed and `dp[i][j] = dp[i - 1][j - 1]`.

If `word1[i - 1] != word2[j - 1]`, we need to consider three cases.

 1. **Replace** `word1[i - 1]` by `word2[j - 1]` (`dp[i][j] = dp[i - 1][j - 1] + 1`);
 2. If `word1[0..i - 1) = word2[0..j)` then **delete** `word1[i - 1]` (`dp[i][j] = dp[i - 1][j] + 1`);
 3. If `word1[0..i) + word2[j - 1] = word2[0..j)` then **insert** `word2[j - 1]` to `word1[0..i)` (`dp[i][j] = dp[i][j - 1] + 1`).

So when `word1[i - 1] != word2[j - 1]`, `dp[i][j]` will just be the minimum of the above three cases.

```cpp
class Solution {
public:
    int minDistance(string word1, string word2) {
        int m = word1.size(), n = word2.size();
        vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
        for (int i = 1; i <= m; i++) {
            dp[i][0] = i;
        }
        for (int j = 1; j <= n; j++) {
            dp[0][j] = j;
        }
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (word1[i - 1] == word2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = min(dp[i - 1][j - 1], min(dp[i][j - 1], dp[i - 1][j])) + 1;
                }
            }
        }
        return dp[m][n];
    }
};
```

Note that each time when we update `dp[i][j]`, we only need `dp[i - 1][j - 1]`, `dp[i][j - 1]` and `dp[i - 1][j]`. We may optimize the space of the code to use only two vectors.

```cpp
class Solution {
public:
    int minDistance(string word1, string word2) {
        int m = word1.size(), n = word2.size();
        vector<int> pre(n + 1, 0), cur(n + 1, 0);
        for (int j = 1; j <= n; j++) {
            pre[j] = j;
        }
        for (int i = 1; i <= m; i++) {
            cur[0] = i;
            for (int j = 1; j <= n; j++) {
                if (word1[i - 1] == word2[j - 1]) {
                    cur[j] = pre[j - 1];
                } else {
                    cur[j] = min(pre[j - 1], min(cur[j - 1], pre[j])) + 1;
                }
            }
            fill(pre.begin(), pre.end(), 0);
            swap(pre, cur);
        }
        return pre[n];
    }
};
```

Or even just one vector.

```cpp
class Solution {
public:
    int minDistance(string word1, string word2) {
        int m = word1.size(), n = word2.size(), pre;
        vector<int> cur(n + 1, 0);
        for (int j = 1; j <= n; j++) {
            cur[j] = j;
        }
        for (int i = 1; i <= m; i++) {
            pre = cur[0];
            cur[0] = i;
            for (int j = 1; j <= n; j++) {
                int temp = cur[j];
                if (word1[i - 1] == word2[j - 1]) {
                    cur[j] = pre;
                } else {
                    cur[j] = min(pre, min(cur[j - 1], cur[j])) + 1;
                }
                pre = temp;
            }
        }
        return cur[n];
    }
};
```


# Python Solution:
#### Intuition :
- Here we have to find the minimum edit distance problem between two strings word1 and word2. 
- The minimum edit distance is defined as the minimum number of operations required to transform one string into another.
<!-- Describe your first thoughts on how to solve this problem. -->

#### Approach :
- The approach here that I am using is dynamic programming. The idea is to build a 2D matrix dp where `dp[i][j] `represents the minimum number of operations required to transform the substring `word1[0...i-1]` into the substring `word2[0...j-1].`
#### How is Matrix built :
- The matrix is built iteratively using the following recurrence relation:
1. If `word1[i-1] == word2[j-1]`, then `dp[i][j] = dp[i-1][j-1]`. That is, no operation is required because the characters at positions `i-1` and `j-1` are already the same.
2. Otherwise, `dp[i][j]` is the minimum of the following three values:
- `dp[i-1][j-1] + 1`: replace the character at position `i-1` in `word1` with the character at position `j-1` in` word2`.
- `dp[i-1][j] + 1`: delete the character at position `i-1` in `word1.`
- `dp[i][j-1] + 1`: insert the character at position `j-1` in `word2` into `word1` at position `i`.
#### The base cases are:
- `dp[i][0] = i`: transforming `word1[0...i-1]` into an empty string requires `i` deletions.
- `dp[0][j] = j`: transforming an empty string into `word2[0...j-1] `requires `j` insertions.
<!-- Describe your approach to solving the problem. -->
#### Final Step :
- Finally, return `dp[m][n]`, which represents the minimum number of operations required to transform `word1 `into `word2`, where `m` is the length of `word1` and `n` is the length of `word2`.

#### Complexity
- Time complexity : O(mn)
<!-- Add your time complexity here, e.g. $$O(n)$$ -->

- Space complexity : O(mn)
<!-- Add your space complexity here, e.g. $$O(n)$$ -->

#### Please Upvote
```
Thanks for visiting my solution.
```
#### Codes [cpp |Java |Python3] : With Comments
```cpp
class Solution {
 public:
  int minDistance(string word1, string word2) {
    const int m = word1.length();//first word length
    const int n = word2.length();//second word length
    // dp[i][j] := min #### of operations to convert word1[0..i) to word2[0..j)
    vector<vector<int>> dp(m + 1, vector<int>(n + 1));

    for (int i = 1; i <= m; ++i)
      dp[i][0] = i;

    for (int j = 1; j <= n; ++j)
      dp[0][j] = j;

    for (int i = 1; i <= m; ++i)
      for (int j = 1; j <= n; ++j)
        if (word1[i - 1] == word2[j - 1])//same characters
          dp[i][j] = dp[i - 1][j - 1];//no operation
        else
          dp[i][j] = min({dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1]}) + 1;
                             //replace       //delete        //insert
    return dp[m][n];
  }
};
```
```Java
class Solution {
  public int minDistance(String word1, String word2) {
    final int m = word1.length();//first word length
    final int n = word2.length();///second word length
    // dp[i][j] := min #### of operations to convert word1[0..i) to word2[0..j)
    int[][] dp = new int[m + 1][n + 1];

    for (int i = 1; i <= m; ++i)
      dp[i][0] = i;

    for (int j = 1; j <= n; ++j)
      dp[0][j] = j;

    for (int i = 1; i <= m; ++i)
      for (int j = 1; j <= n; ++j)
        if (word1.charAt(i - 1) == word2.charAt(j - 1))//same characters
          dp[i][j] = dp[i - 1][j - 1];//no operation
        else
          dp[i][j] = Math.min(dp[i - 1][j - 1], Math.min(dp[i - 1][j], dp[i][j - 1])) + 1;                      //replace               //delete        //insert

    return dp[m][n];
  }
}

```
```Python
class Solution:
  def minDistance(self, word1: str, word2: str) -> int:
    m = len(word1)
    n = len(word2)
    #### dp[i][j] := min #### Of operations to convert word1[0..i) to word2[0..j)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
      dp[i][0] = i

    for j in range(1, n + 1):
      dp[0][j] = j

    for i in range(1, m + 1):
      for j in range(1, n + 1):
        if word1[i - 1] == word2[j - 1]:
          dp[i][j] = dp[i - 1][j - 1]
        else:
          dp[i][j] = min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1]) + 1

    return dp[m][n]
```
#### Please Upvote


