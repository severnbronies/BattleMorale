from constants import ASSET_DIRECTORY
from tree import Tree
from character import Character
from spritesheet import SpriteSheet
from constants import ASSET_DIRECTORY
import os.path
import pygame

class Game:
    def __init__(self, screen, start_level):
        self.mood = 0.0
        self.background = None
        self.screen = screen
        self.level = Tree(start_level)
        self.current_action = None
        self.sprite_sheet = SpriteSheet("sprites.png","sprites.yaml")
        self.chracter = Character((0,0), self.sprite_sheet.get_sprite("npc_head_idle"), self.sprite_sheet.get_sprite("npc_body_idle"))

        self.background_dirty = False

    def add_npc_message(self, text):
        pass

    def add_pc_choices(self, choices):
        pass

    def change_npc_sprite(self, head, body):
        pass

    def move_npc(self, pos):
        pass

    def show_phone(self, visible):
        pass

    def change_level(self, name):
        pass

    def wait_click(self):
        pass

    def set_background(self, name):
        image = pygame.image.load(os.path.join(ASSET_DIRECTORY, name)).convert()
        self.background = pygame.transform.scale(image, self.screen.get_size())
        self.background_dirty = True

    def on_event(self, event):
        pass

    def on_update(self, frametime):
        if self.current_action is None:
            self.level.pre_update(self)
        
    def on_render(self, screen):
        if self.background_dirty:
            screen.blit(self.background, (0, 0))
            self.background_dirty = False

        if self.character.dirty:
            # Draw over the character's old position
            screen.blit(self.background, (0, 0), area=self.character.old_bounds())
            # Redraw the character
            self.character.render(screen)
    