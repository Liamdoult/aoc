from typing import List
from itertools import combinations

DEBUG=0

def load_dataset(path: str) -> List[str]:
    with open(path, 'r') as file:
        return file.readlines()

def get_vertical_matches(schematic: List[List[str]], r, c, condition):
    matches = []
    if r > 0 and condition(schematic[r-1][c]): matches.append((r-1, c)) 
    if r < len(schematic)-1 and condition(schematic[r+1][c]): matches.append((r+1, c))
    if condition(schematic[r][c]): matches.append((r, c))
    return matches

def process_schematic(schematic, condition, apply):
    cur, symbols_, now, symbols = "", [], False, {}
    max_r, max_c = len(schematic), len(schematic[0])
    for r in range(max_r):
        for c in range(max_c):
            vertical = get_vertical_matches(schematic, r, c, condition)
            symbols_.extend(vertical)
            if schematic[r][c].isdigit(): cur += schematic[r][c]
            else:
                if cur and symbols_:
                    for symbol in symbols_:
                        if symbol in symbols: symbols[symbol].append(int(cur))
                        else: symbols[symbol] = [int(cur)]
                cur, symbols_ = "", vertical 
    if DEBUG > 0: print(symbols)

    return [n for symbol in symbols.values() for n in apply(symbol)]

# part 1
condition = lambda x: not x.isdigit() and x != "." and x != "\n"
apply = lambda x: x
assert (result := sum(process_schematic(load_dataset('sample.txt'), condition, apply))) == (expected := 4361), f"{result} != {expected}"
assert (result := sum(process_schematic(load_dataset('schematic.txt'), condition, apply))) == (expected := 530849), f"{result} != {expected}"

# part 2
apply = lambda x: [a*b for a, b in combinations(x, 2)]
assert (result := sum(process_schematic(load_dataset('sample.txt'), condition, apply))) == (expected := 467835), f"{result} != {expected}"
assert (result := sum(process_schematic(load_dataset('schematic.txt'), condition, apply))) == (expected := 84900879), f"{result} != {expected}"
print("==== Success ===")
