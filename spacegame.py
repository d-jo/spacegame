import pygame
import os, sys
from pygame.locals import *
import numpy as np
from enum import Enum


print("font,", (None != pygame.font))
print("audio,", (None != pygame.mixer))

class GameInit:

    def __init__(self, width=640, height=480):
        pygame.init()
        self.dimensions = (width, height)
        self.screen = pygame.display.set_mode(self.dimensions)
        self.all_sprites = pygame.sprite.Group()
        self.player = pygame.sprite.Group()
        self.all_sprites.add(ShipBase())
        self.MOVETICK = pygame.USEREVENT + 1
        pygame.time.set_timer(self.MOVETICK, 10)
    
    def handle_events(self, events):
        for event in events:
            if event.type == self.MOVETICK:
                for entity in self.all_sprites:
                    entity.move()
            if event.type == pygame.QUIT:
                sys.exit()

            
    def tick(self):
        num = 0
        while 1:
            inputs = pygame.key.get_pressed()
            self.handle_events(pygame.event.get())
            self.screen.fill((0,0,0))
            for entity in self.all_sprites:
                entity.update(inputs, num)
                self.screen.blit(entity.surf, entity.rect)
            pygame.display.flip()
            num = num + 1


class ShipType(Enum):
    CIV = 0
    CARGO = 1
    DESTROYER = 2
    FLEET = 3

class Force:
    
    # IN RADIANS!!!
    # REMEMBER THIS!!
    def __init__(self, magnitude, angle):
        self.magnitude = magnitude
        self.angle = angle

    def get_x_y(self):
        return np.multiply(self.magnitude, (np.cos(self.angle), np.sin(self.angle)))

class ShipBase(pygame.sprite.Sprite):

    def __init__(self):
        super(ShipBase, self).__init__()
        self.surf = pygame.Surface((10,10))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.type = ShipType.CIV
        self.mass = 10.0
        self.forces = [Force(0, 0)]

    def update(self, inputs, num):
        if inputs[K_UP]:
            self.forces[0].magnitude += 0.1
        if inputs[K_DOWN]:
            self.forces[0].magnitude -= 0.1


    def move(self):
        xydelta = np.array((1,2), dtype=np.float32)
        fullarr = np.zeros((1,2), dtype=np.float32)
        for force in self.forces:
            fullarr = np.vstack((fullarr, force.get_x_y()))
        
        np.sum(a=fullarr, axis=1, out=xydelta, dtype=np.float32)
        xaccel = (xydelta[0]/np.float32(self.mass))
        yaccel = (xydelta[1]/np.float32(self.mass))
        self.rect.move_ip(xaccel, yaccel)


if __name__ == "__main__":
    window = GameInit()
    window.tick()
