import pygame
import sys
import random
import math

pygame.init()


LARGURA = 900
ALTURA = 600
FPS = 60


TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Penalti")
RELOGIO = pygame.time.Clock()

