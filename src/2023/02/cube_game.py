from typing import List, Tuple, Dict
from pathlib import Path
from functools import reduce

DEBUG=0
COLOUR_KEYS = {"red": 0, "blue": 1, "green": 2}

def load_dataset(path: str) -> List[str]:
    with open(path, 'r') as file:
        return file.readlines()

def load_rounds(rounds: str) -> List[List[int]]:
    rounds = rounds.split(";")
    for i, round in enumerate(rounds):
        converted_round = [0, 0, 0]
        for turn in round.split(","):
            v, k = turn.strip().split(" ") 
            converted_round[COLOUR_KEYS[k]] += int(v)
        rounds[i] = converted_round
    return rounds

def load_game(game: str) -> Tuple[int, List[List[int]]]:
    game, rounds = game.strip().split(":")
    game = int(game.split(" ")[-1])
    return game, load_rounds(rounds)

def load_games(lines: List[str]):
    return list(map(load_game, lines))

def is_possible(game: List[List[int]], in_bag: List[int]) -> bool:
    return all([round[i] <= in_bag[i] for round in game for i in range(len(COLOUR_KEYS))])

def max_possible(game: List[List[int]]) -> List[int]:
    max_ = [0]*len(COLOUR_KEYS)
    for round in game:
        for i in range(len(max_)):
            max_[i] = max(round[i], max_[i])
    return max_

def play_game(games: List[str], rule) -> List[int]:
    return map(rule, load_games(games))

in_bag = [12, 14, 13]
rule = lambda g: g[0] if is_possible(g[1], in_bag) else 0
assert (result := sum(play_game(load_dataset('sample.txt'), rule))) == (expected := 8), f"{result} != {expected}"
assert (result := sum(play_game(load_dataset('games.txt'), rule))) == (expected := 2727), f"{result} != {expected}"

rule = lambda g: reduce(lambda a, b: a*b, max_possible(g[1]))
assert (result := sum(play_game(load_dataset('sample.txt'), rule))) == (expected := 2286), f"{result} != {expected}"
assert (result := sum(play_game(load_dataset('games.txt'), rule))) == (expected := 56580), f"{result} != {expected}"
print("==== Success ===")
