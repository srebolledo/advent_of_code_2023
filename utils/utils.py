def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read().split("\n")


def format_solution(day, part_one, part_two):
    return f"Day {day}:\n\tPart One: {part_one}\n\tPart Two: {part_two}"

class Colors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    def __init__(self):
        self.index = 0
        self.colors = [self.PURPLE, self.CYAN, self.DARKCYAN, self.BLUE, self.GREEN, self.YELLOW, self.RED]

    def get_color(self):
        self.index += 1
        return self.colors[self.index % len(self.colors)]

