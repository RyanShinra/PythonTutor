from typing import Any


def main():
    # for subset in make_subsets([1, 2, 3]):
        # print(subset)
        
    for subset in make_subsets_with_dups([1, 2, 2, 3]):
        print(subset)
    pass


def make_subsets(items: list[Any]):
    n: int = len(items)
    # There are 2^n subsets (gah! Exponential time)
    num_subsets: int = 2**n

    # the bit mask of elements to use for this permutation
    for current_mask in range(num_subsets):
        current_subset = []
        # Consider if we want to use each item in the array or not
        for idx in range(n):
            cur_mask = 1 << idx  # Each item is represented by one bit
            if cur_mask & current_mask > 0:
                current_subset.append(items[idx])

        yield current_subset

from collections import Counter
from typing import Any

def make_subsets_with_dups(items: list[Any]):
    # Get frequency of each item
    freq = Counter(items)
    current_subset = []
    
    def backtrack(unique_nums: list[int], pos: int):
        if pos == len(unique_nums):
            yield current_subset.copy()  # Important to copy!
            return
            
        current_num = unique_nums[pos]
        # Try using current_num 0 to freq[current_num] times
        for count in range(freq[current_num] + 1):
            # Add 'count' copies of current_num
            for _ in range(count):
                current_subset.append(current_num)
            
            yield from backtrack(unique_nums, pos + 1)
            
            # Remove what we added (backtrack)
            for _ in range(count):
                current_subset.pop()
    
    yield from backtrack(list(freq.keys()), 0)

# Test


if __name__ == "__main__":
    main()
