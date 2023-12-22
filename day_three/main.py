import copy
import os
import sys
import traceback

from icecream import ic

from utils.utils import read_file, format_solution, Colors

ic.disable()

colors = Colors()

def to_matrix(lines):
    matrix = []
    for line in lines:
        inner = []
        for c in line:
            inner.append(c)
        matrix.append(inner)
    return matrix


def has_symbol_in_row(matrix, colored_matrix, row_index: int, checking_row: int, number_start: int, number_end: int) -> \
        tuple[
            bool, int, int, int, [[str]], [str]]:
    row = matrix[row_index]
    row_colored = colored_matrix[row_index]

    start_pos = number_start
    end_pos = number_end
    start_pos = max(0, start_pos - 1)
    end_pos = min(end_pos + 1, len(row) - 1)

    solution = []
    color = colors.get_color()
    iter_start = start_pos
    while iter_start < end_pos:
        try:
            if row[iter_start] != '.' and not row[iter_start].isnumeric():
                ic(
                    f"Found symbol {row[iter_start]} at {row_index + 1}:{iter_start + 1} ({number_start}:{number_end} -> {start_pos}:{end_pos})!")
                number = []
                word = []
                for i in range(start_pos, end_pos):
                    word.append(f"{row[i]}")
                    number.append(f"{matrix[checking_row][i]}")

                    if row_colored[i] != '.' and not row_colored[i].isnumeric():
                        row_colored[i] = f"{color}{matrix[row_index][i]}{Colors.END}"
                    if matrix[checking_row][i].isnumeric():
                        colored_matrix[checking_row][i] = f"{color}{matrix[checking_row][i]}{Colors.END}"
                if row_index == checking_row:
                    solution.append(word)
                if row_index > checking_row:
                    solution.append(number)
                    solution.append(word)
                if row_index < checking_row:
                    solution.append(word)
                    solution.append(number)

                ic(f"Current row is {checking_row}, positions {start_pos} to {end_pos}")
                return True, row_index, checking_row, start_pos, solution, word
        except Exception as e:
            print(f"Exception: {e}")
        iter_start += 1
    return False, row_index, checking_row, -1, [], []


def check_symbol_tuple(potential_number: [str], symbol_tuple: tuple[bool, int, int, int, [[str]], [str]]) -> tuple[
    bool, int, int]:
    found_char, row_index, checking_row, column_index, solution, array_found = symbol_tuple
    row_desc = "same row" if row_index == checking_row else ""
    if checking_row > row_index:
        row_desc = "previous row"
    elif checking_row < row_index:
        row_desc = "next row"
    if found_char:
        s = []
        for ss in solution:
            for sss in ss:
                s.append(sss)
            s.append('\n')
        ic(f"{potential_number} found in {row_desc} {row_index} column {column_index} \n {' '.join(s)}")
        return True, row_index, column_index
    return False, -1, -1


def print_matrix(matrix):
    for i in range(len(matrix)):
        word = []
        for j in range(len(matrix[i])):
            word.append(matrix[i][j])
        ic(''.join(word))


def part_one(lines):
    res = 0
    matrix = to_matrix(lines)
    colored_matrix = copy.deepcopy(matrix)
    row_index = 0
    numbers_found = []
    while row_index < len(matrix):
        column_index = 0
        while column_index < len(matrix[row_index]):
            if matrix[row_index][column_index].isnumeric():
                potential_number = []
                column_search = column_index
                while column_search < len(matrix[row_index]) and matrix[row_index][column_search].isnumeric():
                    potential_number.append(matrix[row_index][column_search])
                    column_search += 1
                number_start = column_index
                number_end = column_index + len(potential_number)
                prev_row = row_index - 1
                post_row = row_index + 1
                n = []
                for i in range(number_start, number_end):
                    n.append(matrix[row_index][i])
                    ic(f"{''.join(potential_number)} ({''.join(n)}) found on position {number_start + 1}:{number_end} of row {row_index}")

                try:
                    # same row
                    check_result, row_id, column_id = check_symbol_tuple(potential_number,
                                                                         has_symbol_in_row(matrix, colored_matrix,
                                                                                           row_index, row_index,
                                                                                           number_start,
                                                                                           number_end))
                    # prev row only if 0
                    if prev_row > -1 and not check_result:
                        check_result, row_id, column_id = check_symbol_tuple(potential_number,
                                                                             has_symbol_in_row(matrix, colored_matrix,
                                                                                               prev_row, row_index,
                                                                                               number_start,
                                                                                               number_end))
                    if post_row < len(matrix) and not check_result:
                        check_result, row_id, column_id = check_symbol_tuple(potential_number,
                                                                             has_symbol_in_row(matrix, colored_matrix,
                                                                                               post_row, row_index,
                                                                                               number_start,
                                                                                               number_end))

                    if check_result:
                        number = int(''.join(potential_number))
                        numbers_found.append(number)
                        res += number
                    else:
                        ic(f"{''.join(potential_number)} is not valid")
                    column_index = column_index + len(potential_number)

                except Exception as e:
                    line_number = []
                    for i in range(number_start, number_end):
                        line_number.append(matrix[row_index][i])
                    ic(f"{''.join(line_number)} {row_index} {number_start} {number_end} {number_start}")
                    print(traceback.print_exc(file=sys.stdout))
                    sys.exit(0)
            else:
                column_index += 1
        row_index += 1
    print_matrix(colored_matrix)
    return res


def part_two(lines):
    res = 0

    return res


def solutions():
    path = os.path.dirname(os.path.realpath(__file__))
    lines = read_file(os.path.join(path, "input.txt"))
    print(format_solution(1, part_one(lines), part_two(lines)))


if __name__ == '__main__':
    solutions()
