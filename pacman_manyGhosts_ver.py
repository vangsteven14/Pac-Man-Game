# Setting up the game environment and initializing Pygame
from board import boards
import pygame, math
import copy

pygame.init()

WIDTH = 900
HEIGHT = 950

screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
countdown_font = pygame.font.Font('freesansbold.ttf', 80)
level = copy.deepcopy(boards) 
color = 'blue'
PI = math.pi

# Load player images
player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)))

# Load ghost images
blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (45, 45))
inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (45, 45))
pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (45, 45))
clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (45, 45))
spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (45, 45))
dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (45, 45))

# Initial player position
player_x = 450
player_y = 663
direction = 0

# Intial ghost positions
blinky_x = 56
blinky_y = 58
blinky_direction = 0

inky_x = 440
inky_y = 388
inky_direction = 2

pinky_x = 440
pinky_y = 448
pinky_direction = 2

clyde_x = 440    
clyde_y = 428
clyde_direction = 2

# Intial ghost_clone positions
blinky_clone_x = 50
blinky_clone_y = 48
blinky_clone_direction = 0

inky_clone_x = 430
inky_clone_y = 378
inky_clone_direction = -2

pinky_clone_x = 430
pinky_clone_y = 438
pinky_clone_direction = -2

clyde_clone_x = 430  
clyde_clone_y = 418
clyde_clone_direction = -2

counter = 0
flicker = 0

# Initial game variables
turns_allowed = [False, False, False, False, False, False, False, False]
direction_command = 0
player_speed = 2
score = 0
powerup = False
power_counter = 0
eaten_ghost = [False, False, False, False, False, False, False, False] 
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]

blinky_dead = False
inky_dead = False
clyde_dead = False
pinky_dead = False

blinky_box = False
inky_box = False
clyde_box = False
pinky_box = False

# Additional 4 more ghosts
blinky_clone_dead = False
inky_clone_dead = False
clyde_clone_dead = False
pinky_clone_dead = False

blinky_clone_box = False
inky_clone_box = False
clyde_clone_box = False
pinky_clone_box = False

moving = False
ghost_speeds = [2, 2, 2, 2, 2, 2, 2, 2]  # Speeds for 8 ghosts
startup_counter = 0
lives = 3
game_over = False
game_won = False

class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead 
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()
        
    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect
    
    def check_collisions(self):
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]  # Right, Left, Up, Down

        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box
    
    # Move the ghost based on its direction and target
    def move_clyde(self):
        # r, l, u, d
        # clyde is going to turn whenever advantageous for pursuit
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_blinky(self):
        # r, l, u, d
        # blinky is going to turn whenever colliding with walls, otherwise continue straight
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_inky(self):
        # r, l, u, d
        # inky turns up or down at any point to pursue, but left and right only on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_pinky(self):
        # r, l, u, d
        # inky is going to turn left or right whenever advantageous, but only up or down on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

def draw_countdown(counter):
    if counter < 60:
        text = "3"
    elif counter < 120:
        text = "2"
    elif counter < 180:
        text = "1"
    elif 180 <= counter < 240:
        text = "Go!"
    else:
        return
    
    countdown_text = countdown_font.render(text, True, "yellow")
    rect = countdown_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    bg_rect = rect.inflate(40, 40)
    pygame.draw.rect(screen, 'black', bg_rect, border_radius = 10)
    pygame.draw.rect(screen, 'blue', bg_rect, width = 4, border_radius = 10)
    screen.blit(countdown_text, rect)

def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))

    # Initial pacman's lives and powerup display
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))

    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300], 0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        game_over_text = font.render('Game Over! Space bar to restart', True, 'red')
        screen.blit(game_over_text, (100, 300))

    if game_won:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300], 0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        game_won_text = font.render('Victory! Space bar to restart', True, 'green')
        screen.blit(game_won_text, (100, 300))

def check_collisions(score, power, power_count, eaten_ghost):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30

    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            score += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            score += 50
            power = True
            power_count = 0
            eaten_ghost = [False, False, False, False, False, False, False, False]  # Track eaten ghosts
    return score, power, power_count, eaten_ghost

def draw_board():
    num1 = ((HEIGHT - 50) // 32)    # Height of each row
    num2 = (WIDTH // 30)            # Width of each column

    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', 
                                   (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', 
                                   (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, 
                                 (j * num2 + (0.5 * num2), i * num1), (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, 
                                 (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1], 0, PI/2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI, 3 * PI/2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI/2, 2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white',
                                 (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 3)

# Player as Pacman
def draw_player():
    # RIGHT = 0, LEFT = 1, UP = 2, DOWN = 3
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))

def check_position(center_x, center_y):
    turns = [False, False, False, False]  # Right, Left, Up, Down
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15

    # check collisions based on center x and center y of player +/- fudge number
    if center_x // 30 < 29:
        if direction == 0:
            if level[center_y // num1][(center_x - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[center_y // num1][(center_x + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(center_y + num3) // num1][center_x  // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(center_y - num3) // num1][center_x // num2] < 3:
                turns[2] = True

        # Check for vertical and horizontal lines of player to block movement
        if direction == 2 or direction == 3:
            if 12 <= center_x % num2 <= 18:
                if level[(center_y + num3) // num1][center_x // num2] < 3:
                    turns[3] = True
                if level[(center_y - num3) // num1][center_x // num2] < 3:
                    turns[2] = True
            if 12 <= center_y % num1 <= 18:
                if level[center_y // num1][(center_x - num2) // num2] < 3:
                    turns[1] = True
                if level[center_y // num1][(center_x + num2) // num2] < 3:
                    turns[0] = True

        if direction == 0 or direction == 1:
            if 12 <= center_x % num2 <= 18:
                if level[(center_y + num1) // num1][center_x // num2] < 3:
                    turns[3] = True
                if level[(center_y - num1) // num1][center_x // num2] < 3:
                    turns[2] = True
            if 12 <= center_y % num1 <= 18:
                if level[center_y // num1][(center_x - num3) // num2] < 3:
                    turns[1] = True
                if level[center_y // num1][(center_x + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True
    return turns

def move_player(play_x, play_y):
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y

def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y,
                blink_clone_x, blink_clone_y, ink_clone_x, ink_clone_y, pink_clone_x, pink_clone_y, clyd_clone_x, clyd_clone_y):
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0

    return_target = (380, 400)

    if powerup:
        # Targets for blinky ghost on player position and powerup state
        if not blinky.dead and not eaten_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky.dead and eaten_ghost[0]:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        # Targets for inky ghost on player position and powerup state
        if not inky.dead and not eaten_ghost[1]:
            ink_target = (runaway_x, player_y)
        elif not inky.dead and eaten_ghost[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        # Targets for pinky ghost on player position and powerup state
        if not pinky.dead:
            pink_target = (player_x, runaway_y)
        elif not pinky.dead and eaten_ghost[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        # Targets for clyde ghost on player position and powerup state
        if not clyde.dead and not eaten_ghost[3]:
            clyde_target = (450, 450)
        elif not clyde.dead and eaten_ghost[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyde_target = (400, 100)
            else:
                clyde_target = (player_x, player_y)
        else:
            clyde_target = return_target

        # Targets for blinky clone ghost on player position and powerup state
        if not blinky_clone.dead and not eaten_ghost[4]:
            blink_clone_target = (runaway_x, runaway_y)
        elif not blinky_clone.dead and eaten_ghost[4]:
            if 340 < blink_clone_x < 560 and 340 < blink_clone_y < 500:
                blink_clone_target = (400, 100)
            else:
                blink_clone_target = (player_x, player_y)
        else:
            blink_clone_target = return_target
        # Targets for inky clone ghost on player position and powerup state
        if not inky_clone.dead and not eaten_ghost[5]:
            ink_clone_target = (runaway_x, player_y)
        elif not inky_clone.dead and eaten_ghost[5]:
            if 340 < ink_clone_x < 560 and 340 < ink_clone_y < 500:
                ink_clone_target = (400, 100)
            else:
                ink_clone_target = (player_x, player_y)
        else:
            ink_clone_target = return_target
        # Targets for pinky clone ghost on player position and powerup state
        if not pinky_clone.dead and not eaten_ghost[6]:
            pink_clone_target = (player_x, runaway_y)
        elif not pinky_clone.dead and eaten_ghost[6]:
            if 340 < pink_clone_x < 560 and 340 < pink_clone_y < 500:
                pink_clone_target = (400, 100)
            else:
                pink_clone_target = (player_x, player_y)
        else:
            pink_clone_target = return_target
        # Targets for clyde clone ghost on player position and powerup state
        if not clyde_clone.dead and not eaten_ghost[7]:
            clyde_clone_target = (450, 450)
        elif not clyde_clone.dead and eaten_ghost[7]:
            if 340 < clyd_clone_x < 560 and 340 < clyd_clone_y < 500:
                clyde_clone_target = (400, 100)
            else:
                clyde_clone_target = (player_x, player_y)
        else:
            clyde_clone_target = return_target
    else:
        if not blinky.dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyde_target = (400, 100)
            else:
                clyde_target = (player_x, player_y)
        else:
            clyde_target = return_target
        if not blinky_clone.dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_clone_target = (400, 100)
            else:
                blink_clone_target = (player_x, player_y)
        else:
            blink_clone_target = return_target
        if not inky_clone.dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_clone_target = (400, 100)
            else:
                ink_clone_target = (player_x, player_y)
        else:
            ink_clone_target = return_target
        if not pinky_clone.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_clone_target = (400, 100)
            else:
                pink_clone_target = (player_x, player_y)
        else:
            pink_clone_target = return_target
        if not clyde_clone.dead:    
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyde_clone_target = (400, 100)
            else:
                clyde_clone_target = (player_x, player_y)
        else:
            clyde_clone_target = return_target
    return [blink_target, ink_target, pink_target, clyde_target, blink_clone_target, ink_clone_target, pink_clone_target, clyde_clone_target]

# -----------------------------------------------------------------------------------------------
# Initial game loop
# -----------------------------------------------------------------------------------------------
run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True

    # Powerup timer and ghost reset
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
            power_counter = 0
            powerup = False
            eaten_ghost = [False, False, False, False, False, False, False, False]  # Resets eaten ghosts

    # Startup game with delay before player movement        
    if startup_counter < 200 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True
    

    # Functions for game logic
    screen.fill('black')
    draw_board()

    center_x = player_x + 23
    center_y = player_y + 24

    # Set 4 additional ghost speeds based on powerup and eaten status
    if powerup:
        ghost_speeds = [1, 1, 1, 1, 1, 1, 1, 1]
    else:
        ghost_speeds = [2, 2, 2, 2, 2, 2, 2, 2]
        
    if eaten_ghost[0]:
        ghost_speeds[0] = 2
    if eaten_ghost[1]:
        ghost_speeds[1] = 2
    if eaten_ghost[2]:
        ghost_speeds[2] = 2
    if eaten_ghost[3]:
        ghost_speeds[3] = 2
    if eaten_ghost[4]:
        ghost_speeds[4] = 2
    if eaten_ghost[5]:
        ghost_speeds[5] = 2
    if eaten_ghost[6]:
        ghost_speeds[6] = 2
    if eaten_ghost[7]:
        ghost_speeds[7] = 2

    if blinky_dead:
        ghost_speeds[0] = 4
    if inky_dead:
        ghost_speeds[1] = 4
    if pinky_dead:
        ghost_speeds[2] = 4
    if clyde_dead:
        ghost_speeds[3] = 4
    if blinky_clone_dead:
        ghost_speeds[4] = 4
    if inky_clone_dead:
        ghost_speeds[5] = 4
    if pinky_clone_dead:
        ghost_speeds[6] = 4
    if clyde_clone_dead:
        ghost_speeds[7] = 4

    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False

    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 20, 2)
    draw_player()

    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_img, blinky_direction, blinky_dead, blinky_box, 0)
    inky = Ghost(inky_x, inky_y, targets[1], ghost_speeds[1], inky_img, inky_direction, inky_dead, inky_box, 1)
    pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speeds[2], pinky_img, pinky_direction, pinky_dead, pinky_box, 2)
    clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speeds[3], clyde_img, clyde_direction, clyde_dead, clyde_box, 3)

    blinky_clone = Ghost(blinky_clone_x, blinky_clone_y, targets[4], ghost_speeds[4], blinky_img, blinky_direction, blinky_clone_dead, blinky_clone_box, 4)
    inky_clone = Ghost(inky_clone_x, inky_clone_y, targets[5], ghost_speeds[5], inky_img, inky_direction, inky_clone_dead, inky_clone_box, 5)
    pinky_clone = Ghost(pinky_clone_x, pinky_clone_y, targets[6], ghost_speeds[6], pinky_img, pinky_direction, pinky_clone_dead, pinky_clone_box, 6)
    clyde_clone = Ghost(clyde_clone_x, clyde_clone_y, targets[7], ghost_speeds[7], clyde_img, clyde_direction, clyde_clone_dead, clyde_clone_box, 7)

    draw_misc()

    # Display countdown at beginning of game or after losing a life
    if startup_counter < 200 and not game_over and not game_won:
        draw_countdown(startup_counter)

    pygame.display.flip()

    targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y,
                          blinky_clone_x, blinky_clone_y, inky_clone_x, inky_clone_y, pinky_clone_x, pinky_clone_y, clyde_clone_x, clyde_clone_y)

    turns_allowed = check_position(center_x, center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
        if not blinky_dead and not blinky.in_box:
            blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
        else:
            blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
        if not pinky_dead and not pinky.in_box:
            pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
        else:
            pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
        if not inky_dead and not inky.in_box:
            inky_x, inky_y, inky_direction = inky.move_inky()
        else:
            inky_x, inky_y, inky_direction = inky.move_clyde()
        if not clyde_dead and not clyde.in_box:
            clyde_x, clyde_y, clyde_direction = clyde.move_clyde()
        else:
            clyde_x, clyde_y, clyde_direction = clyde.move_clyde()


        if not blinky_clone_dead and not blinky_clone.in_box:
            blinky_clone_x, blinky_clone_y, blinky_direction = blinky_clone.move_clyde()
        else:
            blinky_clone_x, blinky_clone_y, blinky_direction = blinky_clone.move_clyde()
        if not pinky_clone_dead and not pinky_clone.in_box:
            pinky_clone_x, pinky_clone_y, pinky_direction = pinky_clone.move_clyde()
        else:
            pinky_clone_x, pinky_clone_y, pinky_direction = pinky_clone.move_clyde()
        if not inky_clone_dead and not inky_clone.in_box:
            inky_clone_x, inky_clone_y, inky_direction = inky_clone.move_clyde()
        else:
            inky_clone_x, inky_clone_y, inky_direction = inky_clone.move_clyde()

        clyde_clone_x, clyde_clone_y, clyde_direction = clyde_clone.move_clyde()

    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)

    if not powerup:
        if (player_circle.colliderect(blinky.rect) and not blinky.dead) or \
           (player_circle.colliderect(inky.rect) and not inky.dead) or \
           (player_circle.colliderect(pinky.rect) and not pinky.dead) or \
           (player_circle.colliderect(clyde.rect) and not clyde.dead) or \
           (player_circle.colliderect(blinky_clone.rect) and not blinky_clone.dead) or \
           (player_circle.colliderect(inky_clone.rect) and not inky_clone.dead) or \
           (player_circle.colliderect(pinky_clone.rect) and not pinky_clone.dead) or \
           (player_circle.colliderect(clyde_clone.rect) and not clyde_clone.dead):
            if lives > 0:
                lives -= 1
                startup_counter = 0
                powerup = False
                power_counter = 0

                # Initial player position
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0

                # Intial ghost positions
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0

                inky_x = 440
                inky_y = 388
                inky_direction = 2

                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2

                clyde_x = 440    
                clyde_y = 438
                clyde_direction = 2

                blinky_clone_x = 50
                blinky_clone_y = 48
                blinky_clone_direction = 0

                inky_clone_x = 430
                inky_clone_y = 378
                inky_clone_direction = -2

                pinky_clone_x = 430
                pinky_clone_y = 438
                pinky_clone_direction = -2

                clyde_clone_x = 430  
                clyde_clone_y = 418
                clyde_clone_direction = -2

                eaten_ghost = [False, False, False, False, False, False, False, False]

                blinky_dead = False
                inky_dead = False
                pinky_dead = False
                clyde_dead = False
                blinky_clone_dead = False
                inky_clone_dead = False
                pinky_clone_dead = False
                clyde_clone_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
    
    # Reset player and ghosts if player collides with a ghost while powered up
    if powerup and player_circle.colliderect(blinky.rect) and eaten_ghost[0] and not blinky.dead:
            if lives > 0:
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0

                # Initial player position
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0

                # Intial ghost positions
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0

                inky_x = 440
                inky_y = 388
                inky_direction = 2

                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2

                clyde_x = 440    
                clyde_y = 438
                clyde_direction = 2

                blinky_clone_x = 50
                blinky_clone_y = 48
                blinky_clone_direction = 0

                inky_clone_x = 430
                inky_clone_y = 378
                inky_clone_direction = -2

                pinky_clone_x = 430
                pinky_clone_y = 438
                pinky_clone_direction = -2

                clyde_clone_x = 430  
                clyde_clone_y = 418
                clyde_clone_direction = -2

                eaten_ghost = [False, False, False, False, False, False, False, False]

                blinky_dead = False
                inky_dead = False
                pinky_dead = False
                clyde_dead = False
                blinky_clone_dead = False
                inky_clone_dead = False
                pinky_clone_dead = False                
                clyde_clone_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0

    if powerup and player_circle.colliderect(inky.rect) and eaten_ghost[1] and not inky.dead:
            if lives > 0:
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0

                # Initial player position
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0

                # Intial ghost positions
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0

                inky_x = 440
                inky_y = 388
                inky_direction = 2

                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2

                clyde_x = 440    
                clyde_y = 438
                clyde_direction = 2

                blinky_clone_x = 50
                blinky_clone_y = 48
                blinky_clone_direction = 0

                inky_clone_x = 430
                inky_clone_y = 378
                inky_clone_direction = -2

                pinky_clone_x = 430
                pinky_clone_y = 438
                pinky_clone_direction = -2

                clyde_clone_x = 430  
                clyde_clone_y = 418
                clyde_clone_direction = -2

                eaten_ghost = [False, False, False, False, False, False, False, False]

                blinky_dead = False
                inky_dead = False
                pinky_dead = False
                clyde_dead = False
                blinky_clone_dead = False
                inky_clone_dead = False
                pinky_clone_dead = False                
                clyde_clone_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0

    if powerup and player_circle.colliderect(pinky.rect) and eaten_ghost[2] and not pinky.dead:
            if lives > 0:
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0

                # Initial player position
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0

                # Intial ghost positions
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0

                inky_x = 440
                inky_y = 388
                inky_direction = 2

                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2

                clyde_x = 440    
                clyde_y = 438
                clyde_direction = 2

                blinky_clone_x = 50
                blinky_clone_y = 48
                blinky_clone_direction = 0

                inky_clone_x = 430
                inky_clone_y = 378
                inky_clone_direction = -2

                pinky_clone_x = 430
                pinky_clone_y = 438
                pinky_clone_direction = -2

                clyde_clone_x = 430  
                clyde_clone_y = 418
                clyde_clone_direction = -2

                eaten_ghost = [False, False, False, False, False, False, False, False]

                blinky_dead = False
                inky_dead = False
                pinky_dead = False
                clyde_dead = False
                blinky_clone_dead = False
                inky_clone_dead = False
                pinky_clone_dead = False                
                clyde_clone_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
                
    if powerup and player_circle.colliderect(clyde.rect) and eaten_ghost[3] and not clyde.dead:
            if lives > 0:
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0

                # Initial player position
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0

                # Intial ghost positions
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0

                inky_x = 440
                inky_y = 388
                inky_direction = 2

                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2

                clyde_x = 440    
                clyde_y = 438
                clyde_direction = 2

                blinky_clone_x = 50
                blinky_clone_y = 48
                blinky_clone_direction = 0

                inky_clone_x = 430
                inky_clone_y = 378
                inky_clone_direction = -2

                pinky_clone_x = 430
                pinky_clone_y = 438
                pinky_clone_direction = -2

                clyde_clone_x = 430  
                clyde_clone_y = 418
                clyde_clone_direction = -2

                eaten_ghost = [False, False, False, False, False, False, False, False]

                blinky_dead = False
                inky_dead = False
                pinky_dead = False
                clyde_dead = False
                blinky_clone_dead = False
                inky_clone_dead = False
                pinky_clone_dead = False                
                clyde_clone_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0

    if powerup and player_circle.colliderect(clyde.rect) and eaten_ghost[4] and not blinky_clone.dead:
        if lives > 0:
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0

                # Initial player position
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0

                # Intial ghost positions
                blinky_x = 54
                blinky_y = 58
                blinky_direction = 0

                inky_x = 440
                inky_y = 388
                inky_direction = 2

                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2

                clyde_x = 440    
                clyde_y = 438
                clyde_direction = 2

                blinky_clone_x = 50
                blinky_clone_y = 48
                blinky_clone_direction = 0

                inky_clone_x = 430
                inky_clone_y = 378
                inky_clone_direction = -2

                pinky_clone_x = 430
                pinky_clone_y = 438
                pinky_clone_direction = -2

                clyde_clone_x = 430  
                clyde_clone_y = 418
                clyde_clone_direction = -2

                eaten_ghost = [False, False, False, False, False, False, False, False]

                blinky_dead = False
                inky_dead = False
                pinky_dead = False
                clyde_dead = False
                blinky_clone_dead = False
                inky_clone_dead = False
                pinky_clone_dead = False                
                clyde_clone_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0

    if powerup and player_circle.colliderect(clyde.rect) and eaten_ghost[5] and not inky_clone.dead:
        if lives > 0:
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0

                # Initial player position
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0

                # Intial ghost positions
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0

                inky_x = 440
                inky_y = 388
                inky_direction = 2

                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2

                clyde_x = 440    
                clyde_y = 438
                clyde_direction = 2

                blinky_clone_x = 50
                blinky_clone_y = 48
                blinky_clone_direction = 0

                inky_clone_x = 430
                inky_clone_y = 378
                inky_clone_direction = -2

                pinky_clone_x = 430
                pinky_clone_y = 438
                pinky_clone_direction = -2

                clyde_clone_x = 430  
                clyde_clone_y = 418
                clyde_clone_direction = -2

                eaten_ghost = [False, False, False, False, False, False, False, False]

                blinky_dead = False
                inky_dead = False
                pinky_dead = False
                clyde_dead = False
                blinky_clone_dead = False
                inky_clone_dead = False
                pinky_clone_dead = False                
                clyde_clone_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0

    if powerup and player_circle.colliderect(clyde.rect) and eaten_ghost[6] and not pinky_clone.dead:
        if lives > 0:
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0

                # Initial player position
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0

                # Intial ghost positions
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0

                inky_x = 440
                inky_y = 388
                inky_direction = 2

                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2

                clyde_x = 440    
                clyde_y = 438
                clyde_direction = 2

                blinky_clone_x = 50
                blinky_clone_y = 48
                blinky_clone_direction = 0

                inky_clone_x = 430
                inky_clone_y = 378
                inky_clone_direction = -2

                pinky_clone_x = 430
                pinky_clone_y = 438
                pinky_clone_direction = -2

                clyde_clone_x = 430  
                clyde_clone_y = 418
                clyde_clone_direction = -2

                eaten_ghost = [False, False, False, False, False, False, False, False]

                blinky_dead = False
                inky_dead = False
                pinky_dead = False
                clyde_dead = False
                blinky_clone_dead = False
                inky_clone_dead = False
                pinky_clone_dead = False                
                clyde_clone_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0

    if powerup and player_circle.colliderect(clyde.rect) and eaten_ghost[7] and not clyde_clone.dead:
        if lives > 0:
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0

                # Initial player position
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0

                # Intial ghost positions
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0

                inky_x = 440
                inky_y = 388
                inky_direction = 2

                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2

                clyde_x = 440    
                clyde_y = 438
                clyde_direction = 2

                blinky_clone_x = 50
                blinky_clone_y = 48
                blinky_clone_direction = 0

                inky_clone_x = 430
                inky_clone_y = 378
                inky_clone_direction = -2

                pinky_clone_x = 430
                pinky_clone_y = 438
                pinky_clone_direction = -2

                clyde_clone_x = 430  
                clyde_clone_y = 418
                clyde_clone_direction = -2

                eaten_ghost = [False, False, False, False, False, False, False, False]

                blinky_dead = False
                inky_dead = False
                pinky_dead = False
                clyde_dead = False
                blinky_clone_dead = False
                inky_clone_dead = False
                pinky_clone_dead = False                
                clyde_clone_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0

    if powerup and player_circle.colliderect(blinky.rect) and not blinky.dead and not eaten_ghost[0]:
        blinky_dead = True
        eaten_ghost[0] = True
        score += (2 ** eaten_ghost.count(True)) * 100

    if powerup and player_circle.colliderect(inky.rect) and not inky.dead and not eaten_ghost[1]:
        inky_dead = True
        eaten_ghost[1] = True
        score += (2 ** eaten_ghost.count(True)) * 100

    if powerup and player_circle.colliderect(pinky.rect) and not pinky.dead and not eaten_ghost[2]:
        pinky_dead = True
        eaten_ghost[2] = True
        score += (2 ** eaten_ghost.count(True)) * 100

    if powerup and player_circle.colliderect(clyde.rect) and not clyde.dead and not eaten_ghost[3]:
        clyde_dead = True
        eaten_ghost[3] = True
        score += (2 ** eaten_ghost.count(True)) * 100

    if powerup and player_circle.colliderect(blinky_clone.rect) and not blinky_clone.dead and not eaten_ghost[4]:
        blinky_clone_dead = True
        eaten_ghost[4] = True
        score += (2 ** eaten_ghost.count(True)) * 100

    if powerup and player_circle.colliderect(inky_clone.rect) and not inky_clone.dead and not eaten_ghost[5]:
        inky_clone_dead = True
        eaten_ghost[5] = True
        score += (2 ** eaten_ghost.count(True)) * 100

    if powerup and player_circle.colliderect(pinky_clone.rect) and not pinky_clone.dead and not eaten_ghost[6]:
        pinky_clone_dead = True
        eaten_ghost[6] = True
        score += (2 ** eaten_ghost.count(True)) * 100

    if powerup and player_circle.colliderect(clyde_clone.rect) and not clyde_clone.dead and not eaten_ghost[7]:
        clyde_clone_dead = True
        eaten_ghost[7] = True
        score += (2 ** eaten_ghost.count(True)) * 100

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_over or game_won):
                lives -= 1
                startup_counter = 0
                powerup = False
                power_counter = 0

                # Initial player position
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0

                # Intial ghost positions
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0

                inky_x = 440
                inky_y = 388
                inky_direction = 2

                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2

                clyde_x = 440    
                clyde_y = 438
                clyde_direction = 2

                blinky_clone_x = 50
                blinky_clone_y = 48
                blinky_clone_direction = 0

                inky_clone_x = 430
                inky_clone_y = 378
                inky_clone_direction = -2

                pinky_clone_x = 430
                pinky_clone_y = 438
                pinky_clone_direction = -2

                clyde_clone_x = 430  
                clyde_clone_y = 418
                clyde_clone_direction = -2

                eaten_ghost = [False, False, False, False, False, False, False, False]

                blinky_dead = False
                inky_dead = False
                pinky_dead = False
                clyde_dead = False
                blinky_clone_dead = False
                inky_clone_dead = False
                pinky_clone_dead = False
                clyde_clone_dead = False 

                score = 0
                lives = 3
                level = copy.deepcopy(boards) 
                game_over = False
                game_won = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction
 
    for i in range(4):
        if direction_command == i and turns_allowed[i]:
            direction = i
    '''
    # Alternative way to set direction based on command and allowed turns
    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3
    '''
    
    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897

    if blinky.in_box and blinky_dead:
        blinky_dead = False
    if inky.in_box and inky_dead:
        inky_dead = False
    if pinky.in_box and pinky_dead:
        pinky_dead = False
    if clyde.in_box and clyde_dead:
        clyde_dead = False
    if blinky_clone.in_box and blinky_clone_dead:
        blinky_clone_dead = False
    if inky_clone.in_box and inky_clone_dead:
        inky_clone_dead = False
    if pinky_clone.in_box and pinky_clone_dead:
        pinky_clone_dead = False
    if clyde_clone.in_box and clyde_clone_dead:
        clyde_clone_dead = False
        
    pygame.display.flip()

pygame.quit()