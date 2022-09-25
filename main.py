from dataclasses import dataclass
import random

# individual parameters according to the task
day = 31
month = 10
year = 2001

# positions for the game
game_positions = range(1, day + month + year + 1)

# moves that both players can do
range_of_moves = range(1, day + month + 1)

# final position to win for both players
first_player_final_positions = {day + month + year}
second_player_final_positions = {day + month + year}

# available positions for both players
first_player_available_position = set(range(1, day + month + year + 1))
second_player_available_position = set(range(1, day + month + year + 1))


# dataclass for player with all necessary parameters
@dataclass
class Player:
    final_positions: set  # set of final positions for player
    available_positions: set  # set of available positions for player
    winning_strategy_from_your_turn: set  # set of winning positions if it is your turn now
    winning_strategy_from_opponent_turn: set  # set of winning positions if it is opponent turn now
    your_turn: bool  # flag to check which turn is now to calculate winning strategy


# objects of player for the current game
my_player = Player(
    final_positions=first_player_final_positions,
    available_positions=first_player_available_position,
    winning_strategy_from_your_turn=set(),
    winning_strategy_from_opponent_turn=first_player_final_positions.copy(),
    your_turn=True,
)


# function that determines if current play p->q is valid
def if_move_is_possible(p, q):
    return (q - p) > day + month


# function that returns set of all possible moves from current position
def possible_moves_from_position(p):
    result = []
    for i in range(1, day + month + 1):
        if (p + i) <= day + month + year:
            result.append(p + i)
    return set(result)


# function that add moves to winning strategy from your turn
def exists_move_to_winning_position(p, player):
    moves = possible_moves_from_position(p)
    for (
        move
    ) in (
        moves
    ):  # check if there is a move to winning position from any turn of your opponent
        if move in player.winning_strategy_from_opponent_turn:
            return True  # if from position to which we moved any opponent play leads to winning position
            # from your next turn then we can add this position to winning strategy
    return False  # if there is no such move then we can't add this position to winning strategy


# function that add moves to winning strategy from opponent turn
def all_moves_to_winning_position(p, player):
    moves = possible_moves_from_position(p)
    for move in moves:
        if (
            move not in player.winning_strategy_from_your_turn
        ):  # if any move from opponent turn leads to position from which
            # we can't move to winning position from our turn then we can't add this position to winning strategy
            return False
    return True  # else we can add this position to winning strategy


# function that calculates winning strategy for player
def FPG_solution(player_to_wining):
    for position in (
        player_to_wining.available_positions - player_to_wining.final_positions
    ):
        if (
            player_to_wining.your_turn
        ):  # if it is your turn calculate winning strategy from your turn
            if exists_move_to_winning_position(position, player_to_wining):
                player_to_wining.winning_strategy_from_your_turn.add(position)
        else:  # if it is opponent turn calculate winning strategy from opponent turn
            if all_moves_to_winning_position(position, player_to_wining):
                player_to_wining.winning_strategy_from_opponent_turn.add(position)
    player_to_wining.your_turn = (
        not player_to_wining.your_turn
    )  # change player turn to opposite


# function to interact with user to make manual plays
def player_manually_move(current_position):
    print(
        f"It is your turn. Current position is "
        f"{current_position}. Possible moves are from"
        # range of possible moves from current position for player
        f" {min(possible_moves_from_position(current_position))} "
        f"to {max(possible_moves_from_position(current_position))}"
    )

    print("Enter available position to move")
    move = -1
    while True:  # check that entered data is move and it is possible
        try:
            move = int(input())
            if move not in possible_moves_from_position(current_position):
                print("Wrong move, try again")
                continue
            break
        except ValueError:
            print("Wrong input, try again")
            continue
    print(f"Your move {current_position}->{move}")
    print("------------------")
    return move


# function to make smart move to bot
def bot_smart_move(current_position, player):
    print("Now it is Spoiler turn")
    # if there is a move to final position from your turn then make it
    if (day + month + year) in possible_moves_from_position(current_position):
        print(f"Spoiler move {current_position}->{day + month + year}")
        return day + month + year
    # make random move initially
    spoiler_move = random.choice(list(possible_moves_from_position(current_position)))

    # if there is a move to winning position from opponent turn then make it
    if (
        current_position in player.winning_strategy_from_your_turn
    ):  # check we are in winning position from your turn
        # find move to winning position from any opponent turn
        for move in possible_moves_from_position(
            current_position
        ):  # check all possible moves
            # if move leads to winning position from opponent turn then make it
            if move in player.winning_strategy_from_opponent_turn:
                spoiler_move = move  # make this move
                break
    else:
        # if there is no move to winning position from your turn then make random move
        print("I don't know what to do, so I will move randomly")
    print(f"Spoiler move {current_position}->{spoiler_move}")
    print("------------------")
    current_position = spoiler_move
    return current_position


# main function to play game
def main():
    # calculate winning position from your turn and opponent turn
    # according to the Knaster-Tarski theorem this while loop will end
    while True:
        # winning strategy before applying FPG solution function
        before = my_player.winning_strategy_from_your_turn.union(
            my_player.winning_strategy_from_opponent_turn
        )
        # calculate step of FPG solution function
        FPG_solution(my_player)
        # winning strategy after applying FPG solution function
        after = my_player.winning_strategy_from_your_turn.union(
            my_player.winning_strategy_from_opponent_turn
        )
        # loop terminates when we reach fixed point of the FPG solution function
        if before == after:
            break
    start_position = None
    game_mode = None
    print(
        "How start position should be chosen? Press 1 to chose it randomly, 2 to chose it manually"
    )

    # start position choose from the user with exception handling
    while True:
        try:
            start_mode = int(input())
            if start_mode == 1:
                start_position = random.randint(1, day + month + year)
                break
            elif start_mode == 2:
                print(f"Choose start position from 1 to {day + month + year}")
                start_position = int(input())
                if start_position not in my_player.available_positions:
                    print("Wrong position, try again")
                    continue
                break
            else:
                print("Wrong choice")
                continue
        except ValueError:
            print("Wrong input, try again")
            continue
    print("Chose playing mode: 1 - smart, 2 - random, 3 - advisor")

    # game mode choose from the user with exception handling
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

    # check if player won before the first move
    current_position = start_position
    if current_position in my_player.final_positions:
        print(f"You won from the beginning")
        return

    # simulation for game mode 2
    if game_mode == 2:
        while True:
            # manual move from player
            move = player_manually_move(current_position)
            current_position = move
            if move in my_player.final_positions:
                print("You won, game over")
                return

            # random move from bot
            spoiler_move = random.choice(
                list(possible_moves_from_position(current_position))
            )
            print(f"Spoiler move {current_position}->{spoiler_move}")
            current_position = spoiler_move
            if spoiler_move in my_player.final_positions:
                print("Spoiler won, game over")
                return

    # simulation for game mode 1
    if game_mode == 1:
        while True:
            # manual move from player
            move = player_manually_move(current_position)
            current_position = move
            if move in my_player.final_positions:
                print("You won, game over")
                return

            # smart move from bot
            current_position = bot_smart_move(current_position, my_player)
            if current_position in my_player.final_positions:
                print("Spoiler won, game over")
                return

    # simulation for game mode 3
    if game_mode == 3:
        while True:
            # advise to the player from the winning strategy
            if current_position in my_player.winning_strategy_from_your_turn:
                for win_move in possible_moves_from_position(current_position):
                    if win_move in my_player.winning_strategy_from_opponent_turn:
                        print(f"You can win if you move to {win_move}")
                        break
            else:
                # if where is no winning strategy from your turn then advise to make random move
                print("You can't win from this position, just make random move")

            move = player_manually_move(current_position)
            current_position = move
            if move in my_player.final_positions:
                print("You won, game over")
                return
            # smart move from bot
            current_position = bot_smart_move(current_position, my_player)
            if current_position in my_player.final_positions:
                print("Spoiler won, game over")
                return


if __name__ == "__main__":
    main()
