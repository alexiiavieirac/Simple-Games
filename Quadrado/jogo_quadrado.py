from sys import displayhook

import pygame
import sys

# Inicializar o pygame
pygame.init()

# Definir a janela do jogo
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))

# Definir a cor (RGB)
branco = (255, 255, 255)
preto = (0, 0, 0)

# Definir o quadrado
jogador_pos = [largura // 2, altura // 2]
jogador_tamanho = 50
velocidade = 5

# Loop principal do jogo
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimento do Jogador
    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        jogador_pos[0] -= velocidade
    if teclas[pygame.K_RIGHT]:
        jogador_pos[0] += velocidade
    if teclas[pygame.K_UP]:
        jogador_pos[1] -= velocidade
    if teclas[pygame.K_DOWN]:
        jogador_pos[1] += velocidade

    # Limpar tela
    tela.fill(branco)

    # Desenhar quadrado
    pygame.draw.rect(tela, preto, (*jogador_pos, jogador_tamanho, jogador_tamanho))

    # Atualizar a tela
    pygame.display.flip()

    # Controla a taxa de quadros por segundo (FPS)
    pygame.time.Clock().tick(30)