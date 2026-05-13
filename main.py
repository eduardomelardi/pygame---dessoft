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

goleiros_jogo = [
    pygame.transform.scale(pygame.image.load("assets/GoleiroDuda.png").convert_alpha(), (100, 140)),
    pygame.transform.scale(pygame.image.load("assets/GoleiroLucas.png").convert_alpha(), (100, 140)),
    pygame.transform.scale(pygame.image.load("assets/GoleiroDudu.png").convert_alpha(), (100, 140)),
]


estado = "inicio"
tempo_inicio = pygame.time.get_ticks()

personagem_escolhido = None

BOLA_INICIO_X = 415
BOLA_INICIO_Y = 552
GOLEIRO_INICIO_X = 400
GOLEIRO_INICIO_Y = 310

goleiro_x = float(GOLEIRO_INICIO_X)
goleiro_y = float(GOLEIRO_INICIO_Y)
VELOCIDADE_GOLEIRO = 5

bola_x = float(BOLA_INICIO_X)
bola_y = float(BOLA_INICIO_Y)
bola_destino_x = float(BOLA_INICIO_X)
bola_destino_y = float(BOLA_INICIO_Y)
bola_movendo = False
velocidade_bola = 9
tempo_reset = None
tempo_gol = None
tempo_reposicionar = None
GOL_RECT = pygame.Rect(150, 150, 600, 300)


DESTINOS_BOLA = [
    (200, 170), (350, 160), (500, 160), (620, 170), (700, 180),  # alto
    (180, 270), (320, 260), (450, 250), (570, 260), (700, 270),  # meio
    (200, 370), (350, 360), (450, 350), (560, 360), (680, 370),  # baixo
]

contador_inicio = 0

# Botoes dos personagens
botao1 = pygame.Rect(130, 250, 160, 160)
botao2 = pygame.Rect(370, 250, 160, 160)
botao3 = pygame.Rect(610, 250, 160, 160)


def escrever(texto, fonte, cor, x, y):
    imagem_texto = fonte.render(texto, True, cor)
    retangulo = imagem_texto.get_rect(center=(x, y))
    TELA.blit(imagem_texto, retangulo)


def desenhar_inicio():
    TELA.blit(fundo_inicio, (0, 0))
    escrever("Bem vindo!", FONTE_GRANDE, BRANCO, LARGURA // 2, ALTURA // 2)


def desenhar_escolha_personagem():
    TELA.blit(fundo_inicio, (0, 0))
    escrever("Escolha seu goleiro", FONTE_MEDIA, BRANCO, LARGURA // 2, 100)

    pygame.draw.rect(TELA, AZUL, botao1, border_radius=20)
    pygame.draw.rect(TELA, VERDE, botao2, border_radius=20)
    pygame.draw.rect(TELA, VERMELHO, botao3, border_radius=20)

    TELA.blit(goleiros[0], (botao1.x + 10, botao1.y + 10))
    TELA.blit(goleiros[1], (botao2.x + 10, botao2.y + 10))
    TELA.blit(goleiros[2], (botao3.x + 10, botao3.y + 10))

    escrever("Eduardo Sanches", FONTE_PEQUENA, BRANCO, botao1.centerx, botao1.top - 20)
    escrever("Lucas Santana", FONTE_PEQUENA, BRANCO, botao2.centerx, botao2.top - 20)
    escrever("Eduardo Melardi", FONTE_PEQUENA, BRANCO, botao3.centerx, botao3.top - 20)

    escrever("Clique em uma das opções", FONTE_PEQUENA, PRETO, LARGURA // 2, 480)

def desenhar_countdown():
    TELA.fill(BRANCO)

    tempo_atual = pygame.time.get_ticks()
    tempo_passado = (tempo_atual - contador_inicio) // 1000
    numero = 3 - tempo_passado

    if numero > 0:
        escrever(str(numero), FONTE_GRANDE, PRETO, LARGURA // 2, ALTURA // 2)
    else:
        escrever("Vai!", FONTE_GRANDE, PRETO, LARGURA // 2, ALTURA // 2)


def iniciar_goleiro():
    global goleiro_x, goleiro_y
    goleiro_x = float(GOLEIRO_INICIO_X)
    goleiro_y = float(GOLEIRO_INICIO_Y)


def atualizar_goleiro():
    global goleiro_x, goleiro_y
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        goleiro_x = max(0, goleiro_x - VELOCIDADE_GOLEIRO)
    if teclas[pygame.K_RIGHT]:
        goleiro_x = min(LARGURA - 150, goleiro_x + VELOCIDADE_GOLEIRO)
    if teclas[pygame.K_UP]:
        goleiro_y = max(200, goleiro_y - VELOCIDADE_GOLEIRO)
    if teclas[pygame.K_DOWN]:
        goleiro_y = min(GOLEIRO_INICIO_Y + 80, goleiro_y + VELOCIDADE_GOLEIRO)


def desenhar_countdown():
    TELA.fill(BRANCO)

    tempo_atual = pygame.time.get_ticks()
    tempo_passado = (tempo_atual - contador_inicio) // 1000
    numero = 3 - tempo_passado

    if numero > 0:
        escrever(str(numero), FONTE_GRANDE, PRETO, LARGURA // 2, ALTURA // 2)
    else:
        escrever("Vai!", FONTE_GRANDE, PRETO, LARGURA // 2, ALTURA // 2)


def iniciar_goleiro():
    global goleiro_x, goleiro_y
    goleiro_x = float(GOLEIRO_INICIO_X)
    goleiro_y = float(GOLEIRO_INICIO_Y)


def atualizar_goleiro():
    global goleiro_x, goleiro_y
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        goleiro_x = max(0, goleiro_x - VELOCIDADE_GOLEIRO)
    if teclas[pygame.K_RIGHT]:
        goleiro_x = min(LARGURA - 150, goleiro_x + VELOCIDADE_GOLEIRO)
    if teclas[pygame.K_UP]:
        goleiro_y = max(200, goleiro_y - VELOCIDADE_GOLEIRO)
    if teclas[pygame.K_DOWN]:
        goleiro_y = min(GOLEIRO_INICIO_Y + 80, goleiro_y + VELOCIDADE_GOLEIRO)


def sortear_chute():
    global bola_destino_x, bola_destino_y, bola_movendo, tempo_reset
    destino = random.choice(DESTINOS_BOLA)
    bola_destino_x = float(destino[0])
    bola_destino_y = float(destino[1])
    bola_movendo = True
    tempo_reset = None


def desenhar_jogo():
    TELA.blit(campo, (0, 0))
    if personagem_escolhido is not None:
        goleiro_img = goleiros_jogo[personagem_escolhido - 1]
        TELA.blit(goleiro_img, (int(goleiro_x), int(goleiro_y)))
    TELA.blit(bola_img, (int(bola_x), int(bola_y)))
    escrever("Use as setas para mover o goleiro", FONTE_PEQUENA, BRANCO, LARGURA // 2, 40)
    if tempo_gol:
        escrever("Gooolll!", FONTE_GOL, VERMELHO, LARGURA // 2, ALTURA // 2)
