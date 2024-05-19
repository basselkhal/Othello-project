from Board import set_up_board
from AI import Bot
from GUI import PlayGround, Button, TextBox, changeSpeed, WINDOW_SIZE, BOARD_WIDTH, TILE_SPACING
from Tuples import V
import math
import pygame as pg
from pygame import gfxdraw

######################################################
#               Helper Functions
######################################################

def initialize_game():
    global speed_l, diff_l, single_bot, double_bot, p2_l, undo_on, show_moves_on, skip_on
    global bots,window_offset, screen
    
    speed_l = 0x0004
    diff_l = 0x0005
    single_bot = 0x0001
    double_bot = 0x0000
    p2_l = 0x0005
    undo_on = 0x0001
    show_moves_on = 0x0001
    skip_on = 0x0000
    
    # Get the game started
    bots = getBots()  # List of bots
    window_offset = V(((WINDOW_SIZE[0]-BOARD_WIDTH)/2, (WINDOW_SIZE[1]-BOARD_WIDTH)/2+50))
    screen = pg.display.set_mode(WINDOW_SIZE)  # This makes the display
    pg.init()

def set_game_colors():
    global othello_color, light_button_color, background_color, play_text_color, board_color, dark_button_color,start_button_color, setting_label_color, bubble_color
    othello_color = (0, 200, 200)  # A bright cyan color for the game title
    light_button_color = (0, 100, 100)  # A darker cyan color for the buttons in the settings page
    background_color = (30, 30, 30)  # A dark gray color for the background
    play_text_color = (255, 255, 255)  # A white color for the play text
    board_color = V((50, 150, 50))  # A green color for the board
    dark_button_color = V((0, 50, 50))  # A very dark cyan color for the buttons on the board
    start_button_color = V((75, 82, 50)) 
    setting_label_color = (200, 200, 200)  # A light gray color for the setting labels
    bubble_color = (100, 100, 100)  # A medium gray color for the sliders
def setup_board_images():
    global board_images, board_image_rects, board_image_shrunks, board_image_shrunk_rects, background, line_length, diff_h, p2_h, speed_h, players
    
    board_images = [pg.Surface((BOARD_WIDTH, BOARD_WIDTH)) for i in range(5)]
    for i, im in enumerate(board_images):
        n = 2*i + 4
        im.fill(board_color)
        for l in range(n + 1):
            pg.draw.line(im, (0, 0, 0), (l * (BOARD_WIDTH - 2) / n, 0), (l * (BOARD_WIDTH - 2) / n, BOARD_WIDTH), width=2)
            pg.draw.line(im, (0, 0, 0), (0, l * (BOARD_WIDTH - 2) / n), (BOARD_WIDTH, l * (BOARD_WIDTH - 2) / n), width=2)
    board_image_rects = [image.get_rect() for image in board_images]
    for tangle in board_image_rects:
        tangle.center = window_offset + V((BOARD_WIDTH, BOARD_WIDTH)) / 2

    board_image_shrunks = [pg.Surface((BOARD_WIDTH / 2, BOARD_WIDTH / 2)) for i in range(5)]
    for i, im in enumerate(board_image_shrunks):
        n = 2*i + 4
        im.fill(board_color)
        for l in range(n + 1):
            pg.draw.line(im, (0, 0, 0), (l * (BOARD_WIDTH - 1) / n / 2, 0), (l * (BOARD_WIDTH - 1) / n / 2, BOARD_WIDTH), width=1)
            pg.draw.line(im, (0, 0, 0), (0, l * (BOARD_WIDTH - 1) / n / 2), (BOARD_WIDTH / 2, l * (BOARD_WIDTH - 1) / n / 2), width=1)

    board_image_shrunk_rects = [shrunk.get_rect() for shrunk in board_image_shrunks]
    for tangle in board_image_shrunk_rects:
        tangle.midtop = (WINDOW_SIZE[0] / 2, 100)

    background = pg.Surface(WINDOW_SIZE)
    background.fill((148, 172, 136))
    background.fill(background_color)
    changeSpeed(1.4 ** (speed_l - 5))   # Changes animation speed based on speed level
    line_length = 300
    diff_h = 30
    p2_h = 130
    speed_h = -120

    if double_bot:
        players = [bots[p2_l], bots[diff_l]]
    elif single_bot:
        players = ['human', bots[diff_l]]
    else:
        players = ['human', 'human']

def gameOver():
    global game_over
    game_over = True  # Indicates the game is over
    update_turn_text()

def getBots():
    # This creates a list of bots to choose from later. Parameters defined in Bot_Class
    BabyBot = Bot(1, 1, depth=0, name="BabyBot")
    SillyBot = Bot(4, 16, depth=0, name="SillyBot")
    ThinkerBot = Bot(100, 10000, depth=0, name="ThinkerBot")
    CleverBot = Bot(100, 10000, depth=0.5, name="CleverBot")
    Megamind = Bot(100, 10000, depth=1, name="Megamind")
    Sherlock = Bot(100, 10000, depth=1.5, name="Sherlock")
    Data = Bot(100, 10000, depth=2, name="Data")
    VIKI = Bot(100, 10000, depth=2.5, name="VIKI")
    Ultron = Bot(100, 10000, depth=3, name="Ultron")
    HAL = Bot(100, 10000, depth=4, name="HAL")
    Skynet = Bot(100, 10000, depth=5, name="Skynet")
    Rando = Bot(100, 10000, depth=0, name="Rando", RANDOM=True)
    # List of bots:
    bots = [Rando, BabyBot, SillyBot, ThinkerBot, CleverBot, Megamind, Sherlock, Data, VIKI, Ultron, HAL, Skynet]

    return bots

def updateTileList(board):
    global tiles_to_remove
    # We search through the entire tile_list
    for r, row in enumerate(tile_list):
        for e, element in enumerate(tile_list):
            bval = board[r][e] * (turn * 2 - 1)
            tval = tile_list[r][e]
            if bval == 0:  # If there's no game piece here, destroy the pieces
                if tval is not None:  # If there is a piece
                    tiles_to_remove.append(tval)  # List for animations
                    tile_list[r][e] = None  # Take it off the list for gameplay
                    tval.remove()  # Tile function
            else:  # This means there should be a tile
                if tval is not None:  # If there's a tile here, check if it agrees:
                    if tval.color_index != (bval + 1) / 2:
                        tval.flip()  # If it doesn't agree with the board, flip it
                if tval is None:
                    tile_list[r][e] = PlayGround(e, r, int((bval + 1) / 2), sw)  # Place a new tile; there should be one but there isn't

def set_board_size(input):
    global board_image, board_image_rect, game_over
    global board_image_shrunk_rect, board_image_shrunk
    global boardSize, B, tile_list, sw, memory, turn
    global tiles_to_remove, black_prog, white_prog
    game_over = False  # Reset the game over flag
    tiles_to_remove = []  # For removal animations
    black_prog = 0  # Set or reset the progress bar for black
    white_prog = 0  # Set or reset the progress bar for white
    i = 2  # This is the index of the board size. For 4x4, it's 0, for 6x6, it's 1, etc.
    turn = 0  # Set or reset the turn
    board_image = board_images[i]  # Get the board image surface
    board_image_rect = board_image_rects[i]
    board_image_shrunk = board_image_shrunks[i]  # Get the shrunk board image for the title screen
    board_image_shrunk_rect = board_image_shrunk_rects[i]
    boardSize = 8  # Set or update the board size
    sw = BOARD_WIDTH / boardSize  # Set or update the square width
    B = set_up_board(boardSize)  # Set up the board
    tile_list = [[None for _ in row] for row in B]  # Create a new tile list in the proper size
    memory = [B]  # Set or reset the memory
    updateTileList(B)  # Place the first tiles on the board
    update_turn_text()

def updateScores():
    blackAdv = (1 - turn * 2) * sum([sum(i) for i in B])  # B - W
    tileCount = B.count_tiles()  # B + W
    scores[0] = int((blackAdv + tileCount) / 2)  # B
    scores[1] = int((tileCount - blackAdv) / 2)  # W

    # Update the score display surfaces
    white_score_box.changeText(str(scores[1]))
    black_score_box.changeText(str(scores[0]))

    # Update the progress bar
    global animating_prog_bar
    animating_prog_bar = True


def roboTurn(bot):
    # We go back to the spot in our memory, either as far back as we can,
    # or to the patience limit of the bot.
    memory_spot = (-1) * min(bot.patience, len(memory))
    # If the board hasn't changed in that long, we should disqualify skipping as an option
    # Allow skips only if the memory_spot is not the same as the board and skips are allowed.
    allow_skips = memory[memory_spot] != B and memory[memory_spot].inverted() != B and skip_on
    # The bot will choose a move and only skip if they HAVE to or they're allowed to.
    best_move = bot.Move_Selection(B, allow_skips)  # This returns a tuple of board position
    if best_move[0] == -5:  # -5 is a kind of code word meaning to skip
        print("Bot passes")
    else:
        # the best move is a tuple, so we use * to unpack the coords and move to there
        moveTo(*best_move)
    next_turn()

def flipTiles(flips):
    # Given flips, a generator of tuples, we flip those coords
    global scores
    for x, y in flips:
        tile_list[y][x].flip()  # This turns over the tile

def moveTo(xspot,yspot): # This adds a tile to a location given that it is legal
    global turn, B
    #Put the turtle down in the right spot in the right color
    tile_list[yspot][xspot]=(PlayGround(xspot, yspot, turn,sw))
    B, flips = B.place_tile(xspot, yspot)  #Place tile and get the new board and flips
    flipTiles(flips) #Flip the tiles
    updateScores()
    
def next_turn():
    global turn, no_moves, B
    # The board is always from the player's perspective.
    # Different player? Flip the perspective.
    updateScores()
    if turn == 1:
        turn = 0
        memory.append(B.inverted())
    else:
        turn = 1
        memory.append(B)
    # Next, we add the board to memory. The memory is strictly from Black's perspective.
    # As a result, if it's White's turn (turn == 1), we remember the inverted board
    B = B.inverted()
    # Check if the game is over by tile count. If nobody can move, the game ends.
    if B.empty_spaces() == 0 or ((not B.are_legal_moves()) and (not (B.inverted()).are_legal_moves())):
        gameOver()
    else:
        # This allows players to skip even if skip is disabled.
        no_moves = not B.are_legal_moves()
        update_turn_text()

def undo():
    global turn, B, game_over, no_moves

    print(game_over)
    if game_over:  # At the end of the game, undo means start over.
        while len(memory) > 1:
            memory.pop()  # This backs up the memory to the beginning
        global black_prog, white_prog
        black_prog = 0
        white_prog = 0  # Reset the progress bar.
        turn = 0  # Reset turn
        B = set_up_board(boardSize)  # Reset board
        game_over = False  # Reset game_over
    else:
        def backup():
            global turn, B
            memory.pop()  # Back up 1
            B = memory[-1]  # Revert to last memory
            turn = (turn + 1) % 2  # Switch turn
            if turn == 1:  # Memories are stored from Black's perspective, so we must invert for White
                # B.invert()
                B = B.inverted()

        backup()  # Backup once, and then again if there's a bot on the other side
        if players[turn] != "human":
            backup()
    updateScores()
    updateTileList(B)  # Flip and remove necessary tiles
    update_turn_text()
    no_moves = not B.are_legal_moves()  # Allows players to skip even if skip is disabled.

def update_turn_text():
    if game_over:
        if scores[1] > scores[0]:
            turn_box.changeText("White Wins!", (210, 210, 210))
        elif scores[1] < scores[0]:
            turn_box.changeText("Black Wins!", (0, 0, 0))
        else:
            turn_box.changeText("Tie Game!", board_color)
    else:
        if turn == 1:
            turn_box.changeText("White Turn", (210, 210, 210))
        else:
            turn_box.changeText("Black Turn", (0, 0, 0))


def animate_prog_bar():
    global black_prog, white_prog, animating_prog_bar

    m = 9  # Resolution of progress bar
    d = 1 + 2 * double_bot  # Step size. Two bots play so fast, we have to speed it up.

    # Move the progress bar up or down appropriately
    if scores[0] * m > black_prog:
        black_prog += d
    elif scores[0] * m < black_prog:
        black_prog -= d

    if scores[1] * m > white_prog:
        white_prog += d
    elif scores[1] * m < white_prog:
        white_prog -= d

    # If the progress bars are exactly at the right position, stop the animation
    if scores[0] * m == black_prog and scores[1] * m == white_prog:
        animating_prog_bar = False

    # Draw the progress bar
    prog_bar.fill(dark_button_color)  # Background
    black_perc = black_prog / len(B) / len(B) / m  # Black Percentage
    black_bar_height = black_perc * prog_bar_size[1]
    black_bar_rect = pg.Rect(0, 0, prog_bar_size[0], black_bar_height)
    pg.draw.rect(prog_bar, (20, 20, 20), black_bar_rect, border_radius=2)  # Black bar

    white_perc = white_prog / len(B) / len(B) / m  # White Percentage
    white_bar_height = white_perc * prog_bar_size[1]
    white_bar_rect = pg.Rect(0, (1 - white_perc) * prog_bar_size[1], prog_bar_size[0], white_bar_height)
    pg.draw.rect(prog_bar, (200, 200, 200), white_bar_rect, border_radius=2)  # White bar

    # Draw a line at the midpoint
    y_cord = prog_bar_size[1] // 2
    if black_perc > 0.5:
        pg.draw.line(prog_bar, (220, 220, 220), (0, y_cord), (prog_bar_size[0], y_cord), 1)
    else:
        pg.draw.line(prog_bar, (0, 0, 0), (0, y_cord), (prog_bar_size[0], y_cord), 1)

