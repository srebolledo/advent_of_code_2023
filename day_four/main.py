import copy
import os
import sys
import traceback

from icecream import ic

from utils.utils import read_file, format_solution, Colors

colors = Colors()

def part_one(lines):
    res = 0
    return res


def part_two(lines):
    res = 0
    return res


def solutions():
    path = os.path.dirname(os.path.realpath(__file__))
    lines = read_file(os.path.join(path, "input.txt"))
    print(format_solution(4, part_one(lines), part_two(lines)))


if __name__ == '__main__':
    solutions()
