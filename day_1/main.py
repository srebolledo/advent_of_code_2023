import os

from icecream import ic

from utils.timeit import timeit
from utils.utils import read_file, run_solutions
from utils.utils import format_solution

numbers_dict = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

ic.disable()

biggest_word = -1
for k in numbers_dict.keys():
    if len(k) > biggest_word:
        biggest_word = len(k)


def part_one(lines):
    res = 0
    for line in lines:
        numbers = []
        for c in line:
            if c.isnumeric():
                numbers.append(int(c))
        if len(numbers) == 1:
            numbers.append(numbers[0])
        ic(f"\t{line} -> {numbers} -> {numbers[0]}{numbers[-1]}")
        res += int(f"{numbers[0]}{numbers[-1]}")
    return res


def part_two(lines):
    res = 0
    for line in lines:
        numbers = []
        counter = 0
        for c in line:
            ic(f"\tWorking with {c}")
            word_array = []
            if c.isnumeric():
                ic(f"\t\tfound {c} in pos {counter + 1}")
                numbers.append(int(c))
            else:
                word_array.append(c)
                for i in range(1, biggest_word + 1):
                    word = ''.join(word_array)
                    if word in numbers_dict.keys():
                        ic(f"\t\t\tfound {word} in pos {counter + 1, counter + len(word)}")
                        numbers.append(int(numbers_dict[word]))
                        break
                    else:
                        if counter + i >= len(line):
                            break
                        word_array.append(line[counter + i])
            counter += 1
        try:
            if len(numbers) == 1:
                numbers.append(numbers[0])
            ic(f"\t{line} -> {numbers} -> {numbers[0]}{numbers[-1]}")
            res += int(f"{numbers[0]}{numbers[-1]}")
        except Exception as e:
            print(f"Error in line {line} {numbers}")
    return res


@timeit
def solutions():
    path = os.path.dirname(os.path.realpath(__file__))
    lines = read_file(os.path.join(path, "input.txt"))
    run_solutions(path, part_one, part_two, lines)

if __name__ == '__main__':
    solutions()