from  dataclasses import dataclass


day = 31
month = 10
year = 2001
game_positions = range(1, day + month + year + 1)
range_of_moves = range(1, day + month + 1)

first_player_final_positions = {day + month + year}
second_player_final_positions = {day + month + year}

first_player_available_position = set(range(1, day + month + year + 1))
second_player_available_position = set(range(1, day + month + year + 1))


@dataclass
class Player:
    final_positions: set
    available_positions: set
    winning_strategy_positions: set
    name: str


first_plyer = Player(final_positions=first_player_final_positions,
                     available_positions=first_player_available_position,
                     winning_strategy_positions=set(),
                     name='spoiler')

second_player = Player(final_positions=second_player_final_positions,
                       available_positions=second_player_available_position,
                       winning_strategy_positions=set(),
                       name='duplicator')


def if_move_is_possible(p, q):
    return (q - p) > day + month


def possible_moves_from_position(p):
    result = []
    for i in range(day+month):
        if (p + i) <= day + month + year:
            result.append(p+i)
    return set(result)


def exists_move_to_winning_position(p, player):
    moves = possible_moves_from_position(p)
    have_winning_move = False
    for move in moves:
        if move in player.winning_strategy_positions:
            have_winning_move = True
            break
    return have_winning_move


def all_moves_to_winning_position(p, player):
    moves = possible_moves_from_position(p)
    for move in moves:
        if move not in player.winning_strategy_positions:
            return False
    return True


def FPG_solution(player_to_wining, opposite_player):
    strategy = player_to_wining.final_positions
    first_subset = set()
    second_subset = set()
    for p in (player_to_wining.available_positions - player_to_wining.final_positions):
        if exists_move_to_winning_position(p, player_to_wining):
            first_subset.add(p)
    for p in (opposite_player.available_positions - opposite_player.final_positions):
        if all_moves_to_winning_position(p, player_to_wining):
            second_subset.add(p)
    strategy = strategy.union(first_subset)
    strategy = strategy.union(second_subset)
    return strategy


def main():
    for i in range(3):
        first_plyer.winning_strategy_positions = FPG_solution(first_plyer, second_player)
        # print(first_plyer.winning_strategy_positions)


if __name__ == '__main__':
    main()
