from Settings import *
from AI import request_ai_move
import time
import copy

x_wins = 0
o_wins = 0
ties = 0

#Inits
def init_board():
    board = [[str(" ") for i in range(5)] for j in range(5)]
    return board

def init_safe_pickup_spots():
    edges_of_The_board = []
    for i in range(5):
        edges_of_The_board.append("(0,"+str(i)+")")
    for i in range(5):
        edges_of_The_board.append("("+str(i)+",0)")
    for i in range(5):
        edges_of_The_board.append("(4,"+str(i)+")")
    for i in range(5):
        edges_of_The_board.append("("+str(i)+",4)")
    return edges_of_The_board

#CONST VARS
EDGES_OF_THE_BOARD = init_safe_pickup_spots()

#Validations
def request_input(prompt, acceptable_responses):
    result = None
    while (result not in acceptable_responses):
        result = input(prompt)
    return result

def valid_pickup(board, player_turn, move_from):
    #Rule: You cannot move another players piece
    move_from_data = move_from[1:4].split(",")
    origin_row, origin_col = int(move_from_data[0]), int(move_from_data[1])
    if (player_turn != board[origin_row][origin_col] and board[origin_row][origin_col] != " "):
        print("Can't pickup another players piece.")
        return False
    
    #Rule: You can only pick from the edge of the board
    if not ("("+str(origin_row)+","+str(origin_col)+")" in EDGES_OF_THE_BOARD):
        print("Pickup must be on the edge of the board.")
        return False

    return True

def valid_placement(board, player_turn, move_from, move_to):
    move_from_data = move_from[1:4].split(",")
    origin_row, origin_col = int(move_from_data[0]), int(move_from_data[1])

    move_to_data = move_to[1:4].split(",")
    targ_row, targ_col = int(move_to_data[0]), int(move_to_data[1])

    #Rule: You cannot place the block where you just picked it from
    if (origin_row == targ_row and origin_col == targ_col):
        print("Must place piece at a different spot")
        return False

    #Rule: You must push where there is space to
    move_to_data = move_to[1:4].split(",")
    targ_row, targ_col = int(move_to_data[0]), int(move_to_data[1])
    if (targ_row == origin_row or targ_col == origin_col):
        if ("("+str(targ_row)+","+str(targ_col)+")" in EDGES_OF_THE_BOARD):
            return True

    print("There is no space to push.")
    return False

#Functionality
def print_board(board):
    print("\nCurrent Board State:")

    print("   0, 1, 2, 3, 4,")
    print("   _  _  _  _  _ ")
    row_iterator = 0
    for row in board:
        print(str(row_iterator) + "| ", end="")
        row_iterator += 1
        for item in row:
            if (item == "X"):
                print("\u001b[31m" + item, end= "\u001b[0m, ")
            elif (item == "O"):
                print("\u001b[35m" + item, end= "\u001b[0m, ")
            else:
                print("\u001b[0m" + item, end= ", ")
        print()
    print("\u001b[0m")

def change_turn(player_turn):
    if (player_turn == "X"):
        return "O"
    else:
        return "X"

def check_line(array, item_to_check_for):
    if array.count(item_to_check_for) == 5:
        return True
    return False

def place_block(board, player_moving, move_from):
    move_to = request_input("Where would you like to place your piece? ", EDGES_OF_THE_BOARD)
    while (not valid_placement(board, player_moving, move_from, move_to)):
        move_to = request_input("Where would you like to place your piece? ", EDGES_OF_THE_BOARD)
    return move_to

def pickup_block(board, player_moving):
    move_from = request_input("Where do you want to pick up a piece from? ", EDGES_OF_THE_BOARD)
    while (not valid_pickup(board, player_moving, move_from)):
        move_from = request_input("Where do you want to pick up a piece from? ", EDGES_OF_THE_BOARD)
    return move_from

def apply_move(board, move_block_from, move_block_to, player_turn):
    if (move_block_to[1] != move_block_from[1]):
        #Were moving rows
        old_row = int(move_block_from[1])
        new_row = int(move_block_to[1])
        Col = int(move_block_from[3])

        blocks_to_shift = new_row - old_row
        if (blocks_to_shift > 0):
            for i in range(0, abs(blocks_to_shift)):            
               board[old_row + i][Col] = board[old_row + i + 1][Col]
        else:
            for i in range(0, abs(blocks_to_shift)):            
                board[old_row - i][Col] = board[old_row - i -+ 1][Col]
    else:
        #Were moving cols
        old_col = int(move_block_from[3])
        new_col = int(move_block_to[3])
        Row = int(move_block_from[1])

        blocks_to_shift = new_col - old_col
        if (blocks_to_shift > 0):
            for i in range(0, abs(blocks_to_shift)):            
                board[Row][old_col + i] = board[Row][old_col + i + 1]
        else:
            for i in range(0, abs(blocks_to_shift)):            
                board[Row][old_col - i] = board[Row][old_col - i -+ 1]

    board[int(move_block_to[1])][int(move_block_to[3])] = player_turn

def check_for_win(board, player_turn):
    winners = []
    for row in board:
        if check_line(row, "O"):
            winners.append("O")
        if check_line(row, "X"):
            winners.append("X")

    for col in zip(*board):
        if check_line(col, "O"):
            winners.append("O")
        if check_line(col, "X"):
            winners.append("X")

    for letter in {"O", "X"}:
        if all(board[i][i] == letter for i in range(5)):
            winners.append(letter)

    for letter in {"O", "X"}:
        if all(board[i][len(board) - 1 - i] == letter for i in range(5)):
            winners.append(letter)

    if (player_turn == "X"):
        if ("O" in winners and "X" in winners):
            winners.insert(0 , "O")
    elif (player_turn == "O"):
        if ("O" in winners and "X" in winners):
            winners.insert(0 , "X")

    return winners

def next_move_or_match_end(board, player_turn):
    wins_list = check_for_win(board, player_turn)

    if ("X" in wins_list or "O" in wins_list):
        print_board(board)
        print(wins_list[0]+" has won. \n")
        if (BUILD_AI_ONLY_PLAY):
            if (wins_list[0] == "X"):
                global x_wins
                x_wins += 1
            else:
                global o_wins
                o_wins += 1
        return None
    else:
        return change_turn(player_turn)

def check_for_undo(last_board_state, board):
    undo_response = request_input("Undo? (U or C) ", {"U", "C"})
    if (undo_response == "U"):
        board = last_board_state
        return "U"
    return "C"

def get_player_move(board, player_turn):
    move_block_from, move_block_to = None, None
    confirmed_move = False
    last_board_state, cloned_original_board = copy.deepcopy(board), copy.deepcopy(board)

    while (confirmed_move != "C"):
        print_board(cloned_original_board)

        move_block_from = pickup_block(cloned_original_board, player_turn)
        move_block_to = place_block(cloned_original_board, player_turn, move_block_from)
        apply_move(cloned_original_board, move_block_from, move_block_to, player_turn)
        print_board(cloned_original_board)

        confirmed_move = check_for_undo(last_board_state, cloned_original_board)
        cloned_original_board = last_board_state 

    return move_block_from, move_block_to

def start_match():
    board = init_board()
    player_turn = "X"
    
    #AI
    turn_counter = 0

    if (BUILD_AI_ONLY_PLAY):
        x_or_o = "X"
    else:
        x_or_o = request_input("\u001b[0mType your team: X or O ", {'X', 'O'})

    while (player_turn != None and turn_counter < AI_GAME_MAX_MOVES):
        move_block_from, move_block_to = None, None
        if (player_turn != x_or_o):
            move_block_from, move_block_to = request_ai_move(board, player_turn, AI_SCORE_SKEW_AMOUNT)
        else:
            if (BUILD_AI_ONLY_PLAY):
                move_block_from, move_block_to = request_ai_move(board, player_turn, AI_SCORE_SKEW_AMOUNT)
            else:
                move_block_from, move_block_to = get_player_move(board, player_turn)

        turn_counter += 1
        apply_move(board, move_block_from, move_block_to, player_turn)
        player_turn = next_move_or_match_end(board, player_turn)
        if (BUILD_AI_ONLY_PLAY):
            time.sleep(AI_WAIT_SPEED)

    global ties
    ties += 1

if (BUILD_AI_ONLY_PLAY):
    print(time.asctime())

    start = time.time()
    for i in range(10):
        start_match()
    end = time.time()

    print("\u001b[31m X Wins: " + str(x_wins), end= "\u001b[0m, \n")
    print("\u001b[35m O Wins: " + str(o_wins), end= "\u001b[0m, \n")
    print("\u001b[0m Ties: " + str(ties), end= " ")
    print("Time Taken: " + str(round(end - start)))
else:
    start_match()

