from collections import deque
from typing import List, Tuple

DEBUG=0
DATASETNAME = 'scratch_cards.txt'

def load_dataset(path: str) -> List[str]:
    with open(path, 'r') as file:
        return file.readlines()

def convert(s: str) -> List[int]: return list(map(int, s.strip().replace("  ", " ").split(" ")))
def read_cards(cards: List[str]):
    for card in cards:
        card = card.split(":")[1]
        yield list(map(convert, card.split("|")))

def card_points(cards):
    cards = read_cards(cards)
    for card in cards:
        assert len(l := card[0]) == len(s := set(card[0])), f"{l} != {s}"
        assert len(l := card[1]) == len(s := set(card[1])), f"{l} != {s}"
        yield int(2**(len(set(card[0]).intersection(set(card[1])))-1))

def check_cards(cards):
    q = deque([0]*len(cards[0]))
    for card in read_cards(cards):
        q.append(0)
        duplicates = q.popleft() + 1
        m = len(set(card[0]).intersection(set(card[1])))
        for i in range(m): q[i] += 1*duplicates
        yield duplicates

# part 1
assert (result := sum(card_points(load_dataset('sample.txt')))) == (expected := 13), f"{result} != {expected}"
assert (result := sum(card_points(load_dataset(DATASETNAME)))) == (expected := 25174), f"{result} != {expected}"

# part 2
assert (result := sum(check_cards(load_dataset('sample.txt')))) == (expected := 30), f"{result} != {expected}"
assert (result := sum(check_cards(load_dataset(DATASETNAME)))) == (expected := 6420979), f"{result} != {expected}"
print("==== Success ===")


