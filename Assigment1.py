# Scientific Computing - Roskilde University
# author: Maja H Kirkeby
# Editor: Ulrikke Andersen

# Simulation there represents a cannon shooting
# a cannonball with a specific randomly chosen wind and a velocity there are changeable

# import pygame and sys modules
import random
import sys

import pygame

# initialize pygame
pygame.init()

# colors #
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 102, 0)

# Initialize Real world parameters
g = 9.8  # Gravitational acceleration (m/s**2)
D = 0.1  # drag coefficient
Mass = 1  # mass of the ball
Wind = 0

# Defined the parameters related to the screen and its motion:
FramesPerSec = 60
SpeedUp = 8
T = 0.0
dt = (1 / FramesPerSec) * SpeedUp

Width = 2000.0  # Width of screen
Height = 1000.0  # Height of screen

#  the interval of x and y-axis grid of the coordinate system
XGrid = 100
YGrid = 100

ScaleToScreen = 0.5  # scale from the real-world to the screen-coordinate system


# generates a wind randomly
def GenerateWind():
    global Wind
    Wind = random.randint(-15, 15)


# Convert from real-world to screen( pixel) world
def ConvertToPixel(RealWorld_x, RealWorld_y, Scale=ScaleToScreen, RealWorld_Height=Height):
    # calculate the pixel coordinates from the real-world coordinates and the scale
    return int(RealWorld_x * Scale), int((RealWorld_Height - RealWorld_y) * Scale - 1)


# Convert from the screen world to the real-world
def ConvertToReal(PixX, PixY, Scale_To_Screen, height):
    Real_X = PixX / Scale_To_Screen
    Real_Y = - (PixY / Scale_To_Screen) + height
    return Real_X, Real_Y


# Calculates the center of the cannon in respect to x- and y- direction
def Cal_Balls_Init_Position(Cannon):
    return Cannon['x'] + Cannon['Width'] / 2, \
           Cannon['y'] - Cannon['Height'] / 2


# defines the screen size in relation to the real-world
def IsInField(RealWorld_x, RealWorld_y, Field_Width=Width):
    # when the x is bigger the zero and smaller then gird width and y is bigger then zero
    return (0 < RealWorld_x < Field_Width
            and RealWorld_y > 0)


# Init the cannon on the screen
Cannon_Width, Cannon_Height = 33, 31
CannonS = {"x": 200,
           "y": 0 + Cannon_Height,
           "Vx": 84.85,  # ≈ 120 m/s angle 45
           "Vy": 84.85,  # ≈ 120 m/s angle 45
           "Width": Cannon_Width,
           "Height": Cannon_Height,
           "Color": WHITE,
           'Balls Radius': 10  # radius in meters
           }

# more players
Players = [CannonS]


# Init the player and their cannons inti parameters( wind and states that the ball are not shooting)
def ChangePlayer():
    global Players, Turn, Shooting, x, y, vx, vy, BallsColor, BallsRadius
    Turn = (Turn + 1) % len(Players)  # will rotate through the list of players

    (x, y) = Cal_Balls_Init_Position(Players[Turn])
    vx = Players[Turn]['Vx']
    vy = Players[Turn]['Vy']
    BallsColor = Players[Turn]['Color']
    BallsRadius = Players[Turn]['Balls Radius']
    GenerateWind()
    print('Round:', Round, 'with a wind speed of:', Wind)  # print the players round and the winds speed
    Shooting = False


# Updates the force effecting the ball
def UpdateStatus(X, Y, Vx, Vy, mass, DT=1 / 60, d=0.0):
    # Force field
    F_g = -9.81 * mass

    F_drag_x = -d * (Vx - Wind)
    F_drag_y = -d * Vy

    F_x = F_drag_x
    F_y = F_g + F_drag_y

    Vx = Vx + F_x / mass * DT
    Vy = Vy + F_y / mass * DT

    X = X + Vx * DT
    Y = Y + Vy * DT

    return X, Y, Vx, Vy


# Draw real-world grid on screen
def DrawGrid(Surface, Color, Real_XGrid, Real_YGrid, Real_Width=Width, Real_Height=Height):
    # vertical lines
    for i in range(int(Real_Width / Real_XGrid)):
        pygame.draw.line(Surface, Color,
                         ConvertToPixel(i * Real_XGrid, 0),
                         ConvertToPixel(i * Real_XGrid, Real_Height))
    # horizontal lines
    for i in range(int(Real_Height / YGrid)):
        pygame.draw.line(Surface, Color,
                         ConvertToPixel(0, i * Real_YGrid),
                         ConvertToPixel(Real_Width, i * Real_YGrid))


# Draw the cannon on surface out from the parameters taken from init of cannon
def DrawCannon(Surface, Cannon):
    # Base of the cannon
    pygame.draw.rect(Surface, Cannon['Color'],
                     (ConvertToPixel(Cannon['x'], Cannon['y']),
                      (Cannon['Width'] * ScaleToScreen, Cannon['Height'] * ScaleToScreen)))
    # center of cannon
    CannonCenter = Cal_Balls_Init_Position(Cannon)

    # Barrel of cannon
    pygame.draw.line(Surface, Cannon['Color'],
                     ConvertToPixel(CannonCenter[0], CannonCenter[1]),
                     ConvertToPixel(CannonCenter[0] + Cannon['Vx'] * ScaleToScreen,
                                    CannonCenter[1] + Cannon['Vy'] * ScaleToScreen), 3)


# drawing the wind representation
def DrawWind(Surface, wind):
    pygame.draw.line(Surface, WHITE,
                     (50 * 3, 50 * 3),
                     (50 * 3 + int(wind) * 10, 50 * 3), 4)


# create screen:
# 1. specify screen size
screen_Width, screen_Height = int(Width * ScaleToScreen), int(Height * ScaleToScreen)
# 2. define screen
screen = pygame.display.set_mode((screen_Width, screen_Height))
# 3. set caption
pygame.display.set_caption("My Pygame Skeleton")

# update pygame's clock use the framerate
clock = pygame.time.Clock()

# game loop variables initialized
Running = True
Turn = 0
Shooting = False
Round = 0
Limit = 5

# initialize the projectile's: color, pixel velocity and pixel position according to the current player
(x, y) = Cal_Balls_Init_Position(Players[Turn])
vx = Players[Turn]['Vx']  # x velocity in meters per second
vy = Players[Turn]['Vy']  # y velocity in meters per second
BallsColor = Players[Turn]['Color']
BallsRadius = Players[Turn]['Balls Radius']
GenerateWind()

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Shooting = True

        # a if statement there checks if the limit of turns in our case 5 is reached and quit the game
        if Round == Limit:
            Running = False

        if event.type == pygame.MOUSEBUTTONDOWN and Shooting is False:
            MousePosition = pygame.mouse.get_pos()
            (mx, my) = ConvertToReal(MousePosition[0], MousePosition[1], ScaleToScreen, Height)

            (CannonX, CannonY) = Cal_Balls_Init_Position(Players[Turn])
            (VectorX, VectorY) = (mx - CannonX), (my - CannonY)

            Players[Turn]['Vx'] = VectorX

            Players[Turn]['Vy'] = VectorY

            vx = Players[Turn]['Vx']

            vy = Players[Turn]['Vy']

    if Shooting:
        # drag force with the x - y axis in focus
        x, y, vx, vy = UpdateStatus(x, y, vx, vy, Mass, D, dt)

    # checks if ball is inside screen before changing player
    if not (IsInField(x, y)):
        Round += 1
        ChangePlayer()

    # game logic
    # draw a background using screen.fill()
    screen.fill(GREEN)

    # draw grid
    DrawGrid(screen, BLACK, XGrid, YGrid, Width, Height)

    # draw the player's cannon
    DrawCannon(screen, CannonS)

    # draw the wind
    DrawWind(screen, Wind)

    # convert the real-world coordinates to pixel-coordinates
    (x_pix, y_pix) = ConvertToPixel(x, y)
    BallsRadius_pix = round(ScaleToScreen * BallsRadius)

    # draw ball using the pixel coordinates
    pygame.draw.circle(screen, BallsColor, (x_pix, y_pix), BallsRadius_pix)

    # redraw the screen
    pygame.display.flip()

    # Limit the framerate (must be called in each iteration)
    clock.tick(FramesPerSec)

# after the game loop
pygame.quit()
sys.exit()
