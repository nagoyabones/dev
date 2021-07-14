import numpy as np

n, m, k = list(map(int, input().split(" ")))
my_evaluation = list(map(int, input().split(" ")))
evaluation = []
ans = []

for i in range(m):
    data = list(map(int, input().split(" ")))
    evaluation.append(data)
    evaluation_diff = (np.array(my_evaluation) - np.array(data)).tolist()

    if (
        evaluation_diff.count(0) >= k
        and data.count(3) >= k
        and my_evaluation.count(3) >= k
    ):
        for i in range(n):
            if my_evaluation[i] == 0 and data[i] == 3:
                ans.append(i + 1)

ans = list(set(ans))

if len(ans) > 0:
    print(*ans)
else:
    print("no")
