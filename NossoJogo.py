import pygame
import random
import sys
import math

# Inicialização do Pygame
pygame.init()

# Tamanho da janela
LARGURA = 800
ALTURA = 600
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Point Clicker Game")
clock = pygame.time.Clock()

# Cores
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)

# Fundo
fundo = pygame.image.load("IMG/FundoReal.jpeg")
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))

# Parâmetros dos círculos
RAIO = 30
NUMERO_DE_PONTOS = 7

# Fonte
font = pygame.font.SysFont(None, 48)

# Estado do jogo
jogo_vencido = False
jogo_perdido = False

# Cronômetro
TEMPO_LIMITE = 60_000  # 90 segundos
tempo_inicial = pygame.time.get_ticks()

# Classe para representar cada ponto com imagem própria
class Alvo:
    def __init__(self, x, y, imagem):
        self.imagem = pygame.transform.scale(imagem, (RAIO * 2, RAIO * 2))
        self.rect = pygame.Rect(x - RAIO, y - RAIO, RAIO * 2, RAIO * 2)

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)

    def colidiu(self, pos):
        return self.rect.collidepoint(pos)

# Carregar imagens diferentes para os pontos
nomes_imagens = [
    "IMG/img1.png",
    "IMG/img3.png",
    "IMG/img2.png",

]

imagens = [pygame.image.load(nome) for nome in nomes_imagens]

# Função para verificar sobreposição
def sobreposto(novo_rect, alvos):
    for alvo in alvos:
        dx = novo_rect.centerx - alvo.rect.centerx
        dy = novo_rect.centery - alvo.rect.centery
        if math.hypot(dx, dy) < RAIO * 2:
            return True
    return False

# Geração dos pontos como objetos Alvo
pontos = []
i = 0
while len(pontos) < NUMERO_DE_PONTOS and i < len(imagens):
    x = random.randint(RAIO, LARGURA - RAIO)
    y = random.randint(RAIO, ALTURA - RAIO)
    rect_teste = pygame.Rect(x - RAIO, y - RAIO, RAIO * 2, RAIO * 2)

    if not sobreposto(rect_teste, pontos):
        pontos.append(Alvo(x, y, imagens[i]))
        i += 1

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

    if not jogo_vencido and not jogo_perdido:
        if len(pontos) == 0:
            jogo_vencido = True
        elif tempo_passado >= TEMPO_LIMITE:
            jogo_perdido = True

    # Desenha todos os pontos
    for alvo in pontos:
        alvo.desenhar(screen)

    # Mostrar tempo restante
    segundos = tempo_restante // 1000
    tempo_texto = font.render(f"Tempo: {segundos}", True, BRANCO)
    screen.blit(tempo_texto, (10, 10))

    # Mensagens de fim de jogo
    if jogo_vencido:
        msg = font.render("Você Venceu!", True, VERDE)
        screen.blit(msg, (LARGURA // 2 - msg.get_width() // 2, ALTURA // 2))
    elif jogo_perdido:
        msg = font.render("Tempo Esgotado!", True, VERMELHO)
        screen.blit(msg, (LARGURA // 2 - msg.get_width() // 2, ALTURA // 2))

    pygame.display.flip()
    clock.tick(60)
