# Cpp Solution:
 Check out [LeetCode The Hard Way](https://wingkwong.github.io/leetcode-the-hard-way/) for more solution explanations and tutorials. 
 Check out our [Discord](https://discord.gg/Nqm4jJcyBf) for live discussion.
 Give a star on [Github Repository](https://github.com/wingkwong/leetcode-the-hard-way) and upvote this post if you like it.

<iframe src="https://leetcode.com/playground/aFX68kxW/shared" frameBorder="0" width="100%" height="500"></iframe>

For most BFS problems, you should see the following pattern.

<iframe src="https://leetcode.com/playground/Sb9vuTRo/shared" frameBorder="0" width="100%" height="500"></iframe>

Another nice solution from @martin0327. Instead of actual mutating, we can check the difference between the current gene string and those in `bank`. Push the target one in `bank` to the queue if they are different by 1 character and increase the distance by 1.

```
class Solution {
public:
  int minMutation(string start, string end, vector<string>& b) {
    map<string,int> dist;
    dist[start] = 0;
    queue<string> q;
    q.push(start);
    while (q.size()) {
      auto u = q.front(); q.pop();
      for (auto v : b) {
        if (dist.count(v)) continue;
        int cnt = 0;
        for (int i = 0; i < 8; i++) {
          if (u[i] != v[i]) cnt++;
        }
        if (cnt == 1) {
          dist[v] = dist[u] + 1;
          q.push(v);
        }
      }
    }
    if (dist.count(end)) return dist[end];
    else return -1;
  }
}; 
```


# Python Solution:
```
class Solution:
    def minMutation(self, start: str, end: str, bank: list[str]) -> int:

        queue, seen = deque([(start, 0)]), {start}      #### Ex: start = "AACCGGTT" ;    end = "AAACGGTA"
                                                        ####     bank  = ["AACCGATT","AACCGATA","AAACGATA","AAACGGTA"]
        while queue:
            s, n = queue.popleft()                      ####   n    queue             seen
                                                        ####  –––  ––––––––––––––––  –––––––––––––– 
            if s == end: return n                       ####   0   [('AACCGGTA', 1)]  {'AACCGGTA', 'AACCGGTT'}
                                                        #
            for i in range(8):                          ####   1   [('AAACGGTA', 2),  {'AACCGGTA', 'AACCGGTT',
                for ch in 'ACGT':                       ####        ('AACCGCTA', 2)]   'AACCGCTA', 'AAACGGTA'}
                                                        ####                           
                    m = s[:i]+ch+s[i+1:]                ####   2                       'AACCGCTA', 'AAACGGTA'}
                                                        ####   |
                    if m in bank and m not in seen:     #### answer    
                        seen.add(m)
                        queue.append((m, n+1))
        return -1

```
[https://leetcode.com/problems/minimum-genetic-mutation/submissions/1270694058/](https://leetcode.com/problems/minimum-genetic-mutation/submissions/1270694058/)

I could be wrong, but I think that time complexity is *O*(*N* × 8 × 4) ~ *O*(*N*) and space complexity is *O*(*N*), in which *N* ~ `len(bank)`.