import os

from icecream import ic
from utils.utils import read_file, format_solution

rules = {
    'red': 12,
    'green': 13,
    'blue': 14
}

ic.disable()


def split_iterations(line):
    cubes_to_return = {}
    games = line.split(';')
    counter = 1
    for game in games:
        config = {}
        cubes = game.split(',')
        for cube in cubes:
            s = cube.strip().split(" ")
            if s[1] not in config:
                config[s[1]] = 0
            config[s[1]] += int(s[0])
        cubes_to_return[counter] = config
        counter += 1
    return cubes_to_return


def configuration_valid(configuration: dict):
    for key, cube_amounts in configuration.items():
        for color, cube_amount in cube_amounts.items():
            ic(f"\t>> {color} {cube_amount} <= {rules[color]}")

            if color in rules and cube_amount <= rules[color]:
                continue
            else:
                ic(f"Not satisfies {color} {cube_amount} <= {rules[color]}")
                return False
    return True


def part_one(played_games):
    res = 0
    for key, game in played_games.items():
        ic(f"{key} -> {game} ({len(game)})")
        if configuration_valid(game):
            res += int(key)
    return res


def part_two(played_games):
    res = 0
    for key, game in played_games.items():
        ic(f"{key} -> {game} ({len(game)})")
        configuration = {key: 0 for key, value in rules.items()}
        for k, config in game.items():

            for color, cube_amount in config.items():
                if configuration[color] < cube_amount:
                    configuration[color] = cube_amount
        ic(f"Configuration: {configuration}")
        power_of_cubes = configuration['red'] * configuration['green'] * configuration['blue']
        ic(f"Result game {key}: {power_of_cubes}")
        res += power_of_cubes
    return res


def solutions():
    path = os.path.dirname(os.path.realpath(__file__))
    directory_name = " ".join(path.split(os.path.sep)[-1].capitalize().split("_"))

    lines = read_file(os.path.join(path, "input.txt"))
    games = {}
    for line in lines:
        games[line.split(":")[0].replace("Game ", "")] = split_iterations(line.split(":")[1])

    print(format_solution(directory_name, part_one(games), part_two(games)))


if __name__ == '__main__':
    solutions()
