import os
from utils.timeit import timeit

from icecream import ic

from utils.utils import read_file, format_solution, Colors

colors = Colors()


def parse_lines(lines: list[str]):
    return lines


def part_one(lines):
    res = 0
    return res


def part_two(lines):
    res = 0
    return res


@timeit
def solutions():
    path = os.path.dirname(os.path.realpath(__file__))
    directory_name = " ".join(path.split(os.path.sep)[-1].capitalize().split("_"))

    lines = read_file(os.path.join(path, "input.txt"))
    print(format_solution(directory_name, part_one(lines), part_two(lines)))


if __name__ == '__main__':
    solutions()
