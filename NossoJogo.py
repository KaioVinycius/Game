import pygame
import sys
import cv2
from pygame.locals import *

# Inicialização do Pygame
pygame.init()

# Tamanho da janela
LARGURA = 1024
ALTURA = 768
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Point Clicker Game")
clock = pygame.time.Clock()


# Função para tocar vídeo com OpenCV
def tocar_video(caminho_video, tela):
    cap = cv2.VideoCapture(caminho_video)

    if not cap.isOpened():
        print(f"Erro ao abrir o vídeo: {caminho_video}")
        return

    clock_video = pygame.time.Clock()

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Fim do vídeo

        # Converter o frame do OpenCV (BGR) para RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Redimensionar para caber na tela
        frame = cv2.resize(frame, (LARGURA, ALTURA))

        # Converter para superfície do Pygame
        surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        for event in pygame.event.get():
            if event.type == QUIT:
                cap.release()
                pygame.quit()
                sys.exit()

        tela.blit(surface, (0, 0))
        pygame.display.update()
        clock_video.tick(24)  # Ajuste conforme FPS desejado

    cap.release()

# Cores
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

# Fundo
fundo = pygame.image.load("IMG/IMAGEM DE FUNDO CERTA (1).png")
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

# Fonte
font = pygame.font.SysFont(None, 48)

# Estado do jogo
jogo_vencido = False
jogo_perdido = False

# Cronômetro
TEMPO_LIMITE = 60_000  # 60 segundos
tempo_inicial = pygame.time.get_ticks()


# Classe para representar cada ponto com imagem própria
class Alvo:
    def __init__(self, x, y, imagem):
        self.imagem = imagem
        self.rect = self.imagem.get_rect(center=(x, y))

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)

    def colidiu(self, pos):
        return self.rect.collidepoint(pos)


# Lista de imagens diferentes para os pontos
nomes_imagens = [
    "IMG/Anel.png",
    "IMG/Balão.png",
    "IMG/Cachecol.png",
    "IMG/Cachorro.png",
    "IMG/Chapéu.png",
    "IMG/Colar.png",
    "IMG/Olho de Orus.png"
]

imagens = [pygame.image.load(nome) for nome in nomes_imagens]

# Coordenadas fixas para os alvos
posicoes_fixas = [
    (310, 650),
    (1000, 25),
    (30 , 700),
    (675, 768),
    (945, 235),
    (415, 400),
    (610, 660)
]

# Criar os alvos com posições fixas e imagens
pontos = []
for i in range(min(len(imagens), len(posicoes_fixas))):
    x, y = posicoes_fixas[i]
    pontos.append(Alvo(x, y, imagens[i]))

tocar_video("Video/cutscenefase1.mp4", screen)
# Loop principal
while True:
    tempo_passado = pygame.time.get_ticks() - tempo_inicial
    tempo_restante = max(0, TEMPO_LIMITE - tempo_passado)

    screen.blit(fundo, (0, 0))  # Aplica imagem de fundo

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not jogo_vencido and not jogo_perdido and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for alvo in pontos[:]:
                if alvo.colidiu(mouse_pos):
                    pontos.remove(alvo)

    # Condições de vitória/derrota
    if not jogo_vencido and not jogo_perdido:
        if len(pontos) == 0:
            jogo_vencido = True
        elif tempo_passado >= TEMPO_LIMITE:
            jogo_perdido = True

    # Desenhar os alvos restantes
    for alvo in pontos:
        alvo.desenhar(screen)

    # Mostrar tempo restante
    segundos = tempo_restante // 1000
    tempo_texto = font.render(f"Tempo: {segundos}", True, BRANCO)
    screen.blit(tempo_texto, (10, 10))

    # Mensagem de fim de jogo
    if jogo_vencido:
        msg = font.render("Você Venceu!", True, VERDE)
        screen.blit(msg, (LARGURA // 2 - msg.get_width() // 2, ALTURA // 2))
    elif jogo_perdido:
        msg = font.render("Tempo Esgotado!", True, VERMELHO)
        screen.blit(msg, (LARGURA // 2 - msg.get_width() // 2, ALTURA // 2))

    pygame.display.flip()
    clock.tick(60)
