# Cpp Solution:
#### Video Solution (`Aryan Mittal`) - Link in LeetCode Profile
`Evaluate Division` by `Aryan Mittal`



#### Approach & Intution













#### Code
```cpp
class Solution {
public:

    void dfs(string node, string& dest, unordered_map<string, unordered_map<string, double>>& gr, unordered_set<string>& vis, double& ans, double temp) {
        if(vis.find(node) != vis.end()) return;

        vis.insert(node);
        if(node == dest){
            ans = temp;
            return;
        }

        for(auto ne : gr[node]){
            dfs(ne.first, dest, gr, vis, ans, temp * ne.second);
        }
    }

    unordered_map<string, unordered_map<string, double>> buildGraph(const vector<vector<string>>& equations, const vector<double>& values) {
        unordered_map<string, unordered_map<string, double>> gr;

        for (int i = 0; i < equations.size(); i++) {
            string dividend = equations[i][0];
            string divisor = equations[i][1];
            double value = values[i];

            gr[dividend][divisor] = value;
            gr[divisor][dividend] = 1.0 / value;
        }

        return gr;
    }

    vector<double> calcEquation(vector<vector<string>>& equations, vector<double>& values, vector<vector<string>>& queries) {
        unordered_map<string, unordered_map<string, double>> gr = buildGraph(equations, values);
        vector<double> finalAns;

        for (auto query : queries) {
            string dividend = query[0];
            string divisor = query[1];

            if (gr.find(dividend) == gr.end() || gr.find(divisor) == gr.end()) {
                finalAns.push_back(-1.0);
            } else {
                unordered_set<string> vis;
                double ans = -1, temp=1.0;
                dfs(dividend, divisor, gr, vis, ans, temp);
                finalAns.push_back(ans);
            }
        }

        return finalAns;
    }
};
```
```Java
class Solution {
    public void dfs(String node, String dest, HashMap<String, HashMap<String, Double>> gr, HashSet<String> vis, double[] ans, double temp) {
        if (vis.contains(node))
            return;

        vis.add(node);
        if (node.equals(dest)) {
            ans[0] = temp;
            return;
        }

        for (Map.Entry<String, Double> entry : gr.get(node).entrySet()) {
            String ne = entry.getKey();
            double val = entry.getValue();
            dfs(ne, dest, gr, vis, ans, temp * val);
        }
    }

    public HashMap<String, HashMap<String, Double>> buildGraph(List<List<String>> equations, double[] values) {
        HashMap<String, HashMap<String, Double>> gr = new HashMap<>();

        for (int i = 0; i < equations.size(); i++) {
            String dividend = equations.get(i).get(0);
            String divisor = equations.get(i).get(1);
            double value = values[i];

            gr.putIfAbsent(dividend, new HashMap<>());
            gr.putIfAbsent(divisor, new HashMap<>());

            gr.get(dividend).put(divisor, value);
            gr.get(divisor).put(dividend, 1.0 / value);
        }

        return gr;
    }

    public double[] calcEquation(List<List<String>> equations, double[] values, List<List<String>> queries) {
        HashMap<String, HashMap<String, Double>> gr = buildGraph(equations, values);
        double[] finalAns = new double[queries.size()];

        for (int i = 0; i < queries.size(); i++) {
            String dividend = queries.get(i).get(0);
            String divisor = queries.get(i).get(1);

            if (!gr.containsKey(dividend) || !gr.containsKey(divisor)) {
                finalAns[i] = -1.0;
            } else {
                HashSet<String> vis = new HashSet<>();
                double[] ans = {-1.0};
                double temp = 1.0;
                dfs(dividend, divisor, gr, vis, ans, temp);
                finalAns[i] = ans[0];
            }
        }

        return finalAns;
    }
}
```
```Python
from typing import List

class Solution:
    def dfs(self, node: str, dest: str, gr: dict, vis: set, ans: List[float], temp: float) -> None:
        if node in vis:
            return

        vis.add(node)
        if node == dest:
            ans[0] = temp
            return

        for ne, val in gr[node].items():
            self.dfs(ne, dest, gr, vis, ans, temp * val)

    def buildGraph(self, equations: List[List[str]], values: List[float]) -> dict:
        gr = {}

        for i in range(len(equations)):
            dividend, divisor = equations[i]
            value = values[i]

            if dividend not in gr:
                gr[dividend] = {}
            if divisor not in gr:
                gr[divisor] = {}

            gr[dividend][divisor] = value
            gr[divisor][dividend] = 1.0 / value

        return gr

    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        gr = self.buildGraph(equations, values)
        finalAns = []

        for query in queries:
            dividend, divisor = query

            if dividend not in gr or divisor not in gr:
                finalAns.append(-1.0)
            else:
                vis = set()
                ans = [-1.0]
                temp = 1.0
                self.dfs(dividend, divisor, gr, vis, ans, temp)
                finalAns.append(ans[0])

        return finalAns

```


# Python Solution:
We can treat each equation as an edge, variables as nodes and value as weight, and build a weighted graph. Then for each queries `(x, y)`, we try to find a path from `x` to `y`. The answer is the product of all edges' weights. If either `x` or `y` is not in graph or `x` and `y` are not connected in graph, the answer doesn't exist.
We can use a `defaultdict(dict) G` to build a weighted graph and `G[x][y]` will be the weight of edge `x->y` which is the value of `x / y`

So one solution is BFS (or DFS) for each query.
```
def calcEquation(equations, values, queries):
	G = collections.defaultdict(dict)
	for (x, y), v in zip(equations, values):
		G[x][y] = v
		G[y][x] = 1/v
	def bfs(src, dst):
		if not (src in G and dst in G): return -1.0
		q, seen = [(src, 1.0)], set()
		for x, v in q:
			if x == dst: 
				return v
			seen.add(x)
			for y in G[x]:
				if y not in seen: 
					q.append((y, v*G[x][y]))
		return -1.0
	return [bfs(s, d) for s, d in queries]
```

Another solution is Union Find. 

Our root map is `root` and each `root[x]` is in form of `(root(x), ratio)` where `ratio = x/root(x)`. If `x == root(x)`, then `ratio = 1.0`. So just consider root as a denominator here. Then, we process the equations. For each `x/y = v`, we union `x` to `y` or set `root(root(x)) = root(y)` as `y` is the denominator. After union all `x, y` in the equations, for each `a, b` in the queries, if `a` and `b` are not in the same union set, then `a` and `b` are not transmissable to each other so `a/b` should return `-1.0`.

Now that we have a `ratio` element in each `root[x]`, we need to update it in `find()` and `union()` as well.
In `find(x)`, we have `root[x] = (p, x/p)` where `p` is the parent node of x and not neccessarily the root node. But we will do path compression and recursively update all the parent nodes in the path to root. And `ratio` should be updated as well. Eventually `find(p)` returns updated `root[p] = (root(p), p/root(p))`. 
So `root[x]` should be updated to `(root(x), x/root(x)) = (root(p), x/p * p/root(p))) = (root[p][0], root[x][1] * root[p][1])`

For `union(x, y)` in equations processing, we make `root(root(x)) = root(y)` as mentiond previously. And for `root[root(x)]`'s `ratio`, as `root(y)` is `root(x)`'s new root, we update it to `root(x)/root(y) = (x/y) * (y/root(y)) / (x/root(x)) = x/y * root[y][1] / root[x][1]`. `x/y` is the provided equation outcome value.

For `union(x, y)` in queries, we can just simply return `x/y = (x/root(x)) / (y/root(y)) = root[x][1]/root[y][1]`.

```
def calcEquation(equations, values):
	root = {}
	
	#### xr = x/parent(x), pr = parent(x)/root(x), update xr to xr*pr = x/root(x)
	def find(x):
		p, xr = root.setdefault(x, (x, 1.0))
		if x != p:
			r, pr = find(p)
			root[x] = (r, xr*pr)
		return root[x]

	#### if root(x) = root(y), equations "x / y" doable as (x/root(x)) / (y/root(y)) = xr / yr
	def union(x, y, ratio):
		px, xr, py, yr = *find(x), *find(y)
		if not ratio:
			return xr / yr if px == py else -1.0
		if px != py:
			root[px] = (py, yr/xr*ratio)

	for (x, y), v in zip(equations, values):
		union(x, y, v)
	return [union(x, y, 0) if x in root and y in root else -1.0 for x, y in queries]
```