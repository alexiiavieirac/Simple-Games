import pygame
import random

# Inicializando o pygame
pygame.init()

# Definir cores
branco = (255, 255, 255)
preto = (0, 0, 0)

# Definindo a largura da tela
largura, altura = 800, 400
tela = pygame.display.set_mode((largura, altura))

# Configurando o relógio do jogo (FPS)
relogio = pygame.time.Clock()

# Definindo o personagem dinassouro
class Dinossauro:
    def __init__(self):
        self.imagem = pygame.image.load("t-rex.jpg")
        self.rect = self.imagem.get_rect()
        self.rect.x = 50
        self.rect.y = altura - self.rect.height - 10
        self.pulando = False
        self.velocidade_y = 0
        self.gravidade = 1


    def pular(self):
        if not self.pulando:
            self.pulando = True
            self.velocidade_y = -15 # Força do pulo


    def atualizar(self):
        if self.pulando:
            self.velocidade_y += self.gravidade
            self.rect.y += self.velocidade_y
            if self.rect.y >= altura - self.rect.height - 10:
                self.rect.y = altura - self.rect.height - 10
                self.pulando = False


    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)


# Definindo o obstáculo
class Obstaculo:
    def __init__(self, velocidade):
        self.largura = 45
        self.altura = random.randint(40, 80)

        imagem_original = pygame.image.load("cacto.png")

        fator_escala = 1.5
        nova_largura = int(self.largura * fator_escala)
        nova_altura = int(self.altura * fator_escala)
        self.imagem = pygame.transform.scale(imagem_original, (nova_altura, nova_largura))

        self.rect = self.imagem.get_rect()
        self.rect.x = largura
        self.rect.y = altura - self.rect.height
        self.velocidade = velocidade


    def atualizar(self):
        self.rect.x -= self.velocidade
        # Se o obstáculo sair da tela, retornamos False para removê-las da lista
        if self.rect.x + self.largura < 0:
            return False
        return True


    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)


# Função principal do jogo
def jogo():
    # Criando instâncias do dinossauro e do obstáculo
    dino = Dinossauro()

    velocidade_obstaculo = 10
    obstaculos = []

    pontuacao = 0
    nivel = 100

    # Controla o tempo para gerar novos obstáculos
    intervalo_proximo_obstaculo = random.randint(30, 100)
    frames_para_proximo_obstaculo = 0

    # Loop principal do jogo
    jogando = True
    while jogando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    dino.pular()

        # Atualizando o dinossauro e o obstaculo
        dino.atualizar()

        # Gerar novos obstáculos após o intervalo aleatório
        frames_para_proximo_obstaculo += 1
        if frames_para_proximo_obstaculo >= intervalo_proximo_obstaculo:
            obstaculos.append(Obstaculo(velocidade_obstaculo))
            frames_para_proximo_obstaculo = 0
            intervalo_proximo_obstaculo = random.randint(30, 100)

        # Atualizar e remover obstáculos fora da tela
        obstaculos = [obs for obs in obstaculos if obs.atualizar()]

        # Checa colisão
        for obstaculo in obstaculos:
            if dino.rect.colliderect(obstaculo.rect):
                print("Game Over!")
                jogando = False

        # Atualiza a pontuação
        pontuacao += 1

        # Aumentar a dificuldade: aumentar a velocidade a cada 500 pontos
        if pontuacao >= nivel:
            velocidade_obstaculo += 1
            nivel += 100
            print(f"Velocidade aumentada para {velocidade_obstaculo}, pontuação: {pontuacao}")

        # Desenhando na tela
        tela.fill(branco)
        dino.desenhar(tela)

        # Desenhar todos os obstáculos
        for obstaculo in obstaculos:
            obstaculo.desenhar(tela)

        # Exibindo a pontuação
        fonte = pygame.font.SysFont(None, 36)
        texto_pontuacao = fonte.render(f"Pontuação: {pontuacao}", True, preto)
        tela.blit(texto_pontuacao, (10, 10))

        pygame.display.flip()
        relogio.tick(30)

# Inicializando o jogo
jogo()

# Encerrando o jogo
pygame.quit()