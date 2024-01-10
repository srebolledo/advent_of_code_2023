from __future__ import annotations

import math
import os
import re
from utils.timeit import timeit

from icecream import ic

from utils.utils import read_file, format_solution, Colors

colors = Colors()


def parse_lines(lines: list[str]) -> [str, dict[str, tuple[str, str]]]:
    parse = dict()
    index = 0
    steps = ""
    for line in lines:
        if index == 0:
            steps = line.strip()
        elif line.strip() == "":
            continue
        else:
            res = re.search(r"(\w+) = \((\w+), (\w+)\)", line)
            split = line.strip().split(" ")
            ic(f"root: {res.group(1)}, left: {res.group(2)}, right: {res.group(3)}")
            root = res.group(1)
            left = res.group(2)
            right = res.group(3)
            parse[root] = (left, right)
        index += 1

    return steps, parse


def part_one(lines):
    ic.disable()
    steps, res_dict = parse_lines(lines)
    # walk the dict
    actual_node = "AAA"
    step_amount = 0
    index = 0
    while actual_node != "ZZZ":
        # check that the step is in the length of steps string, if not, step should be 0 again
        if index == len(steps):
            index = 0
        instruction = steps[index]
        old_node = actual_node
        if instruction == "L":
            actual_node = res_dict[actual_node][0]
        elif instruction == "R":
            actual_node = res_dict[actual_node][1]
        ic(f"Instruction {instruction} makes us go from {old_node} -> {actual_node}")

        step_amount += 1
        index += 1
    ic(f"From AAA to ZZZ in {step_amount} steps")
    return step_amount


def part_two(lines):
    res = []
    steps, res_dict = parse_lines(lines)
    actual_nodes = list(filter(lambda x: x.endswith("A"), res_dict.keys()))
    steps_per_node: dict[str, list[str]] = dict()
    for node in actual_nodes:
        if node not in steps_per_node:
            steps_per_node[node] = list()
        index = 0
        actual_node = node
        while not actual_node.endswith("Z"):
            if index == len(steps):
                index = 0
            # update all actual nodes with step
            instruction = steps[index]
            steps_per_node[node].append(instruction)
            if instruction == "L":
                actual_node = res_dict[actual_node][0]
            elif instruction == "R":
                actual_node = res_dict[actual_node][1]
            index += 1
    for key, value in steps_per_node.items():
        res.append(len(value))
    return math.lcm(*res)


@timeit
def solutions():
    path = os.path.dirname(os.path.realpath(__file__))
    directory_name = " ".join(path.split(os.path.sep)[-1].capitalize().split("_"))

    lines = read_file(os.path.join(path, "input.txt"))
    print(format_solution(directory_name, part_one(lines), part_two(lines)))


if __name__ == '__main__':
    solutions()
