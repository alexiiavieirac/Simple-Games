import pygame
import random
import time

# Inicializar o Pygame
pygame.init()

# Definir as cores
branco = (255, 255, 255)
preto = (0, 0, 0)
verde = (0, 255, 0)
vermelho = (213, 50, 0)
azul = (50, 153, 213)

# Definir o tamanho da janela
largura = 600
altura = 400

# Configuração da tela de jogo
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Snake")

# Definir a velocidade da cobra
clock = pygame.time.Clock()

# Definir o tamanho da cobra e da comida
tamanho_cobra = 10
velocidade_cobra = 15

# Fontes
fonte_estilo = pygame.font.SysFont("bahnschrift", 25)
fonte_pontuacao = pygame.font.SysFont("comicsans", 35)

# Função para exibir a pontuação
def pontos(score):
    valor = fonte_pontuacao.render(f"Pontuação: {score}", True, azul)
    tela.blit(valor, [0, 0])


# Função para a cobra
def cobra(tamanho_cobra, lista_cobra):
    for posicao in lista_cobra:
        pygame.draw.rect(tela, preto, [posicao[0], posicao[1], tamanho_cobra, tamanho_cobra])


# Função mensagem
def mensagem(msg, cor):
    mesg = fonte_estilo.render(msg, True, cor)
    tela.blit(mesg, [largura / 6, altura / 3])


# Função principal do jogo
def jogo():
    game_over = False
    game_close = False

    # Posição inicial da cobra
    x = largura / 2
    y = altura / 2

    # Mudanças de posição
    x_mudanca = 0
    y_mudanca = 0

    # Listas para manter o rastro da cobra
    lista_cobra = []
    comprimento_cobra = 1

    # Posição inicial da comida
    comida_x = round(random.randrange(0, largura - tamanho_cobra) / 10.0) * 10.0
    comida_y = round(random.randrange(0, altura - tamanho_cobra) / 10.0) * 10.0

    while not game_over:
        # Tela game over
        while game_close:
            tela.fill(branco)
            mensagem("Perdeu! Pressione C para jogar novamente ou Q para sair", vermelho)
            pontos(comprimento_cobra - 1)
            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if evento.key == pygame.K_c:
                        jogo()

        # Captura eventos de movimento
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                game_over = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    x_mudanca = -tamanho_cobra
                    y_mudanca = 0
                elif evento.key == pygame.K_RIGHT:
                    x_mudanca = tamanho_cobra
                    y_mudanca = 0
                elif evento.key == pygame.K_UP:
                    y_mudanca = -tamanho_cobra
                    x_mudanca = 0
                elif evento.key == pygame.K_DOWN:
                    y_mudanca = tamanho_cobra
                    x_mudanca = 0

        # Se a cobra atingir as bordas da tela
        if x >= largura or x < 0 or y >= altura or y < 0:
            game_close = True

        # Movimentação da cobra
        x += x_mudanca
        y += y_mudanca
        tela.fill(branco)
        pygame.draw.rect(tela, vermelho, [comida_x, comida_y, tamanho_cobra, tamanho_cobra])

        cabeca_cobra = []
        cabeca_cobra.append(x)
        cabeca_cobra.append(y)
        lista_cobra.append(cabeca_cobra)

        # Atualiza o corpo da cobra
        if len(lista_cobra) > comprimento_cobra:
            del lista_cobra[0]

        # Se a cobra colidir com ela mesma
        for bloco in lista_cobra[:-1]:
            if bloco == cabeca_cobra:
                game_close = True

        cobra(tamanho_cobra, lista_cobra)
        pontos(comprimento_cobra - 1)

        pygame.display.update()

        # Se a cobra comer a comida
        if x == comida_x and y == comida_y:
            comida_x = round(random.randrange(0, largura - tamanho_cobra) / 10.0) * 10.0
            comida_y = round(random.randrange(0, altura - tamanho_cobra) / 10.0) * 10.0
            comprimento_cobra += 1

        clock.tick(velocidade_cobra)

    pygame.quit()
    quit()


# Iniciar o jogo
jogo()