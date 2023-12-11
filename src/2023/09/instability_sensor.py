
DATASET="instrument_readings.txt"

def load_dataset(path):
    with open(path, 'r') as f: return f.readlines()

def load_seq(line): return list(map(int, line.strip().split(" ")))

def get_pervious_reading(seq):
    assert len(seq) > 1
    p, prev_reading = seq[0], []
    for s in seq[1:]:
        prev_reading.append(s-p)
        p = s
    return prev_reading

def get_next(seq):
    stack = []
    while not all(map(lambda x: x==0, seq)):
        stack.append(seq[-1])
        seq = get_pervious_reading(seq)
    c = 0
    while stack: c = stack.pop() + c
    return c

def read_instrument(path):
    return sum(map(get_next, map(load_seq, load_dataset(path))))

def read_instrument_back(path):
    return sum(map(get_next, map(list, map(reversed, map(load_seq, load_dataset(path))))))

assert (result := read_instrument('sample.txt')) == (expected := 114), f"{result} != {expected}"
assert (result := read_instrument(DATASET)) == (expected := 1974232246), f"{result} != {expected}"

assert (result := read_instrument_back('sample.txt')) == (expected := 2), f"{result} != {expected}"
assert (result := read_instrument_back(DATASET)) == (expected := 928), f"{result} != {expected}"

print("===== Success =====")
