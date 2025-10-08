# Cpp Solution:
#### Intuition
The idea is to consider for each element of array of nums2[i] as minimum once and check for maximum possible values available in nums1 keeping in mind nums2[i] as minimum .

#### Approach
- First we sort the nums2 array in decreasing order and as we need to know the mapping of nums2[i] to nums1[i]  so for that we make their pairs and then we sort.

- Now we we will iterate through p array one by one and let p[i].first as the minimum for an instance then all the elements to left of p array can be considered for sum part.

- But we can make priority queue for knowing top k elements to left of p array 

- And we will only keep k maximum elements at a time in priority queue and keep the tab of their sum .

- Now please read the code and you will understand it . Upvotes are appreciated  

#### Complexity
- Time complexity: O( N * Log(N) + (N-k) * Log(k) )

- Space complexity: O(N) + O(k) = O(N+K)

#### Code
```
class Solution {
    public:
    long long maxScore(vector<int>& nums1, vector<int>& nums2, int k) {
        
       vector<pair<int, int>> p ;
        
        for(int i = 0 ; i<nums1.size() ; i++)
        {
            p.push_back({nums2[i] , nums1[i]});
        }
        
        sort(p.rbegin() , p.rend());
        
        long long ans  = 0;
        long long sum  = 0;
        priority_queue<int> pq;
        for(int i = 0 ; i<k-1 ; i++)
        {
            sum += p[i].second;
            pq.push(-p[i].second);
        }

        for(int i = k-1 ; i<nums1.size() ; i++)
        {

            sum += p[i].second;
            pq.push(-p[i].second);
            
            ans = max(ans, sum * p[i].first );

            sum += pq.top();
            pq.pop();
        }
        
        return ans;
        
        
    }
};
```


# Python Solution:
#### **Intuition**
Almost exactly same as
[1383. Maximum Performance of a Team](https://leetcode.com/problems/maximum-performance-of-a-team/discuss/539687/JavaC%2B%2BPython-Priority-Queue).
<br>

#### **Explanation**
We iterate all pairs `(A[i], B[i])` with `B[i]` from big to small,
We keep the priority queue with maximum size of `k`.
Each time when we introduce a new pair of `(A[i], B[i])`,
the current minimum value on B is `B[i]`
the current sum value on A is `sum(priority queue)`

If the size of queue > k,
we pop the minimum `A[i]`.
also update total `sum -= A[i]`

If the size of queue == k,
we update `res = res = max(res, sum * B[i])`
<br>

#### **Complexity**
Time `O(nlogn)`
Space `O(n)`
<br>

**Java**
```java
    public long maxScore(int[] speed, int[] efficiency, int k) {
        int n = speed.length;
        int[][] ess = new int[n][2];
        for (int i = 0; i < n; ++i)
            ess[i] = new int[] {efficiency[i], speed[i]};
        Arrays.sort(ess, (a, b) -> b[0] - a[0]);
        PriorityQueue<Integer> pq = new PriorityQueue<>(k, (a, b) -> a - b);
        long res = 0, sumS = 0;
        for (int[] es : ess) {
            pq.add(es[1]);
            sumS = (sumS + es[1]);
            if (pq.size() > k) sumS -= pq.poll();
            if (pq.size() == k) res = Math.max(res, (sumS * es[0]));
        }
        return res;
    }
```

**cpp**
```cpp
    long long maxScore(vector<int>& speed, vector<int>& efficiency, int k) {
        int n = speed.size();
        vector<pair<int, int>> ess(n);
        for (int i = 0; i < n; ++i)
            ess[i] = {efficiency[i], speed[i]};
        sort(rbegin(ess), rend(ess));
        long long sumS = 0, res = 0;
        priority_queue <int, vector<int>, greater<int>> pq; //min heap
        for (auto& [e, s] : ess) {
            pq.emplace(s);
            sumS += s;
            if (pq.size() > k) {
                sumS -= pq.top();
                pq.pop();
            }
            if (pq.size() == k)
                res = max(res, sumS * e);
        }
        return res;
    }
```

**Python**
```py
    def maxScore(self, A, B, k):
        total = res = 0
        h = []
        for a,b in sorted(list(zip(A, B)), key=lambda ab: -ab[1]):
            heappush(h, a)
            total += a
            if len(h) > k:
                total -= heappop(h)
            if len(h) == k:
                res = max(res, total * b)
        return res
```
