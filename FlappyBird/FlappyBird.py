import pygame
import os
import random

LARGURA_TELA = 500
ALTURA_TELA = 800
# buscando as imagens que vão ser usadas pelo pygame
IMAGEM_PAUSE = pygame.image.load(os.path.join('C:\\Users\\ryan0\\OneDrive\\Documentos\\PROGRAMMING\\VSCODE\\PYTHON\\pygame\\FlappyBird\\imagens\\pause.png'))
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('C:\\Users\\ryan0\\OneDrive\\Documentos\\PROGRAMMING\\VSCODE\\PYTHON\\pygame\\FlappyBird\\imagens\\pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('C:\\Users\\ryan0\\OneDrive\\Documentos\\PROGRAMMING\\VSCODE\\PYTHON\\pygame\\FlappyBird\\imagens\\base.png')))
IMAGEM_FUNDO = pygame.transform.scale2x(pygame.image.load(os.path.join('C:\\Users\\ryan0\\OneDrive\\Documentos\\PROGRAMMING\\VSCODE\\PYTHON\\pygame\\FlappyBird\\imagens\\bg.png')))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('C:\\Users\\ryan0\\OneDrive\\Documentos\\PROGRAMMING\\VSCODE\\PYTHON\\pygame\\FlappyBird\\imagens\\bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('C:\\Users\\ryan0\\OneDrive\\Documentos\\PROGRAMMING\\VSCODE\\PYTHON\\pygame\\FlappyBird\\imagens\\bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('C:\\Users\\ryan0\\OneDrive\\Documentos\\PROGRAMMING\\VSCODE\\PYTHON\\pygame\\FlappyBird\\imagens\\bird3.png')))
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('TimesNewRoman', 50)


class Passaro:
    IMGS = IMAGENS_PASSARO
    # ANIMAÇÕES DE ROTAÇÃO
    ROTACAO_MAXIMO = 25
    VELOCIDADE_DE_ROTACAO = 10
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_da_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.35 * (self.tempo ** 2) + self.velocidade * self.tempo

        # restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 3

        self.y += deslocamento

        # rotação do passaro
        if deslocamento < 0 or self.y < (self.altura - 50):
            if self.angulo < self.ROTACAO_MAXIMO:
                self.angulo = self.ROTACAO_MAXIMO
        elif self.angulo > -90:
            self.angulo -= self.VELOCIDADE_DE_ROTACAO

    def desenhar(self, tela):
        # definir a imagem
        self.contagem_da_imagem += 1

        if self.contagem_da_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_da_imagem < self.TEMPO_ANIMACAO * 2:
            self.imagem = self.IMGS[1]
        elif self.contagem_da_imagem < self.TEMPO_ANIMACAO * 3:
            self.imagem = self.IMGS[2]
        elif self.contagem_da_imagem < self.TEMPO_ANIMACAO * 4:
            self.imagem = self.IMGS[1]
        elif self.contagem_da_imagem >= self.TEMPO_ANIMACAO * 4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_da_imagem = 0

        # não alterar se tiver caindo
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_da_imagem = self.TEMPO_ANIMACAO * 2

        # desenhar
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_BASE = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_TOPO = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_base = self.altura - self.CANO_TOPO.get_height()
        self.pos_topo = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        # calculando as distancias
        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        # colisao
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)
        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        if base_ponto or topo_ponto:
            return True
        else:
            return False


class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x0 = 0
        self.x1 = self.LARGURA

    def mover(self):
        self.x0 -= self.VELOCIDADE
        self.x1 -= self.VELOCIDADE

        if self.x0 + self.LARGURA < 0:
            self.x0 = self.LARGURA - 4

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.LARGURA - 4

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x0, self.y))
        tela.blit(self.IMAGEM, (self.x1, self.y))


def desenhar_tela(tela, passaros, chao, canos, pontos):
    tela.blit(IMAGEM_FUNDO, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)
    texto = FONTE_PONTOS.render(f"{pontos}", True, (25, 57, 30))
    tela.blit(texto, ((LARGURA_TELA - texto.get_width()) / 2, 10))
    chao.desenhar(tela)
    pygame.display.update()


def main():
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pontos = 0
    relogio = pygame.time.Clock()
    playing = True

    while playing:
        relogio.tick(30)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                playing = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()
                if evento.key == pygame.K_BACKSPACE:
                    pausado = True
                    while pausado:
                        tela.blit(IMAGEM_PAUSE, (
                            (LARGURA_TELA - IMAGEM_PAUSE.get_width()) / 2,
                            (ALTURA_TELA - IMAGEM_PAUSE.get_height()) / 2)
                                  )
                        pygame.display.update()
                        for pause in pygame.event.get():
                            if pause.type == pygame.KEYDOWN:
                                if evento.key == pygame.K_BACKSPACE:
                                    pausado = False
        for passaro in passaros:
            passaro.mover()
        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)
        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) >= chao.y or passaro.y <= -10:
                passaros.pop(i)

        desenhar_tela(tela, passaros, chao, canos, pontos)
        if len(passaros) == 0:
            perda = True
            while perda:
                for evento in pygame.event.get():
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_k:
                            passaros = [Passaro(230, 350)]
                            canos = [Cano(700)]
                            pontos = 0
                            perda = False
                        if evento.key == pygame.K_x:
                            pygame.quit()
                            quit()
                fonte = pygame.font.SysFont('TimesNewRoman', 30)
                perdeu = fonte.render(f"Você perdeu!", True, (255, 255, 255))
                fechar = fonte.render(f"Aperte 'X' para fechar", True, (255, 255, 255))
                restart = fonte.render(f"Aperte 'K' para recomeçar", True, (255, 255, 255))
                tela.blit(perdeu, ((LARGURA_TELA - perdeu.get_width()) / 2, (ALTURA_TELA - perdeu.get_height()) / 2))
                tela.blit(restart, ((LARGURA_TELA - restart.get_width()) / 2,
                                    (ALTURA_TELA - restart.get_height()) / 2 + perdeu.get_height()))
                tela.blit(fechar,
                          (
                              (LARGURA_TELA - fechar.get_width()) / 2,
                              (ALTURA_TELA - fechar.get_height()) / 2 + perdeu.get_height() + restart.get_height()
                          )
                          )
                pygame.display.update()


if __name__ == '__main__':
    main()
