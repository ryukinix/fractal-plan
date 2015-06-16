#coding=utf-8
from __future__ import division
"""

Animation: bugado pra caralho, não funciona nem a pau com python2, somente no bug—indows. 
Ask-answer: parece que o problema se refere ao division delicion, vou importar do futuro então
Commit: CARALHO!!! ERA ESSA PORRA! DIVISÃO FUDIDA

Python2:

>>>1/3
1
>>>1//3
1
>>>1.0/3
0.3333333

Python3:
>>>1/3
0.333333
>>>1/3
1
>>>1.0/3


Corrigi com o futuro ! kkkk ai q delicia
Em python podemos sim ir pro futuro!


"""

import pygame, os, sys
from pygame.locals import *
from math import *
from random import randint as random
from random import choice
from getpass import getuser as usr

def treeGenerator(path, lista = []):
	files = os.listdir(path)
	for f in files:
		if os.path.isdir(f):
			os.chdir(f)
			newPath = path+ '/' + f
			treeGenerator(newPath, lista)
			os.chdir('..')
		else:
			lista.append(path +'/' + f)	
	return lista



#Colors  #R    #G   #B
WHITE = (255, 255, 255)
GREEN = (0,   255,   0)
BLUE =  (0,     0, 255)
BLACK = (0,     0,   0)
RED =   (255,   0,   0)

pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size, FULLSCREEN)
pygame.display.set_caption("Animation")

pygame.mouse.set_visible(False)


#Sound
musics = treeGenerator('/home/%s/Música' %usr())

done = False
 
# Usado para gerenciar o quão rápido a tela é atualizada
clock = pygame.time.Clock()



#Numeros de pontos na espiral
n = 50
dn = 10
maxRadius = 450

#Determine a configuração inicial da espiral
angleChange = random(90, 180)

#Cores da espiral
redValue = random(0, 255)
greenValue = random(0, 255)
blueValue  = random(0, 255)



def notNull(a, b):
	x = random(a, b)
	if x != 0:
		return x
	return notNull(a, b)

#Como as cores irão variar
dRed = notNull(-2, 2)
dGreen = notNull(-2, 2)
dBlue = notNull(-2, 2)

def musicPath(path):
		inverse = path[::-1]
		index = inverse.find('/')
		music = inverse[:index]
		path = inverse[index:]
		return music[::-1], path[::-1]
def fib(n):
	cont = 0
	a, b = 0, 1
	while n > cont:
		a, b = b, a + b
		cont += 1
	return b
def anglePolyg(n):
	if n < 3:
		n = 3
	return ((n-2)*180)/n


pause = False
dx, dy = 0, 0
# -------- Main Program Loop -----------
while not done:
	# --- Evento do laço (loop) principal
	for event in pygame.event.get(): # User did something
		if event.type == QUIT: # If user clicked close
			done = True # Flag that we are done so we exit this loop
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				done = True
			elif event.key == K_RETURN:
				if pause == False:
					positionMusic = float(pygame.mixer.music.get_pos()/1000)
					pygame.mixer.music.pause()
					
				else:
					pygame.mixer.music.play(0, positionMusic)
				pause = ~pause
			elif event.key == K_TAB:
				pygame.mixer.music.stop()
				pause = False


			elif event.key == K_BACKSPACE:
				if n < 180 or n > 360:
					dn = -dn
				n += int(sin((n - 180) * 3.14/180)*5)



			elif event.key == K_UP:
				dy -= 5
			elif event.key == K_LEFT:
				dx -= 5
			elif event.key == K_DOWN:
				dy += 5
			elif event.key == K_RIGHT:
				dx += 5
				
	#Play if not busy
	if not pygame.mixer.music.get_busy() and pause == False:
		try:
			music = choice(musics)
			music, path = musicPath(music)
			os.chdir(path)
			pygame.mixer.music.load(music)
			pygame.mixer.music.play(0, 0.0)
		except pygame.error:
			continue

	# --- A lógica do jogo pode vir aqui
 
	# --- O código para desenhar pode vir aqui
 
	# Primeiro, limpa a tela e pinta ela de branco. Não coloque nenhum
	# comando de desenho antes disso, porque serão apagados com esse
	# comando
	screen.fill(BLACK)



	lastX, lastY = WIDTH // 2, HEIGHT // 2 
	

	for i in range(n):
		theta = float(angleChange * i)
		radius = float(maxRadius * sqrt(i / n))
		x = int(WIDTH // 2 + radius*cos(theta))
		y = int(HEIGHT // 2 + radius*sin(theta))
		
		color = (redValue, greenValue, blueValue)
		lastPosition = (lastX + dx, lastY - dy)
		position = (x - dx, y + dy)

		pygame.draw.line(screen, color, lastPosition, position)
		pygame.draw.line(screen, color, position, lastPosition)
		
		lastX = x
		lastY = y

	

	
	lastX, lastY = WIDTH * 7 // 8, HEIGHT * 9 // 11
	color = (blueValue, redValue, greenValue)
	radius = 30
	for h in range(3, 25):
		for i in range(h + 1):
			angle = abs(anglePolyg(h) - 180) * i *(angleChange ** 1.8)
			xc = WIDTH * 7 // 8 + radius * cos(angle * pi / 180)
			yc = HEIGHT * 9 // 11 + radius * sin(angle * pi / 180)

			pos = xc + dx, yc - dy
			lastPos = lastX -dx , lastY + dy
			if i > 0:
				pygame.draw.line(screen, color, pos, lastPos)
			
			lastX = xc 
			lastY = yc
			
		radius += 5 


	#Se as cores estão fora do escopo[0,255], mude o sentido dos acréscimo
	if redValue + dRed < 0 or redValue + dRed > 255:
		dRed = -dRed
	if greenValue + dGreen < 0 or greenValue + dGreen > 255:
		dGreen = -dGreen
	if blueValue + dBlue < 0 or blueValue + dBlue > 255:
		dBlue = -dBlue

	#I3 // 4ncremento de cores
	redValue += dRed
	greenValue += dGreen
	blueValue += dBlue

	angleChange += 0.0001

	
	# --- seguir em frente e atualizando a tela com o que foi desenhado
	pygame.display.flip()
	# --- Limita para 60 frames por segundo
	clock.tick(60)

pygame.quit()

