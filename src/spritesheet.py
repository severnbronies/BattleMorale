from constants import ASSET_DIRECTORY, SCALE_FACTOR
import pygame
import os.path
import yaml

class SpriteSheet:
    def __init__(self, sheet_filename, config_filename):
        image = pygame.image.load(os.path.join(ASSET_DIRECTORY, sheet_filename)).convert()
        self.sheet = pygame.transform.scale(image, image.get_width()* SCALE_FACTOR, image.get_height()* SCALE_FACTOR)

        with open(os.path.join(ASSET_DIRECTORY,config_filename)) as config:
            self.config = yaml.load(config)

    def get_sprite(self, name):
        sprite_config = self.config[name]
        left = sprite_config["left"] * SCALE_FACTOR
        top = sprite_config["top"] * SCALE_FACTOR
        width = sprite_config["width"] * SCALE_FACTOR
        height = sprite_config["height"] * SCALE_FACTOR
        return self.sheet.subsurface((left, top, width, height))