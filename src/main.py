import pygame
import sys
from utils import get_yaml
from game import Game
from constants import WINDOW_SIZE


def main():

    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Battle Morale")

    config = get_yaml("global.yaml")
    game_instance = Game(screen, config)
    game_instance.play_music(config["default-music"])

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