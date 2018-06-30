from constants import ASSET_DIRECTORY, SCALE_FACTOR
import pygame
import os.path

class SpriteSheet:
    def __init__(self, filename):
        image = pygame.image.load(os.path.join(ASSET_DIRECTORY, filename)).convert()
        self.sheet = pygame.transform.scale(image, image.get_width()* SCALE_FACTOR, image.get_height()* SCALE_FACTOR)

    def get_sprite(self, name):
        pass