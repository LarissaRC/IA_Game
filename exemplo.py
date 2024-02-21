import pygame
import random
import numpy as np

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE, RED, GREEN, BLUE, BLACK = (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)

# Configurações do Agente e do Jogo
agent_size = 20
n_actions = 4  # cima, baixo, esquerda, direita
epsilon = 0.1
alpha = 0.1
gamma = 0.9

# Estado é a posição do agente
state_size = (WIDTH // agent_size) * (HEIGHT // agent_size)
Q_table = np.zeros((state_size, n_actions))

# Fonte para texto
font = pygame.font.Font(None, 24)

# Converte posição para estado
def pos_to_state(pos):
    return (pos[1] // agent_size) * (WIDTH // agent_size) + (pos[0] // agent_size)

# Atualiza a tabela Q
def update_Q_table(state, action, reward, next_state):
    future = np.max(Q_table[next_state])
    Q_table[state, action] += alpha * (reward + gamma * future - Q_table[state, action])

# Escolhe uma ação usando a política ε-greedy
def choose_action(state):
    if random.uniform(0, 1) < epsilon:
        return random.randint(0, n_actions - 1)
    else:
        return np.argmax(Q_table[state])

# Configurações iniciais
agent_pos = [WIDTH // 4, HEIGHT // 4]
goal_pos = [WIDTH * 3 // 4, HEIGHT * 3 // 4]
obstacle_pos = [WIDTH // 2, HEIGHT // 2]

# Função para mover o agente
def move_agent(action):
    if action == 0 and agent_pos[1] > 0:  # cima
        agent_pos[1] -= agent_size
    if action == 1 and agent_pos[1] < HEIGHT - agent_size:  # baixo
        agent_pos[1] += agent_size
    if action == 2 and agent_pos[0] > 0:  # esquerda
        agent_pos[0] -= agent_size
    if action == 3 and agent_pos[0] < WIDTH - agent_size:  # direita
        agent_pos[0] += agent_size

# Verifica se o agente atingiu o objetivo ou o obstáculo
def check_collision():
    reward = -0.1  # Penalidade leve por movimento, para encorajar a eficiência
    if agent_pos == goal_pos:
        reward = 1  # Recompensa alta por alcançar o objetivo
    elif agent_pos == obstacle_pos:
        reward = -1  # Penalidade alta por colidir com o obstáculo
    return reward


# Desenha os elementos do jogo
def draw_elements():
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (*agent_pos, agent_size, agent_size))
    pygame.draw.rect(screen, GREEN, (*goal_pos, agent_size, agent_size))
    pygame.draw.rect(screen, RED, (*obstacle_pos, agent_size, agent_size))

    # Mostrar valores Q para o estado atual
    state = pos_to_state(agent_pos)
    q_values = Q_table[state]
    q_text = font.render(f"Q-values: {q_values}", True, BLACK)
    screen.blit(q_text, (5, HEIGHT - 30))

    pygame.display.flip()

# Loop principal do jogo
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_state = pos_to_state(agent_pos)
    action = choose_action(current_state)
    move_agent(action)
    reward = check_collision()
    next_state = pos_to_state(agent_pos)
    update_Q_table(current_state, action, reward, next_state)

    draw_elements()
    clock.tick(10)  # Controla a velocidade do jogo

pygame.quit()