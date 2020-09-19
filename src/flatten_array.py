from datetime import datetime
from typing import List

"""
# I took a recursive approach to the problem as it is simple to visualize.
# Since there was no restriction on the space and time complexity I just assumed both.
# A few improvements to this solution would be to remove the additional array that was created
# for results and make the adjustments in place.

"""


def flatten_array(l: List, result: List = []):
    for item in l:
        if isinstance(item, (list, tuple)):
            flatten_array(item, result)
        else:
            result.append(item)
    print(result)


if __name__ == "__main__":
    x = [1, [2], [[3]], [4, [[5]]]]
    flatten_array(x)
