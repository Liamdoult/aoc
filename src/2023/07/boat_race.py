import math
import time
from collections import deque
from typing import List, Tuple, Generator
from itertools import chain

DEBUG=0
DATASET_NAME = '.txt'

def perf(f):
    def perf_f(*args, **kwargs):
        tic = time.perf_counter()
        result = f(*args, **kwargs)
        toc = time.perf_counter()
        print(f"====== {toc-tic} ======")
        return result
    return perf_f

def load_dataset(path: str) -> List[str]:
    with open(path, 'r') as file:
        return file.readlines()


# part 1
assert (result := perf(calculate_winning_options)(load_dataset('sample.txt'))) == (expected := 0), f"{result} != {expected}"
assert (result := perf(calculate_winning_options)(load_dataset(DATASET_NAME))) == (expected := 0), f"{result} != {expected}"

# part 2
# assert (result := perf(calculate_winning_options)(load_dataset('sample.txt'), join_numbers=True)) == (expected := 0), f"{result} != {expected}"
# assert (result := perf(calculate_winning_options)(load_dataset(DATASET_NAME), join_numbers=True)) == (expected := 0), f"{result} != {expected}"
print("==== Success ===")


