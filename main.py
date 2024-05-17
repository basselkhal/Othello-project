from Board import set_up_board
from AI import Bot
from GUI import PlayGround, Button, TextBox, changeSpeed, WINDOW_SIZE, BOARD_WIDTH, TILE_SPACING
from Tuples import V
import math
import pygame as pg
from pygame import gfxdraw
# from algorithm import *

######################################################
#               Helper Functions
######################################################

def initialize_game():
    global speed_l, diff_l, single_bot, double_bot, p2_l, undo_on, show_moves_on, skip_on
    global bots, window_offset, screen
    
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
    global othello_color, light_button_color, background_color, play_text_color, board_color, dark_button_color,start_button_color,setting_label_color, bubble_color
    othello_color = (255, 255, 255)  # A white color for the game title
    light_button_color = (43, 161, 95)  # A darker  color for the buttons in the settings page
    background_color = (81, 91, 120)  # A dark gray color for the background
    play_text_color = (255, 255, 255)  # A white color for the play text
    board_color = V((50, 150, 50))  # A green color for the board
    dark_button_color = V((43, 161, 95))  # A very dark green color for the buttons on the board
    start_button_color = V((43, 161, 95))  # A very dark green color for the buttons on the board
    setting_label_color = (200, 200, 200)  # A light gray color for the modes labels
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

def set_buttons_text():
    global othello_font, game_over_font, turn_font, skip_font, board_size_font, scale_font, show_moves_font, settings_label_font, settings_button_font, play_font
    global prog_bar_size, prog_bar, prog_bar_rect, animating_prog_bar, black_prog, white_prog
    global skip_button, undo_button, quit_button, play_button, settings_button
    global bot_buttons_h, double_bot_button, no_bot_button, single_bot_button
    global undo_setting_button, skip_setting_button, show_moves_button
    global slider_size, slider_shift, diff_slider, p2_slider, speed_slider
    global othello_box, turn_box, white_score_box, black_score_box, scores_box, game_over_button
    global diff_label_box, p1_label_box, p2_label_box

    # Make pygame fonts
    othello_font = pg.font.SysFont('Helvetica', 60, bold=False)
    game_over_font = pg.font.SysFont('Helvetica', 60, bold=True)
    turn_font = pg.font.SysFont('calibri', 30, bold=False)
    skip_font = pg.font.SysFont('calibri', 35, bold=False)
    board_size_font = pg.font.SysFont('calibri', 30, bold=True)
    scale_font = pg.font.SysFont('calibri', 20)
    show_moves_font = pg.font.SysFont('calibri', 18)
    settings_label_font = pg.font.SysFont('calibri', 30)
    settings_button_font = pg.font.SysFont('calibri', 33, bold=False)
    play_font = pg.font.SysFont('calibri', 40, bold=False)

    # Progress bar: surface with rectangle
    prog_bar_size = V((30, 250))
    prog_bar = pg.Surface(prog_bar_size)
    prog_bar_rect = prog_bar.get_rect()
    prog_bar_rect.center = ((BOARD_WIDTH + 3 * WINDOW_SIZE[0]) / 4, 500)
    animating_prog_bar = False
    black_prog, white_prog = (0, 0)

    # Making buttons!
    skip_button = Button((window_offset[0] - 50, 50), dark_button_color, "Skip", (20, 20, 20), skip_font)
    skip_button.midleft((10, WINDOW_SIZE[1] / 2))
    undo_button = Button((window_offset[0] - 50, 50), dark_button_color, "Undo", (20, 20, 20), skip_font)
    undo_button.midleft((10, WINDOW_SIZE[1] / 2 - 70))
    quit_button = Button((window_offset[0] - 50, 50), dark_button_color, 'Quit', (20, 20, 20), skip_font)
    quit_button.midleft((10, WINDOW_SIZE[1] / 2 + 70))

    play_button = Button((250, 70), start_button_color , "Start game", play_text_color, play_font)
    play_button.center((WINDOW_SIZE / 2 + V((-200, 200))))
    settings_button = Button((210, 60), start_button_color, "Modes", (255, 255, 255), settings_button_font)
    settings_button.center((WINDOW_SIZE / 2 + V((200, 200))))

    # These buttons are for the different play options
    bot_buttons_h = -55
    double_bot_button = Button((150, 40), light_button_color, "AI vs AI ", (10, 10, 10), scale_font, thickness=1)
    double_bot_button.center(WINDOW_SIZE / 2 + V((-line_length / 1, bot_buttons_h)))
    no_bot_button = Button((150, 40), light_button_color, "Human vs Human ", (10, 10, 10), scale_font, thickness=1)
    no_bot_button.center(WINDOW_SIZE / 2 + V((line_length / 1, bot_buttons_h)))
    single_bot_button = Button((150, 40), light_button_color, "Human vs AI", (10, 10, 10), scale_font, thickness=1)
    single_bot_button.center(WINDOW_SIZE / 2 + V((0, bot_buttons_h)))
    # Changing color to reflect which play option is selected.
    if single_bot:
        single_bot_button.changeColor(dark_button_color)
    elif double_bot:
        double_bot_button.changeColor(dark_button_color)
    else:
        no_bot_button.changeColor(dark_button_color)

    # Undo, Skip, and Show moves enabled buttons!
    undo_setting_button = Button((90, 40), light_button_color, "Undo: OFF", (10, 10, 10), scale_font, thickness=1)
    undo_setting_button.center(WINDOW_SIZE / 2 + V((-100, -200)))
    if undo_on:
        undo_setting_button.changeColor(dark_button_color)
        undo_setting_button.changeText("Undo: ON")
    skip_setting_button = Button((90, 40), light_button_color, "Skip: OFF", (10, 10, 10), scale_font, thickness=1)
    skip_setting_button.center(WINDOW_SIZE / 2 + V((0, -200)))
    if skip_on:
        skip_setting_button.changeColor(dark_button_color)
        skip_setting_button.changeText("Skip: ON")
    show_moves_button = Button((130, 40), light_button_color, "Show Moves: OFF", (10, 10, 10), show_moves_font, thickness=1)
    show_moves_button.center(WINDOW_SIZE / 2 + V((120, -200)))
    if show_moves_on:
        show_moves_button.changeColor(dark_button_color)
        show_moves_button.changeText("Show Moves: ON")

    # The sliders are just buttons with text shifted down
    slider_size = (12, 30)
    slider_shift = V((0, 27))  # This shifts the text down underneath the slider 25 pixels
    diff_slider = Button(slider_size, bubble_color, str(diff_l), othello_color, scale_font, thickness=1)
    diff_slider.center((WINDOW_SIZE / 2 + ((diff_l - 5) * line_length / 10, diff_h)))
    diff_slider.shiftText(slider_shift)
    p2_slider = Button(slider_size, bubble_color, str(p2_l), othello_color, scale_font, thickness=1)
    p2_slider.center((WINDOW_SIZE / 2 + ((p2_l - 5) * line_length / 10, p2_h)))
    p2_slider.shiftText(slider_shift)
    speed_slider = Button(slider_size, bubble_color, str(round(1.4 ** (speed_l - 5), 1)), othello_color, scale_font, thickness=1)
    speed_slider.center((WINDOW_SIZE / 2 + ((speed_l - 5) * line_length / 10, speed_h)))
    speed_slider.shiftText(slider_shift)
    if speed_l > 10: speed_slider.changeText("MAX")  # In case the maximum speed is chosen

    # These are just plain text which we'll put on the screen
    # In game text:
    othello_box = TextBox("Let's Play", othello_color, othello_font)
    othello_box.center((WINDOW_SIZE[0] / 2, 40))
    turn_box = TextBox("Black Turn", (0, 0, 0), turn_font)
    turn_box.center((WINDOW_SIZE[0] / 2, 95))
    white_score_box = TextBox("2", (255, 255, 255), turn_font)
    white_score_box.center(((BOARD_WIDTH + 3 * WINDOW_SIZE[0]) / 4, 350))
    black_score_box = TextBox("2", (28, 237, 63), turn_font)
    black_score_box.center(((BOARD_WIDTH + 3 * WINDOW_SIZE[0]) / 4, 300))
    scores_box = TextBox("Scores:", othello_color, turn_font)
    scores_box.center(((BOARD_WIDTH + 3 * WINDOW_SIZE[0]) / 4, 250))
    game_over_button = Button((300, 80), background_color + V((10, 10, 10)), "Game Over", (255, 255, 255), game_over_font, thickness=3)
    game_over_button.center(WINDOW_SIZE / 2)
    # Text in Settings
    diff_label_box = TextBox("Difficulty", setting_label_color, settings_label_font)
    diff_label_box.center((WINDOW_SIZE / 2 + V((0, diff_h - 35))))
    p1_label_box = TextBox("White Bot", setting_label_color, settings_label_font)
    p1_label_box.center((WINDOW_SIZE / 2 + V((0, diff_h - 35))))
    p2_label_box = TextBox("Black Bot", setting_label_color, settings_label_font)
    p2_label_box.center((WINDOW_SIZE / 2 + V((0, p2_h - 35))))

def rest_game():
    global clock,no_moves,game_active,settings_open,left_clicking,game_over,blocked,counter
    # Initialize Stuff
    set_board_size(8)       # Set board up
    clock = pg.time.Clock()  # pygame thing
    no_moves = False        # Assume there are moves
    game_active = False     # Start in the title screen
    settings_open = False
    left_clicking = None    # Not clicking on anything
    game_over = False
    blocked = True
    counter = 0            # Reset

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
        pass
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


# Game Colors
set_game_colors()
# Animation speed, difficulty (white player) level, True or False playing 0-player
# black player level, undo enabled, skip enabled, show legal moves enabled?
initialize_game()
########################################################################################################################
#                                       IMAGES AND SHAPES
########################################################################################################################
setup_board_images()
########################################################################################################################
#                                       BUTTONS AND TEXT
########################################################################################################################
set_buttons_text()
########################################################################################################################
rest_game()
########################################################################################################################
#                                           MAIN LOOP
########################################################################################################################

while True:
    
    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()
            from sys import exit
            exit()
        #####################################################################################
        if game_active:                 # GAME ACTIVE
            if event.type == pg.MOUSEBUTTONDOWN:
                if quit_button.collidepoint(event.pos) and event.button==1:
                    left_clicking = "quit" #quit button selected (always allowed, even when animations active)
                if not blocked:
                    if event.button == 1:
                        x,y = V(event.pos)-window_offset
                        # These are the GRID coords of the clicked pixel.
                        xspot = math.floor(x / sw)
                        yspot = math.floor(y / sw)
                        # This method checks if the clicked grid spot is a valid choice
                        if B.check_click(xspot, yspot):
                            moveTo(xspot, yspot)  # If it's valid, we move to that spot
                            next_turn()
                            blocked=True
                        elif (skip_on or no_moves) and skip_button.collidepoint(event.pos):
                            left_clicking = "skip"      # If allowed, skip selected
                        elif undo_on and undo_button.collidepoint(event.pos):
                            left_clicking = "undo"      # If allowed, undo selected
                        elif game_over and game_over_button.collidepoint(event.pos):
                            left_clicking = "game over"
                    elif event.button == 3:
                        if len(memory) > 1 and undo_on: #If allowed, undo on rightclick
                            undo()
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            elif event.type == pg.MOUSEBUTTONUP: #On upclick
                if event.button==1:
                    if left_clicking == 'skip' and skip_button.collidepoint(event.pos):
                        next_turn() # If skip is selected, skip turn
                    elif left_clicking == "undo" and undo_button.collidepoint(event.pos):
                        if len(memory) > 1: #If undo is selected and we haven't gone too far back, undo.
                            undo()
                            blocked=True
                    elif left_clicking == "game over" and game_over_button.collidepoint(event.pos):
                        undo()
                        blocked=True
                    elif left_clicking == "quit" and quit_button.collidepoint(event.pos):
                        game_active = False # If quit is selected, go to title screen
                    left_clicking = None

        #####################################################################################
        elif settings_open:             # SETTINGS PAGE
            if event.type==pg.MOUSEBUTTONDOWN:
                if event.button==1: #Leftclick down
                    loc=event.pos
                    #Below are all the settings which could be selected.
                    if settings_button.collidepoint(loc):
                        left_clicking = 'close_settings'    # Select the "Close Settings" button
                    elif double_bot_button.collidepoint(loc):
                        left_clicking = "double bot"        # Select the "0 Player" button
                    elif single_bot_button.collidepoint(loc):
                        left_clicking='single bot'          # Select the "1 Player" button
                    elif no_bot_button.collidepoint(loc):
                        left_clicking = "no bot"            # "2 Player" button
                    elif undo_setting_button.collidepoint(loc):
                        left_clicking = "undo setting"      # "Undo: ON/OFF" button
                    elif skip_setting_button.collidepoint(loc):
                        left_clicking = "skip setting"      # "Skip: ON/OFF" button
                    elif show_moves_button.collidepoint(loc):
                        left_clicking = "show moves setting"
                    elif speed_slider.collidepoint(loc):
                        left_clicking = 'speed'             # Select the speed slider
                    elif (single_bot or double_bot) and diff_slider.collidepoint(loc):
                        left_clicking = 'difficulty'        # Difficulty slider
                    elif double_bot and p2_slider.collidepoint(loc):
                        left_clicking='p2'                  # Black bot slider
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            elif event.type==pg.MOUSEBUTTONUP:
                if event.button==1: #Leftclick up
                    if left_clicking=='close_settings' and settings_button.collidepoint(event.pos):
                        settings_open=False                 # Back to titles screen
                        settings_button.changeText("Modes")
                    elif left_clicking=='difficulty':       # Save slider data
                        new_center = (diff_l - 5) * line_length / 10 + WINDOW_SIZE[0] / 2
                        diff_slider.centerx(new_center)  # Move the slider physically
                    elif left_clicking=='speed':            # Save slider data
                        new_center = (speed_l - 5) * line_length / 10 + WINDOW_SIZE[0] / 2
                        speed_slider.centerx(new_center)
                    elif left_clicking=="p2":               # Save slider data
                        new_center = (p2_l - 5) * line_length / 10 + WINDOW_SIZE[0] / 2
                        p2_slider.centerx(new_center)  # Move the slider physically
                    elif left_clicking=="double bot" and double_bot_button.collidepoint(event.pos):
                        double_bot=True                     # Change player lineup
                        single_bot=False
                        players[0] = bots[p2_l]             # 2 bots playing
                        players[1] = bots[diff_l]
                        no_bot_button.changeColor(light_button_color)
                        single_bot_button.changeColor(light_button_color)
                        double_bot_button.changeColor(dark_button_color) #This button is selected, so its a different color
                    elif left_clicking=='no bot' and no_bot_button.collidepoint(event.pos):
                        single_bot=False                    # Change player lineup
                        double_bot=False
                        players[0]="human"                  # 2 humans playing
                        players[1]="human"
                        double_bot_button.changeColor(light_button_color)
                        single_bot_button.changeColor(light_button_color)
                        no_bot_button.changeColor(dark_button_color) # This button is different color
                    elif left_clicking=='single bot' and single_bot_button.collidepoint(event.pos):
                        single_bot=True                     #Change player lineup
                        double_bot=False
                        players[0]='human'                  # Robot vs human
                        players[1]=bots[diff_l]
                        double_bot_button.changeColor(light_button_color)
                        no_bot_button.changeColor(light_button_color)
                        single_bot_button.changeColor(dark_button_color) #This button is different color
                    elif left_clicking=='undo setting' and undo_setting_button.collidepoint(event.pos):
                        undo_on=not undo_on                 #Swap whether undo is on or off
                        if undo_on:                         #If on, it should be selected and say on
                            undo_setting_button.changeColor(dark_button_color)
                            undo_setting_button.changeText("Undo:  ON")
                        else:                               #If off, it should be unselected and say off
                            undo_setting_button.changeColor(light_button_color)
                            undo_setting_button.changeText("Undo: OFF")
                    elif left_clicking=='skip setting' and skip_setting_button.collidepoint(event.pos):
                        skip_on=not skip_on                 #Swap whether skip is enabled or not
                        if skip_on:                         # If on, should be selected and say on
                            skip_setting_button.changeColor(dark_button_color)
                            skip_setting_button.changeText("Skip:  ON")
                        else:                               # If off, should be unselected and say off
                            skip_setting_button.changeColor(light_button_color)
                            skip_setting_button.changeText("Skip: OFF")
                    elif left_clicking=='show moves setting' and show_moves_button.collidepoint(event.pos):
                        show_moves_on=not show_moves_on                 #Swap whether showing moves is enabled or not
                        if show_moves_on:                         # If on, should be selected and say on
                            show_moves_button.changeColor(dark_button_color)
                            show_moves_button.changeText("Show Moves:  ON")
                        else:                               # If off, should be unselected and say off
                            show_moves_button.changeColor(light_button_color)
                            show_moves_button.changeText("Show Moves: OFF")
                    left_clicking=None
        #####################################################################################
        else:                           # TITLE PAGE
            if event.type==pg.MOUSEBUTTONDOWN:
                if event.button==1: #Leftclick down
                    if play_button.collidepoint(event.pos):
                        left_clicking = 'play'          # Play button selected
                    elif settings_button.collidepoint(event.pos):
                        left_clicking = 'open_settings' # Settings button selected
                    
                        # for i, but in enumerate(board_size_buttons):
                        #     if but.rect.collidepoint(event.pos):
                        #         left_clicking = "sizing" + str(i) # Boardsize button selected
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            elif event.type==pg.MOUSEBUTTONUP:
                if event.button==1: #Leftclick up
                    if left_clicking=='play' and play_button.collidepoint(event.pos):
                        game_active = True          # Start the game.
                        set_board_size(boardSize)   # This does some initialization
                        scores = [2, 2]             # Each player starts with 2 tiles
                        updateScores()
                    elif left_clicking=="open_settings" and settings_button.collidepoint(event.pos):
                            settings_open=True      # Open settings
                            settings_button.changeText(text="Close")
                    elif left_clicking and left_clicking[:-1]=="sizing":
                        i=int(left_clicking[-1])    # Finds which size is being selected
                        # if board_size_buttons[i].rect.collidepoint(event.pos): # If still selected, change board
                        #     set_board_size(i*2+4) #Reinitialize everything with new board size
                        #     updateTileList(B)
                    left_clicking=None #upclick means nothing's clicked
    ###########################################################################################################
    ###########################################################################################################
    # No matter what, we always have the background and OTHELLO
    screen.blit(background, (0, 0))
    background_image = pg.image.load("./Photos/modeswindow1.jpg").convert()
    background_image = pg.transform.scale(background_image, (800, 700))
    screen.blit(background_image, (0, 0))
    
    othello_box.blit(screen)
    if game_active:
        quit_button.blit(screen,left_clicking=='quit') #Quit button, highlighted if selected
        if skip_on or no_moves: skip_button.blit(screen,left_clicking=='skip') # Skip if enabled
        if undo_on: undo_button.blit(screen,left_clicking=='undo') # Undo if enabled

        screen.blit(board_image,board_image_rect)               # Draw board
        screen.blit(prog_bar,prog_bar_rect)                     # Progress bar
        rect=pg.Rect((0,0),(V((1,1))+prog_bar_rect.size))
        rect.topright=prog_bar_rect.topright
        pg.draw.rect(screen,(255,255,255),rect,2)         # Progress bar outline

        if not blocked and players[turn] != 'human' and not game_over: # If its a robot's turn, let the robot play
            blocked=True #Don't bother the robot
            roboTurn(players[turn]) # Robot makes a move
            blocked=False

        if animating_prog_bar:
            animate_prog_bar()
        # Below, all of the tiles are animated
        blocked=False
        mult=4
        iii=0
        for row in tile_list:
            for tile in row:
                if tile!=None:
                    if tile.update():
                        blocked=True #If any tile is animating, some clicking is blocked
                    if tile.rect.width>0: #If the tile is too thin, it throws an error
                        pg.gfxdraw.filled_ellipse(screen, *tile.coords(), tile.color)  # Draw the filling
                        pg.gfxdraw.aaellipse(screen,*tile.coords(),tile.color) #Draw the smooth outline
                    else:
                        pg.draw.ellipse(screen,tile.color,tile.rect) #Draw a rougher circle sometimes
        if show_moves_on and not blocked:
            for move in B.legal_moves(): # For all legal moves, draw a circle highlighting the position
                pos=(window_offset+(V(move)+(0.5,0.5))*sw).intify()
                pg.gfxdraw.aaellipse(screen,*pos,int(sw*(1-TILE_SPACING)/2),int(sw*(1-TILE_SPACING)/2),(0,0,0))

        for tile in tiles_to_remove: # These tiles are out of the main list but are still disappearing
            blocked=True # Animations are occurring
            pg.draw.ellipse(screen,tile.color,tile.rect) # Animate the disappearing ellipse
            if not tile.update():
                tiles_to_remove=[]   # If the tiles are done removing, clear the list

        #                                       DRAWING TEXT
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        white_score_box.blit(screen)                                # Score writers
        black_score_box.blit(screen)
        scores_box.blit(screen)
        turn_box.blit(screen)
        if game_over:
            game_over_button.blit(screen,left_clicking=="game over")
        ######################################################################################################
        # JUST IN CASE, every 2 seconds or so, the tiles get fixed so they match the board.
        if counter==120:
            if not blocked:
                updateTileList(B)
            counter=0
        counter+=1
    else:
        settings_button.blit(screen,left_clicking in ('open_settings','close_settings'))
        ######################################################################################################
        if settings_open:
            #Drawing a bunch of buttons on the screen.
            double_bot_button.blit(screen,left_clicking=="double bot")
            no_bot_button.blit(screen, left_clicking=="no bot")
            single_bot_button.blit(screen,left_clicking=="single bot")
            image = pg.image.load('Photos\Capture..jpg')
            new_image_width = 380  # Set the desired width of the image
            new_image_height = 140  # Set the desired height of the image
            image = pg.transform.scale(image, (new_image_width, new_image_height))
            
            screen.blit(image, (210, 90))
            if single_bot or double_bot:
                #Slider line for white bot setting
                pg.draw.line(screen,(255,255,255),WINDOW_SIZE/2+(-line_length/2,diff_h),WINDOW_SIZE/2+(line_length/2,diff_h),2)
                diff_slider.blit(screen, left_clicking == 'difficulty') #Draw slider
                if left_clicking == 'difficulty':           # If slider is selected
                    x_pos = pg.mouse.get_pos()[0]           # Approximate mouse postion to set difficulty
                    diff_l = max(min(round((x_pos - WINDOW_SIZE[0] / 2) * 10 / line_length + 5), 10), 0)
                    diff_slider.changeText(str(diff_l))     # Change the text appropriately
                    players[1] = bots[diff_l]               # Set the bot to be a player
                    new_center= min(max(x_pos,WINDOW_SIZE[0]/2-line_length/2),WINDOW_SIZE[0]/2+line_length/2)                                                                                   # TBD
                    diff_slider.centerx(new_center)         # Move the slider physically
            if single_bot:
                diff_label_box.blit(screen)                         # Write difficulty on the screen
            if double_bot:
                p1_label_box.blit(screen)                           # Write white player on the screen
                p2_label_box.blit(screen)                           # Write black player on the screen
                pg.draw.line(screen, (255, 255, 255), WINDOW_SIZE / 2 + (-line_length / 2, p2_h),
                             WINDOW_SIZE / 2 + (line_length / 2, p2_h), 2)  # Line for p2 slider
                p2_slider.blit(screen,left_clicking=='p2')                  # Draw p2 Slider
                if left_clicking=="p2":
                    x_pos = pg.mouse.get_pos()[0]                   # Approximate mouse pos gets p2 skill lvl
                    p2_l = min(max(round((x_pos - WINDOW_SIZE[0] / 2) * 10 / line_length + 5),0),10)
                    p2_slider.changeText(str(p2_l))
                    new_center=min(max(x_pos,WINDOW_SIZE[0]/2-line_length/2),WINDOW_SIZE[0]/2+line_length/2)                                                                                    #TBD
                    p2_slider.centerx(new_center)
                    players[0] = bots[p2_l]             # Set black player
            if left_clicking=='speed':
                x_pos = pg.mouse.get_pos()[0]  # use mouse position to set speed
                speed_l=max(round((x_pos-WINDOW_SIZE[0]/2)*10/line_length+5),0)
                if speed_l>10 and speed_l<11:  # Speed lvl 12 is the secret max lvl
                    speed_l=10
                if speed_l>=11:
                    speed_l=11
                    changeSpeed(100000)                 # Max speed
                    speed_slider.changeText("MAX")
                    new_center = WINDOW_SIZE[0]/2+line_length*0.6
                else:
                    changingspeed = 1.4 ** (speed_l-5)  # Set speed and text
                    speed_slider.changeText(str(round(changingspeed,1)))
                    changeSpeed(changingspeed)          # Change tile animations
                    new_center = min(max(x_pos,WINDOW_SIZE[0]/2-line_length/2),WINDOW_SIZE[0]/2+line_length/2)
                speed_slider.centerx(new_center)        # Move slider
            # speed_slider.blit(screen,left_clicking=="speed") # Draw slider
        else:   # TITLE SCREEN
            screen.blit(board_image_shrunk,board_image_shrunk_rect) # Show little board drawing
            play_button.blit(screen,left_clicking=='play')          # Play button
            # for i,but in enumerate(board_size_buttons):             # Board sizing buttons
            #     but.blit(screen,left_clicking=="sizing{}".format(i))
    window_title = "Othello Game"  # Set the desired name for the window
    
    pg.display.set_caption(window_title)
    icon = pg.image.load("./Photos/Capture..jpg")
    pg.display.set_icon(icon)
    pg.display.update()
    clock.tick(60) # Limits to 60 fps
