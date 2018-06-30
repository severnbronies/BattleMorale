import pygame
from game import Game

def main():
    game_instance = Game()

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("First Pygame Application")

    clock = pygame.time.Clock()
    while True:
        frametime = clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            else:
                game_instance.on_event(event)

        game_instance.on_update(frametime)
        game_instance.on_render(screen)

        pygame.display.flip()



if __name__ == '__main__':
    main()