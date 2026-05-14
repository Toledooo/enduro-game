import pygame, random
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, SKY_COLOR, GRASS_COLOR, ROAD_COLOR, WHITE, BORDER_COLOR

class Track:
    def __init__(self):
        self.horizon_y = SCREEN_HEIGHT // 4 # Linha do horizonte em 1/4 da altura da tela
        self.road_width = SCREEN_WIDTH * 0.8 # Largura da estrada próxima ao jogador
        self.horizon_road_width = 0 # Largura da estrada no horizonte
        self.speed = 0
        self.lines_y = [] # Lista para armazenar as posições Y das faixas centrais que se movem para baixo
        self.spawn_timer = 0 # Timer para controlar o tempo entre o spawn das faixas centrais
        self.spawn_delay_base = 19  # Tempo base de geração (em frames)
        self.current_curve = 0.0 # Curva atual da estrada (negativa para esquerda, positiva para direita)
        self.target_curve = 0.0  # Curva alvo que a estrada deve alcançar
        self.track_state = "STRAIGHT" # O jogo sempre começa em uma reta
        self.state_timer = 0
        self.straight_durations = [10 * 60, 12 * 60] # Define o tempo da primeira reta: entre 10 e 12 segundos (x 60 FPS)
        self.curve_durations = [3 * 60, 5 * 60] # Define o tempo da primeira curva: entre 3 e 5 segundos (x 60 FPS)
        self.curve_choices = [-0.3, 0.3] # Curvas possíveis: esquerda, direita ou reta        
        # --- Parallax do Céu ---
        self.sky_offset = 0.0
        try:
            # Carrega a imagem e força ela a ocupar a largura da tela e a altura do horizonte
            original_sky = pygame.image.load("assets/images/clouds.jpg").convert_alpha()
            self.sky_image = pygame.transform.scale(original_sky, (SCREEN_WIDTH, self.horizon_y))
        except FileNotFoundError:
            print("Aviso: assets/images/nuvens.jpg não encontrada. Usando cor sólida.")
            self.sky_image = None

    def update(self):
        # Se o carro tiver velocidade, as faixas se movem para baixo
        if self.speed > 0:
            # 1. Gerador de faixas no tempo

            # Movimento do Céu (Mais lento que as montanhas para profundidade)
            self.sky_offset -= self.current_curve * self.speed * 0.5
            
            # Loop infinito do céu
            if self.sky_offset <= -SCREEN_WIDTH:
                self.sky_offset += SCREEN_WIDTH
            elif self.sky_offset >= SCREEN_WIDTH:
                self.sky_offset -= SCREEN_WIDTH

            self.state_timer += 1

            if self.state_timer >= random.choice(self.straight_durations):
                self.target_curve = random.choice(self.curve_choices)
                self.state_timer = 0
                if self.track_state == "STRAIGHT":
                    # Sai da reta e entra em uma curva
                    self.track_state = "CURVING"
                    # Define duração da curva: 3 a 5 segundos
                    self.state_duration = random.choice(self.curve_durations)
                    
                    self.target_curve = random.choice(self.curve_choices) # Escolhe aleatoriamente a direção da curva
                    
                elif self.track_state == "CURVING":
                    # Sai da curva e volta para a reta
                    self.track_state = "STRAIGHT"
                    # Define duração da reta: 10 a 12 segundos
                    self.state_duration = random.choice(self.straight_durations)
                    
                    # O alvo volta a ser o centro
                    self.target_curve = 0.0

            diferenca = abs(self.target_curve - self.current_curve)
            
            # Validação para evitar oscilações quando estiver muito próximo do alvo
            if diferenca < 0.015:
                self.current_curve = self.target_curve
            else:
                # Transição suave para a curva: Aumenta ou diminui gradualmente o valor atual em direção ao alvo.
                if self.current_curve < self.target_curve:
                    self.current_curve += 0.01 
                elif self.current_curve > self.target_curve:
                    self.current_curve -= 0.01

            if self.current_curve < self.target_curve:
                self.current_curve += 0.01 # Transição suave para a nova curva
            elif self.current_curve > self.target_curve:
                self.current_curve -= 0.01
            
            self.spawn_timer += 1
            # Quanto maior a velocidade, menor o tempo de espera (delay) para gerar a próxima faixa.
            # Isso evita que fique um "buraco" gigante entre as faixas em altas velocidades.
            current_delay = max(5, self.spawn_delay_base - int(self.speed * 0.8))

            if self.spawn_timer >= current_delay:
                self.lines_y.append(self.horizon_y)  # Nova faixa nasce no horizonte
                self.spawn_timer = 0

            # 2. Movimento das faixas para baixo
            for i in range(len(self.lines_y)):
                distance_from_horizon = self.lines_y[i] - self.horizon_y
                line_speed = (self.speed * 0.5) + (distance_from_horizon * 0.05)
                self.lines_y[i] += line_speed

            # Mantém na lista apenas as faixas que ainda estão dentro da tela.
            self.lines_y = [y for y in self.lines_y if y <= SCREEN_HEIGHT]

    def get_center_x(self, y):
        """Calcula o centro X da pista com uma curva parabólica (Arco)."""
        scale = (y - self.horizon_y) / (SCREEN_HEIGHT - self.horizon_y)
        
        # O segredo do arco: (1 - scale) elevado ao quadrado (** 2) ou cubo (** 3).
        # Isso faz a pista ficar quase reta perto do carro e curvar drasticamente no horizonte.
        curve_shift = self.current_curve * (SCREEN_WIDTH // 1.5) * ((1 - scale) ** 2)
        return (SCREEN_WIDTH // 2) + curve_shift

    def draw(self, surface):
        DARK_GRASS = (30, 100, 30)

        # 1. Desenha o Céu com Imagem (Parallax Infinito)
        if self.sky_image:
            # Desenha a imagem duas vezes para o loop ser invisível
            surface.blit(self.sky_image, (int(self.sky_offset), 0))
            surface.blit(self.sky_image, (int(self.sky_offset + SCREEN_WIDTH), 0))
            surface.blit(self.sky_image, (int(self.sky_offset - SCREEN_WIDTH), 0))

        # Desenha a grama
        grass_rect = pygame.Rect(0, self.horizon_y, SCREEN_WIDTH, SCREEN_HEIGHT - self.horizon_y)
        pygame.draw.rect(surface, GRASS_COLOR, grass_rect)

        road_points = []
        left_edge_points = []  # NOVO: Lista para guardar o traçado da borda esquerda
        right_edge_points = [] # NOVO: Lista para guardar o traçado da borda direita
        
        steps = 20  # Quantidade de "fatias" horizontais para suavizar o arco da curva

        # 4.1 Lado Esquerdo do Asfalto (do topo descendo para a base)
        for i in range(steps + 1):
            step_scale = i / steps
            current_y = self.horizon_y + step_scale * (SCREEN_HEIGHT - self.horizon_y)
            center_x = self.get_center_x(current_y)
            road_width = self.horizon_road_width + (self.road_width - self.horizon_road_width) * step_scale
            
            left_x = center_x - (road_width // 2)
            road_points.append((left_x, current_y))
            left_edge_points.append((left_x, current_y)) # Salva o ponto para a linha contínua

        # 4.2 Lado Direito do Asfalto (da base subindo para o topo)
        for i in range(steps, -1, -1):
            step_scale = i / steps
            current_y = self.horizon_y + step_scale * (SCREEN_HEIGHT - self.horizon_y)
            center_x = self.get_center_x(current_y)
            road_width = self.horizon_road_width + (self.road_width - self.horizon_road_width) * step_scale
            
            right_x = center_x + (road_width // 2)
            road_points.append((right_x, current_y))
            # Inserimos no início da lista (índice 0) para que a linha seja desenhada de cima para baixo corretamente
            right_edge_points.insert(0, (right_x, current_y)) 

        # Desenha a estrada com os pontos gerados
        road_rect = pygame.draw.polygon(surface, ROAD_COLOR, road_points)

        # --- NOVO: Desenha as Bordas Contínuas ---
        # Usamos draw.lines (superfície, cor, fechado?, pontos, espessura)
        pygame.draw.lines(surface, BORDER_COLOR, False, left_edge_points, 4)
        pygame.draw.lines(surface, BORDER_COLOR, False, right_edge_points, 4)

        # Desenha os elementos móveis (Faixa central e Manchas de grama)
        for line in self.lines_y:
            if line <= self.horizon_y + 2:
                continue
                
            scale = (line - self.horizon_y) / (SCREEN_HEIGHT - self.horizon_y)
            current_center_x = self.get_center_x(line)
            current_road_width = self.horizon_road_width + (self.road_width - self.horizon_road_width) * scale
            
            # --- FAIXA CENTRAL ---
            line_width = max(4, int(20 * scale))
            line_height = max(2, int(40 * scale))
            center_rect = pygame.Rect(int(current_center_x - line_width // 2), int(line), line_width, line_height)
            pygame.draw.rect(surface, WHITE, center_rect)

            # A mancha cresce conforme desce a tela
            patch_width = max(10, int(80 * scale))
            patch_height = max(5, int(25 * scale))
            
            # Afastamento extra para não colar na pista (também cresce com a escala)
            offset = 20 + (50 * scale)
            
            # Posiciona usando o centro da curva como referência matemática
            left_patch_x = current_center_x - (current_road_width // 2) - offset - patch_width
            right_patch_x = current_center_x + (current_road_width // 2) + offset
            
            left_patch = pygame.Rect(int(left_patch_x), int(line), patch_width, patch_height)
            right_patch = pygame.Rect(int(right_patch_x), int(line), patch_width, patch_height)
            
            pygame.draw.rect(surface, DARK_GRASS, left_patch)
            pygame.draw.rect(surface, DARK_GRASS, right_patch)

        return road_rect