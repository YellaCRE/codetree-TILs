n = int(input())
graph = []
for _ in range(n):
    graph.append(list(map(int, input().split())))

dp = [[0 for _ in range(n)] for _ in range(n)]

for r in range(n):
    for c in range(n):
        if r == 0 and c == 0: 
            dp[r][c] = graph[r][c]
            continue
        
        if r > 0 and c > 0:
            dp[r][c] = graph[r][c] + max(dp[r-1][c], dp[r][c-1])
        elif r == 0:
            dp[r][c] = graph[r][c] + dp[r][c-1]
        else:
            dp[r][c] = graph[r][c] + dp[r-1][c]

print(dp[-1][-1])