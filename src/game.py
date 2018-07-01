from tree import Tree
from character import Character
from spritesheet import SpriteSheet
from constants import ASSET_DIRECTORY,SCALE_FACTOR
import os.path
import math
import pygame
from phone import Phone, BubbleConfig

class MoveNpcAction:
    def __init__(self, start, dest, speed):
        self.start = start
        self.dest = dest
        distance = math.sqrt((start[0]-dest[0])**2 + (start[1]-dest[1])**2)
        self.duration = distance/speed
        self.progress = 0.0
        self.finished = None
        self.ani_speed = speed//2

    def run(self, game, timestep):
        if self.duration == 0:
            return True
        self.progress += timestep/1000

        percentage = self.progress/self.duration
        if percentage >= 1.0:
            percentage = 1.0
            self.finished = True
        x = self.start[0]*(1.0-percentage) + self.dest[0]*(percentage)
        y = self.start[1]*(1.0-percentage) + self.dest[1]*(percentage)
        game.character.move((x, y))
        frame_index = int(self.progress*self.ani_speed)
        game.character.set_walk_frame(frame_index)

        if self.finished is not None:
            game.character.set_body_no_walk()

        return self.finished


class PcChoicesAction:
    def __init__(self):
        self.response = None

    def set_response(self, response):
        self.response = response

    def run(self, game, timestep):
        return self.response


class DelayAction:
    def __init__(self, duration):
        self.duration = duration
        self.progress = 0.0

    def run(self, game, timestep):
        self.progress += timestep / 1000

        percentage = self.progress / self.duration
        if percentage > 1.0:
            return True
        else:
            return None


class TextDelayAction(DelayAction):
    def __init__(self, text):
        super().__init__(len(text) * 0.05)


class Game:
    def __init__(self, screen, config):
        self.screen = screen
        self.global_nodes = config["global-nodes"]
        self.level = Tree(config["start-level"], self.global_nodes)
        self.current_action = None
        self.sprite_sheet = SpriteSheet("sprites.png","sprites.yaml")
        self.background = self.sprite_sheet.get_sprite(os.path.join(ASSET_DIRECTORY, config["default-background"]))
        self.character = Character(
            (-20,0), 
            self.sprite_sheet.get_sprite("npc_head_happier"),
            self.sprite_sheet.get_sprite("npc_body_idle"),
            [
                self.sprite_sheet.get_sprite("npc_body_walk_1"),
                self.sprite_sheet.get_sprite("npc_body_idle"),
                self.sprite_sheet.get_sprite("npc_body_walk_2"),
                self.sprite_sheet.get_sprite("npc_body_idle")
            ]
        )

        self.notification_sound = pygame.mixer.Sound(os.path.join(ASSET_DIRECTORY, config["notification-sound"]))
        self.notification_sound.set_volume(0.4)

        self.mood_high = config["mood-thresholds"]["max"]
        self.mood_low = config["mood-thresholds"]["min"]
        self.mood_sprites = config["mood-sprites"]

        self.font = pygame.font.Font(os.path.join(ASSET_DIRECTORY, config["font"]["file"]),config["font"]["size"]*SCALE_FACTOR)

        self.phone = Phone(
            self.font,
            self.sprite_sheet.get_sprite("phone"),
            self.sprite_sheet.get_sprite("phone-keyboard"),
            16*SCALE_FACTOR,
            BubbleConfig.from_dict(config["pc-bubbles"],self.sprite_sheet),
            BubbleConfig.from_dict(config["npc-bubbles"],self.sprite_sheet),
            BubbleConfig.from_dict(config["choice-buttons"],self.sprite_sheet),
            10*SCALE_FACTOR
        )

    def add_npc_message(self, text):
        self.phone.add_npc_message(text)
        self.notification_sound.play()
        self.current_action = TextDelayAction(text)

    def add_pc_message(self, text):
        self.phone.add_pc_message(text)
        self.current_action = TextDelayAction(text)

    def add_pc_choices(self, choices):
        self.current_action = PcChoicesAction()
        self.phone.add_pc_choices(choices)

    def change_npc_sprite(self, head=None, body=None):
        if head is not None:
            self.character.set_head(self.sprite_sheet.get_sprite(head))
            if head == "npc_head_idle":
                self.character.mood_changed = True
        if body is not None:
            self.character.set_body(self.sprite_sheet.get_sprite(body))
        self.level.post_update(None)

    def move_npc(self, x=None, y=None, speed=50.0):
        if x is None:
            x = self.character.position[0]
        if y is None:
            y = self.character.position[1]
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
        self.level = Tree(name, self.global_nodes)

    def wait_click(self):
        pass

    def set_node(self, name):
        self.level.set_node(name)

    def set_background(self, file):
        image = pygame.image.load(os.path.join(ASSET_DIRECTORY, file)).convert()
        self.background = pygame.transform.scale(image, self.screen.get_size())
        self.background_dirty = True
        self.level.post_update(None)

    def play_music(self, name):
        pygame.mixer.music.load(os.path.join(ASSET_DIRECTORY, name))
        pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()

    def clear_phone(self):
        self.phone.messages = []
        self.level.post_update(None)

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if isinstance(self.current_action, PcChoicesAction):
                x,y = event.pos
                if self.phone.get_bounds().collidepoint(x,y):
                    collision_key = self.phone.on_click_return_key(x-self.phone.x,y-self.phone.y)
                    if collision_key is not None:
                        self.current_action.set_response(collision_key)

    def on_update(self, frametime):
        if self.current_action is None:
            if self.character.mood >= self.mood_high:
                self.character.mood = 0
                self.level.set_node('mood_too_high')
            elif self.character.mood <= self.mood_low:
                self.character.mood = 0
                self.level.set_node('mood_too_low')
            if self.character.mood_changed:
                print("current mood:", self.character.mood)
                for limit, sprite in self.mood_sprites.items():
                    if self.character.mood <= limit:
                        self.character.set_head(self.sprite_sheet.get_sprite(sprite))
                        break
                self.character.mood_changed = False
            self.level.pre_update(self)
        else:
            result = self.current_action.run(self, frametime)
            if result is not None:
                self.current_action = None
                self.level.post_update(result)
        
    def on_render(self, screen):
        screen.blit(self.background, (0, 0))
        self.character.render(screen)
        self.phone.render(screen)

