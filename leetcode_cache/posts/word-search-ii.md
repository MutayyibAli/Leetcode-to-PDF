# Cpp Solution:
cpp implementation in this [post](https://leetcode.com/problems/word-search-ii/discuss/59780/Java-15ms-Easiest-Solution-(100.00))
```
class Solution {
    struct TrieNode {
        TrieNode *children[26];
        string word;

        TrieNode() : word("") {
            for (int i = 0; i < 26; i++) {
                children[i] = nullptr;
            }
        }
    };

public:
    vector<string> findWords(vector<vector<char>> &board, vector<string> &words) {
        TrieNode *root = buildTrie(words);
        vector<string> result;
        for (int i = 0; i < board.size(); i++) {
            for (int j = 0; j < board[0].size(); j++) {
                dfs(board, i, j, root, result);
            }
        }
        return result;
    }

    /** Inserts a word into the trie. */
    TrieNode *buildTrie(vector<string> &words) {
        TrieNode *root = new TrieNode();
        for (int j = 0; j < words.size(); j++) {
            string word = words[j];
            TrieNode *curr = root;
            for (int i = 0; i < word.length(); i++) {
                char c = word[i] - 'a';
                if (curr->children[c] == nullptr) {
                    curr->children[c] = new TrieNode();
                }
                curr = curr->children[c];
            }
            curr->word = word;
        }
        return root;
    }

    void dfs(vector<vector<char>> &board, int i, int j, TrieNode *p, vector<string> &result) {
        char c = board[i][j];
        if (c == '#' || !p->children[c - 'a']) return;
        p = p->children[c - 'a'];
        if (p->word.size() > 0) {
            result.push_back(p->word);
            p->word = "";
        }

        board[i][j] = '#';
        if (i > 0) dfs(board, i - 1, j, p, result);
        if (j > 0) dfs(board, i, j - 1, p, result);
        if (i < board.size() - 1) dfs(board, i + 1, j, p, result);
        if (j < board[0].size() - 1) dfs(board, i, j + 1, p, result);
        board[i][j] = c;
    }
};
```



# Python Solution:
Here is an implementation based on  [Implement Trie][1] in LeetCode. TrieNode, Trie, Solution are treated as seperated classes. 

    class TrieNode():
        def __init__(self):
            self.children = collections.defaultdict(TrieNode)
            self.isWord = False
        
    class Trie():
        def __init__(self):
            self.root = TrieNode()
        
        def insert(self, word):
            node = self.root
            for w in word:
                node = node.children[w]
            node.isWord = True
        
        def search(self, word):
            node = self.root
            for w in word:
                node = node.children.get(w)
                if not node:
                    return False
            return node.isWord
        
    class Solution(object):
        def findWords(self, board, words):
            res = []
            trie = Trie()
            node = trie.root
            for w in words:
                trie.insert(w)
            for i in xrange(len(board)):
                for j in xrange(len(board[0])):
                    self.dfs(board, node, i, j, "", res)
            return res
        
        def dfs(self, board, node, i, j, path, res):
            if node.isWord:
                res.append(path)
                node.isWord = False
            if i < 0 or i >= len(board) or j < 0 or j >= len(board[0]):
                return 
            tmp = board[i][j]
            node = node.children.get(tmp)
            if not node:
                return 
            board[i][j] = "#"
            self.dfs(board, node, i+1, j, path+tmp, res)
            self.dfs(board, node, i-1, j, path+tmp, res)
            self.dfs(board, node, i, j-1, path+tmp, res)
            self.dfs(board, node, i, j+1, path+tmp, res)
            board[i][j] = tmp


  [1]: https://leetcode.com/problems/implement-trie-prefix-tree/