import pygame
import sys
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, DARK_GRAY
from src.entities.track import Track
from src.entities.player import Player

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Enduro Game")
    clock = pygame.time.Clock()

    track = Track()
    player = Player()
    track.speed = 2 # Velocidade inicial da estrada
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.move_right()
        
        track.update()
        track_rect = track.draw(screen)
        player_rect = player.draw(screen)

        pygame.display.flip() # Atualiza a tela
        clock.tick(FPS) # Controla a taxa de quadros por segundo

    # Encerra o Pygame e sai do programa
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()