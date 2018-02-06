import pygame
from space_util import *
from entity import *
import os, sys
from pygame.locals import *
import numpy as np
from enum import Enum


print("font,", (None != pygame.font))
print("audio,", (None != pygame.mixer))

class GameInit:

    def __init__(self, width=640, height=480):
        pygame.init()
        pygame.time.Clock().tick(60)
        self.dimensions = (width, height)
        self.screen = pygame.display.set_mode(self.dimensions)
        self.all_sprites = pygame.sprite.Group()
        self.MOVETICK = pygame.USEREVENT + 1
        self.CREATE_ENTITY = pygame.USEREVENT + 2
        self.font = pygame.font.SysFont("Hack", 12)
        self.player = pygame.sprite.Group()
        self.all_sprites.add(ShipBase({"create_entity": self.CREATE_ENTITY}))
        pygame.time.set_timer(self.MOVETICK, 500)
    
    def handle_events(self, events):
        for event in events:
            if event.type == self.MOVETICK:
                for entity in self.all_sprites:
                    entity.move()
            if event.type == self.CREATE_ENTITY:
                self.all_sprites.add(event.entity)
            if event.type == pygame.QUIT:
                sys.exit()

            
    def tick(self):
        num = 0
        while 1:
            inputs = pygame.key.get_pressed()
            events = pygame.event.get()
            self.handle_events(events)
            self.screen.fill((0,0,0))
            for entity in self.all_sprites:
                entity.update(events, inputs, num)
                self.screen.blit(entity.surf, entity.rect)
                self.screen.blit(self.font.render(entity.text, True, entity.color), (entity.rect[0] + 2, entity.rect[1]))
            pygame.display.flip()
            num = num + 1



if __name__ == "__main__":
    window = GameInit()
    window.tick()
