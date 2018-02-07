import space_util
import math
from pygame.locals import *
import pygame
import spacegame
from enum import Enum
import numpy as np
import pygame

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
        self.surf = pygame.Surface((3,3))

    def update(self, events=None, inputs=None, num=0):
        self.surf.fill(self.color)

    def selected(self, click_pos, button):
        self.rect.inflate_ip(20, 20)
        self.surf = pygame.transform.scale(self.surf, (int(math.fabs(self.rect.w)), int(math.fabs(self.rect.h))))

    def unselected(self, click_pos, button):
        self.rect.inflate_ip(-20,-20)
        self.surf = pygame.transform.scale(self.surf, (int(math.fabs(self.rect.w)), int(math.fabs(self.rect.h))))

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

    def __init__(self, force, start=(0,0), color=(255,0,0)):
        super(RayMissle, self).__init__()
        self.surf = pygame.Surface((1,1))
        self.rect = self.surf.get_rect()
        self.rect.move(start[0], start[1])
        self.color = color
        self.forces = {"base": force}
        self.mass = 1.0
        self.explosive_energy = 1.0
        self.explosive_radius = 1.0
        self.text = ("RayMissle")
        
    def move(self):
        super(RayMissle, self).move()
        self.text = ("RayMissle " + self.explosive_energy)


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
        self.forces = {"ctrl": space_util.Force(0, 0)}


    def update(self, events, inputs, num):
        super(ShipBase, self).update()
        if inputs[K_UP]:
            self.forces["ctrl"].xmagnitude -= 0.1
        if inputs[K_DOWN]:
            self.forces["ctrl"].xmagnitude += 0.1
        if inputs[K_RIGHT]:
            self.forces["ctrl"].ymagnitude += 0.1
        if inputs[K_LEFT]:
            self.forces["ctrl"].ymagnitude -= 0.1

        
