from typing import List, Any
import sys


def swap_lists_on_indexes(
    list1: List[Any], list2: List[Any], *, indexes_to_swap
) -> None:
    debug = None
    try:
        for i in indexes_to_swap:
            debug = i
            list2.insert(i, list1[i])
            list1.insert(i + 1, list2[i + 1])
            list2.pop(i + 1)
            list1.pop(i + 1)
    except IndexError as e:
        print(f"i={debug}")
        print(f"{list1=} {list2=} {indexes_to_swap=}")
        print(f"{len( list1 )=} {len( list2 )=}")
        sys.exit()
