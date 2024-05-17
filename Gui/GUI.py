# Import pygame and tuples module
import pygame as pg
from Tuples import V

# Import math module for calculations
import math

# Define constants for board size and color
BOARD_WIDTH = 500
TILE_SPACING = 0.12
COLORS = [(25, 25, 25), (175, 175, 175)]
RAD = 10 # Corner radius of buttons

# Initialize pygame and window size
pg.init()
WINDOW_SIZE = V((800, 650))
BOARD_DIMENSION = V((BOARD_WIDTH, BOARD_WIDTH))
WINDOW_SHIFT = (WINDOW_SIZE - BOARD_DIMENSION) / 2


# Define a class for tiles
class PlayGround():
    # Initialize a tile with position, color index and size
    def __init__(self, x, y, color_index, sw):
        # Set the attributes of the tile
        self.sw = sw
        self.x = x
        self.y = y
        self.window_position = WINDOW_SHIFT + V((sw * (x + 0.5), sw * (y + 0.5) + 50))
        self.rect = pg.Rect(0, 0, sw * (1 - TILE_SPACING), sw * (1 - TILE_SPACING))
        self.rect.center = self.window_position
        self.color_index = color_index
        self.color = COLORS[self.color_index]

        # Place the tile on the board with animation
        self.place()

        # Set the flags for flipping and removing
        self.flipping = False
        self.removing = False

    # Place a tile on the board with animation
    def place(self):
        # The piece accelerates towards the board.
        self.placing = True
        self.placing_t = 0

    def place_animation(self):
        # Update the placing time and scale the tile size accordingly
        self.placing_t += 1
        scale = (2 - (self.placing_t / placing_tmax) ** 2) * self.sw * (1 - TILE_SPACING)
        self.rect = pg.Rect(0, 0, scale, scale)
        self.rect.center = self.window_position

        # Check if the placing is done and reset the tile size if so
        if self.placing_t >= placing_tmax:
            self.placing = False
            self.rect = pg.Rect(0, 0, self.sw * (1 - TILE_SPACING), self.sw * (1 - TILE_SPACING))
            self.rect.center = self.window_position

    # Return the coordinates of the tile ellipse
    def coords(self):
        return (*self.rect.center, int(self.rect.width / 2), int(self.rect.height / 2))

    # Flip the tile over with animation
    def flip(self):
        # Set the flipping flag and color change flag to True
        self.flipping = True
        self.must_flip_color = True
        # Set the flipping time to zero
        self.flipping_t = 0

    def flip_animation(self):
        # Update the flipping time and scale and rotate the tile size accordingly
        self.flipping_t += 1

        scale = (self.flipping_t / (flipping_tmax ** 2) * (flipping_tmax - self.flipping_t) * 3 + 1) * \
                self.sw * (1 - TILE_SPACING)
        # Below, we use cosine to show rotation in addition to the jumping rescaling
        self.rect = pg.Rect(0, 0, scale * math.cos(self.flipping_t / flipping_tmax * math.pi), scale)
        self.rect.center = self.window_position

        # Change the color of the tile if necessary
        if self.must_flip_color and self.flipping_t > flipping_tmax / 2:
            self.color_index = (self.color_index + 1) % 2
            self.color = COLORS[self.color_index]
            self.must_flip_color = False

            # Check if the flipping is done and reset the tile size if so
        if self.flipping_t >= flipping_tmax:
            self.flipping = False
            self.rect = pg.Rect(0, 0, self.sw * (1 - TILE_SPACING), self.sw * (1 - TILE_SPACING))  # Final rescale
            self.rect.center = self.window_position
        pass

    # Remove a tile from the board with animation
    def remove(self):
        # Set the removing flag to True
        self.removing = True
        # Set the removing time to zero
        self.removing_t = 0

    def remove_animation(self):
        # Update the removing time and rotate and shift the tile accordingly
        self.removing_t += 1
        t = self.removing_t / placing_tmax  # Percentage of animation
        scale = self.sw * (1 - TILE_SPACING)  # Scale is normal
        theta = (math.pi / 2 * t ** 2)  # The rotation angle increases
        shift = -((t + t ** 2) / 2) * self.sw  # Shift center up over time
        self.rect = pg.Rect(0, 0, scale * math.cos(theta), scale)  # Rescale and rotate
        self.rect.center = self.window_position + V((0, shift))  # Recenter and shift

        # Check if the removing is done and stop the animation if so
        if self.removing_t >= placing_tmax:
            self.removing = False

    # Update the tile state and run any animations if needed
    def update(self):
        # Check if flipping animation is needed and run it
        if self.flipping:
            self.flip_animation()

        # Check if placing animation is needed and run it
        if self.placing:
            self.place_animation()

        # Check if removing animation is needed and run it
        if self.removing:
            self.remove_animation()

        # Return True if any animation is still running, False otherwise
        return self.flipping or self.placing or self.removing


# Define a class for buttons
class Button():
    # Initialize a button with size, color, text, font and thickness
    def __init__(self, size, color, text="", text_color=(0, 0, 0), font=pg.font.SysFont('calibri', 20), thickness=2):

        # Set the attributes of the button
        self.font = font  # Font of text
        self.thickness = thickness  # Thickness of border
        self.color = V(color)  # Color of fill
        self.text_color = text_color  # Color of text
        self.text = text  # Words to print
        self.rect = pg.Rect(0, 0, *size)  # Dimensions of button
        self.text_surface = font.render(text, True, text_color)  # Rendering text onto surface
        self.text_rect = self.text_surface.get_rect()  # Used for centering text surface
        self.text_shift = V((0, 0))  # Used to shift text off center

    # Change the color of the button
    def changeColor(self, color):
        self.color = V(color)

    # Change some properties of the text on the button
    def changeText(self, text=None, color=None, font=None):
        # Update the attributes of the text if needed
        if text != None:
            self.text = text  # Change the words
        if color != None:
            self.text_color = color  # Change color of the text
        if font != None:
            self.font = font  # Change the font

        # Re-render and re-center the text surface
        self.text_surface = (self.font).render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.rect.center + self.text_shift

    # Draw the button on the screen with different effects depending on clicking state
    def blit(self, surf, clicking):
        # Draw the button with different colors and thicknesses depending on clicking state
        if clicking:
            pg.draw.rect(surf, self.color * .9, self.rect, border_radius=RAD)
            surf.blit(self.text_surface, self.text_rect)  # Write text
            pg.draw.rect(surf, V(self.color) / 3, self.rect, self.thickness * 2, border_radius=RAD)
        else:
            pg.draw.rect(surf, self.color, self.rect, border_radius=RAD)
            surf.blit(self.text_surface, self.text_rect)  # Write text
            pg.draw.rect(surf, V(self.color) / 3, self.rect, self.thickness, border_radius=RAD)

    # Move button by setting the midleft point
    def midleft(self, loc):
        # Update the rect position and re-center the text surface
        self.rect.midleft = loc
        self.text_rect.center = self.rect.center + self.text_shift

    # Move button by setting the center point
    def center(self, loc):
        # Update the rect position and re-center the text surface
        self.rect.center = loc
        self.text_rect.center = loc + self.text_shift

    # Move the central x coord of the button
    def centerx(self, pos):
        # Update the rect position and re-center the text surface
        self.center((pos, self.rect.centery))

    # Shift the text on the button by a given offset
    def shiftText(self, shift=(0, 0)):
        # Update the text shift attribute and re-center the text surface
        self.text_shift = shift
        self.text_rect.center = V(shift) + self.rect.center

    # Check if a given point collides with the button
    def collidepoint(self, point):
        # Return True if the point is inside the button rect, False otherwise
        return self.rect.collidepoint(point)


# Define a class for text boxes
class TextBox():
    # Initialize a text box with text, color and font
    def __init__(self, text="", color=(0, 0, 0), font=pg.font.SysFont('calibri', 20)):
        # Set the attributes of the text box
        self.font = font  # Font of text
        self.color = color  # Color of text
        self.text = text  # Words to print
        self.surf = font.render(text, True, color)  # Rendering text onto surface
        self.rect = self.surf.get_rect()  # Dimensions of text box
        self.middle = self.rect.center  # Center of text box

    # Set the center of the text box to a given position
    def center(self, pos):
        # Update the rect position and the middle attribute
        self.rect.center = pos
        self.middle = pos

    # Change some properties of the text on the text box
    def changeText(self, text=None, color=None, font=None):
        # Update the attributes of the text if needed
        if text != None:
            self.text = text  # Change the words
        if color != None:
            self.color = color  # Change color of the text
        if font != None:
            self.font = font  # Change the font

        # Re-render and re-center the text surface
        self.surf = self.font.render(self.text, True, self.color)
        self.rect = self.surf.get_rect()
        self.center(self.middle)

        # Draw the text box on the screen

    def blit(self, screen):
        screen.blit(self.surf, self.rect)

# Change the animation speed to a given value
def changeSpeed(newSpeed):
    # Update the global variables for flipping and placing time limits
    global flipping_tmax, placing_tmax
    flipping_tmax = 20 / newSpeed
    placing_tmax = 15 / newSpeed


