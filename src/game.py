from constants import ASSET_DIRECTORY
from tree import Tree
from character import Character
from spritesheet import SpriteSheet
from constants import ASSET_DIRECTORY
import os.path
import math
import pygame



class MoveNpcAction:
    def __init__(self, start, dest, speed):
        self.start = start
        self.dest = dest
        distance = math.sqrt((start[0]-dest[0])**2 + (start[1]-dest[1])**2)
        self.duration = distance/speed
        self.progress = 0.0
        self.finished = None

    def run(self, game, timestep):
        self.progress += timestep/1000

        percentage = self.progress/self.duration
        if percentage >= 1.0:
            percentage = 1.0
            self.finished = True
        x = self.start[0]*(1.0-percentage) + self.dest[0]*(percentage)
        y = self.start[1]*(1.0-percentage) + self.dest[1]*(percentage)
        game.character.move((x, y))
        return self.finished

class PcChoicesAction:
    def __init__(self, choices):
        self.choices = choices
        self.response = None

    def set_response(self, response):
        self.response = response

    def run(self, game, timestep):
        if self.response is None:
            return None
        return list(self.choices.keys())[0]


class Game:
    def __init__(self, screen, config):
        self.mood = 0.0
        self.screen = screen
        self.level = Tree(config["start-level"])
        self.current_action = None
        self.sprite_sheet = SpriteSheet("sprites.png","sprites.yaml")
        self.background = self.sprite_sheet.get_sprite("")
        self.character = Character((-20,0), self.sprite_sheet.get_sprite("npc_head_happier"), self.sprite_sheet.get_sprite("npc_body_idle"))

        self.win_mood = config["win-mood"]
        self.lose_mood = config["lose-mood"]

    def add_npc_message(self, text):
        self.level.post_update(None)

    def add_pc_message(self, text):
        self.level.post_update(None)

    def add_pc_choices(self, choices):
        self.current_action = PcChoicesAction(choices)

    def change_npc_sprite(self, head=None, body=None):
        if head is not None:
            self.character.set_head(self.sprite_sheet.get_sprite(head))
        if body is not None:
            self.character.set_body(self.sprite_sheet.get_sprite(body))
        self.level.post_update(None)

    def move_npc(self, x, y, speed=50.0):
        if speed == 0.0:
            self.character.move((x, y))
            self.level.post_update(None)
        else:
            self.current_action = MoveNpcAction(self.character.position, (x, y), speed)


    def change_npc_mood(self, delta):
        self.character.mood += delta
        self.level.post_update(None)

    def change_level(self, name):
        self.character.move((-20, 0))
        self.level = Tree(name)

    def wait_click(self):
        pass

    def set_background(self, name):
        image = pygame.image.load(os.path.join(ASSET_DIRECTORY, name)).convert()
        self.background = pygame.transform.scale(image, self.screen.get_size())
        self.background_dirty = True
        self.level.post_update(None)

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if isinstance(self.current_action, PcChoicesAction):
                self.current_action.set_response("aaaaa") #TODO link this with the phone rendering

    def on_update(self, frametime):
        if self.current_action is None:
            self.level.pre_update(self)
        else:
            result = self.current_action.run(self, frametime)
            if result is not None:
                self.current_action = None
                self.level.post_update(result)
        
    def on_render(self, screen):
        screen.blit(self.background, (0, 0))
        self.character.render(screen)
    