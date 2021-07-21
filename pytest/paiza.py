from pprint import pprint
import numpy as np

x, y, z = list(map(int, input().split(" ")))
object_ = np.array([])
x_axis = []

for _ in range(z * 2):
    step = []
    x_axis_row = np.zeros(y)
    sep = False

    for __ in range(x):
        line = input().replace("#", "1").replace(".", "0")

        if line == "--":
            sep = True
            break
        line = list(map(int, line))
        step.append(line)

    if sep is False:
        step_np = np.array(step)
        for data in step_np:
            x_axis_row = x_axis_row + data

        x_axis_row = list(map(int, x_axis_row.tolist()))

        for i in range(len(x_axis_row)):
            if x_axis_row[i] > 0:
                x_axis_row[i] = "#"
            elif x_axis_row[i] == 0:
                x_axis_row[i] = "."

        x_axis = [x_axis_row] + x_axis

for data in x_axis:
    print("".join(data))

