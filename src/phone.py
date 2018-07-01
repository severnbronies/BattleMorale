LINE_SPACING = -2

import pygame
from collections import namedtuple
from constants import SCALE_FACTOR

BubbleSprites = namedtuple("BubbleSprites","top_left, top_right, bottom_left, bottom_right, top, bottom, left, right, center")
BubbleConfig = namedtuple("BubbleConfig","margin_left, margin_right, margin_top, margin_bottom, sprites")
def _from_dict(dict,sprite_sheet):
    mdict = dict.copy()
    masterSprite = sprite_sheet.get_sprite(mdict["sprites"])
    width,height = masterSprite.get_size()
    halfWidth,halfHeight=width//2,height//2
    
    mdict["sprites"] = BubbleSprites(
        top_left = masterSprite.subsurface((0,0,halfWidth,halfHeight)),
        top_right = masterSprite.subsurface((width-halfWidth,0,halfWidth,halfHeight)),
        bottom_left = masterSprite.subsurface((0,height-halfHeight,halfWidth,halfHeight)),
        bottom_right = masterSprite.subsurface((width-halfWidth,height-halfHeight,halfWidth,halfHeight)),
        top = masterSprite.subsurface((halfWidth,0,1,halfHeight)),
        bottom = masterSprite.subsurface((halfWidth,height-halfHeight,1,halfHeight)),
        left = masterSprite.subsurface((0,halfHeight,halfWidth,1)),
        right = masterSprite.subsurface((width-halfWidth,halfHeight,halfWidth,1)),
        center = masterSprite.subsurface((width-halfWidth,height-halfHeight,1,1))
    )
    return BubbleConfig(**mdict)

BubbleConfig.from_dict = _from_dict


class Message:
    interactable = False
    font = None
    sprites = None
    margin_left = None
    margin_right = None
    margin_top = None
    margin_bottom = None
    max_text_width = None

    def __init__(self,text):
        self.splitText(text)
        self.surface = self.pre_render()

    def splitText(self,text):
        self.lines = []
        self.line_space = self.font.size("Tg")[1] + LINE_SPACING
        self.text_height = -LINE_SPACING
        self.text_width = 0

        max_text_width = self.max_bubble_width-self.margin_left-self.margin_right
        while text:
            i = 1
            # determine maximum width of line
            line_width = self.font.size(text[:i])[0]
            while line_width < max_text_width and i < len(text):
                i += 1
                line_width = self.font.size(text[:i])[0]
            # if we've wrapped the text, then adjust the wrap to the last word      
            if i < len(text): 
                i = text.rfind(" ", 0, i) + 1

            self.lines.append(text[:i])
            self.text_height += self.line_space
            if self.text_width < line_width:
                self.text_width = line_width
            text = text[i:]
    
    def pre_render(self):
        total_width = self.text_width + self.margin_left + self.margin_right
        total_height = self.text_height + self.margin_top + self.margin_bottom

        if total_width < self.bubble_min_width:
            total_width = self.bubble_min_width
        if total_height < self.bubble_min_height:
            total_height = self.bubble_min_height

        x1,y1 = self.sprites.top_left.get_size()
        right_width,bottom_height = self.sprites.bottom_right.get_size()
        x2 = total_width-right_width
        y2 = total_height-bottom_height

        surface = pygame.Surface((total_width,total_height), pygame.SRCALPHA, 32)

        surface.blit(self.sprites.top_left,(0,0))
        surface.blit(self.sprites.top_right,(x2,0))
        surface.blit(self.sprites.bottom_left,(0,y2))
        surface.blit(self.sprites.bottom_right,(x2,y2))

        top_subsurface = surface.subsurface((x1,0,x2-x1,y1))
        bottom_subsurface = surface.subsurface((x1,y2,x2-x1,bottom_height))
        left_subsurface = surface.subsurface((0,y1,x1,y2-y1))
        right_subsurface = surface.subsurface((x2,y1,right_width,y2-y1))
        center_subsurface = surface.subsurface((x1,y1,x2-x1,y2-y1))
 
        pygame.transform.scale(self.sprites.top,top_subsurface.get_size(),top_subsurface)
        pygame.transform.scale(self.sprites.bottom,bottom_subsurface.get_size(),bottom_subsurface)
        pygame.transform.scale(self.sprites.left,left_subsurface.get_size(),left_subsurface)
        pygame.transform.scale(self.sprites.right,right_subsurface.get_size(),right_subsurface)
        pygame.transform.scale(self.sprites.center,center_subsurface.get_size(),center_subsurface)

        y = self.margin_top
        for line in self.lines:
            textRender = self.font.render(line,False,self.color)
            surface.blit(textRender,(self.margin_left,y))
            y += self.line_space

        return surface
    
    @classmethod
    def factory(cls, name, *mixins, **options):
        subtype = type(name, mixins+(cls,), options)
        w,h = options["sprites"].top_left.get_size()

        subtype.bubble_min_width = w*2
        subtype.bubble_min_height = h*2
        return subtype

class ChoiceMixin:
    interactable = True

    def __init__(self,text,key):
        super().__init__(text)
        self.key = key
    
    def get_bounds(self):
        return pygame.Rect(self.x,self.y,*self.surface.get_size())

class Phone:
    def __init__(self,font,phone_sprite,keyboard_back_sprite,bubbles_bottom,pc_bubble_config,npc_bubble_config,choice_config,bubble_margin):
        max_bubble_width = phone_sprite.get_size()[0]-bubble_margin*2

        self.PcMessage = Message.factory("PcMessage",
            font = font,
            sprites = pc_bubble_config.sprites,
            margin_left = pc_bubble_config.margin_left*SCALE_FACTOR,
            margin_right = pc_bubble_config.margin_right*SCALE_FACTOR,
            margin_top = pc_bubble_config.margin_top*SCALE_FACTOR,
            margin_bottom = pc_bubble_config.margin_bottom*SCALE_FACTOR,
            max_bubble_width = max_bubble_width,
            color = (0,0,0),
            align = "RIGHT"
        )

        self.NpcMessage = Message.factory("NpcMessage",
            font = font,
            sprites = npc_bubble_config.sprites,
            margin_left = npc_bubble_config.margin_left*SCALE_FACTOR,
            margin_right = npc_bubble_config.margin_right*SCALE_FACTOR,
            margin_top = npc_bubble_config.margin_top*SCALE_FACTOR,
            margin_bottom = npc_bubble_config.margin_bottom*SCALE_FACTOR,
            max_bubble_width = max_bubble_width,
            color = (0,0,0),
            align = "LEFT"
        )

        self.Choice = Message.factory("Choice",ChoiceMixin,
            font = font,
            sprites = choice_config.sprites,
            margin_left = choice_config.margin_left*SCALE_FACTOR,
            margin_right = choice_config.margin_right*SCALE_FACTOR,
            margin_top = choice_config.margin_top*SCALE_FACTOR,
            margin_bottom = choice_config.margin_bottom*SCALE_FACTOR,
            max_bubble_width = max_bubble_width,
            color = (0,0,0),
            align = "CENTER"
        )

        self.sprite = phone_sprite
        self.keyboard_back_sprite = keyboard_back_sprite
        self.bubbles_bottom = bubbles_bottom
        self.bubble_margin = bubble_margin

        self.x = 320*SCALE_FACTOR - self.sprite.get_size()[0]
        self.y = 0

        self.messages = []
        self.options = []
        self.dirty = True

        self.screen_top = 25*SCALE_FACTOR

    def get_bounds(self):
        w,h = self.sprite.get_size()
        return pygame.Rect(self.x,self.y,w,h)

    def add_npc_message(self, text):
        self.messages.append(self.NpcMessage(text))

    def add_pc_message(self, text):
        self.messages.append(self.PcMessage(text))

    def add_pc_choices(self, choices):
        self.options = [self.Choice(text,key=key) for (key,text) in choices.items()]

    def render_message(self, message, surface, width, height, bubble_y):
        bubble_width, bubble_height = message.surface.get_size()
        bubble_y -= bubble_height + SCALE_FACTOR #TODO CONST: bubble vertical gap
        if bubble_y < self.screen_top:
            return (None,None)
        if message.align == "RIGHT":
            bubble_x = width - self.bubble_margin - bubble_width
        elif message.align == "CENTER":
            bubble_x = (width - bubble_width)/2
        else: #default LEFT
            bubble_x = self.bubble_margin
        
        surface.blit(message.surface,(self.x+bubble_x, self.y+bubble_y))   
        return bubble_x, bubble_y    

    def render(self, surface):
        if not self.dirty:
            return
        surface.blit(self.sprite,(self.x,self.y))
        width, height = self.sprite.get_size()
        bubble_y = height - self.bubbles_bottom

        keyboard_height = sum(m.surface.get_size()[1]+SCALE_FACTOR for m in self.options)
        if keyboard_height > 0:
            keyboard_height += SCALE_FACTOR*3
            keyboard_width = self.keyboard_back_sprite.get_size()[0]
            keyboard_y = height - self.bubbles_bottom - keyboard_height + self.y
            keyboard_x = 8*SCALE_FACTOR + self.x
            surface.blit(self.keyboard_back_sprite, (keyboard_x,keyboard_y), (0,0,keyboard_width,keyboard_height))

        for message in self.options[::-1]:
            bubble_x,bubble_y = self.render_message(message,surface,width,height,bubble_y)
            message.x = bubble_x
            message.y = bubble_y

        bubble_y -= SCALE_FACTOR*5

        for message in self.messages[::-1]:
            bubble_x,bubble_y = self.render_message(message,surface,width,height,bubble_y)
            if bubble_y is None:
                return
    
    def on_click_return_key(self,x,y):
        key = None
        for message in self.options:
            if message.get_bounds().collidepoint(x,y):
                key = message.key
                break
        if key is not None:
            self.options = []
        return key
        
            