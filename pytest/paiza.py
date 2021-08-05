from pprint import pprint

n, m = list(map(int, input().split(" ")))
training = [list(map(int, input().split(" "))) for _ in range(n)]
skill_need = [list(map(int, input().split(" "))) for _ in range(m)]

dp = [[0, 0, 0, 0] for _ in range(31)]
for x in range(4):
    dp[training[0][x]][x] = 1

pprint(dp)

for i in range(1, n):
    for x in range(4):
        p = training[i][x]
        if dp[p][x] >= 1:
            dp[] = dp[p][x] + p

