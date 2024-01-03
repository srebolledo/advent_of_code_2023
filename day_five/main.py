import copy
import os

from icecream import ic

from utils.utils import read_file, format_solution, Colors

colors = Colors()


class AtoB:
    def __init__(self, lines, map_name):
        self.lines = lines
        self.map_name = map_name
        self.maps = []
        for line in self.lines:
            dest, orig, r = line.split(" ")
            self.maps.append({
                "dest": int(dest),
                "orig": int(orig),
                "range": int(r)
            })

    def get_number(self, index):

        for number_map in self.maps:
            orig = number_map["orig"]
            dest = number_map["dest"]
            map_range = number_map["range"]
            ic(f"{index} -> {orig} - {dest} - {map_range}")
            if index >= orig and index <= orig + map_range:
                # in range, needs to transform
                return index - orig + dest
        return index


def parse_lines(lines):
    seeds = []
    maps = []
    map_name = ""
    map_lines = []
    line_index = 0
    for line in lines:
        if line_index == 0:
            seeds = map(int, line.replace("seeds: ", "").strip().split(" "))
            ic(f"Found seeds {seeds}")

        elif line.endswith(" map:"):
            map_name = line.replace(" map:", "")
            ic(f"Found map with name {map_name}")

        elif line == "" and len(map_name) == 0:
            ic("Found a blank line but no map, doing nothing!")
        elif line == "":
            ic("Found a blank line, processing map")
            maps.append(AtoB(map_lines, map_name))
            map_lines = []
            map_name = ""
        else:
            ic(f"found numbers for map {map_name}: {line}")
            map_lines.append(line)

        line_index += 1
    if len(map_name) > 0 and len(map_lines) > 0:
        maps.append(AtoB(map_lines, map_name))

    return seeds, maps


def part_one(lines):
    res = []
    seeds, maps = parse_lines(lines)
    for i in seeds:
        n = i
        mappings = []
        for m in maps:
            n = m.get_number(n)
            mappings.append(f"{m.map_name} {n} ")
        res.append(n)

        ic(f"seed: {i} {''.join(mappings)}")

    return min(res)


def get_seed_and_range(seeds: list[int]) -> list[(int, int)]:
    seeds = list(seeds)
    seed_and_range = []
    index = 0
    while index < len(seeds):
        ic(f"{seeds[index]} {seeds[index + 1]}")
        seed_and_range.append((seeds[index], seeds[index + 1]))
        index += 2
    return seed_and_range


def part_two(lines):
    res = [1]
    seeds, maps = parse_lines(lines)
    seed_and_range = get_seed_and_range(seeds)
    print(seed_and_range)

    return 0


def solutions():
    path = os.path.dirname(os.path.realpath(__file__))
    lines = read_file(os.path.join(path, "input.txt"))
    ic.disable()
    print(format_solution(5, part_one(lines), part_two(lines)))


if __name__ == '__main__':
    solutions()
