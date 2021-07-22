seven_segment = [
    [1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 1, 0, 0, 1],
    [0, 1, 1, 0, 0, 1, 1],
    [1, 0, 1, 1, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1],
]


def symmetrical_movement(state):
    result = [state[0], state[5], state[4], state[3], state[2], state[1], state[6]]
    return result


def rotational_transfer(state):
    result = [state[3], state[4], state[5], state[0], state[1], state[2], state[6]]
    return result


a = list(map(int, input().split(" ")))
b = list(map(int, input().split(" ")))
if a in seven_segment and b in seven_segment:
    print("Yes")
else:
    print("No")

a_t = symmetrical_movement(a)
b_t = symmetrical_movement(b)
print(a_t)
print(b_t)
if a_t in seven_segment and b_t in seven_segment:
    print("Yes")
else:
    print("No")


a_r = rotational_transfer(a)
b_r = rotational_transfer(b)
print(a_r)
print(b_r)
if a_r in seven_segment and b_r in seven_segment:
    print("Yes")
else:
    print("No")
