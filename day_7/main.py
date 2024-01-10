from __future__ import annotations
import os
from enum import Enum
from utils.timeit import timeit

from icecream import ic

from utils.utils import read_file, format_solution, Colors, run_solutions

colors = Colors()

cards_score = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2", "f"]
cards_to_char = ["a", "b", "c", "d", "e", "f", "g", "h", 'i', "j", "k", "l", "m", "n", "o"]
cards_score.reverse()

ic.disable()

for i in range(0, len(cards_score)):
    ic(f"Mapping: {cards_score[i]} -> {cards_to_char[i]}")


class HandTypes(Enum):
    FIVE_KIND = 7
    FOUR_KIND = 6
    FULL_HOUSE = 5
    THREE_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1
    NONE = 0


class Hand_Pot:
    hand: str
    pot: int
    hand_type: HandTypes
    hand_value: str

    def __init__(self, hand, pot):
        self.hand = hand
        self.pot = int(pot)
        self.hand_type = self.__get_hand_type(self.hand)
        self.hand_value = self.__get_hand_value(self.hand)

    def __get_hand_value(self, hand) -> str:
        value = []
        value.append(str(self.hand_type.value))
        for i in hand:
            value.append(cards_to_char[cards_score.index(i)])
        return "".join(value)

    def __get_hand_type(self, hand) -> HandTypes:
        ret = dict()
        for i in hand:
            if i not in ret:
                ret[i] = 0
            ret[i] += 1
        # five of a kind:
        if len(ret.keys()) == 1:
            return HandTypes.FIVE_KIND
        if len(ret.keys()) == 2:
            for key, value in ret.items():
                if value == 4:
                    return HandTypes.FOUR_KIND
            return HandTypes.FULL_HOUSE

        if len(ret.keys()) == 3:
            # it could be three of a kind, two pair
            for key, value in ret.items():
                if value == 3:
                    return HandTypes.THREE_KIND
            return HandTypes.TWO_PAIR
        if len(ret.keys()) == 4:
            return HandTypes.ONE_PAIR
        return HandTypes.HIGH_CARD

    def __str__(self):
        return f"Hand: {self.hand}, pot: {self.pot}, hand_type: {self.hand_type}, value: {self.hand_value}"

    def special_j(self):
        if "J" not in self.hand:
            return
        replacements = []
        for c in self.hand:
            if c == "J":
                continue
            if c not in replacements:
                replacements.append(c)

        j_replacement = cards_to_char[cards_score.index("J")]
        ic(j_replacement)

        if len(replacements) == 0:
            # special case five J
            self.hand_value = self.__get_hand_value(self.hand).replace("k", "a")
            return

        ic(f"Replacements: {replacements}")
        values = []
        hand_type = HandTypes.NONE
        best_replacement = ""
        for i in replacements:
            hand_potential = self.hand.replace("J", i)
            hand_type_potential = self.__get_hand_type(hand_potential)
            hand_value = self.__get_hand_value(hand_potential)
            values.append(hand_value)
            ic(f"Replacement J->{i} {hand_potential} = {hand_type_potential} - {hand_value}")
            if hand_type_potential.value > hand_type.value:
                hand_type = hand_type_potential
                best_replacement = i

        values.sort()
        self.hand_type = hand_type
        pre_hand_value = self.hand_value
        ic(f"Hand value: {self.hand} -> {self.hand_value}")
        self.hand_value = self.__get_hand_value(self.hand).replace("k", "a")

        ic(f"Best value: {values[0]} with replacement: {best_replacement}, new value: {pre_hand_value} -> {self.hand_value}")


pass


def parse_lines(lines: list[str]):
    res = []
    for line in lines:
        split = line.strip().split(" ")
        res.append(Hand_Pot(split[0], split[1]))
    return res


def swap(array, index_orig, index_swap):
    tmp = array[index_orig]
    array[index_orig] = array[index_swap]
    array[index_swap] = tmp


def part_one(lines):
    res = 0
    hand_pots = parse_lines(lines)

    hand_pots.sort(key=by_hand_value)
    index = 1
    for hand_pot in hand_pots:
        res += hand_pot.pot * index
        index += 1

    return res


def by_hand_value(element: Hand_Pot) -> str:
    return element.hand_value


def part_two(lines):
    res = 0
    hand_pots = parse_lines(lines)
    for hand_pot in hand_pots:
        hand_pot.special_j()

    index = 1
    hand_pots.sort(key=by_hand_value)
    for hand_pot in hand_pots:
        res += hand_pot.pot * index
        index += 1
    return res


@timeit
def solutions():
    path = os.path.dirname(os.path.realpath(__file__))
    lines = read_file(os.path.join(path, "input.txt"))
    run_solutions(path, part_one, part_two, lines)


if __name__ == '__main__':
    solutions()
