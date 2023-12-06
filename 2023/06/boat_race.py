import math
import time
from collections import deque
from typing import List, Tuple, Generator
from itertools import chain

DEBUG=0
DATASET_NAME = 'race_info.txt'

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

def load_races(races: List[str], join_numbers: bool = False) -> List[Tuple[int, int]]:
    time = races[0].split(":")[1].strip().split(" ")
    distance = races[1].split(":")[1].strip().split(" ")
    f = lambda x: filter(lambda y: y != '', x)
    if join_numbers:
        time, distance = ["".join(time)], ["".join(distance)]

    return [(int(t), int(d)) for t, d in zip(f(time), f(distance))]

def calculate_winning_options(races: List[str], join_numbers: bool = False):
    races = load_races(races, join_numbers)
    winnable = 1
    for t, d  in races:
        d += 1
        # d = s.t
        # d = (i).(t-i)
        # 0 = -i^2+ti-d
        # d will always be - and so a*c in quadratic equation (a = -1) cancel out
        l = int((-t - math.sqrt(t**2 - 4*d)) / (2 * -1))
        r = int(math.ceil((-t + math.sqrt(t**2 - 4*d)) / (2 * -1))-1)
        print(t, d, l, r, l-r)
        winnable *= l-r 
    return winnable

# part 1
assert (result := perf(calculate_winning_options)(load_dataset('sample.txt'))) == (expected := 288), f"{result} != {expected}"
assert (result := perf(calculate_winning_options)(load_dataset(DATASET_NAME))) == (expected := 1195150), f"{result} != {expected}"

# part 2
assert (result := perf(calculate_winning_options)(load_dataset('sample.txt'), join_numbers=True)) == (expected := 71503), f"{result} != {expected}"
assert (result := perf(calculate_winning_options)(load_dataset(DATASET_NAME), join_numbers=True)) == (expected := 42550411), f"{result} != {expected}"
print("==== Success ===")


