from dataclasses import dataclass


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
    winning_strategy_from_your_turn: set
    winning_strategy_from_opponent_turn: set
    your_turn: bool
    name: str


first_plyer = Player(final_positions=first_player_final_positions,
                     available_positions=first_player_available_position,
                     winning_strategy_from_your_turn=set(),
                     winning_strategy_from_opponent_turn=first_player_final_positions,
                     your_turn=True,
                     name='spoiler')

second_player = Player(final_positions=second_player_final_positions,
                       available_positions=second_player_available_position,
                       winning_strategy_from_your_turn=set(),
                       winning_strategy_from_opponent_turn=second_player_final_positions,
                       your_turn=False,
                       name='duplicator')


def if_move_is_possible(p, q):
    return (q - p) > day + month


def possible_moves_from_position(p):
    result = []
    for i in range(1, day+month + 1):
        if (p + i) <= day + month + year:
            result.append(p+i)
    return set(result)


def exists_move_to_winning_position(p, player):
    moves = possible_moves_from_position(p)
    for move in moves:
        if move in player.winning_strategy_from_opponent_turn:
            return True
    return False


def all_moves_to_winning_position(p, player):
    moves = possible_moves_from_position(p)
    for move in moves:
        if move not in player.winning_strategy_from_your_turn:
            return False
    return True


def FPG_solution(player_to_wining):
    your_move_subset = set()
    opponent_move_subset = set()
    for position in (player_to_wining.available_positions - player_to_wining.final_positions):
        if player_to_wining.your_turn:
            if exists_move_to_winning_position(position, player_to_wining):
                player_to_wining.winning_strategy_from_your_turn.add(position)
        else:
            if all_moves_to_winning_position(position, player_to_wining):
                player_to_wining.winning_strategy_from_opponent_turn.add(position)
    player_to_wining.your_turn = not player_to_wining.your_turn


def main():
    while True:
        before = first_plyer.winning_strategy_from_your_turn.union(first_plyer.winning_strategy_from_opponent_turn)
        FPG_solution(first_plyer)
        after = first_plyer.winning_strategy_from_your_turn.union(first_plyer.winning_strategy_from_opponent_turn)
        if before == after:
            break
    print(f'First player winning strategy: {first_plyer.winning_strategy_from_your_turn}')
    print(f'First player losing strategy: {first_plyer.winning_strategy_from_opponent_turn}')
    print(list(filter(lambda x: x > 1931, first_plyer.winning_strategy_from_opponent_turn)))


if __name__ == '__main__':
    main()
