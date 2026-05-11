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


BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (40, 90, 220)
VERDE = (40, 180, 90)
VERMELHO = (220, 60, 60)
CINZA = (220, 220, 220)

FONTE_GRANDE = pygame.font.SysFont(None, 80)
FONTE_MEDIA = pygame.font.SysFont(None, 50)
FONTE_PEQUENA = pygame.font.SysFont(None, 32)
FONTE_GOL = pygame.font.SysFont(None, 130)




