input_line = input()
h = [
    [["8"], ["0", "6", "9"], []],
    [["7"], ["1"], []],
    [[], ["2", "3"], []],
    [["9"], ["3", "2", "5"], []],
    [[], ["4"], []],
    [["6", "9"], ["5", "3"], []],
    [["8"], ["6", "9", "0"], ["5"]],
    [[], ["7"], []],
    [[], ["8"], ["0", "6", "9"]],
    [["8"], ["9", "0", "6"], ["3", "5"]],
]
n = len(input_line)
result = []
temp = []
for i in range(n):
    num = int(input_line[i])
    temp.append(h[num])
for data in temp:
    print(data)
