import copy
import os
import sys

from icecream import ic

from utils.utils import read_file, format_solution, Colors

colors = Colors()


class TimeDistance:
    time: int
    to_beat_distance: int

    def __init__(self, time, distance):
        self.time = int(time)
        self.to_beat_distance = int(distance)

    def calculate_time_to_beat(self):
        pass

    def get_amount_of_best_times(self) -> int:

        minimum_time = -1
        for i in range(1, self.time):
            distance = i * (self.time - i)
            if self.to_beat_distance < distance:
                minimum_time = i
                break

        return self.time - 2 * minimum_time + 1


def get_numbers(line):
    ret = []
    numbers_str = []
    for i in line:
        if i.isnumeric():
            numbers_str.append(i)
        else:
            if len(numbers_str) > 0:
                ret.append(int("".join(numbers_str)))
                numbers_str = []
    if len(numbers_str) > 0:
        ret.append(int("".join(numbers_str)))
    return ret


def parse_lines(lines: list[str], without_spaces=False) -> list[TimeDistance]:
    time_numbers = []
    distance_numbers = []
    for line in lines:
        if line.startswith("Time"):
            time = line.split("Time:")[1].strip()
            time_numbers = get_numbers(time)
        if line.startswith("Distance"):
            distance = line.split("Distance:")[1].strip()
            distance_numbers = get_numbers(distance)
    res: list[TimeDistance] = []
    # both ranges are equal
    if without_spaces:
        res.append(TimeDistance("".join([str(t) for t in time_numbers]), "".join([str(t) for t in distance_numbers])))
    else:
        for i in range(0, len(time_numbers)):
            res.append(TimeDistance(time_numbers[i], distance_numbers[i]))

    return res


def part_one(lines):
    res = 1
    time_distance_list = parse_lines(lines)
    for time_distance in time_distance_list:
        best_times = time_distance.get_amount_of_best_times()
        res *= best_times
    return res


def part_two(lines):
    res = 1
    time_distance_list = parse_lines(lines, True)
    for time_distance in time_distance_list:
        best_times = time_distance.get_amount_of_best_times()
        res *= best_times
    return res


def solutions():
    path = os.path.dirname(os.path.realpath(__file__))
    directory_name = " ".join(path.split(os.path.sep)[-1].capitalize().split("_"))

    lines = read_file(os.path.join(path, "input.txt"))
    print(format_solution(directory_name, part_one(lines), part_two(lines)))


if __name__ == '__main__':
    solutions()
