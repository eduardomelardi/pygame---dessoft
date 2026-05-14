import pygame
import sys
import random
import math

pygame.init()

pygame.mixer.music.load("assets/McBilly-mc-guime-original-mc-guime-pais-do-futebol-part-emicida-2014-c27bdb_[cut_181sec].mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

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
VELOCIDADE_GOLEIRO = 6.5

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

gols = 0
defesas = 0
chutes_total = 0
tempo_fim = None

fase_atual = 1

# Fase 1: centro do gol, bem acessivel
DESTINOS_BOLA = [
    (350, 210), (450, 210), (550, 210),  # alto centro
    (320, 280), (450, 270), (580, 280),  # meio
    (350, 360), (450, 350), (550, 360),  # baixo centro
]

# Fase 2: destinos variados (era a fase 1 antes)
DESTINOS_FASE2 = [
    (200, 190), (350, 180), (500, 180), (620, 190), (700, 200),
    (180, 270), (320, 260), (450, 250), (570, 260), (700, 270),
    (200, 370), (350, 360), (450, 350), (560, 360), (680, 370),
]

# Fase 3: cantos e extremos (era a fase 2 antes)
DESTINOS_FASE3 = [
    (230, 185), (650, 185), (230, 185), (650, 185), (450, 180),
    (230, 270), (660, 270), (230, 270), (660, 270), (450, 250),
    (230, 375), (650, 375), (230, 375), (650, 375), (450, 350),
]

VELOCIDADE_POR_FASE = {1: 6, 2: 9, 3: 13}

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


def desenhar_instrucoes():
    TELA.blit(fundo_inicio, (0, 0))
    overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    TELA.blit(overlay, (0, 0))

    escrever("Como Jogar", FONTE_MEDIA, BRANCO, LARGURA // 2, 45)

    # Caixa esquerda - Controles
    pygame.draw.rect(TELA, (20, 20, 20, 200), pygame.Rect(30, 80, 390, 430), border_radius=12)
    pygame.draw.rect(TELA, AZUL, pygame.Rect(30, 80, 390, 430), 2, border_radius=12)
    escrever("Controles do Goleiro", FONTE_PEQUENA, AZUL, 225, 110)
    linhas_controles = [
        "Use as setas do teclado",
        "para mover o goleiro:",
        "",
        "  Seta Esquerda  ->  mover esquerda",
        "  Seta Direita   ->  mover direita",
        "  Seta Cima      ->  subir",
        "  Seta Baixo     ->  abaixar",
        "",
        "Tente interceptar a bola",
        "antes que ela entre no gol!",
    ]
    for i, linha in enumerate(linhas_controles):
        escrever(linha, FONTE_PEQUENA, BRANCO, 225, 150 + i * 32)

    # Caixa direita - Fases
    pygame.draw.rect(TELA, (20, 20, 20, 200), pygame.Rect(480, 80, 390, 430), border_radius=12)
    pygame.draw.rect(TELA, VERDE, pygame.Rect(480, 80, 390, 430), 2, border_radius=12)
    escrever("Fases do Jogo", FONTE_PEQUENA, VERDE, 675, 108)
    linhas_fases = [
        "O jogo tem 3 fases,",
        "5 chutes por fase.",
        "Defenda mais do que",
        "leve gols para avancar.",
        "",
        "Fase 1: bola normal",
        "Fase 2: bola mais rapida",
        "        e nos cantos",
        "Fase Final: bola muito",
        "        rapida, extremos",
    ]
    for i, linha in enumerate(linhas_fases):
        escrever(linha, FONTE_PEQUENA, BRANCO, 675, 140 + i * 34)

    escrever("Pressione ENTER para continuar", FONTE_PEQUENA, CINZA, LARGURA // 2, 540)


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


def sortear_chute():
    global bola_destino_x, bola_destino_y, bola_movendo, tempo_reset, velocidade_bola
    if fase_atual == 1:
        destino = random.choice(DESTINOS_BOLA)
    elif fase_atual == 2:
        destino = random.choice(DESTINOS_FASE2)
    else:
        destino = random.choice(DESTINOS_FASE3)
    velocidade_bola = VELOCIDADE_POR_FASE[fase_atual]
    bola_destino_x = float(destino[0])
    bola_destino_y = float(destino[1])
    bola_movendo = True
    tempo_reset = None



def nome_fase():
    if fase_atual == 1:
        return "Fase 1"
    elif fase_atual == 2:
        return "Fase 2"
    else:
        return "Fase Final"


def desenhar_jogo():
    TELA.blit(campo, (0, 0))
    # Caixa de fase no topo
    caixa = pygame.Rect(LARGURA // 2 - 80, 8, 160, 34)
    pygame.draw.rect(TELA, PRETO, caixa, border_radius=8)
    pygame.draw.rect(TELA, BRANCO, caixa, 2, border_radius=8)
    escrever(nome_fase(), FONTE_PEQUENA, BRANCO, LARGURA // 2, 25)
    if bola_movendo:
        sombra = bola_img.copy()
        sombra.set_alpha(100)
        TELA.blit(sombra, (int(bola_destino_x), int(bola_destino_y)))
    if personagem_escolhido is not None:
        goleiro_img = goleiros_jogo[personagem_escolhido - 1]
        TELA.blit(goleiro_img, (int(goleiro_x), int(goleiro_y)))
    TELA.blit(bola_img, (int(bola_x), int(bola_y)))
    escrever("Use as setas para mover o goleiro", FONTE_PEQUENA, BRANCO, LARGURA // 2, 55)
    escrever(f"Defesas: {defesas}  |  Gols: {gols}  |  Chute: {chutes_total}/5", FONTE_PEQUENA, BRANCO, LARGURA // 2, 125)
    if tempo_gol:
        escrever("Gooolll!", FONTE_GOL, VERMELHO, LARGURA // 2, ALTURA // 2)


def desenhar_fim_fase():
    TELA.blit(fundo_inicio, (0, 0))
    escrever(nome_fase(), FONTE_MEDIA, BRANCO, LARGURA // 2, 150)
    escrever(f"Defesas: {defesas}  |  Gols: {gols}", FONTE_MEDIA, BRANCO, LARGURA // 2, 220)
    if defesas > gols:
        if fase_atual < 3:
            escrever("Você avançou!", FONTE_GRANDE, VERDE, LARGURA // 2, ALTURA // 2 - 30)
            escrever("Pressione ENTER para a próxima fase", FONTE_PEQUENA, BRANCO, LARGURA // 2, 420)
        else:
            escrever("Você venceu o jogo!", FONTE_GRANDE, VERDE, LARGURA // 2, ALTURA // 2 - 30)
            escrever("Pressione ENTER para jogar novamente", FONTE_PEQUENA, BRANCO, LARGURA // 2, 420)
    else:
        escrever("Você perdeu!", FONTE_GRANDE, VERMELHO, LARGURA // 2, ALTURA // 2 - 30)
        escrever("Pressione ENTER para jogar novamente", FONTE_PEQUENA, BRANCO, LARGURA // 2, 420)


def desenhar_fim():
    TELA.blit(fundo_inicio, (0, 0))
    escrever(f"Defesas: {defesas}  |  Gols: {gols}", FONTE_MEDIA, BRANCO, LARGURA // 2, 200)
    escrever("Você venceu o jogo!", FONTE_GRANDE, VERDE, LARGURA // 2, ALTURA // 2)
    escrever("Pressione ENTER para jogar novamente", FONTE_PEQUENA, BRANCO, LARGURA // 2, 420)


def mover_bola():
    global bola_x, bola_y, bola_movendo, bola_destino_x, bola_destino_y, tempo_reset, tempo_gol, gols, defesas, chutes_total, estado, tempo_fim, fase_atual

    dx = bola_destino_x - bola_x
    dy = bola_destino_y - bola_y
    distancia = (dx**2 + dy**2) ** 0.5

    if distancia <= velocidade_bola:
        bola_x = bola_destino_x
        bola_y = bola_destino_y
        bola_movendo = False

        bola_cx = bola_destino_x + 35
        bola_cy = bola_destino_y + 23
        goleiro_rect = pygame.Rect(int(goleiro_x), int(goleiro_y), 100, 140)

        if goleiro_rect.collidepoint(int(bola_cx), int(bola_cy)):
            bola_destino_x = bola_x + (bola_cx - (goleiro_x + 50)) * 1.5
            bola_destino_y = float(BOLA_INICIO_Y)
            bola_movendo = True
        elif GOL_RECT.collidepoint(int(bola_destino_x), int(bola_destino_y)):
            gols += 1
            tempo_gol = pygame.time.get_ticks()
        else:
            defesas += 1
            tempo_reset = pygame.time.get_ticks()
        return

    bola_x += velocidade_bola * dx / distancia
    bola_y += velocidade_bola * dy / distancia


def resetar_bola():
    global bola_x, bola_y, bola_destino_x, bola_destino_y, bola_movendo, tempo_reset, tempo_gol, tempo_reposicionar, chutes_total, estado, tempo_fim, fase_atual
    bola_x = float(BOLA_INICIO_X)
    bola_y = float(BOLA_INICIO_Y)
    bola_destino_x = float(BOLA_INICIO_X)
    bola_destino_y = float(BOLA_INICIO_Y)
    bola_movendo = False
    tempo_reset = None
    tempo_gol = None
    chutes_total += 1
    if chutes_total >= 5:
        estado = "fim_fase"
        tempo_fim = pygame.time.get_ticks()
    else:
        tempo_reposicionar = pygame.time.get_ticks()



rodando = True
while rodando:
    RELOGIO.tick(FPS)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN and estado == "instrucoes":
                estado = "escolha"
            if evento.key == pygame.K_ESCAPE:
                if estado == "instrucoes":
                    estado = "inicio"
                    tempo_inicio = pygame.time.get_ticks()
                elif estado == "escolha":
                    estado = "instrucoes"
                elif estado == "countdown":
                    estado = "escolha"
                elif estado == "jogo":
                    estado = "escolha"
            if evento.key == pygame.K_RETURN and estado == "fim_fase":
                if defesas > gols and fase_atual < 3:
                    fase_atual += 1
                    gols = 0
                    defesas = 0
                    chutes_total = 0
                    tempo_fim = None
                    estado = "countdown"
                    contador_inicio = pygame.time.get_ticks()
                    iniciar_goleiro()
                else:
                    # Perdeu ou completou fase 3 -> reinicia tudo
                    fase_atual = 1
                    gols = 0
                    defesas = 0
                    chutes_total = 0
                    tempo_fim = None
                    personagem_escolhido = None
                    estado = "escolha"
            if evento.key == pygame.K_RETURN and estado == "fim":
                fase_atual = 1
                gols = 0
                defesas = 0
                chutes_total = 0
                tempo_fim = None
                personagem_escolhido = None
                estado = "escolha"

        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()

            if estado == "escolha":
                if botao1.collidepoint(mouse):
                    personagem_escolhido = 1
                    estado = "countdown"
                    contador_inicio = pygame.time.get_ticks()

                elif botao2.collidepoint(mouse):
                    personagem_escolhido = 2
                    estado = "countdown"
                    contador_inicio = pygame.time.get_ticks()

                elif botao3.collidepoint(mouse):
                    personagem_escolhido = 3
                    estado = "countdown"
                    contador_inicio = pygame.time.get_ticks()

            elif estado == "jogo":
                pass

   
    if estado == "inicio":
        desenhar_inicio()
        if pygame.time.get_ticks() - tempo_inicio >= 3000:
            estado = "instrucoes"

    elif estado == "instrucoes":
        desenhar_instrucoes()

    elif estado == "escolha":
        desenhar_escolha_personagem()

    elif estado == "countdown":
        desenhar_countdown()
        if pygame.time.get_ticks() - contador_inicio >= 4000:
            estado = "jogo"
            iniciar_goleiro()
            tempo_reposicionar = pygame.time.get_ticks()

    elif estado == "jogo":
        atualizar_goleiro()
        if bola_movendo and not tempo_gol:
            mover_bola()
        if tempo_gol and pygame.time.get_ticks() - tempo_gol >= 1500:
            resetar_bola()
            iniciar_goleiro()
        if tempo_reset and pygame.time.get_ticks() - tempo_reset >= 2000:
            resetar_bola()
            iniciar_goleiro()
        if tempo_reposicionar and pygame.time.get_ticks() - tempo_reposicionar >= 1000:
            tempo_reposicionar = None
            sortear_chute()
        desenhar_jogo()

    elif estado == "fim_fase":
        desenhar_fim_fase()

    elif estado == "fim":
        desenhar_fim()

    pygame.display.update()

pygame.quit()
sys.exit()