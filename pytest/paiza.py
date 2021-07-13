legs, heads, c_leg, t_leg = list(map(int, input().split(" ")))
ok = 0
c_ans, t_ans = 0, 0

for i in range(1, heads):
    c_head = i
    t_head = heads - i

    if legs == c_head * c_leg + t_head * t_leg:
        ok += 1
        c_ans = c_head
        t_ans = t_head

if ok == 1:
    print(c_ans, t_ans)
else:
    print("miss")
