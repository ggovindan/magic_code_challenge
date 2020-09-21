from datetime import datetime
from typing import List
from memory_profiler import profile

"""
# I took a recursive approach to the problem as it is simple to visualize.
# Since there was no restriction on the space and time complexity I just assumed both.
# A few improvements to this solution would be to remove the additional array that was created
# for results and make the adjustments in place.

"""

@profile(precision=4)
def flatten_array(l: List, result: List = []):
    for item in l:
        if isinstance(item, (list, tuple)):
            flatten_array(item, result)
        else:
            result.append(item)
    print(result)


@profile(precision=4)
def flatten_array_non_recursive(l: List, result: List = []):
    for item in l:
        if isinstance(item, (list, tuple)):
            stack = []
            stack.extend(item)
            for x in stack:
                if isinstance(x, (list, tuple)):
                    stack.extend(x)
                else:
                    result.append(x)
        else:
            result.append(item)
    return result




if __name__ == "__main__":
    # x = [1, [2], [[3]], [4, [[5]]]]
    # x = [[1, 2, 3, 4, 5, 6, 7, 8, 9], (10, 11, 12), [13, [14, 15, 16]], [17, 18]]
    x = [[[[[[[[[[[[[[[[0]]]],0]]]]]]]]]]]]
    start = datetime.utcnow()
    flatten_array(x)
    print("recursive time={}".format(datetime.utcnow() - start))
    start = datetime.utcnow()
    print(flatten_array_non_recursive(x))
    print("iterative time={}".format(datetime.utcnow() - start))

