import spacegame
import pygame
import util

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
