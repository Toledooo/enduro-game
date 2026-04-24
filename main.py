import pygame
import sys
from src.core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, BLACK, DARK_GRAY
from src.entities.track import Track

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Enduro Game")
    clock = pygame.time.Clock()

    track = Track()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False


        screen.fill(DARK_GRAY)
        track.draw(screen)

        pygame.display.flip() # Atualiza a tela
        clock.tick(FPS) # Controla a taxa de quadros por segundo

    # Encerra o Pygame e sai do programa
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()