import pygame, random
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, ROAD_COLOR, WHITE, BORDER_COLOR

class Track:
    def __init__(self, grass_images_list, cloud_image, mountain_image):
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
        self.grass_images = grass_images_list # Recebe a lista de imagens de grama do main.py
        # --- Parallax do Céu ---
        self.sky_offset = 0.0
        self.sky_img = pygame.transform.scale(cloud_image, (SCREEN_WIDTH, self.horizon_y))
        # --- Parallax das Montanhas ---
        self.mountain_img = self.sky_image = pygame.transform.scale(mountain_image, (SCREEN_WIDTH, self.horizon_y))
        self.mountain_offset = 0.0

        # Ciclo de Dia e Noite
        self.time_of_day = 0.0
        self.day_speed = 0.001
        
        # A película que vai cobrir a tela (criada 1 vez só na memória)
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # As 4 fases do dia agora guardam (R, G, B, Transparência)
        # Transparência (Alpha) vai de 0 (invisível) a 255 (sólido)
        self.time_phases = [
            (0, 0, 0, 0),         # 0: Dia (Totalmente transparente)
            (150, 80, 0, 80),     # 1: Pôr do Sol (Laranja, transparência leve)
            (5, 5, 25, 170),      # 2: Noite (Azul muito escuro, quase opaco)
            (180, 100, 150, 70)   # 3: Amanhecer (Rosa/Roxo, transparência leve)
        ]

    def update(self):
        # Se o carro tiver velocidade, as faixas se movem para baixo
        if self.speed > 0:
            # --- Passagem do Tempo ---
            self.time_of_day += self.day_speed
            if self.time_of_day >= 4.0:
                self.time_of_day = 0.0
            # Movimento do Céu (Mais lento que as montanhas para profundidade)
            self.sky_offset -= self.current_curve * self.speed * 0.5
            # Loop infinito do céu
            if self.sky_offset <= -SCREEN_WIDTH:
                self.sky_offset += SCREEN_WIDTH
            elif self.sky_offset >= SCREEN_WIDTH:
                self.sky_offset -= SCREEN_WIDTH

            # Movimento das Montanhas (Velocidade intermediária)
            self.mountain_offset -= self.current_curve * self.speed * 0.8
            if self.mountain_offset <= -SCREEN_WIDTH:
                self.mountain_offset += SCREEN_WIDTH
            elif self.mountain_offset >= SCREEN_WIDTH:
                self.mountain_offset -= SCREEN_WIDTH

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
                # Sorteamos a BASE do afastamento aqui (sem a escala, pois a escala muda)
                opcoes_base = [40, 80, 120, 160, None]
                escolhas = random.choices(opcoes_base, k=2)
                
                # Em vez de salvar apenas o Y, salvamos um dicionário com as escolhas fixas!
                self.lines_y.append({
                    'y': self.horizon_y,
                    'left_base': escolhas[0],
                    'right_base': escolhas[1],
                    # Sorteia tamanhos independentes para a esquerda e direita
                    'left_size_mult': random.uniform(0.5, 1.5),
                    'right_size_mult': random.uniform(0.5, 1.5),
                    # Sorteia a imagem específica para cada lado
                    'left_img': random.choice(self.grass_images) if escolhas[0] is not None else None,
                    'right_img': random.choice(self.grass_images) if escolhas[1] is not None else None
                })
                self.spawn_timer = 0

            # Atualiza o Y de cada item
            for item in self.lines_y:
                distance_from_horizon = item['y'] - self.horizon_y
                line_speed = (self.speed * 0.5) + (distance_from_horizon * 0.05)
                item['y'] += line_speed

            # Limpa as que saíram da tela
            self.lines_y = [item for item in self.lines_y if item['y'] <= SCREEN_HEIGHT]

    def get_center_x(self, y):
        """Calcula o centro X da pista com uma curva parabólica (Arco)."""
        scale = (y - self.horizon_y) / (SCREEN_HEIGHT - self.horizon_y)
        
        # O segredo do arco: (1 - scale) elevado ao quadrado (** 2) ou cubo (** 3).
        # Isso faz a pista ficar quase reta perto do carro e curvar drasticamente no horizonte.
        curve_shift = self.current_curve * (SCREEN_WIDTH // 1.5) * ((1 - scale) ** 2)
        return (SCREEN_WIDTH // 2) + curve_shift
    
    def get_overlay_color(self):
        """Calcula a cor e o alpha da película baseada na hora atual"""
        fase_atual = int(self.time_of_day) % 4
        fase_seguinte = (fase_atual + 1) % 4
        
        t = self.time_of_day - int(self.time_of_day)
        
        c1 = self.time_phases[fase_atual]
        c2 = self.time_phases[fase_seguinte]
        
        # Faz o Lerp (Interpolação) do R, G, B e também da Transparência (Alpha)
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        a = int(c1[3] + (c2[3] - c1[3]) * t)
        
        return (r, g, b, a)
    
    def draw_time_overlay(self, surface):
        """Aplica a película colorida por cima de tudo"""
        r, g, b, a = self.get_overlay_color()
        
        # Só gasta processamento desenhando a película se ela for visível (a > 0)
        if a > 0:
            self.overlay.fill((r, g, b))    # Pinta a tela toda com a cor atual
            self.overlay.set_alpha(a)       # Aplica o nível de transparência atual
            surface.blit(self.overlay, (0, 0)) # Cola por cima de tudo

    def draw(self, surface):
        DARK_GRASS = (30, 100, 30)

        # Desenha o Céu com Imagem (Parallax Infinito)
        if self.sky_img:
            # Desenha a imagem duas vezes para o loop ser invisível
            surface.blit(self.sky_img, (int(self.sky_offset), 0))
            surface.blit(self.sky_img, (int(self.sky_offset + SCREEN_WIDTH), 0))
            surface.blit(self.sky_img, (int(self.sky_offset - SCREEN_WIDTH), 0))

        if self.mountain_img:
            # O Y das montanhas é calculado para que a base delas encoste exatamente 
            # na linha do horizonte (grama).
            mountain_y = self.horizon_y - self.mountain_img.get_height()
            
            # Desenha 3 vezes para o loop infinito não deixar "buracos"
            surface.blit(self.mountain_img, (int(self.mountain_offset), mountain_y))
            surface.blit(self.mountain_img, (int(self.mountain_offset + SCREEN_WIDTH), mountain_y))
            surface.blit(self.mountain_img, (int(self.mountain_offset - SCREEN_WIDTH), mountain_y))

        # Desenha a grama
        grass_rect = pygame.Rect(0, self.horizon_y, SCREEN_WIDTH, SCREEN_HEIGHT - self.horizon_y)
        pygame.draw.rect(surface, DARK_GRASS, grass_rect)

        road_points = []
        left_edge_points = []  # Lista para guardar o traçado da borda esquerda
        right_edge_points = [] # Lista para guardar o traçado da borda direita
        
        steps = 20  # Quantidade de "fatias" horizontais para suavizar o arco da curva

        # 4.1 Lado Esquerdo do Asfalto (do topo descendo para a base)
        for i in range(steps + 1):
            step_scale = i / steps
            current_y = self.horizon_y + step_scale * (SCREEN_HEIGHT - self.horizon_y) # Calcula a posição Y atual para esta "fatia"
            center_x = self.get_center_x(current_y) # Calcula o centro X para esta posição Y usando a função de curva
            road_width = self.horizon_road_width + (self.road_width - self.horizon_road_width) * step_scale # Interpola a largura da estrada entre o horizonte e a base
            
            left_x = center_x - (road_width // 2) # Calcula a posição X do lado esquerdo da estrada para esta "fatia"
            road_points.append((left_x, current_y)) # Adiciona o ponto do lado esquerdo à lista de pontos da estrada
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

        # Desenha as Bordas Contínuas
        # Usamos draw.lines (superfície, cor, fechado?, pontos, espessura)
        pygame.draw.lines(surface, BORDER_COLOR, False, left_edge_points, 4)
        pygame.draw.lines(surface, BORDER_COLOR, False, right_edge_points, 4)

        # Desenha os elementos móveis (Faixa central e Manchas de grama)
        for item in self.lines_y:
            line_y = item['y']
            
            if line_y <= self.horizon_y + 2:
                continue
            
            scale = (line_y - self.horizon_y) / (SCREEN_HEIGHT - self.horizon_y)
            current_center_x = self.get_center_x(line_y)
            current_road_width = self.horizon_road_width + (self.road_width - self.horizon_road_width) * scale
            
            # --- DESENHA A FAIXA CENTRAL ---
            line_width = max(4, int(20 * scale))
            line_height = max(2, int(40 * scale))
            center_rect = pygame.Rect(int(current_center_x - line_width // 2), int(line_y), line_width, line_height)
            pygame.draw.rect(surface, WHITE, center_rect)

            # --- DESENHA AS MANCHAS DE GRAMA ---
            base_patch_width = max(10, int(80 * scale))
            base_patch_height = max(5, int(25 * scale))

            # Lado Esquerdo
            if item['left_base'] is not None:
                # Aplica o multiplicador sorteado para esta mancha
                mult_L = item['left_size_mult']
                # Garante que a largura/altura nunca seja 0 para o Pygame não crachar
                patch_width_L = max(2, int(base_patch_width * mult_L))
                patch_height_L = max(2, int(base_patch_height * mult_L))
                
                offset_left = item['left_base'] + (50 * scale)
                left_patch_x = current_center_x - (current_road_width // 2) - offset_left - patch_width_L
                
                # Escala a imagem PNG sorteada e desenha na tela
                scaled_img_L = pygame.transform.scale(item['left_img'], (patch_width_L, patch_height_L))
                surface.blit(scaled_img_L, (int(left_patch_x), int(line_y)))
                
            # Lado Direito
            if item['right_base'] is not None:
                # Aplica o multiplicador sorteado para esta mancha
                mult_R = item['right_size_mult']
                patch_width_R = max(2, int(base_patch_width * mult_R))
                patch_height_R = max(2, int(base_patch_height * mult_R))
                
                offset_right = item['right_base'] + (50 * scale)
                right_patch_x = current_center_x + (current_road_width // 2) + offset_right
                
                # Escala a imagem PNG sorteada e desenha na tela
                scaled_img_R = pygame.transform.scale(item['right_img'], (patch_width_R, patch_height_R))
                surface.blit(scaled_img_R, (int(right_patch_x), int(line_y)))

        return road_rect