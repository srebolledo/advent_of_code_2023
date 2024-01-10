from __future__ import annotations

import copy
import math
import os
import re
import sys

from utils.timeit import timeit

from icecream import ic

from utils.utils import read_file, format_solution, Colors, run_solutions

colors = Colors()


class Sensor:
    sequence: list[int]
    child_sensors = list

    def __init__(self):
        self.sequence: list[int] = list()
        self.child_sensors: list[Sensor] = list()

    def add_number(self, number: int) -> None:
        self.sequence.append(number)

    def __calculate_until_zero(self):
        self.child_sensors: list[Sensor] = list()
        actual_sensor = self
        while not actual_sensor.zeroed():
            old_sensor = actual_sensor
            actual_sensor = Sensor()
            for index in range(0, len(old_sensor.sequence) - 1):
                actual_sensor.add_number(old_sensor.sequence[index + 1] - old_sensor.sequence[index])
            self.child_sensors.append(actual_sensor)

    def calculate_next_number_for_sequence(self) -> int:
        self.__calculate_until_zero()

        last_decrement = self.child_sensors[-1].sequence[-1]
        ic(f"last_decrement = {last_decrement}")

        for child_sensor_index in range(len(self.child_sensors) - 2, -1, -1):
            decrement = self.child_sensors[child_sensor_index].sequence[-1] + last_decrement
            last_decrement = decrement
            ic(f"last_decrement = {last_decrement}")

        res = self.sequence[-1] + last_decrement
        ic(f"For sequence {self.sequence} we need to add {res}")
        return res

    def calculate_prior_number(self):
        ic(f"for sequence {self.sequence}")
        self.__calculate_until_zero()
        last_increment = self.child_sensors[-1].sequence[0]
        ic(f"last_increment = {last_increment}")

        for child_sensor_index in range(len(self.child_sensors) - 2, -1, -1):
            ic(f"{self.child_sensors[child_sensor_index]}")
            increment = self.child_sensors[child_sensor_index].sequence[0] - last_increment
            last_increment = increment
            ic(f"last_increment = {last_increment} -> {last_increment}, {self.child_sensors[child_sensor_index].sequence}")

        res = self.sequence[0] - last_increment
        ic(f"For sequence {self.sequence} we need to add at the beginning {res}")
        return res

    def zeroed(self):
        return len(list(filter(lambda x: x == 0, self.sequence))) == len(self.sequence)

    def __str__(self):
        return f"{', '.join(map(str, self.sequence))}"


def parse_lines(lines: list[str]) -> list[Sensor]:
    res = list()
    for i in lines:
        sensor = Sensor()
        for number in i.split(' '):
            sensor.add_number(int(number))
        res.append(sensor)

    return res


def part_one(lines):
    res = 0
    main_sensors = parse_lines(lines)
    for main_sensor in main_sensors:
        res += main_sensor.calculate_next_number_for_sequence()
    return res


def part_two(lines):
    res = 0
    main_sensors = parse_lines(lines)
    for main_sensor in main_sensors:
        res += main_sensor.calculate_prior_number()
    return res


@timeit
def solutions():
    path = os.path.dirname(os.path.realpath(__file__))
    lines = read_file(os.path.join(path, "input.txt"))
    run_solutions(path, part_one, part_two, lines)


if __name__ == '__main__':
    solutions()
