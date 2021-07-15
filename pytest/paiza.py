"""
import numpy as np


def decimal_to_bin_int_arr(num, digits):
    bin_str = format(num, str(digits) + "b")
    bin_int_arr = np.array(list(map(int, bin_str.replace(" ", "0"))))
    return bin_int_arr


exam_num = int(input())
exam_point = []
result_arr = []
bin_num = 0
bin_arr = decimal_to_bin_int_arr(bin_num, exam_num)

for _ in range(exam_num):
    exam_point.append(int(input()))
point_arr = np.array(exam_point)

while sum(bin_arr) <= exam_num and bin_arr.size == exam_num:
    result_arr.append(sum(point_arr * bin_arr))

    bin_num += 1
    bin_arr = decimal_to_bin_int_arr(bin_num, exam_num)

ans = sorted(list(set(result_arr)))

print(len(ans))
for data in ans:
    print(data)
"""

import itertools

exam_num = int(input())
exam_point = []
result = []
ans = [0]
for _ in range(exam_num):
    exam_point.append(int(input()))

for i in range(1, exam_num + 1):
    result += list(itertools.combinations(exam_point, i))

for data in result:
    ans.append(sum(data))

ans = sorted(list(set(ans)))

print(len(ans))
for data in ans:
    print(data)
