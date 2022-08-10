import pygame
import os
import random
from PIL import Image
from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.font.init()
pygame.mixer.init()

icon = pygame.image.load("images/icon.png")

display_width = 40
display_height = 40
fps = 60

width_half = display_width / 2
height_half = display_height / 2

os.environ['SDL_VIDEO_CENTERED'] = "1"

pygame.display.set_icon(icon)
pygame.display.set_caption("Grass Battle")
gameDisplay = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()

the_font = "font/OpenSans-Regular.ttf"

def center_text(text, size, x, y, font, color):
    loading_text = pygame.font.Font(font, size)

    TextSurf, TextRect = text_objects(text, loading_text, color)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)

def left_text(text, size, x, y, font, color):
    loading_text = pygame.font.Font(font, size)

    TextSurf, TextRect = text_objects(text, loading_text, color)
    TextRect.midleft = (x, y)
    gameDisplay.blit(TextSurf, TextRect)

def right_text(text, size, x, y, font, color):
    loading_text = pygame.font.Font(font, size)

    TextSurf, TextRect = text_objects(text, loading_text, color)
    TextRect.midright = (x, y)
    gameDisplay.blit(TextSurf, TextRect)

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def display_image(image,x,y):
    gameDisplay.blit(image, (x,y))

def play_music(song, loop):
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loop)

def play_sound(sound):
    sound.play()

global screen_mode
screen_mode = 1

def screen_switch():
    global screen_mode
    if screen_mode == 1:
        gameDisplay = pygame.display.set_mode((display_width,display_height), pygame.FULLSCREEN)
        screen_mode = 2
    else:
        gameDisplay = pygame.display.set_mode((display_width,display_height))
        screen_mode = 1

def random_dirt():

    dtype = random.randint(0,976)

    if 0 <= dtype <= 973:
        return [117, 72, 49]
    elif dtype == 974:
        return [255, 255, 128]
    elif dtype == 975:
        return [127, 127, 127]
    elif dtype == 976:
        return [195, 195, 195]

def generate_dirt():
    baseImage = Image.new(mode="RGB", size=(display_width, display_height))

    for x in range(display_width):
        for y in range(display_height):
            rgb_list = random_dirt()
            baseImage.putpixel((x, y), (rgb_list[0], rgb_list[1], rgb_list[2], 255)) # add pixel to location

    baseImage.save("images/dirtbg.png")

def rand_loc(l1, l2, l3, l4, num):

    loc = []
    if num == 1:
        x = random.randint(2, display_width - 2)
        y = random.randint(2, display_height - 2)

        while x == l1[0]:
            x = random.randint(2, display_width - 2)

        while y == l1[0]:
            y = random.randint(2, display_height - 2)

        loc = [x, y]
        return loc
    elif num == 2:
        x = random.randint(2, display_width - 2)
        y = random.randint(2, display_height - 2)

        while x == l1[0] or x == l2[0]:
            x = random.randint(2, display_width - 2)

        while y == l1[0] or y == l2[0]:
            y = random.randint(2, display_height - 2)

        loc = [x, y]
        return loc
    elif num == 3:
        x = random.randint(2, display_width - 2)
        y = random.randint(2, display_height - 2)

        while x == l1[0] or x == l2[0] or x == l3[0]:
            x = random.randint(2, display_width - 2)

        while y == l1[0] or y == l2[0] or y == l3[0]:
            y = random.randint(2, display_height - 2)

        loc = [x, y]
        return loc

def get_u1(loc):

    n = random.randint(1, 20)
    if n <= 3:
        return [loc[0] - 1, loc[1] - 1]

def get_u2(loc):

    n = random.randint(1, 20)
    if n <= 3:
        return [loc[0] + 1, loc[1] - 1]

def get_u3(loc):

    n = random.randint(1, 20)
    if n <= 3:
        return [loc[0] - 1, loc[1]]

def get_l(loc):

    n = random.randint(1, 20)
    if n <= 3:
        return [loc[0] + 1, loc[1]]

def get_r(loc):

    n = random.randint(1, 20)
    if n <= 3:
        return [loc[0] - 1, loc[1] + 1]

def get_b1(loc):

    n = random.randint(1, 20)
    if n <= 3:
        return [loc[0] - 1, loc[1] + 1]

def get_b2(loc):

    n = random.randint(1, 20)
    if n <= 3:
        return [loc[0], loc[1] + 1]

def get_b3(loc):

    n = random.randint(1, 20)
    if n <= 3:
        return [loc[0] + 1, loc[1] + 1]

class Grass():
    def __init__(self):
        self.color = 0
        self.locations = []

    def remove(self, gl):
        for l in gl:
            self.locations = [z for z in self.locations if z != l]

    def update(self):
        newLs = []
        for i in self.locations:
            u1 = get_u1(i)
            if u1 != None and u1 not in self.locations:
                if u1[0] < display_width and u1[1] < display_height:
                    newLs.append(u1)

            u2 = get_u2(i)
            if u2 != None and u2 not in self.locations:
                if u2[0] < display_width and u2[1] < display_height:
                    newLs.append(u2)

            u3 = get_u3(i)
            if u3 != None and u3 not in self.locations:
                if u3[0] < display_width and u3[1] > 0 and u3[1] < display_height:
                    newLs.append(u3)

            left = get_l(i)
            if left != None and left not in self.locations:
                if left[0] < display_width and left[1] < display_height:
                    newLs.append(left)

            r = get_r(i)
            if r != None and r not in self.locations:
                if r[0] < display_width and r[1] < display_height:
                    newLs.append(r)

            b1 = get_b1(i)
            if b1 != None and b1 not in self.locations:
                if b1[0] > 0 and b1[0] < display_width and b1[1] < display_height:
                    newLs.append(b1)
            
            b2 = get_b2(i)
            if b2 != None and b2 not in self.locations:
                if b2[0] < display_width and b2[1] < display_height:
                    newLs.append(b2)
                
            b3 = get_b3(i)
            if b3 != None and b3 not in self.locations:
                if b3[0] < display_width and b3[1] < display_height:
                    newLs.append(b3)

        if newLs != None:
            for l in newLs:
                self.locations.append(l)

            weededList = []
            for loc in self.locations:
                if loc not in weededList:
                    weededList.append(loc)

            self.locations = weededList

        self.locations = [z for z in self.locations if z != None]
    
    def display(self):
        for i in self.locations:
            pygame.draw.rect(gameDisplay, self.color, (i[0], i[1], 1, 1))

global state
state = 1

grassRGB1 = [34, 177, 76]
grassRGB2 = [44, 193, 17]
grassRGB3 = [21, 255, 9]
grassRGB4 = [133, 231, 35]

def main():

    up = True

    cur_row = 0

    dirtbg = pygame.image.load("images/dirtbg.png")
    title = pygame.image.load("images/title.png")

    play_button = pygame.image.load("images/play_button.png")

    turn = 0
    g_up = 1
    state = 2

    g1 = Grass()
    g1.color = grassRGB1

    g2 = Grass()
    g2.color = grassRGB2

    g3 = Grass()
    g3.color = grassRGB3

    g4 = Grass()
    g4.color = grassRGB4

    time_counter = 0
    count_limit = 1

    while up:

        if state == 1:

            mouse_position = pygame.mouse.get_pos()

            play_button_area = width_half - 50 <= mouse_position[0] <= width_half + 50 and display_height-100 <= mouse_position[1] <= display_height - 50

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F4 or event.key == pygame.K_ESCAPE:
                        screen_switch()
                if event.type == pygame.MOUSEBUTTONUP:
                    if play_button_area:
                        state = 2

            gameDisplay.fill((0, 0, 0))
            display_image(dirtbg, 0, 0)
            display_image(title, width_half - 50, 0)
            display_image(play_button, width_half - 50, display_height-100)

            if cur_row == display_height - 1:
                cur_row = 0
            else:
                cur_row += 1

            pygame.display.update()
            clock.tick(fps)

        elif state == 2:

            mouse_position = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F4 or event.key == pygame.K_ESCAPE:
                        screen_switch()
                if event.type == pygame.MOUSEBUTTONUP:
                    if turn == 0:
                        g1.locations.append([mouse_position[0], mouse_position[1]])
                        g2.locations.append(rand_loc(g1.locations[0], None, None, None, 1))
                        g3.locations.append(rand_loc(g1.locations[0], g2.locations[0], None, None, 2))
                        g4.locations.append(rand_loc(g1.locations[0], g2.locations[0], g3.locations[0], None, 3))
                        turn = 1

            gameDisplay.fill((0, 0, 0))

            display_image(dirtbg, 0, 0)

            if turn >= 0:
                if time_counter == count_limit and g_up == 1:
                    g1.update()
                    g2.remove(g1.locations)
                    g3.remove(g1.locations)
                    g4.remove(g1.locations)
                    time_counter = 0
                    g_up += 1
                elif time_counter == count_limit and g_up == 2:
                    g2.update()
                    g1.remove(g2.locations)
                    g3.remove(g2.locations)
                    g4.remove(g2.locations)
                    time_counter = 0
                    g_up += 1
                elif time_counter == count_limit and g_up == 3:
                    g3.update()
                    g1.remove(g3.locations)
                    g2.remove(g3.locations)
                    g4.remove(g3.locations)
                    time_counter = 0
                    g_up += 1
                elif time_counter == count_limit and g_up == 4:
                    g4.update()
                    g1.remove(g4.locations)
                    g2.remove(g4.locations)
                    g3.remove(g4.locations)
                    time_counter = 0
                    g_up += 1
                    g_up = 1
                else:
                    time_counter += 1

                g1.display()
                g2.display()
                g3.display()
                g4.display()

            pygame.display.update()
            clock.tick(fps)

generate_dirt()
main()