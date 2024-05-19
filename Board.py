class Board(list):
    """A class that represents a board for a game."""

    def count_tiles(self):
        """Return the number of tiles on the board."""
        # Total spaces minus empty spaces
        return len(self) * len(self) - self.empty_spaces()

    def show(self):
        """Display the board in text using matrix form."""
        for row_index, row in enumerate(self):
            out = "["
            first = True
            for element_index, element in enumerate(row):
                if not first:
                    # Add spaces to align the elements
                    out += " " * (4 - len(str(element)))
                else:
                    first = False
                out += str(element)
            out += "]"
            print(out)
        print()

    def inverted(self):
        """Return the opposite of the board."""
        # Accessor
        return Board([[-1 * element for element in row] for row in self])

    def invert(self):
        """Invert the board in place."""
        # Mutator
        for row_index, row in enumerate(self):
            for element_index, element in enumerate(row):
                assert self[row_index][element_index] == element
                self.show()
                print()
                if self[row_index][element_index] == 1:
                    self[row_index][element_index] = -1
                elif self[row_index][element_index] == -1:
                    self[row_index][element_index] = 1
                self.show()

    def place_tile(self, x_coord, y_coord):
        """Place a tile on the board at the given coordinates.
        
        This assumes the move is legal and makes the move.
        """
        board = self.copy()
        flips = []
        # We have to find all possible sandwiches and report back the flips
        # All vertical, horizontal, and diagonal directions are combinations of these two lists.
        for v_dir in [-1, 0, 1]:
            for h_dir in [-1, 0, 1]:
                # If there's a sandwich in this direction...
                if board.check_for_sandwich(x_coord, y_coord, h_dir, v_dir):
                    x_look, y_look = x_coord + h_dir, y_coord + v_dir
                    while board[y_look][x_look] == -1:
                        # While we move through the meet of the sandwich,
                        # we continue flipping tiles.
                        # We flip tiles as long as we're looking at enemy pieces.
                        board[y_look][x_look] = 1       # Change to my piece
                        flips.append((x_look, y_look))  # Gotta flip this one
                        x_look += h_dir
                        y_look += v_dir
        board[y_coord][x_coord] = 1
        return board, flips  # This gives the new board, but also the list of flips that we made.

    def copy(self):
        """Return a copy of the board."""
        return Board([[element for element in row] for row in self])

    def check_click(self, x_coord, y_coord):
        """Check if a click is allowed on the board."""
        # If we're inside the bounds of the grid
        if 0 <= y_coord < len(self):
            if 0 <= x_coord < len(self):
                # If the move is legal, we return true
                return self.is_legal(x_coord, y_coord)
        return False

    def is_legal(self, x_coord, y_coord):
        """Check if a move is legal on the board."""
        # A move is only legal if we can find a sandwich. Thus, we search.
        if self[y_coord][x_coord] == 0:  # It can't already have a piece there...
            for v_dir in [-1, 0, 1]:
                for h_dir in [-1, 0, 1]:
                    # For all directions,
                    # if there's at least ONE sandwich,
                    # the move is legal
                    if self.check_for_sandwich(x_coord, y_coord, h_dir, v_dir):
                        return True
        # If we found no sandwiches, the move is illegal.
        return False

    def check_for_sandwich(self, x_coord, y_coord, h_dir, v_dir):
        """Check if there is a sandwich in a given direction."""
        x_look, y_look = x_coord + h_dir, y_coord + v_dir
        trivial = True  # First,
        # we assume that the sandwich has no contents,
        # i.e. its trivial
        if (y_look == len(self) or y_look == -1 or
                x_look == len(self) or x_look == -1):
            # If We're going to run off the edge of the grid,
            # stop looking.
            return False
        while self[y_look][x_look] == -1:  # While we are looking at enemy pieces:
            # While we're in the sandwich,
            # we found some contents,
            # so the sandwich is not trivial
            trivial = False
            x_look += h_dir
            y_look += v_dir
            if (y_look == len(self) or y_look == -1 or
                    x_look == len(self) or x_look == -1):
                # Make sure we didnt hit the end of the grid...
                return False
        # Once the sandwich is finished,
        # we found a Sandwich ONLY IF:
        # It's not empty,
        # a.k.a trivial
        # The other end of the sandwich is also a friendly piece.
        return self[y_look][x_look] == 1 and not trivial

    def legal_moves(self):
        """Find ALL legal moves on the board."""
        # The bots will need to consider every possibility,
        # so they'll ask for this generator
        for i in range(len(self)):
            for j in range(len(self)):
                if self.is_legal(i, j):
                    # If each spot is legal, we yield it.
                    yield (i, j)

    def empty_spaces(self):
        """Count the empty spaces on the board."""
        count = 0
        # This is a pretty clear function.
        for i in self:
            for j in i:
                if j == 0:
                    count += 1
        return count

    def are_legal_moves(self):
        """Check if there are any legal moves on the board."""
        for i in range(len(self)):
            for j in range(len(self)):
                if self.is_legal(i, j):
                    # If any spot is legal, we say true
                    return True
        return False


def set_up_board(size):
    """Create a board with the given size."""
    # Construct the board
    board = Board([[0 for j in range(size)] for i in range(size)])
    # Get the middle of the board
    mid = int(len(board) / 2 - 1)
    # Set the four tiles down
    board[mid][mid] = 1
    board[mid][mid + 1] = -1
    board[mid + 1][mid + 1] = 1
    board[mid + 1][mid] = -1
    return board
