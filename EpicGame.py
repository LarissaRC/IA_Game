import pygame
import sys
import random
import math

# Inicialização do Pygame
pygame.init()


# Configurações da tela
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo do Agente")

# Cores
WHITE, BLACK, RED, GREEN, BLUE = (255, 255, 255), (0, 0, 0,), (255, 0, 0), (0, 255, 0), (0, 0, 255)

# Configurações do Agente e do Jogo
agent_size = 40
arrow_size = 20
block_size = 30
score = 0
time_remaining = 30
angle = 0

# Carrega a imagem da nave
nave_img = pygame.image.load("nave.png").convert_alpha()
# Redimensiona a imagem da nave para o tamanho do agente
nave_img = pygame.transform.scale(nave_img, (agent_size, agent_size))

# Fonte para texto
font = pygame.font.Font(None, 36)

# Posição inicial do agente
agent_pos = [WIDTH // 2 - agent_size // 2, HEIGHT // 2 - agent_size // 2]

# Direção inicial do agente (0: cima, 1: direita, 2: baixo, 3: esquerda)
agent_direction = 0

# Lista de blocos
blocks = []

# Intervalo de geração de blocos (em segundos)
block_generation_interval = 2.0
last_block_generation_time = pygame.time.get_ticks()

# Função para gerar blocos nos pontos estratégicos
def generate_blocks():
    for side in range(4):  # 0: cima, 1: direita, 2: baixo, 3: esquerda
        block_type = RED if random.random() < 0.5 else GREEN
        if side == 0:
            block_pos = [WIDTH // 2 - block_size // 2, 0]
        elif side == 1:
            block_pos = [WIDTH - block_size, HEIGHT // 2 - block_size // 2]
        elif side == 2:
            block_pos = [WIDTH // 2 - block_size // 2, HEIGHT - block_size]
        else:
            block_pos = [0, HEIGHT // 2 - block_size // 2]

        blocks.append({"pos": block_pos, "type": block_type, "direction": side})

# Função para calcular a distância entre dois pontos
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Função para detectar colisões e destruir blocos
def destroy_blocks():
    global score

    # Cria uma lista de blocos na direção em que o agente está olhando
    blocks_in_direction = [block for block in blocks if block["direction"] == agent_direction]

    if blocks_in_direction:
        # Encontra o bloco mais próximo na direção
        closest_block = min(blocks_in_direction, key=lambda block: distance(agent_pos, block["pos"]))

        # Realiza a destruição do bloco
        if closest_block["type"] == RED:
            score += 1
        else:
            score -= 1
        blocks.remove(closest_block)

# Lista de teclas pressionadas
keys_pressed = set()

# Loop principal do jogo
clock = pygame.time.Clock()
game_active = True

# Função para rotacionar a imagem
def rotate_image(image, angle):
    return pygame.transform.rotate(image, angle)

while game_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_active = False
        elif event.type == pygame.KEYDOWN:
            keys_pressed.add(event.key)
        elif event.type == pygame.KEYUP:
            destroy_blocks()

            keys_pressed.discard(event.key)

    if pygame.K_LEFT in keys_pressed:
        agent_direction = 3
    elif pygame.K_RIGHT in keys_pressed:
        agent_direction = 1
    elif pygame.K_UP in keys_pressed:
        agent_direction = 0
    elif pygame.K_DOWN in keys_pressed:
        agent_direction = 2

    # Gera blocos com um intervalo de tempo
    current_time = pygame.time.get_ticks()
    if current_time - last_block_generation_time > block_generation_interval * 500:
        generate_blocks()
        last_block_generation_time = current_time

    # Movimenta os blocos
    for block in blocks:
        if block["direction"] == 0:  # Cima
            block["pos"][1] += 2
        elif block["direction"] == 1:  # Direita
            block["pos"][0] -= 2
        elif block["direction"] == 2:  # Baixo
            block["pos"][1] -= 2
        elif block["direction"] == 3:  # Esquerda
            block["pos"][0] += 2

    # Verifica colisões
    for block in blocks:
        if (
            agent_pos[0] < block["pos"][0] + block_size
            and agent_pos[0] + agent_size > block["pos"][0]
            and agent_pos[1] < block["pos"][1] + block_size
            and agent_pos[1] + agent_size > block["pos"][1]
        ):
            if block["type"] == RED:
                score -= 5
            else:
                score += 5
            blocks.remove(block)

    # Atualiza o tempo restante
    time_remaining -= 1 / 60  # subtrai 1 segundo a cada iteração

    # Limpa a tela
    screen.fill(BLACK)

    # Desenha o agente
    rotated_nave_img = rotate_image(nave_img, angle)  # angle é o ângulo de rotação
    screen.blit(rotated_nave_img, agent_pos)

    # Desenha o indicador de direção do agente
    indicator_size = 10
    indicator_offset = 10
    if agent_direction == 0:  # Cima
        indicator_pos = [agent_pos[0] + (agent_size - indicator_size) // 2, agent_pos[1] - indicator_size - indicator_offset]
        angle = 0
    elif agent_direction == 1:  # Direita
        indicator_pos = [agent_pos[0] + agent_size + indicator_offset, agent_pos[1] + (agent_size - indicator_size) // 2]
        angle = -90
    elif agent_direction == 2:  # Baixo
        indicator_pos = [agent_pos[0] + (agent_size - indicator_size) // 2, agent_pos[1] + agent_size + indicator_offset]
        angle = 180
    else:  # Esquerda
        indicator_pos = [agent_pos[0] - indicator_size - indicator_offset, agent_pos[1] + (agent_size - indicator_size) // 2]
        angle = 90

    pygame.draw.rect(screen, RED, (*indicator_pos, indicator_size, indicator_size))

    # Desenha os blocos
    for block in blocks:
        pygame.draw.rect(screen, block["type"], (*block["pos"], block_size, block_size))

    # Exibe os pontos
    score_text = font.render(f"SCORE: {max(0, score)}", True, WHITE)
    screen.blit(score_text, (WIDTH - 150, 20))

    # Exibe o tempo restante
    time_text = font.render(f"Seconds left: {max(0, int(time_remaining))}s", True, WHITE)
    screen.blit(time_text, (20, 20))

    pygame.display.flip()
    clock.tick(60)  # 60 frames por segundo

    # Verifica o fim do jogo
    if time_remaining <= 0:
        game_active = False

# Jogo pausado
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Exibe mensagem de fim de jogo
    end_text = font.render(f"Fim de jogo! Pontuação final: {max(0, score)}", True, WHITE)
    screen.blit(end_text, (WIDTH // 4, HEIGHT // 2 - 50))

    pygame.display.flip()
    clock.tick(1)  # 1 frame por segundo

pygame.quit()
sys.exit()
