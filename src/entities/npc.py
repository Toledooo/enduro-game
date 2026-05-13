import pygame
import random
from src.core.settings import SCREEN_HEIGHT

class NPC:
    def __init__(self, track_horizon_y, npc_images):
        self.width = 100
        self.height = 80
        self.speed_y = 5 # Velocidade de movimento vertical (descendo pela pista)
        self.images = []
        
        # Nasce 5 pixels abaixo do horizonte para evitar o "Ponto de Fuga"
        self.y = track_horizon_y + 2
        
        # Define a "faixa" do NPC. 
        # -0.4 é a esquerda da pista, 0.4 é a direita (0.5 seria o limite da grama)
        self.lane_offset = random.uniform(-0.4, 0.4)
        
        # Velocidade base do NPC (Quão rápido ele anda na direção do horizonte).
        # Valores menores significam que o jogador vai alcançá-los mais rápido.
        self.base_speed = random.uniform(1.0, 3.0)
        self.image = random.choice(npc_images)

    def update(self, track_speed, track_horizon_y):
        # A velocidade relativa: Sua Velocidade menos a Dele
        relative_speed = track_speed - self.base_speed
        
        dist_horizon = self.y - track_horizon_y
        
        if relative_speed > 0:
            # VOCÊ É MAIS RÁPIDO: O NPC desce a tela na sua direção
            move_y = (relative_speed * 0.2) + (dist_horizon * 0.05 * (relative_speed / 10))
            self.y += move_y
        else:
            # --- NOVO: NPC É MAIS RÁPIDO (Ou você bateu e parou) ---
            # Ele foge em direção ao horizonte (sobe a tela)
            
            escape_speed = abs(relative_speed) # Converte o negativo para positivo para o cálculo
            
            # Se você bateu (track_speed é zero), damos um "boost" para eles sumirem muito rápido
            boost = 3.0 if track_speed <= 0.5 else 1.0 
            
            # Subtraímos o move_y para que ele suba em direção ao horizonte
            move_y = (escape_speed * 0.5 * boost) + (dist_horizon * 0.02)
            self.y -= move_y

    def draw(self, surface, track):
        # 1. Calcula a escala do 3D
        scale = (self.y - track.horizon_y) / (SCREEN_HEIGHT - track.horizon_y)
        
        if scale <= 0.02: # Não desenha se estiver colado no horizonte
            return None
            
        # 2. Pega a curvatura da pista neste exato pixel Y
        current_center_x = track.get_center_x(self.y)
        current_road_width = track.horizon_road_width + (track.road_width - track.horizon_road_width) * scale
        
        # 3. Calcula o X na tela aplicando a "faixa" do NPC
        npc_x = current_center_x + (current_road_width * self.lane_offset)
        
        # 4. Redimensiona a imagem (fator 2.5 é para a imagem ficar num tamanho bom perto do jogador)
        scaled_w = max(5, int(self.image.get_width() * scale * 2.5) * 0.12)
        scaled_h = max(5, int(self.image.get_height() * scale * 2.5) * 0.12)
        
        scaled_image = pygame.transform.scale(self.image, (scaled_w, scaled_h))
        
        # 5. Desenha a imagem (midbottom alinha a base do pneu com a coordenada Y da pista)
        rect = scaled_image.get_rect(midbottom=(int(npc_x), int(self.y)))
        surface.blit(scaled_image, rect)
        
        return rect