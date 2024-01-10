import copy
import os
import sys

from icecream import ic

from utils.utils import read_file, format_solution, Colors

colors = Colors()


class AtoB:
    def __init__(self, lines, map_name):
        self.lines = lines
        self.map_name = map_name
        map_split = map_name.split("-to-")
        self.map_name_reversed = f"{map_split[1]}-to-{map_split[0]}"
        self.maps = []
        self.maps_reversed = []
        for line in self.lines:
            dest, orig, r = line.split(" ")
            self.maps.append({
                "dest": int(dest),
                "orig": int(orig),
                "range": int(r)
            })

            self.maps_reversed.append({
                "dest": int(orig),
                "orig": int(dest),
                "range": int(r)
            })

    def get_forward_number(self, index):
        return self.__get_number(index, self.maps)

    def get_backward_number(self, index):
        return self.__get_number(index, self.maps_reversed)

    def __get_number(self, index, maps):
        for number_map in maps:
            orig = number_map["orig"]
            dest = number_map["dest"]
            map_range = number_map["range"]
            if orig <= index <= orig + map_range:
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
        n, mappings = get_mapping_number_for_element(maps, n)
        res.append(n)
        ic(f"seed: {i} {''.join(mappings)}")
    return min(res)


def get_mapping_number_for_element(maps: list[AtoB], element):
    n = element
    mappings = []
    for m in maps:
        n = m.get_forward_number(n)
        mappings.append(f"{m.map_name} {n} ")
    return n, mappings


def get_seed_and_range(seeds: list[int]) -> list[(int, int)]:
    seeds = list(seeds)
    seed_and_range = []
    index = 0
    while index < len(seeds):
        print(f"seeds from {seeds[index]} to {seeds[index] + seeds[index+1]}")
        seed_and_range.append((seeds[index], seeds[index] + seeds[index + 1]))
        index += 2
    return seed_and_range


def part_two(lines):
    res = [99999999999999999999999999999]
    seeds, maps = parse_lines(lines)
    seed_and_range = get_seed_and_range(seeds)
    maps.reverse()
    soil_map = maps[0]
    maps = maps[1:]
    max_soil = -1
    iter = 0
    for soil in range(1, 9999999999999999999):
        found_index = soil_map.get_backward_number(soil)
        for mappings in maps:
            found_index = mappings.get_backward_number(found_index)
        for seed_start, seed_end in seed_and_range:
            if found_index >= seed_start:
                if found_index <= seed_end:
                    print(f"found seed in range {seed_start} <= {found_index} <= {seed_end} for soil {soil}")
                    return soil

        iter += 1
        if iter > 1000000:
            print(f"Iterations {iter}")
            iter = 0


    return min(res)


def solutions():
    path = os.path.dirname(os.path.realpath(__file__))
    directory_name = " ".join(path.split(os.path.sep)[-1].capitalize().split("_"))

    lines = read_file(os.path.join(path, "input.txt"))
    print(format_solution(directory_name, part_one(lines), part_two(lines)))


if __name__ == '__main__':
    solutions()
