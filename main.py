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

campo = pygame.image.load("assets/campo.png").convert()
campo = pygame.transform.scale(campo, (LARGURA, ALTURA))

fundo_inicio = pygame.image.load("assets/Fundoprimeiratela.png").convert()
fundo_inicio = pygame.transform.scale(fundo_inicio, (LARGURA, ALTURA))

bola_img = pygame.image.load("assets/bolanova.png").convert_alpha()
bola_img = pygame.transform.scale(bola_img, (70, 47))

goleiros = [
    pygame.transform.scale(pygame.image.load("assets/GoleiroDuda.png").convert_alpha(), (140, 140)),
    pygame.transform.scale(pygame.image.load("assets/GoleiroLucas.png").convert_alpha(), (140, 140)),
    pygame.transform.scale(pygame.image.load("assets/GoleiroDudu.png").convert_alpha(), (140, 140)),
]


