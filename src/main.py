import pygame
import sys
import yaml
import os.path
from game import Game
from constants import ASSET_DIRECTORY, BASE_RESOLUTION, SCALE_FACTOR, WINDOW_SIZE

def main():

    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("First Pygame Application")

    config = yaml.load(open(os.path.join(ASSET_DIRECTORY, "global.yaml")))
    game_instance = Game(screen, config)

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