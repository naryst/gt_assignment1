from dataclasses import dataclass
import random


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
                     winning_strategy_from_opponent_turn=first_player_final_positions.copy(),
                     your_turn=True,
                     name='Duplicator')

second_player = Player(final_positions=second_player_final_positions,
                       available_positions=second_player_available_position,
                       winning_strategy_from_your_turn=set(),
                       winning_strategy_from_opponent_turn=second_player_final_positions.copy(),
                       your_turn=False,
                       name='Spoiler')


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
    for position in (player_to_wining.available_positions - player_to_wining.final_positions):
        if player_to_wining.your_turn:
            if exists_move_to_winning_position(position, player_to_wining):
                player_to_wining.winning_strategy_from_your_turn.add(position)
        else:
            if all_moves_to_winning_position(position, player_to_wining):
                player_to_wining.winning_strategy_from_opponent_turn.add(position)
    player_to_wining.your_turn = not player_to_wining.your_turn


def player_manually_move(current_position):
    print(f'It is your turn. Current position is '
          f'{current_position}. Possible moves are from'
          f' {min(possible_moves_from_position(current_position))} '
          f'to {max(possible_moves_from_position(current_position))}')

    print('Enter available position to move')
    move = -1
    while True:
        try:
            move = int(input())
            if move not in possible_moves_from_position(current_position):
                print("Wrong move, try again")
                continue
            break
        except ValueError:
            print("Wrong input, try again")
            continue
    print(f'Your move {current_position}->{move}')
    print('------------------')
    return move


def bot_smart_move(current_position, player):
    print('Now it is Spoiler turn')
    if (day + month + year) in possible_moves_from_position(current_position):
        print(f'Spoiler move {current_position}->{day + month + year}')
        print("Spoiler won, game over")
        return
    spoiler_move = random.choice(list(possible_moves_from_position(current_position)))
    if current_position in player.winning_strategy_from_your_turn:
        for move in possible_moves_from_position(current_position):
            if move in player.winning_strategy_from_opponent_turn:
                spoiler_move = move
                break
    else:
        print('I don\'t know what to do, so I will move randomly')
    print(f'Spoiler move {current_position}->{spoiler_move}')
    print('------------------')
    current_position = spoiler_move
    return current_position


def main():
    while True:
        before = first_plyer.winning_strategy_from_your_turn.union(first_plyer.winning_strategy_from_opponent_turn)
        FPG_solution(first_plyer)
        after = first_plyer.winning_strategy_from_your_turn.union(first_plyer.winning_strategy_from_opponent_turn)
        if before == after:
            break
    start_position = None
    game_mode = None
    print("How start position should be chosen? Press 1 to chose it randomly, 2 to chose it manually")
    while True:
        try:
            start_mode = int(input())
            if start_mode == 1:
                start_position = random.randint(1, day + month + year)
                break
            elif start_mode == 2:
                print(f'Choose start position from 1 to {day + month + year}')
                start_position = int(input())
                if start_position not in first_plyer.available_positions:
                    print("Wrong position, try again")
                    continue
                break
            else:
                print("Wrong choice")
                continue
        except ValueError:
            print("Wrong input, try again")
            continue
    print('Chose playing mode: 1 - smart, 2 - random, 3 - advisor')

    while True:
        try:
            game_mode = int(input())
            if not ((game_mode == 1) or (game_mode == 2) or (game_mode == 3)):
                print("Wrong choice, try again")
                continue
        except ValueError:
            print("Wrong input, try again")
            continue
        break
    current_position = start_position
    if current_position in first_plyer.final_positions:
        print(f'You won from the beginning')
        return

    # simulation for game mode 2
    if game_mode == 2:
        while True:
            move = player_manually_move(current_position)
            current_position = move
            if move in first_plyer.final_positions:
                print("You won, game over")
                return

            spoiler_move = random.choice(list(possible_moves_from_position(current_position)))
            print(f'Spoiler move {current_position}->{spoiler_move}')
            current_position = spoiler_move
            if spoiler_move in first_plyer.final_positions:
                print("Spoiler won, game over")
                return

    # simulation for game mode 1
    if game_mode == 1:
        while True:
            move = player_manually_move(current_position)
            current_position = move
            if move in first_plyer.final_positions:
                print("You won, game over")
                return
            print('Now it is Spoiler turn')
            current_position = bot_smart_move(current_position, first_plyer)

    # simulation for game mode 3
    if game_mode == 3:
        while True:
            if current_position in first_plyer.winning_strategy_from_your_turn:
                for win_move in possible_moves_from_position(current_position):
                    if win_move in first_plyer.winning_strategy_from_opponent_turn:
                        print(f'You can win if you move to {win_move}')
                        break
            else:
                print('You can\'t win from this position')

            move = player_manually_move(current_position)
            current_position = move
            if move in first_plyer.final_positions:
                print("You won, game over")
                return
            current_position = bot_smart_move(current_position, first_plyer)


if __name__ == '__main__':
    main()
