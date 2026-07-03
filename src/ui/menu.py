import pygame
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Menu:
    def __init__(self):
        pygame.font.init()
        
        # Tenta carregar uma fonte retrô customizada (se você baixar e colocar na pasta)
        try:
            self.title_font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 60)
            self.subtitle_font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 30)
            self.game_over_font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 50)
        except FileNotFoundError:
            # Fallback: Se não achar o arquivo, usa a Impact (nativa, grossa e pesada)
            self.title_font = pygame.font.SysFont("Impact", 80)
            self.subtitle_font = pygame.font.SysFont("Impact", 20)
            self.game_over_font = pygame.font.SysFont("Impact", 70)

        # Fonte menor para as instruções
        self.text_font = pygame.font.SysFont("Courier New", 24, bold=True)

    def draw_main_menu(self, surface, stage):
        surface.fill((10, 10, 20)) # Fundo escuro
        
        # Título do jogo
        title_text = self.title_font.render("ENDURO", True, (255, 255, 100))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        surface.blit(title_text, title_rect)

        # Subtítulo
        subtitle_text = self.subtitle_font.render("UM REMAKE USANDO PYGAME", True, (200, 200, 200))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        surface.blit(subtitle_text, subtitle_rect)

        # Instrução de Start (com efeitinho de piscar)
        current_time = pygame.time.get_ticks()
        if (current_time // 500) % 2 == 0: # Pisca a cada 500ms
            start_text = self.text_font.render("Pressione ENTER para Jogar", True, (255, 255, 255))
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            surface.blit(start_text, start_rect)

        # Seletor de Fase
        stage_text = self.text_font.render(
            "1: Verao   |   2: Inverno", True, (150, 150, 150)
        )
        stage_rect = stage_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 130))
        surface.blit(stage_text, stage_rect)
        sel_text = self.text_font.render(
            f"Fase atual: {stage.display_name}",
            True, stage.display_color
        )
        sel_rect = sel_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        surface.blit(sel_text, sel_rect)

        rank_text = self.text_font.render("Pressione TAB para ver o Ranking", True, (150, 150, 150))
        rank_rect = rank_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        surface.blit(rank_text, rank_rect)

    def draw_leaderboard(self, surface, scores):
        """Desenha a tela com os 5 melhores tempos."""
        surface.fill((10, 10, 20)) # Fundo escuro
        
        # Título da tela
        title = self.game_over_font.render("TOP 5 RANKING", True, (100, 255, 100))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title, title_rect)

        # Cabeçalhos
        header = self.text_font.render("POS   DISTÂNCIA    DATA", True, (200, 200, 200))
        surface.blit(header, (SCREEN_WIDTH // 2 - 180, 160))

        # Lista os scores
        y_offset = 220
        if not scores:
            vazio = self.text_font.render("Nenhuma corrida registrada.", True, (100, 100, 100))
            surface.blit(vazio, (SCREEN_WIDTH // 2 - 180, y_offset))
        else:
            for i, entry in enumerate(scores):
                # Formata a linha (Ex: "1.    1520 m       14/05/2026")
                linha = f"{i+1}.    {entry['score']:<8} m  {entry['date']}"
                
                # Destaca o primeiro lugar em amarelo
                cor = (255, 255, 100) if i == 0 else (255, 255, 255) 
                
                linha_text = self.text_font.render(linha, True, cor)
                surface.blit(linha_text, (SCREEN_WIDTH // 2 - 180, y_offset))
                y_offset += 50

        # Instrução para voltar
        voltar = self.text_font.render("Pressione ESC para voltar", True, (150, 150, 150))
        voltar_rect = voltar.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        surface.blit(voltar, voltar_rect)

    def draw_game_over(self, surface, final_score):
        # Efeito Fade: Cria uma película escura semi-transparente por cima do jogo pausado
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180) # Nível de transparência (0 a 255)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        # Texto GAME OVER
        go_text = self.game_over_font.render("GAME OVER", True, (255, 50, 50))
        go_rect = go_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        surface.blit(go_text, go_rect)

        # Pontuação Final
        score_text = self.text_font.render(f"Distância Final: {int(final_score)} m", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        surface.blit(score_text, score_rect)

        # Instrução de Restart
        current_time = pygame.time.get_ticks()
        if (current_time // 500) % 2 == 0:
            restart_text = self.text_font.render("Pressione ENTER para Tentar Novamente", True, (200, 200, 200))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
            surface.blit(restart_text, restart_rect)