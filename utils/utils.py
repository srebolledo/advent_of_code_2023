def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read().split("\n")


def format_solution(day, part_one, part_two):
    return f"Day {day}:\n\tPart One: {part_one}\n\tPart Two: {part_two}"
