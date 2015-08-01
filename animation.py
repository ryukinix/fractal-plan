# !/usr/bin/env python2
#  -*- coding: utf-8  -*-

from __future__ import division, print_function
import pygame
from pygame.locals import *
from math import sqrt, cos, sin, pi
from random import randint as random
from random import choice
from os import chdir, listdir
from os.path import join, isdir, isfile, expanduser
from mimetypes import guess_type


def tree_generator(path, files=[]):
    files_list = listdir(path)
    for f in files_list:
        new_file = join(path, f)
        if isdir(new_file):
            new_path = join(path, f)
            chdir(new_path)
            tree_generator(new_path, files)
            chdir('..')
        elif isfile(f):
            mime = guess_type(f)[0]
            if mime is not None and 'audio' in mime:
                files.append(new_file)
        if len(files) > 1000:
            break
    return files


def notNull(a, b):
    x = random(a, b)
    if x != 0:
        return x
    return notNull(a, b)


def fib(n_vertex):
    cont = 0
    a, b = 0, 1
    while n_vertex > cont:
        a, b = b, a + b
        cont += 1
    return b


def angle_polyg(n_vertex):
    if n_vertex < 3:
        n_vertex = 3
    return ((n_vertex - 2) * 180) / n_vertex


# Colors  +R    +G   +B
WHITE = (255, 255, 255)
GREEN = (0,   255,   0)
BLUE = (0,     0, 255)
BLACK = (0,     0,   0)
RED = (255,   0,   0)

pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = int(info.current_w // 1.2), int(info.current_h // 1.2)
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Animation")

pygame.mouse.set_visible(False)
done = False

clock = pygame.time.Clock()

# Numbers of vertexes on the spiral
n_vertex = 50
dn = 10
max_radius = WIDTH // 4

# Determine the configuration of initial spiral
angle_change = random(90, 180)

# Colors of spiral
red_value = random(0, 255)
green_value = random(0, 255)
blue_value = random(0, 255)

# How the colors will are change
d_red = notNull(-2, 2)
d_green = notNull(-2, 2)
d_blue = notNull(-2, 2)

# Sound
musics = tree_generator('%s' % expanduser("~/"))
pause = False
dx, dy = 0, 0
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True
            elif event.key == K_RETURN:
                if pause is False:
                    position_music = float(pygame.mixer.music.get_pos() / 1000)
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.play(0, position_music)
                pause = ~pause
            elif event.key == K_TAB:
                pygame.mixer.music.stop()
                pause = False
            elif event.key == K_BACKSPACE:
                if n_vertex < 180 or n_vertex > 360:
                    dn = -dn
                n_vertex += int(sin((n_vertex - 180) * 3.14 / 180) * 5)
            elif event.key == K_UP:
                dy -= 5
            elif event.key == K_LEFT:
                dx -= 5
            elif event.key == K_DOWN:
                dy += 5
            elif event.key == K_RIGHT:
                dx += 5
            elif event.key == K_EQUALS:
                print("[operation]+n_vertex: %d" % n_vertex)
                n_vertex += 1
            elif event.key == K_MINUS:
                print("[operation]-n_vertex: %d" % n_vertex)
                n_vertex -= 1

    # Play if not busy
    if not pygame.mixer.music.get_busy() and pause is False:
        try:
            music = choice(musics)
            pygame.mixer.music.load(music)
            pygame.mixer.music.play(0, 0.0)
            print("[operation]Loading: %s" % music)
        except pygame.error:
            print("[error]Not possible to load this file: %s" % music)
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

    # the second graph
    lastX, lastY = WIDTH * 7 // 8, HEIGHT * 9 // 11
    color = (blue_value, red_value, green_value)
    radius = 50
    for h in range(3, n_vertex // 3):
        for i in range(h + 1):
            angle = abs(angle_polyg(h) - 180) * i * (angle_change ** 1.8)
            xc = WIDTH * 7 // 8 + radius * cos(angle * pi / 180)
            yc = HEIGHT * 9 // 11 + radius * sin(angle * pi / 180)

            pos = xc + dx, yc - dy
            last_position = lastX - dx, lastY + dy

            if i > 0:
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
