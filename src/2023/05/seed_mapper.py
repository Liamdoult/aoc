from collections import deque
from typing import List, Tuple, Generator
from itertools import chain

DEBUG=0
DATASET_NAME = 'seed_instructions.txt'

def load_dataset(path: str) -> List[str]:
    with open(path, 'r') as file:
        return file.readlines()

def read_instructions(instructions: List[str]):
    seeds, map_ = list(map(int, instructions[0].split(":")[1].strip().split(" "))), []

    for line in instructions[1:]:
        if "-to-" in line: continue
        if line == "\n": map_.append([])
        else: map_[-1].append(list(map(int, line.strip().split(" "))))

    return (seeds, map_)
        
def get_mapped_ranges(key_ranges: List[Tuple[int, int]], map_: List[Tuple[int, int, int]]):
    while key_ranges:
        start, range_ = key_ranges.pop()
        is_mapped = False 
        for d, s, r in map_:
            if start >= s and start < s+r:
                is_mapped, rl = True, r - (start - s)
                yield (d + (start - s), min(range_, rl))
                if start+range_ > s+r:
                    key_ranges.append((start + rl, rl))
        if not is_mapped: yield (start, range_)

def get_nearest_location(instructions, expand_seeds=False):
    seeds, instructions = read_instructions(instructions)
    
    # standardize inputs 
    if not expand_seeds: seeds = [(s, 1) for s in seeds]
    else: seeds = [(seeds[i], seeds[i+1]) for i in range(0, len(seeds), 2)]

    for mapping in instructions:
        seeds = list(get_mapped_ranges(seeds, mapping))

    return min(map(lambda x: x[0], seeds))


# part 1
assert (result := get_nearest_location(load_dataset('sample.txt'))) == (expected := 35), f"{result} != {expected}"
assert (result := get_nearest_location(load_dataset(DATASET_NAME))) == (expected := 579439039), f"{result} != {expected}"

# part 2
assert (result := get_nearest_location(load_dataset('sample.txt'), expand_seeds=True)) == (expected := 46), f"{result} != {expected}"
assert (result := get_nearest_location(load_dataset(DATASET_NAME), expand_seeds=True)) == (expected := 7873084), f"{result} != {expected}"
print("==== Success ===")


