import pygame
import random

# Iniciazliar o pygame
pygame.init()

# Definir variáveis
largura, altura = 400, 400
tamanho_peca = 100
margem = 5
colunas = 4
linhas = 4
score = 0

# Definir cores
branco = (255, 255, 255)
preto = (0, 0, 0)
verde = (0, 255, 0)
cinza = (192, 192, 192)

# Criar a tela do jogo
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Puzzle Deslizante')

# Carregar imagens e fontes
fundo_img = pygame.image.load("marmore.jpg")
fonte_pontuacao = pygame.font.Font(None, 35)
fonte_pecas = pygame.font.Font(None, 55)
fonte_vitoria = pygame.font.Font(None, 65)
fonte_score_final = pygame.font.Font(None, 35)
fonte_botao = pygame.font.Font(None, 50)

# Função para desenhar o tabuleiro do jogo
def desenhar_tabuleiro(tabuleiro):
    screen.blit(fundo_img, (0, 0))

    # Desenhar o score
    texto_score = fonte_pontuacao.render(f"Score: {score}", True, branco)
    screen.blit(texto_score, (10, 10))

    # Desenhar as peças do tabuleiro
    for i in range(linhas):
        for j in range(colunas):
            if tabuleiro[i][j] != 0:
                pygame.draw.rect(screen, cinza, (j * tamanho_peca + margem, i * tamanho_peca + margem, tamanho_peca - margem, tamanho_peca - margem), border_radius=20)
                pygame.draw.rect(screen, branco, (j * tamanho_peca + margem + 2, i * tamanho_peca + margem + 2, tamanho_peca - margem - 4, tamanho_peca - margem - 4), border_radius=20)
                texto = fonte_pecas.render(str(tabuleiro[i][j]), True, preto)
                screen.blit(texto, (j * tamanho_peca + tamanho_peca // 2 - texto.get_width() // 2, i * tamanho_peca + tamanho_peca // 2 - texto.get_width() // 2))


# Função para encontrar a posição da peça vazia
def encontrar_vazio(tabuleiro):
    for i in range(linhas):
        for j in range(colunas):
            if tabuleiro[i][j] == 0:
                return i,j


# Função para misturar o tabuleiro (peças)
def embaralhar_tabuleiro(tabuleiro):
    movimentos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    vazio_linha, vazio_coluna = encontrar_vazio(tabuleiro)
    for _ in range(100):
        mov = random.choice(movimentos)
        nova_linha, nova_coluna = vazio_linha + mov[0], vazio_coluna + mov[1]
        if 0 <= nova_linha < linhas and 0 <= nova_coluna < colunas:
            tabuleiro[vazio_linha][vazio_coluna], tabuleiro[nova_linha][nova_coluna] = tabuleiro[nova_linha][nova_coluna], tabuleiro[vazio_linha][vazio_coluna]
            vazio_linha, vazio_coluna = nova_linha, nova_coluna


# Função para mover uma peça
def mover_peca(tabuleiro, linha, coluna):
    vazio_linha, vazio_coluna = encontrar_vazio(tabuleiro)
    if(linha  == vazio_linha and abs(coluna - vazio_coluna) == 1) or (coluna == vazio_coluna and abs(linha - vazio_linha) == 1):
        tabuleiro[vazio_linha][vazio_coluna], tabuleiro[linha][coluna] = tabuleiro[linha][coluna], tabuleiro[vazio_linha][vazio_coluna]
        return True
    return False


# Função para verificar se o tabuleiro está organizado
def verificar_vitoria(tabuleiro):
    esperado = [[(i * colunas + j + 1) % (colunas * linhas) for j in range(colunas)] for i in range(linhas)]
    return tabuleiro == esperado


# Função para exibir a tela de vitória
def exibir_tela_vitoria(score):
    screen.blit(fundo_img, (0, 0))

    # Exibir a mensagem de vitória
    texto_vitoria = fonte_vitoria.render("Você venceu!", True, verde)
    screen.blit(texto_vitoria, (largura // 2 - texto_vitoria.get_width() // 2, altura // 2 - texto_vitoria.get_height() // 2 - 30))

    # Exibir o score final
    texto_score_final = fonte_score_final.render(f"Score final: {score}", True, branco)
    screen.blit(texto_score_final, (largura // 2 - texto_score_final.get_width() // 2, altura // 2 - texto_score_final.get_height() // 2 + 30))

    pygame.display.flip()


# Criar o tabuleiro inicial
tabuleiro = [[(i * colunas + j + 1) % (colunas * linhas) for j in range(colunas)] for i in range(linhas)]
embaralhar_tabuleiro(tabuleiro)

# Loop inicial do jogo
rodando = True
vitoria = False

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and not vitoria:
            x, y = evento.pos

            # Verifica se o clique foi dentro da área do tabuleiro (desconsiderando a margem)
            if y > 40:
                coluna = x // tamanho_peca
                linha = (y - 40) // tamanho_peca
                if 0 <= linha < linhas and 0 <= coluna < colunas:
                    if mover_peca(tabuleiro, linha, coluna):
                        score += 1

        # Verifica se o jogador ganhou
        if verificar_vitoria(tabuleiro):
            vitoria = True

    # Exibir mensagem de vitória
    if vitoria:
        exibir_tela_vitoria(score)
    else:
        desenhar_tabuleiro(tabuleiro)

    pygame.display.flip()

pygame.quit()