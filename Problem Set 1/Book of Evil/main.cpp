// Link to the question 
// https://codeforces.com/problemset/problem/337/D
#include<bits/stdc++.h>

using namespace std;

const int maxn = 1e5 + 10;

int head[maxn];
int tot;
int n, m, d;
bool vis[maxn];
int dp[maxn][3];

struct Edge {
  int to;
  int next;
}
edge[maxn << 1];

void addedge(int u, int v) {
  edge[tot].to = v;
  edge[tot].next = head[u];
  head[u] = tot++;
}

void init() {
  tot = 0;
  memset(head, -1, sizeof head);
  memset(vis, 0, sizeof vis);
}

void dfs1(int u, int fa) {
  for (int i = head[u]; i != -1; i = edge[i].next) {
    int v = edge[i].to;
    if (v == fa) continue;
    if (vis[v]) dp[v][0] = 0;
    dfs1(v, u);
    if (dp[v][0] >= 0) {
      if (dp[v][0] + 1 >= dp[u][0]) {
        dp[u][1] = dp[u][0];
        dp[u][0] = dp[v][0] + 1;
      } else if (dp[v][0] + 1 > dp[u][1]) {
        dp[u][1] = dp[v][0] + 1;
      }
    }
  }
}

void dfs2(int u, int fa) {
  if (vis[u]) dp[u][2] = max(0, dp[u][2]);
  for (int i = head[u]; i != -1; i = edge[i].next) {
    int v = edge[i].to;
    if (v == fa) continue;
    int tmp;
    if (dp[u][0] == dp[v][0] + 1) {
      tmp = max(dp[u][1], dp[u][2]);
    } else {
      tmp = max(dp[u][0], dp[u][2]);
    }
    if (tmp >= 0) dp[v][2] = tmp + 1;
    dfs2(v, u);
  }
}

int main() {

  init();
  scanf("%d%d%d", & n, & m, & d);
  for (int i = 0; i < m; i++) {
    int a;
    scanf("%d", & a);
    vis[a] = 1;
  }
  for (int i = 0; i < n - 1; i++) {
    int u, v;
    scanf("%d%d", & u, & v);
    addedge(u, v);
    addedge(v, u);
  }
  for (int i = 1; i <= n; i++) {
    dp[i][0] = dp[i][1] = dp[i][2] = -111;
  }
  dfs1(1, 1);
  dfs2(1, 1);
  int ans = 0;
  for (int i = 1; i <= n; i++) {
    if (max(dp[i][0], dp[i][2]) <= d) ans++;
  }
  printf("%d\n", ans);
  return 0;
}