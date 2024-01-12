import math
import os
import sys
from enum import Enum, StrEnum
from typing import Tuple, Self

from utils.timeit import timeit

from icecream import ic

from utils.utils import read_file, format_solution, Colors, run_solutions

colors = Colors()


class Direction(Enum):
    UP = -1, 0
    LEFT = 0, -1
    CENTER = 0, 0
    RIGHT = 0, 1
    DOWN = 1, 0
    DEAD_END = 0, 0


map_characters = {
    "|": "\u2503",
    "-": "\u2501",
    "L": "\u2517",
    "J": "\u251b",
    "F": "\u250f",
    "7": "\u2513",
    ".": ".",
    "S": "S",
    "": "0"

}


class PipetType(StrEnum):
    vertical = "|"
    horizontal = "-"
    up_right = "L"
    up_left = "J"
    down_right = "F"
    down_left = "7"
    ground = "."
    start = "S"


def get_opposite_direction(direction: Direction) -> Direction:
    if direction == Direction.UP:
        return Direction.DOWN
    if direction == Direction.DOWN:
        return Direction.UP
    if direction == Direction.LEFT:
        return Direction.RIGHT
    if direction == Direction.RIGHT:
        return Direction.LEFT


def get_connections(pipe_type: PipetType) -> list[Direction]:
    directions: list[Direction] = list()

    if pipe_type == PipetType.vertical:
        directions.append(Direction.UP)
        directions.append(Direction.DOWN)

    if pipe_type == PipetType.horizontal:
        directions.append(Direction.LEFT)
        directions.append(Direction.RIGHT)

    if pipe_type == PipetType.up_right:
        directions.append(Direction.UP)
        directions.append(Direction.RIGHT)

    if pipe_type == PipetType.up_left:
        directions.append(Direction.UP)
        directions.append(Direction.LEFT)

    if pipe_type == PipetType.down_right:
        directions.append(Direction.DOWN)
        directions.append(Direction.RIGHT)

    if pipe_type == PipetType.down_left:
        directions.append(Direction.DOWN)
        directions.append(Direction.LEFT)

    if pipe_type == PipetType.start:
        directions.append(Direction.UP)
        directions.append(Direction.DOWN)
        directions.append(Direction.LEFT)
        directions.append(Direction.RIGHT)

    return directions


class Pipe:
    pipe_char: str
    pipe_type: PipetType
    possible_connections: list[Direction]
    connections: dict[Direction, Self]
    x: int
    y: int

    def __init__(self, char):
        self.pipe_char = char
        self.pipe_type = PipetType(char)
        self.possible_connections = get_connections(self.pipe_type)
        self.connections = dict()

    def __str__(self):
        return f"Char: {self.pipe_char}, pipe type: {self.pipe_type}, possible_connections: {self.possible_connections}, connections: {[str(f'{key}=>{value.pipe_char}') for key, value in self.connections.items()]}"

    def add_connection(self, direction: Direction, pipe: Self):
        self.connections[direction] = pipe

    def add_position(self, row_index, col_index):
        self.x = row_index
        self.y = col_index

    def next_node_for_direction(self, direction: Direction):
        return tuple_sum(direction.value, (self.x, self.y))

    def get_direction_and_node(self, direction) -> Self:
        if direction in self.connections:
            return self.connections[direction]

    def get_other_direction_and_node(self, direction) -> Self:
        return list(filter(lambda x: x != direction, list(self.connections.keys())))[0]


def parse_lines(lines: list[str]) -> [list[list[Pipe]], tuple[int, int]]:
    rows = []
    s_position = ()
    for line in lines:
        columns = []
        for c in line:
            columns.append(Pipe(c))
            if c == "S":
                s_position = (len(rows), len(columns) - 1)
        rows.append(columns)
    return rows, s_position


def tuple_sum(a: tuple, b: tuple) -> tuple:
    return a[0] + b[0], a[1] + b[1]


def is_position_valid(bid_array: list[list], position: tuple[int, int]) -> bool:
    len_x = len(bid_array)
    len_y = len(bid_array[0])
    return 0 <= position[0] < len_x and 0 <= position[1] < len_y


def get_all_possible_pipes(current_pipe: Pipe, position: tuple[int, int], rows: list[list[Pipe]]) -> list[Pipe]:
    connections = current_pipe.possible_connections
    ret_pipes = []
    for direction in connections:
        potential_pipe_pos = tuple_sum(position, direction.value)
        if is_position_valid(rows, potential_pipe_pos):
            potential_pipe = rows[potential_pipe_pos[0]][potential_pipe_pos[1]]
            if potential_pipe.pipe_char == ".":
                continue

            for directions_in_potential_pipe in potential_pipe.possible_connections:

                test_pipe_pos = tuple_sum(directions_in_potential_pipe.value, potential_pipe_pos)
                if is_position_valid(rows, test_pipe_pos):
                    if rows[test_pipe_pos[0]][test_pipe_pos[1]] == current_pipe:
                        ret_pipes.append(potential_pipe)
                        current_pipe.add_connection(direction, potential_pipe)
                        potential_pipe.add_connection(directions_in_potential_pipe, current_pipe)
    return ret_pipes


def make_pipe_connections(rows: list[list[Pipe]]) -> None:
    row_index = 0
    for columns in rows:
        col_index = 0
        for pipe in columns:
            get_all_possible_pipes(pipe, (row_index, col_index), rows)
            pipe.add_position(row_index, col_index)
            col_index += 1
        row_index += 1


def get_grid_copy(len_x: int, len_y: int) -> list[list[str]]:
    rows = list()
    for i in range(len_x):
        columns = list()
        for j in range(len_y):
            columns.append("")
        rows.append(columns)
    return rows


def create_maze_solution(maze_solution, solution_pipes):
    for pipe in solution_pipes:
        maze_solution[pipe.x][pipe.y] = pipe.pipe_char

    print_maze(maze_solution)


def print_maze(maze):
    for i in range(len(maze)):
        col = ""
        for j in range(len(maze[i])):
            col += map_characters[maze[i][j]]
        print(col)


def get_solution_pipes(rows, start):
    make_pipe_connections(rows)
    start_node: Pipe = rows[start[0]][start[1]]
    actual_node: Pipe = start_node
    solution_pipes = [start_node]
    actual_direction = list(actual_node.connections.keys())[0]
    loop_length = 0
    while True:
        actual_node = actual_node.connections[actual_direction]
        opposite_direction = get_opposite_direction(actual_direction)
        actual_direction = actual_node.get_other_direction_and_node(opposite_direction)
        solution_pipes.append(actual_node)
        loop_length += 1
        if actual_node == start_node:
            break
    return solution_pipes, loop_length


def part_one(lines):
    rows, start = parse_lines(lines)
    solution_pipes, loop_length = get_solution_pipes(rows, start)

    maze_solution = get_grid_copy(len(rows), len(rows[0]))
    create_maze_solution(maze_solution, solution_pipes)

    # add connections for each pipe
    return math.floor(loop_length / 2)


def part_two(lines):
    rows, start = parse_lines(lines)
    solution_pipes, loop_length = get_solution_pipes(rows, start)
    return 0


@timeit
def solutions():
    path = os.path.dirname(os.path.realpath(__file__))
    lines = read_file(os.path.join(path, "input.txt"))
    run_solutions(path, part_one, part_two, lines)


if __name__ == '__main__':
    solutions()
