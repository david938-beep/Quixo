from AI import request_ai_move, chars_to_board

#27 Chars Incoming
#The first 25 chars are the board
#The 26th is what player the move is for
#The 27th is the difficulty (0 Hardest - 5 Silly)

#CSharp_input = "X                        O0" #Test Data
CSharp_input = input()

#Breaking down the incoming data
board_data = CSharp_input[0:25:1]
generated_board = chars_to_board(board_data)
team_playing_for = CSharp_input[25:26:1]
difficulty = int(CSharp_input[26:])
print(request_ai_move(generated_board, team_playing_for, difficulty))