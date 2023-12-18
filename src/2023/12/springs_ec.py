

DEBUG=0

def load_dataset(path):
    with open(path, "r") as f: return list(map(lambda x: x.strip(), f.readlines()));

def combinations(row, ec, i=0, cur=0, space=False):
    if DEBUG>1:print(row, ec, i, cur, space)

    # Success in finding full path
    if i >= len(row):
        if ec or cur: return 0
        return 1

    t = 0
    if row[i] != "#":
       if not cur: t += combinations(row, ec, i+1, space=True) 

    if row[i] != ".":
        if cur: t += combinations(row, ec, i=i+1, cur=cur-1)
        elif space and ec:
            ec = ec[::]
            cur = ec.pop() - 1
            t += combinations(row, ec, i=i+1, cur=cur)

    return t

def error_check(row: str) -> int:
    m, ec = row.split(" ")
    ec = list(reversed(list(map(int, ec.split(",")))))
    # m = [g for g in m.split(".") if g != ""]
    res = combinations(m, ec, space=True)
    if DEBUG>0:print(m, list(reversed(ec)), res)

    return res

def error_check_unfolded(row: str) -> int:
    m, ec = row.split(" ")
    ec = list(map(int, ec.split(",")))

    unfoled_m = "?".join([m for _ in range(5)])
    unfoled_ec = []
    for _ in range(5): unfoled_ec.extend(ec)

    # print(unfoled_m)
    # print(unfoled_ec)

    res = combinations(unfoled_m, list(reversed(unfoled_ec)), space=True)
    print(m, list(reversed(ec)), res)

    return res

# Part 1
assert (result := sum(map(error_check, load_dataset('sample.txt')))) == (expected := 21), f"{result} != {expected}"
assert (result := sum(map(error_check, load_dataset('springs_status.txt')))) == (expected := 7843), f"{result} != {expected}"
print("===== Part 1: Success ======")

# Part 2
assert (result := sum(map(error_check_unfolded, load_dataset('sample.txt')))) == (expected := 525152), f"{result} != {expected}"
assert (result := sum(map(error_check_unfolded, load_dataset('springs_status.txt')))) == (expected := 7843), f"{result} != {expected}"
print("===== Part 2: Success ======")
