from typing import List, Tuple
from functools import reduce

DEBUG=1

DOWN, RIGHT, UP, LEFT = 0, 1, 2, 3
PIPES = [
    {"|":DOWN, "L":RIGHT, "J":LEFT},
    {"-":RIGHT, "J":UP, "7":DOWN},
    {"|":UP, "F":RIGHT, "7":LEFT},
    {"-":LEFT, "F":DOWN, "L":UP},
]
MOVE=[(1,0), (0,1), (-1,0), (0,-1)]

def read_dataset(path: str) -> List[str]:
    with open(path, 'r') as f: return list(map(lambda x: x.strip(), f.readlines()))

def find_start(map_: List[str]) -> Tuple[int, int]:
    for i, row in enumerate(map_):
        for j, c in enumerate(row):
            if c == "S": return (i, j) 
    raise ValueError("No start point")

def on_map(map_: List[str], cur: Tuple[int, int]) -> bool:
    return 0<=cur[0]<len(map_) and 0<=cur[1]<len(map_[0])

def move(cur, dir): return (cur[0]+MOVE[dir][0], cur[1]+MOVE[dir][1])

def get_loop(path: str) -> List[Tuple[int, int]]:
    if DEBUG>0: print("File: ", path)
    map_ = read_dataset(path)
    s = find_start(map_)

    def follow(map_:List[str], cur:Tuple[int], dir:int, limit=100000) -> int:
        path, l = [cur], 0
        while l < limit:
            cur = move(cur, dir)
            if not on_map(map_, cur): return []
            p = map_[cur[0]][cur[1]]
            if DEBUG>3:print("current: ", cur, p)
            if p == "S":
                path.append(cur)
                return path
            if p == ".": return [] 
            if p not in PIPES[dir]: return []
            dir, l = PIPES[dir][p], l+1
            path.append(cur)
        raise Exception("Search limit reached")

    for dir in [UP, LEFT, DOWN, RIGHT]:
        if DEBUG>2:print("start: ", s)
        res = follow(map_, s, dir)
        if res: return res
        if DEBUG>2:print("Dead end")

    raise ValueError("No valid path found.")

def print_maps(*maps):
    if len(maps[0]) <= 40:
        for i in range(len(maps[0])): print(*[map_[i] for map_ in maps])
    else:
        for m in maps:
            for r in m:
                print(r)
            print("")
    print("")

def start_is(s, before, after, dir_b, dir_a):
    if dir_a == RIGHT and dir_b == DOWN:
        if DEBUG>3: print(s, before, after, dir_a, dir_b)
        if DEBUG>3: print(before == (s[0] + MOVE[dir_b][0], s[1] + MOVE[dir_b][1]), before, (s[0] + MOVE[dir_b][0], s[1] + MOVE[dir_b][1]))
    return before == (s[0] + MOVE[dir_b][0], s[1] + MOVE[dir_b][1]) and after == (s[0] + MOVE[dir_a][0], s[1] + MOVE[dir_a][1])

def find_down(loop: List[Tuple[int, int]], map_) -> Tuple[int, int]:
    if DEBUG>3: print(len(loop))
    for i in range(len(loop)):
        prev_pos = loop[(i-1)%len(loop)]
        pos = loop[i]
        if map_[pos[0]][pos[1]] == "F" and prev_pos == (pos[0], pos[1]+1): return i
        if map_[pos[0]][pos[1]] == "7" and prev_pos == (pos[0], pos[1]-1): return i
    if DEBUG>3: print_maps(map_)
    raise ValueError("No down point found")

def is_change_down(pos, prev, map_):
    if map_[pos[0]][pos[1]] == "F" and prev == (pos[0]+MOVE[RIGHT][0], pos[1]+MOVE[RIGHT][1]): return True
    if map_[pos[0]][pos[1]] == "7" and prev == (pos[0]+MOVE[LEFT][0], pos[1]+MOVE[LEFT][1]): return True
    return False

def is_change_up(pos, prev, map_):
    if map_[pos[0]][pos[1]] == "J" and prev == (pos[0]+MOVE[LEFT][0], pos[1]+MOVE[LEFT][1]): return True
    if map_[pos[0]][pos[1]] == "L" and prev == (pos[0]+MOVE[RIGHT][0], pos[1]+MOVE[RIGHT][1]): return True
    return False

def get_spaces_inside(path: str) -> int:
    loop = get_loop(path)
    map_ = read_dataset(path)
    clean_map = [["." for _ in range(len(map_[0]))] for _ in range(len(map_))]
    for l in loop: clean_map[l[0]][l[1]] = map_[l[0]][l[1]]

    # replace s with actual letter
    s = find_start(clean_map)
    for i in range(len(loop)):
        if loop[i] == s:
            before = loop[(i-2)%len(loop)]
            after = loop[(i+1)%len(loop)]
            if start_is(s, before, after, UP, DOWN): clean_map[s[0]][s[1]] = "|"
            elif start_is(s, before, after, UP, RIGHT): clean_map[s[0]][s[1]] = "L"
            elif start_is(s, before, after, UP, LEFT): clean_map[s[0]][s[1]] = "J"
            elif start_is(s, before, after, DOWN, UP): clean_map[s[0]][s[1]] = "|"
            elif start_is(s, before, after, DOWN, RIGHT): clean_map[s[0]][s[1]] = "F"
            elif start_is(s, before, after, DOWN, LEFT): clean_map[s[0]][s[1]] = "7"
            elif start_is(s, before, after, LEFT, RIGHT): clean_map[s[0]][s[1]] = "-"
            elif start_is(s, before, after, LEFT, UP): clean_map[s[0]][s[1]] = "J"
            elif start_is(s, before, after, LEFT, DOWN): clean_map[s[0]][s[1]] = "7"
            elif start_is(s, before, after, RIGHT, LEFT): clean_map[s[0]][s[1]] = "-"
            elif start_is(s, before, after, RIGHT, UP): clean_map[s[0]][s[1]] = "L"
            elif start_is(s, before, after, RIGHT, DOWN): clean_map[s[0]][s[1]] = "F"
            else: raise ValueError("start_is did not match any")
            break
    clean_map = ["".join(r) for r in clean_map]
    if clean_map[s[0]][s[1]] == "S": raise Exception("Value S still exists")

    direction_map = [[l for l in row] for row in clean_map]
    ds_idx, down = find_down(loop, clean_map), True
    for i in range(len(loop)):
        idx = (i+ds_idx)%len(loop)
        if is_change_up(loop[idx], loop[(idx-1)%len(loop)], clean_map): down = False
        if is_change_down(loop[idx], loop[(idx-1)%len(loop)], clean_map): down = True 
        direction_map[loop[idx][0]][loop[idx][1]] = "d" if down else "u"

    direction_map = ["".join(r) for r in direction_map]

    inside = [[0 for _ in range(len(map_[0]))] for _ in range(len(map_))]
    is_in = False 
    for i in range(len(inside)):
        f_seen = None
        for j in range(len(inside[0])):
            if not f_seen and direction_map[i][j] != ".": f_seen = direction_map[i][j]
            if direction_map[i][j] == "d": is_in = f_seen == "d"
            if direction_map[i][j] == "u": is_in = f_seen == "u" 
            if direction_map[i][j] == "." and is_in: inside[i][j] += 1

    if DEBUG>0: print_maps(map_, clean_map, direction_map, ["".join(map(str, r)) for r in inside])

    return sum([sum(r) for r in inside])

DATASET = "pipes.txt"
assert (result := len(get_loop('sample0.txt'))//2) == (expected := 4), f"{result} != {expected}"
assert (result := len(get_loop('sample1.txt'))//2) == (expected := 4), f"{result} != {expected}"
assert (result := len(get_loop('sample2.txt'))//2) == (expected := 8), f"{result} != {expected}"
assert (result := len(get_loop('sample3.txt'))//2) == (expected := 8), f"{result} != {expected}"
assert (result := len(get_loop(DATASET))//2) == (expected := 6956), f"{result} != {expected}"

assert (result := get_spaces_inside('sample0.txt')) == (expected := 1), f"{result} != {expected}"
assert (result := get_spaces_inside('sample1.txt')) == (expected := 1), f"{result} != {expected}"
assert (result := get_spaces_inside('sample2.txt')) == (expected := 1), f"{result} != {expected}"
assert (result := get_spaces_inside('sample3.txt')) == (expected := 1), f"{result} != {expected}"
assert (result := get_spaces_inside('sample4.txt')) == (expected := 4), f"{result} != {expected}"
assert (result := get_spaces_inside('sample5.txt')) == (expected := 4), f"{result} != {expected}"
assert (result := get_spaces_inside('sample6.txt')) == (expected := 8), f"{result} != {expected}"
assert (result := get_spaces_inside('sample7.txt')) == (expected := 10), f"{result} != {expected}"
assert (result := get_spaces_inside(DATASET)) == (expected := 455), f"{result} != {expected}"

print("===== Success =====")
