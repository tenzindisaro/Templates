import pygame
import sys
import random
import os

pygame.init()

# Janela
largura, altura = 800, 400
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo do Dinossauro")

# FPS
relogio = pygame.time.Clock()
FPS = 60

# Cores
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)

# Fonte
fonte = pygame.font.SysFont(None, 36)

# Caminho das imagens
pasta_img = os.path.join("game", "img")

# Animações do dinossauro
walk = [pygame.image.load(os.path.join(pasta_img, "walk", f"walk{i}.png")) for i in range(1, 11)]
jump = [pygame.image.load(os.path.join(pasta_img, "jump", f"jump{i}.png")) for i in range(1, 13)]
down = [pygame.image.load(os.path.join(pasta_img, "down", "down1.png"))]

# Obstáculos
cacto_imgs = [
    pygame.transform.scale(pygame.image.load(os.path.join(pasta_img, "cacto1.png")), (40, 60)),
    pygame.transform.scale(pygame.image.load(os.path.join(pasta_img, "cacto2.png")), (30, 50))
]

# Função para resetar o jogo
def resetar():
    return {
        "dino_y": altura - 60 - 50,
        "vel_y": 0,
        "pulando": False,
        "abaixado": False,
        "pontos": 0,
        "game_over": False,
        "obstaculos": gerar_obstaculos()
    }

# Função para gerar obstáculos
def gerar_obstaculos():
    obstaculos = []
    for i in range(2):
        img = random.choice(cacto_imgs)
        x = largura + i * 400
        y = altura - img.get_height() - 50
        obstaculos.append({"img": img, "x": x, "y": y})
    return obstaculos

# Inicialização
estado = resetar()
gravidade = 1
dino_x = 50

# Controle da animação
frame_index = 0
frame_count = 0
frame_delay = 5  # Troca de sprite a cada 5 frames

# Loop principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN:
            if (evento.key == pygame.K_SPACE or evento.key == pygame.K_UP) and not estado["pulando"] and not estado["game_over"]:
                estado["vel_y"] = -15
                estado["pulando"] = True
            if evento.key == pygame.K_DOWN and not estado["pulando"]:
                estado["abaixado"] = True
            if evento.key == pygame.K_r and estado["game_over"]:
                estado = resetar()
                frame_index = 0
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_DOWN:
                estado["abaixado"] = False

    # Ajustar altura do dinossauro
    dino_altura = 35 if estado["abaixado"] else 60
    chao_y = altura - dino_altura - 50

    if not estado["game_over"]:
        estado["vel_y"] += gravidade
        estado["dino_y"] += estado["vel_y"]

        if estado["dino_y"] >= chao_y:
            estado["dino_y"] = chao_y
            estado["vel_y"] = 0
            estado["pulando"] = False

        # Mover obstáculos
        for ob in estado["obstaculos"]:
            ob["x"] -= 8
            if ob["x"] + ob["img"].get_width() < 0:
                ob["x"] = largura + random.randint(300, 600)
                ob["img"] = random.choice(cacto_imgs)
                ob["y"] = altura - ob["img"].get_height() - 50
                estado["pontos"] += 1

    # Animação do dinossauro
    if estado["pulando"]:
        animacao_atual = jump
    elif estado["abaixado"]:
        animacao_atual = down
    else:
        animacao_atual = walk

    frame_count += 1
    if frame_count >= frame_delay:
        frame_count = 0
        frame_index = (frame_index + 1) % len(animacao_atual)

    if not animacao_atual:
        print("Erro: nenhuma imagem carregada para o estado atual!")
        pygame.quit()
        sys.exit()

    dino_sprite = pygame.transform.scale(animacao_atual[frame_index], (60, dino_altura))
    tela.fill(BRANCO)
    tela.blit(dino_sprite, (dino_x, estado["dino_y"]))

    # Retângulo de colisão
    dino_rect = pygame.Rect(dino_x, estado["dino_y"], 60, dino_altura)

    for ob in estado["obstaculos"]:
        tela.blit(ob["img"], (ob["x"], ob["y"]))
        ob_rect = pygame.Rect(ob["x"], ob["y"], ob["img"].get_width(), ob["img"].get_height())
        if dino_rect.colliderect(ob_rect):
            estado["game_over"] = True

    # Pontuação
    pontos_txt = fonte.render(f"Pontos: {estado['pontos']}", True, (0, 0, 0))
    tela.blit(pontos_txt, (10, 10))

    # Game Over
    if estado["game_over"]:
        msg = fonte.render("Game Over! Pressione R para reiniciar", True, VERMELHO)
        tela.blit(msg, (largura//2 - 200, altura//2))

    pygame.display.update()
    relogio.tick(FPS)
