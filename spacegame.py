import pygame, math
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
        self.SELECTION = pygame.USEREVENT + 3
        self.UNSELECTION = pygame.USEREVENT + 4

        self.selected_group = pygame.sprite.Group()
        self.selection_rect = pygame.Rect(0,1,2,3)
        self.dragging = False

        self.font = pygame.font.SysFont("Hack", 12)
        self.player = pygame.sprite.Group()
        self.all_sprites.add(ShipBase({"create_entity": self.CREATE_ENTITY}))
        pygame.time.set_timer(self.MOVETICK, 500)
    
    def handle_events(self, events):
        for event in events:
            if event.type == self.MOVETICK:
                for entity in self.all_sprites:
                    entity.move()
            elif event.type == self.CREATE_ENTITY:
                self.all_sprites.add(event.entity)
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION:
                self.selection(event)
            elif event.type == self.SELECTION:
                for spr in event.group:
                    spr.selected(event.pos, event.button)
            elif event.type == self.UNSELECTION:
                print("unselect group", event.group)
                for spr in event.group:
                    spr.unselected(event.pos, event.button)
            elif event.type == pygame.QUIT:
                sys.exit()

    def selection(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button >= 0:
                localref = self.selected_group
                unselectevent = pygame.event.Event(self.UNSELECTION, {"group": localref.copy(), "pos": event.pos, "button": event.button})
                self.selected_group.empty()
                pygame.event.post(unselectevent)
                self.dragging = True
                mx, my = event.pos
                self.selection_rect.x = mx
                self.selection_rect.y = my
                self.selection_rect.w = 0
                self.selection_rect.h = 0
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button >= 0:
                self.dragging = False
                group = pygame.sprite.Group()
                for sprite in self.all_sprites:
                    print(sprite.rect)
                    print(self.selection_rect)
                    testrect = self.selection_rect.copy()
                    if testrect.w < 0:
                        testrect.x = testrect.x + testrect.w
                        testrect.w = -testrect.w
                    if testrect.h < 0:
                        testrect.y = testrect.y + testrect.h
                        testrect.h = -testrect.h
                    if testrect.colliderect(sprite.rect):
                        group.add(sprite)
                        #sprite.selected(event.pos, 1)

                print(group.sprites)
                select_event = pygame.event.Event(self.SELECTION, {"group": group, "pos": event.pos, "button": event.button})
                self.selected_group = group.copy()
                print("-----",self.selected_group)
                pygame.event.post(select_event)
                




                
                
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mx, my = event.pos
                dx = self.selection_rect.x - mx
                dy = self.selection_rect.y - my
                self.selection_rect.w = -dx
                self.selection_rect.h = -dy


            
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

            if self.dragging:
                su_rect = self.selection_rect.copy()
                su = pygame.Surface((math.fabs(su_rect.w), math.fabs(su_rect.h)))
                su.fill((0,222,222))
                su.set_alpha(100)
                dx = 0 + (su_rect.x)
                dy = 0 + (su_rect.y)
                if su_rect.w < 0:
                    dx = dx + su_rect.w
                if su_rect.h < 0:
                    dy = dy + su_rect.h
                self.screen.blit(su, (dx,dy))
            pygame.display.flip()
            num = num + 1



if __name__ == "__main__":
    window = GameInit()
    window.tick()
