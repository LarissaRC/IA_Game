import pygame
import sys
import random
import math
import numpy as np

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo do Agente")

# Cores
WHITE, RED, GREEN, BLUE = (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)

# Configurações do Agente e do Jogo
agent_size = 40
arrow_size = 20
block_size = 30
score = 0

# Variáveis do Q-learning
n_actions = 5  # cima, baixo, esquerda, direita, atirar
epsilon = 0.1
alpha = 0.1
gamma = 0.9

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

# Inicialização da Q-table
Q_table = {}

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

# Função para converter posição e direção do agente para um estado
def get_game_state(agent_direction, blocks):
    state_vector = [agent_direction]
    
    for block in blocks:
        state_vector.extend([block["pos"][0], block["pos"][1], block["type"]])

    return tuple(state_vector)

# Função para atualizar a Q-table com base nas recompensas
def update_Q_table(previous_state, current_state, action, reward):
    Q_table.setdefault(previous_state, np.zeros(n_actions))
    Q_table.setdefault(current_state, np.zeros(n_actions))
    
    Q_table[previous_state][action] += alpha * (reward + gamma * np.max(Q_table[current_state]) - Q_table[previous_state][action])

# Função para detectar colisões e destruir blocos
def destroy_blocks():
    global score

    # Captura o estado antes da destruição do bloco
    previous_state = get_game_state(agent_direction, blocks)

    reward = -0.1  # Penalidade leve por movimento, para encorajar a eficiência

    # Cria uma lista de blocos na direção em que o agente está olhando
    blocks_in_direction = [block for block in blocks if block["direction"] == agent_direction]

    if blocks_in_direction:
        # Encontra o bloco mais próximo na direção
        closest_block = min(blocks_in_direction, key=lambda block: distance(agent_pos, block["pos"]))

        # Realiza a destruição do bloco
        if closest_block["type"] == RED:
            score += 1
            reward = 1  # Recompensa alta
        else:
            score -= 1
            reward = -1  # Penalidade alta
        blocks.remove(closest_block)
    
    # Captura o estado após a destruição do bloco
    current_state = get_game_state(agent_direction, blocks)

    # Atualiza a Q-table com base nas recompensas
    update_Q_table(previous_state, current_state, action, reward)

# Função para escolher a ação automaticamente com base na Q-table
def choose_action_auto(state):
    if random.uniform(0, 1) < epsilon:
        return random.randint(0, n_actions - 1)
    else:
        if state in Q_table:
            return np.argmax(Q_table[state])
        else:
            Q_table[state] = np.zeros(n_actions)
            return np.argmax(Q_table[state])

# Função para realizar a ação escolhida automaticamente
def perform_action(action):
    global agent_direction, agent_pos, score, blocks

    # Muda a direção do agente
    if action == 0:
        previous_state = get_game_state(agent_direction, blocks)
        reward = -0.1  # Penalidade leve por movimento, para encorajar a eficiência
        agent_direction = 0
        current_state = get_game_state(agent_direction, blocks)
        # Atualiza a Q-table com base nas recompensas
        update_Q_table(previous_state, current_state, action, reward)
    elif action == 1:
        previous_state = get_game_state(agent_direction, blocks)
        reward = -0.1  # Penalidade leve por movimento, para encorajar a eficiência
        agent_direction = 1
        current_state = get_game_state(agent_direction, blocks)
        # Atualiza a Q-table com base nas recompensas
        update_Q_table(previous_state, current_state, action, reward)
    elif action == 2:
        previous_state = get_game_state(agent_direction, blocks)
        reward = -0.1  # Penalidade leve por movimento, para encorajar a eficiência
        agent_direction = 2
        current_state = get_game_state(agent_direction, blocks)
        # Atualiza a Q-table com base nas recompensas
        update_Q_table(previous_state, current_state, action, reward)
    elif action == 3:
        previous_state = get_game_state(agent_direction, blocks)
        reward = -0.1  # Penalidade leve por movimento, para encorajar a eficiência
        agent_direction = 3
        current_state = get_game_state(agent_direction, blocks)
        # Atualiza a Q-table com base nas recompensas
        update_Q_table(previous_state, current_state, action, reward)
    elif action == 4:
        # Atira (destrói blocos)
        destroy_blocks()

# Loop principal do jogo
clock = pygame.time.Clock()
game_active = True

while game_active:
    # Gera blocos com um intervalo de tempo
    current_time = pygame.time.get_ticks()
    if current_time - last_block_generation_time > block_generation_interval * 250:
        generate_blocks()
        last_block_generation_time = current_time

    # Movimenta os blocos
    for block in blocks:
        if block["direction"] == 0:  # Cima
            block["pos"][1] += 4
        elif block["direction"] == 1:  # Direita
            block["pos"][0] -= 4
        elif block["direction"] == 2:  # Baixo
            block["pos"][1] -= 4
        elif block["direction"] == 3:  # Esquerda
            block["pos"][0] += 4

    # Verifica colisões
    for block in blocks:
        if (
            agent_pos[0] < block["pos"][0] + block_size
            and agent_pos[0] + agent_size > block["pos"][0]
            and agent_pos[1] < block["pos"][1] + block_size
            and agent_pos[1] + agent_size > block["pos"][1]
        ):
            # Captura o estado antes da destruição do bloco
            previous_state = get_game_state(agent_direction, blocks)
            reward = -0.1  # Penalidade leve por movimento, para encorajar a eficiência

            if block["type"] == RED:
                score -= 5
                reward = -1  # Penalidade alta
            else:
                score += 5
                reward = 1  # Recompensa alta
            blocks.remove(block)

            # Captura o estado após a destruição do bloco
            current_state = get_game_state(agent_direction, blocks)

            # Atualiza a Q-table com base nas recompensas
            update_Q_table(previous_state, current_state, action, reward)

    # Escolhe automaticamente a ação com base na Q-table
    current_state = get_game_state(agent_direction, blocks)
    action = choose_action_auto(current_state)

    # Executa a ação escolhida automaticamente
    perform_action(action)

    # Limpa a tela
    screen.fill(WHITE)

    # Desenha o agente
    pygame.draw.rect(screen, BLUE, (*agent_pos, agent_size, agent_size))

    # Desenha o indicador de direção do agente
    indicator_size = 10
    indicator_offset = 10
    if agent_direction == 0:  # Cima
        indicator_pos = [agent_pos[0] + (agent_size - indicator_size) // 2, agent_pos[1] - indicator_size - indicator_offset]
    elif agent_direction == 1:  # Direita
        indicator_pos = [agent_pos[0] + agent_size + indicator_offset, agent_pos[1] + (agent_size - indicator_size) // 2]
    elif agent_direction == 2:  # Baixo
        indicator_pos = [agent_pos[0] + (agent_size - indicator_size) // 2, agent_pos[1] + agent_size + indicator_offset]
    else:  # Esquerda
        indicator_pos = [agent_pos[0] - indicator_size - indicator_offset, agent_pos[1] + (agent_size - indicator_size) // 2]

    pygame.draw.rect(screen, RED, (*indicator_pos, indicator_size, indicator_size))

    # Desenha os blocos
    for block in blocks:
        pygame.draw.rect(screen, block["type"], (*block["pos"], block_size, block_size))

    # Exibe os pontos
    score_text = font.render(f"SCORE: {max(0, score)}", True, BLUE)
    screen.blit(score_text, (WIDTH - 150, 20))

    # Exibe os valores da Q-table
    q_table_text = font.render(f"Q-table values: {Q_table.get(current_state, np.zeros(n_actions))}", True, BLUE)
    screen.blit(q_table_text, (20, HEIGHT - 40))

    pygame.display.flip()
    clock.tick(60)  # 60 frames por segundo

# Jogo pausado
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

pygame.quit()
sys.exit()
