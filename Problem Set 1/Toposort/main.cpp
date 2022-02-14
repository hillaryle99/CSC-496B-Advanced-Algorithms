// Link to the problem: 
// https://www.spoj.com/problems/TOPOSORT/

#include <bits/stdc++.h>

using namespace std;

vector < int > arr[100001];
int in [100001];
vector < int > topSort;

bool kahn(int n) {
  priority_queue < int, vector < int > , greater < int >> pq;
  for (int i = 1; i <= n; i++)
    if ( in [i] == 0)
      pq.push(i);

  while (!pq.empty()) {
    int cur = pq.top();
    topSort.push_back(cur);
    pq.pop();
    for (int child: arr[cur]) {
      in [child]--;
      if ( in [child] == 0)
        pq.push(child);
    }
  }
  return topSort.size() == n;
}

int main() {
  int n, x, y, m;
  cin >> n >> m;

  for (int i = 1; i <= m; i++) cin >> x >> y, arr[x].push_back(y), in [y]++;

  if (!kahn(n))
    cout << "Sandro fails.";
  else {
    for (int node: topSort)
      cout << node << " ";
  }

}