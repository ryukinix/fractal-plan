#!/usr/bin/env python3
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_RETURN, \
    K_TAB, K_BACKSPACE, K_UP, K_LEFT, K_DOWN, K_RIGHT, K_EQUALS, K_MINUS
from math import sqrt, cos, sin, pi, tan
from random import randint
from random import shuffle
from os import listdir
from os.path import join, isdir, isfile, expanduser
from mimetypes import guess_type
from argparse import ArgumentParser

home = expanduser('~/')
default_path = [''] + [
    join(home, x) for x in listdir(home) if x.lower() in ('música', 'music')
]
parser = ArgumentParser()
parser.add_argument(
    '-m', '--music-dir',
    dest='music_path',
    default=default_path.pop(),
    help="The path to search musics",
    type=str
)
parser.add_argument(
    '-n', '--no-music',
    dest='music',
    default=True,
    help='Disable music play and search',
    action='store_false'
)


def music_generator(path):
    files_list = listdir(path)
    shuffle(files_list)
    for f in files_list:
        new_file = join(path, f)
        if isfile(new_file):
            mime = guess_type(f)[0]
            if mime is not None and 'audio' in mime:
                yield new_file
        elif isdir(new_file):
            yield from music_generator(join(path, f))


def not_null(a, b):
    x = randint(a, b)
    return x if x != 0 else not_null(a, b)


def angle_polyg(n_vertex):
    if n_vertex < 3:
        n_vertex = 3
    return ((n_vertex - 2) * 180) / n_vertex


# Setup
pygame.init()
info = pygame.display.Info()
clock = pygame.time.Clock()
WIDTH, HEIGHT = int(info.current_w // 1.2), int(info.current_h // 1.2)
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Fractal-plan Exposition")
pygame.mouse.set_visible(False)

# Some colors
BLACK = (0, 0, 0)


# Numbers of vertexes on the spiral
n_vertex = 50
dn = 10
max_radius = WIDTH // 4

# Determine the configuration of initial spiral
angle_change = randint(90, 180)

# Colors of spiral
red_value = randint(0, 255)
green_value = randint(0, 255)
blue_value = randint(0, 255)

# How the colors will are change
d_red = not_null(-2, 2)
d_green = not_null(-2, 2)
d_blue = not_null(-2, 2)

# Sound
options = parser.parse_args()
pause = False
if not options.music:
    pause = True
else:
    musics = music_generator(options.music_path)

dx, dy = 0, 0

# -------- Main Program Loop -----------
done = False
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        if event.type == KEYDOWN:
            if options.music:
                if event.key == K_RETURN:
                    if pause is False:
                        unnormalized_position = pygame.mixer.music.get_pos()
                        position_music = float(unnormalized_position / 1000)
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.play(0, position_music)
                    pause = not pause
                elif event.key == K_TAB:
                    pygame.mixer.music.stop()
                    pause = False
            if event.key == K_ESCAPE:
                done = True
            elif event.key == K_BACKSPACE:
                if n_vertex < 180 or n_vertex > 360:
                    dn = -dn
                n_vertex += int(sin((n_vertex - 180) * pi / 180) * 5)
            elif event.key == K_UP:
                dy -= 5
            elif event.key == K_LEFT:
                dx -= 5
            elif event.key == K_DOWN:
                dy += 5
            elif event.key == K_RIGHT:
                dx += 5
            elif event.key == K_EQUALS:
                print("[operation]+n_vertex: {}".format(n_vertex))
                n_vertex += 1
            elif event.key == K_MINUS:
                print("[operation]-n_vertex: {}".format(n_vertex))
                n_vertex -= 1

    # Play if not busy
    if not pygame.mixer.music.get_busy() and pause is False:
        try:
            music = next(musics)
            pygame.mixer.music.load(music)
            pygame.mixer.music.play(-1, 0.0)
            print("[operation]Loaded: {!r}".format(music))
        except pygame.error:
            print("[error]Not possible to load this file: {!r}".format(music))
            continue

    screen.fill(BLACK)
    lastX, lastY = WIDTH // 2, HEIGHT // 2

    # the main graph
    for i in range(n_vertex):
        theta = float(angle_change * i)
        radius = float(max_radius * sqrt(i / n_vertex))
        x = int(WIDTH // 2 + radius * cos(theta))
        y = int(HEIGHT // 2 + radius * sin(theta))

        color = (red_value, green_value, blue_value)
        last_position = (lastX + dx, lastY - dy)
        position = (x - dx, y + dy)

        pygame.draw.line(screen, color, last_position, position)
        pygame.draw.line(screen, color, position, last_position)

        lastX = x
        lastY = y

    # the secondoray graphs
    weights = [(1 / 8, 9 / 11), (7 / 8, 9 / 11),
               (1 / 8, 2 / 11), (7 / 8, 2 / 11)]
    for w_x, w_y in weights:
        lastX, lastY = WIDTH * w_x, HEIGHT * w_y
        color = (blue_value, red_value, green_value)
        radius = 50
        for h in range(3, n_vertex // 3):
            angle_p = angle_polyg(h)
            for i in range(1, h + 1):
                angle = abs(angle_p - 180) * i * (angle_change ** 1.8)
                mad_factor = sum(map(abs, color))
                xc = (WIDTH * w_x + radius * cos(angle * pi / 180) +
                      2 * n_vertex * cos(mad_factor * pi / 180))
                yc = (HEIGHT * w_y + radius * sin(angle * pi / 180) +
                      2 * n_vertex * sin(mad_factor * pi / 180))

                pos = xc + dx, yc - dy
                last_position = lastX - dx, lastY + dy

                pygame.draw.line(screen, color, pos, last_position)

                lastX = xc
                lastY = yc

            radius += 5

    # Change sense if the colors are out of the range(0, 255)
    if red_value + d_red < 0 or red_value + d_red > 255:
        d_red = -d_red
    if green_value + d_green < 0 or green_value + d_green > 255:
        d_green = -d_green
    if blue_value + d_blue < 0 or blue_value + d_blue > 255:
        d_blue = -d_blue

    # Colors increment
    red_value += d_red
    green_value += d_green
    blue_value += d_blue

    angle_change += 0.0001

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
