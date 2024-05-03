import random
import math
class OthelloGame:
    def __init__(self):
        self.board_size = 8
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'
        self.current_player = 'W'

    def display_board(self):
        print('  0 1 2 3 4 5 6 7\n')
        for i in range(self.board_size):
            print(f'{i} {" ".join(self.board[i])}')

    def is_valid_move(self, board, row, col, player):
        if 0 <= row < 8 and 0 <= col < 8 and board[row][col] == ' ':
            # Check if the move flips opponent's pieces
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8 and board[r][c] != player and board[r][c] != ' ':
                    while 0 <= r < 8 and 0 <= c < 8 and board[r][c] != player and board[r][c] != ' ':
                        r += dr
                        c += dc
                    if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
                        return True
        return False
    def get_valid_moves(self, board, player):
        valid_moves = []
        for row in range(8):
         for col in range(8):
            if self.is_valid_move(board, row, col, player):
                valid_moves.append((row, col))
        return valid_moves
    def make_move(self,board,row, col,player):
        if self.is_valid_move(board,row, col,player):
            self.board[row][col] = self.current_player
            opponent = 'W' if self.current_player == 'B' else 'B'
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if not (0 <= r < self.board_size and 0 <= c < self.board_size):
                    continue
                if self.board[r][c] == opponent:
                    to_flip = []
                    while 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == opponent:
                        to_flip.append((r, c))
                        r += dr
                        c += dc
                    if 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == self.current_player:
                        for flip_row, flip_col in to_flip:
                            self.board[flip_row][flip_col] = self.current_player
            self.current_player = 'W' if self.current_player == 'B' else 'B'
        else:
            print('Invalid move!')
            return False
    def ai_easy(self):
        valid_moves = self.get_valid_moves(self.board, 'W')  # Assuming AI plays as 'X'
        if valid_moves:
            move = valid_moves[0]  # Choose the first valid move
            return move
        else:
            return None

    
    def ai_medium(self):
        valid_moves = self.get_valid_moves(self.board, 'W')
        scores = []
        for move in valid_moves:
            score = self.evaluate_move(move)
            scores.append((move, score))
        best_move = max(scores, key=lambda x: x[1])[0]
        self.make_move(best_move[0], best_move[1])
    def ai_hard(self):
     depth = 4  # Adjust the depth of search based on difficulty level
     best_move, _ = self.minimax(self.board, depth, float('-inf'), float('inf'), True)
     self.make_move(best_move[0], best_move[1])

    def minimax(self, board, depth, alpha, beta, maximizing_player):
     if depth == 0 or self.is_game_over(board):
        return None, self.evaluate_board(board)  # Evaluate the board position
    
     valid_moves = self.get_valid_moves(board)
     if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in valid_moves:
            new_board = self.simulate_move(board, move)
            _, eval = self.minimax(new_board, depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return best_move, max_eval
     else:
        min_eval = float('inf')
        best_move = None
        for move in valid_moves:
            new_board = self.simulate_move(board, move)
            _, eval = self.minimax(new_board, depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return best_move, min_eval

    def count_pieces(self):
        count_B = sum(row.count('B') for row in self.board)
        count_W = sum(row.count('W') for row in self.board)
        return count_B, count_W
    def evaluate_move(self, move):
            # Simple evaluation function for medium difficulty
        row, col = move
        return len(self.get_flipped_pieces(row, col))
    def simulate_move(self, board, move, player):
     new_board = [row[:] for row in board]
     row, col = move
    # Apply the move on the new board
     new_board[row][col] = player

    # Update the board by flipping opponent's pieces
     for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
        r, c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8 and new_board[r][c] != player:
            new_board[r][c] = player
            r += dr
            c += dc

     return new_board
    
    def is_game_over(self, board):
        # Game is over if there are no valid moves for both players
     return len(self.get_valid_moves(board, 'W')) == 0 and len(self.get_valid_moves(board, 'B')) == 0
     



##### Game Play
game = OthelloGame()
game.display_board()
bl,wh=game.count_pieces()
print("\nblacks:"+str(bl)+"\nwhites:"+str(wh)+"\n")
while(game.is_game_over(game.board)==False):
   ### AI makes a move

  row,col=game.ai_easy() 
  game.make_move(game.board,row, col,"W")  
  game.display_board()
  bl,wh=game.count_pieces()
  print("\nblacks:"+str(bl)+"\nwhites:"+str(wh)+"\n")
  
  ###Human make move

  if(game.get_valid_moves(game.board,'B')!=[]):
   print(game.get_valid_moves(game.board,'B'))  
   row=int(input("enter row:"))
   col=int(input("enter col:"))
   while((game.make_move(game.board,row,col,"B"))==False):
     z=0
     row=int(input("enter row:"))
     col=int(input("enter col:"))
   game.display_board()
   bl,wh=game.count_pieces()
   print("\nblacks:"+str(bl)+"\nwhites:"+str(wh)+"\n")
   ####Game Over

#####check winner   
if(bl>wh):
    print("Black wins!!!")
elif(wh>bl):
    print("white wins!!!")
else:
    print("!!!draw!!!")
