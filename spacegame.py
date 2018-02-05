import pygame
from space_util import *
import entity
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
            self.handle_events(pygame.event.get())
            self.screen.fill((0,0,0))
            for entity in self.all_sprites:
                entity.update(inputs, num)
                self.screen.blit(entity.surf, entity.rect)
                self.screen.blit(self.font.render(entity.text, True, entity.color), (entity.rect[0] + 2, entity.rect[1]))
            pygame.display.flip()
            num = num + 1


class ShipType(Enum):
    CIV = 0
    CARGO = 1
    DESTROYER = 2
    FLEET = 3



class SpaceEntity(pygame.sprite.Sprite):
    
    def __init__(self):
        super(SpaceEntity, self).__init__()
        self.text = "space"
        self.actions = {}


    def update(self, inputs=None, num=0):
        self.surf.fill(self.color)

    def move(self):
        xydelta = np.array((1,2), dtype=np.float32)
        fullarr = np.zeros((1,2), dtype=np.float32)
        for force in self.forces:
            fullarr = np.vstack((fullarr, self.forces[force].get_x_y()))
        np.sum(a=fullarr, axis=0, out=xydelta, dtype=np.float32)
        xaccel = (xydelta[1]/np.float32(self.mass))
        yaccel = (xydelta[0]/np.float32(self.mass))
        self.rect.move_ip(xaccel, yaccel)


class RayMissle(SpaceEntity):

    def __init__(self, forces, color=(255,0,0)):
        super(RayMissle, self).__init__()
        self.surf = pygame.Surface((1,1))
        self.rect = self.surf.get_rect()
        self.color = color
        self.forces = forces
        self.mass = 1.0
        self.explosive_energy = 1.0
        self.explosive_radius = 1.0
        self.text = ("RayMissle")
        
    def move(self):
        super(RayMissle, self).move()
        forceStr = ""
        for force in self.forces:
            forceStr = forceStr + "XV{0} YV{1}".format(self.forces[force].xmagnitude,self.forces[force].ymagnitude)
        self.text = ("RayMissle" + forceStr)


class ShipBase(SpaceEntity):

    def __init__(self, actions):
        super(ShipBase, self).__init__()
        self.surf = pygame.Surface((3,3))
        self.rect = self.surf.get_rect()
        self.energy = 10.0
        self.type = ShipType.CIV
        self.text = (self.type.name)
        self.color = (255,255,255)
        self.actions = actions

        self.mass = 9.0
        self.forces = {"ctrl": Force(0, 1)}

    def update(self, inputs, num):
        super(ShipBase, self).update()
        if inputs[K_UP]:
            self.forces["ctrl"].xmagnitude -= 0.1
        if inputs[K_DOWN]:
            self.forces["ctrl"].xmagnitude += 0.1
        if inputs[K_RIGHT]:
            self.forces["ctrl"].ymagnitude += 0.1
        if inputs[K_LEFT]:
            self.forces["ctrl"].ymagnitude -= 0.1
        
        if inputs[K_SPACE]:
            if self.energy >= 1000:
                event = pygame.event.Event(self.actions["create_entity"], {"entity": RayMissle(self.forces)})
                pygame.event.post(event)
                self.energy = 0
            self.energy += 4




if __name__ == "__main__":
    window = GameInit()
    window.tick()
