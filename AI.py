# Import Board class and random module
from Board import Board
import random


# Define a Bot class
class Bot():
    # Initialize the bot with some attributes
    def __init__(self, edgeX=1, cornX=1, depth=0, name="NamelessBot", patience=4, RANDOM=False):
        # Assign attributes to the bot
        self.name = name  # Name is just for fun
        self.edgeX = edgeX  # Edge fitness multiplier
        self.cornX = cornX  # Corner fitness multiplier
        self.depth = depth  # How many iterations to think forward
        self.patience = patience  # How many times can we undo until we do something else
        self.RANDOM = RANDOM  # Whether to make random moves or not

    # Define a method to calculate the heuristic of a board state for the bot
    def Evaluation(self, board):
        # Define heuristic weights for different factors
        mobility_weight = 1  # Weight for the number of legal moves
        coin_parity_weight = 1  # Weight for the difference in number of tiles
        corners_captured_weight = 5  # Weight for the difference in number of corners captured
        stability_weight = 10  # Weight for the difference in stability of tiles

        # Get the board size
        board_len = len(board)

        # Initialize some variables to count tiles, corners, and mobility for each player
        my_tiles = 0
        opponent_tiles = 0
        my_corners = 0
        opponent_corners = 0
        my_mobility = 0
        opponent_mobility = 0

        # Loop through the board and update the variables accordingly
        for yCord in range(board_len):
            for xCord in range(board_len):
                valHere = board[yCord][xCord]

                if valHere == 1:  # If the tile belongs to the bot
                    my_tiles += 1  # Increment the bot's tile count
                    if (xCord == 0 or xCord == board_len - 1) and (
                            yCord == 0 or yCord == board_len - 1):  # If the tile is a corner
                        my_corners += 1  # Increment the bot's corner count

                elif valHere == -1:  # If the tile belongs to the opponent
                    opponent_tiles += 1  # Increment the opponent's tile count
                    if (xCord == 0 or xCord == board_len - 1) and (
                            yCord == 0 or yCord == board_len - 1):  # If the tile is a corner
                        opponent_corners += 1  # Increment the opponent's corner count

        # Calculate mobility by counting legal moves for each player using the board methods
        my_mobility = len(list(board.legal_moves()))
        opponent_mobility = len(list(board.inverted().legal_moves()))

        # Calculate coin parity by computing the percentage difference in tile counts
        coin_parity = 100 * (my_tiles - opponent_tiles) / (my_tiles + opponent_tiles)

        # Handle division by zero error for stability calculation by setting it to zero if no corners are captured by either player
        if my_corners + opponent_corners == 0:
            stability = 0

        else:  # Otherwise, calculate stability by computing the percentage difference in corner counts
            stability = 100 * (my_corners - opponent_corners) / (my_corners + opponent_corners)

        # Calculate the overall utility by adding up the weighted sum of heuristics
        utility = (
                mobility_weight * (my_mobility - opponent_mobility)
                + coin_parity_weight * coin_parity
                + corners_captured_weight * stability
                + stability_weight * stability
        )
        return utility

    # Define MinMAx method
    def MinMAx(self, board, depth):
        """Find the best move for the bot using minmax algorithm."""
        # Base case: return the Value of the board
        # when depth is zero
        if depth == 0:
            # At 0 depth, we just look at the surface level quality of the board
            return self.Evaluation(board)

        else:
            # for the bot and call minmax on inverted board
            new_board = board.inverted()

            # The opponent has a set of possible moves on this board.
            Moves = new_board.legal_moves()

            # If we're predicting the opponent's move, this means we're
            # thinking with a depth 1 less than them.
            new_depth = depth - 1

            # Initialize best value to negative infinity
            best_value = float("-inf")

            # Loop through the opponent moves and update the best Value accordingly
            for move in Moves:
                # Recursive case: loop through all possible moves
                moveUt = self.MinMAx(new_board.place_tile(*move)[0], new_depth)
                # Update the best Value if it is higher than the current one
                if moveUt > best_value:
                    # Update best value and best move if better move is found
                    best_value = moveUt

            # Check if passing is better than any move for the opponent
            # Call minmax on inverted board
            passUt = self.MinMAx(new_board, new_depth)
            if passUt > best_value:
                # Update best value and best move if better move is found
                best_value = passUt

            # Negate the value since it's from opponent's perspective
            # Return best value.
            return -1 * best_value
        pass

    # Define a method to choose a move for the bot
    def Move_Selection(self, board, passAllowed=True):
        # If RANDOM is True, choose a random move from the legal moves or pass if none are available
        if self.RANDOM:
            moves = list(board.legal_moves())
            if moves:
                return random.choice(moves)

            else:
                return (-5, -5)

        # Choose a random depth from int(self.depth) or int(self.depth + 0.5)
        depth = random.choice((int(self.depth), int(self.depth + 0.5)))

        # -5 is our keyword default, meaning that no move beats the utility of just passing.
        bestMove = (-5, -5)

        # If passing is allowed (based on patience), we say that the utility of default (passing)
        # is the utility of the current board.
        if not (board.inverted()).are_legal_moves():
            # If inverting the board gives the opponent no legal moves, there's no point in passing.
            passAllowed = False

        if passAllowed:
            bestMoveUtility = self.MinMAx(board, depth)

        else:
            # If passing is not allowed, this utility should be the WORST possible case (all enemies).
            bestMoveUtility = self.Evaluation(Board([[-1 for i in row] for row in board]))

        # Now we look through all legal moves and compare them to our best case (or default case)
        for move in board.legal_moves():
            # The move quality is the utility of the board after going there.
            moveUtility = self.MinMAx(board.place_tile(*move)[0], depth)
            if moveUtility > bestMoveUtility:  # If we have a new best, dethrone the best.
                bestMoveUtility = moveUtility
                bestMove = move
        return bestMove
