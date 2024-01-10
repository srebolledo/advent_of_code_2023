import copy
import os

from icecream import ic

from utils.utils import read_file, format_solution, Colors

colors = Colors()


class Card:
    card_index: int
    winning_numbers: list[int]
    my_numbers: list[int]
    winning_numbers_colored: list[int]
    my_numbers_colored: list[int]
    matches: list[int]
    copies: int

    def __init__(self, card_index, winning_numbers, my_numbers):
        self.card_index = int(card_index)
        self.winning_numbers = winning_numbers
        self.my_numbers = my_numbers
        # for visualization
        self.my_numbers_colored = copy.deepcopy(self.my_numbers)
        self.winning_numbers_colored = copy.deepcopy(winning_numbers)
        self.value = 0
        self.matches = []
        self.copies = 1
        self.__get_value()

    def __get_value(self):
        if self.value != 0:
            return self.value
        for my_number in self.my_numbers:
            if my_number in self.winning_numbers:
                self.matches.append(my_number)
        if len(self.matches) > 0:
            self.value = pow(2, len(self.matches) - 1)
        else:
            self.value = 0
        return self.value

    def __str__(self):
        return f"id: {self.card_index}, winning_numbers: {self.winning_numbers_colored}, my_numbers: {self.my_numbers_colored}, matches: {self.matches}, len(matches): {len(self.matches)}, value: {self.value}, copies: {self.copies}"


def parse_cards(lines) -> list[Card]:
    parsed_cards = []
    for line in lines:
        split = line.split(":")
        card_index = split[0].replace("Card ", "")
        card = split[1].replace("  ", " ").split("|")
        winning_numbers = [number.strip() for number in card[0].strip().split(" ")]
        my_numbers = [number.strip() for number in card[1].strip().split(" ")]
        parsed_cards.append(Card(card_index, winning_numbers, my_numbers))
    return parsed_cards


def part_one(lines):
    res = 0
    cards = parse_cards(lines)
    for card in cards:
        res += card.value
        ic(card)
    return res


def create_copies(copy_range: list[Card]):
    store_copies = []
    for inner_card in copy_range:
        store_copies.append(inner_card)
    return store_copies


iteration = 0


def process_copies(cards, copies):
    new_copies = []
    for c in copies:
        c_index = c.card_index
        for i in range(c_index, c_index + len(c.matches)):
            new_copies.append(cards[i])
    return new_copies


def part_two(lines):
    cards = parse_cards(lines)
    copies = []
    for card in cards:
        if len(card.matches) == 0:
            ic(f"card {card.card_index} doesn't award copies")
            continue
        for i in range(card.card_index, card.card_index + len(card.matches)):
            copies.append(cards[i])
    cards.extend(copies)
    while len(copies) > 0:
        copies = process_copies(cards, copies)
        if len(copies) > 0:
            cards.extend(copies)
    res = len(cards)

    return res


def solutions():
    path = os.path.dirname(os.path.realpath(__file__))
    directory_name = " ".join(path.split(os.path.sep)[-1].capitalize().split("_"))

    lines = read_file(os.path.join(path, "input.txt"))
    ic.disable()
    print(format_solution(directory_name, part_one(lines), part_two(lines)))


if __name__ == '__main__':
    solutions()
