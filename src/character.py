from constants import ASSET_DIRECTORY, SCALE_FACTOR
import pygame

class Character:
    def __init__(self, position, head, body, body_walk_cycle):
        self.position = position
        self.old_position = position
        self.set_head(head)
        self.set_body(body)
        self.mood = 0
        self.mood_changed = False
        self.body_walk_cycle = body_walk_cycle
        self.body_no_walk = body

    def set_walk_frame(self,index):
        index = index % len(self.body_walk_cycle)
        self.set_body(self.body_walk_cycle[index])
    
    def set_body_no_walk(self):
        self.set_body(self.body_no_walk)

    def set_head(self, head):
        self.head = head
        self.dirty = True

    def set_body(self, body):
        self.body = body
        self.dirty = True

    def move(self, pos):
        self.old_position = self.position
        self.position = pos
        self.dirty = True

    @property
    def mood(self):
        return self._mood

    @mood.setter
    def mood(self, value):
        self._mood = value
        self.mood_changed = True

    def old_bounds(self):
        return pygame.Rect(self.old_position, self.head.get_size())

    def new_bounds(self):
        return pygame.Rect(self.position, self.head.get_size())

    def render(self, surface):
        x = int(self.position[0]*SCALE_FACTOR)
        y = int(self.position[1]*SCALE_FACTOR)
        surface.blit(self.body, (x, y))
        surface.blit(self.head, (x, y))
