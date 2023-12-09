from typing import List, Tuple

DATASET_NAME = 'camel_cards_hands.txt'

CARDS = "AKQJT98765432"
CARDS_J = "AKQT98765432J"
CARDS_N = { c: i for i, c in enumerate(reversed(CARDS)) }
CARDS_J_N = { c: i for i, c in enumerate(reversed(CARDS_J)) }
TYPES = { (5,): 6, (4,): 5, (3, 2): 4, (3,): 3, (2, 2): 2, (2,): 1 }

def load_dataset(path: str) -> List[str]:
    with open(path, 'r') as f:
        return f.readlines()

def load_hands(lines: List[str], joker) -> List[Tuple[str, int]]:
    f = lambda hand, bid: (score(hand, joker), to_int_array(hand, joker), hand, int(bid))
    return [f(*line.split(" ")) for line in lines]

def to_int_array(cards, joker):
    return list(map(lambda x: CARDS_N[x] if not joker else CARDS_J_N[x], cards))

def score(hand, joker):
    _tally = {k: 0 for k in CARDS}
    j = 0
    for c in hand:
        if joker and c == "J":
            j += 1
            for k in _tally.keys(): _tally[k] += 1
        else: _tally[c] += 1
    tmp = sorted(_tally.values(), reverse=True)
    if joker and len(tmp) > 1:
        tmp = [tmp[0]] + [x-j for x in tmp[1:]]
    tmp = filter(lambda x: x > 1, tmp)
    tmp = tuple(tmp)
    # print(hand, tmp)
    return TYPES.get(tmp , 0)


def total_winnings(hands: List[str], joker=False):
    hands = sorted(load_hands(hands, joker))
    ranked = list(zip(hands, range(1, len(hands)+1)))
    if DEBUG:
        t = 0
        [print((x[0][0], x[0][1], x[0][2], x[0][3], x[1], x[1]*x[0][3], (t:=t+(x[1]*x[0][3])))) for x in ranked]
    hand_scores = list(map(lambda x: x[0][3]*x[1], ranked))
    return sum(hand_scores)

# part 1
DEBUG=0
assert (result := total_winnings(load_dataset('sample.txt'))) == (expected := 6440), f"{result} != {expected}"
assert (result := total_winnings(load_dataset(DATASET_NAME))) < (expected := 249690428), f"{result} !< {expected}"
assert (result := total_winnings(load_dataset(DATASET_NAME))) == (expected := 249638405), f"{result} != {expected}"

# part 2
assert (result := total_winnings(load_dataset('sample.txt'), joker=True)) == (expected := 5905), f"{result} != {expected}"
assert (result := total_winnings(load_dataset(DATASET_NAME), joker=True)) == (expected := 249776650), f"{result} != {expected}"
print("====== Success ======")
