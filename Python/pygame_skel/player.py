# -*- coding: utf-8 -*-
'''
Copyright (c) 2013 Victor Wåhlström

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

   1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.

   2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.

   3. This notice may not be removed or altered from any source
   distribution.
'''

import pygame
import gameconstants


class Player(object):

    def __init__(self):

        self._image = pygame.image.load("test_spritemap.png").convert()
        self._sprite_size = 128

        self._vel = [0, 0]
        self._pos = [0, 0]

        self._anim_pos = 0
        self._anim_paused = False

        self.set_anim_fps(0.5)

        self._anim_update_diff = 0
        self._time_since_last_anim_update = pygame.time.get_ticks()

        rect = self._image.get_rect()
        self._num_sprites_width = rect.width / self._sprite_size
        self._num_sprites_height = rect.height / self._sprite_size
        self._num_sprites = self._num_sprites_width * self._num_sprites_height

    def set_anim_fps(self, fps):
        self._anim_fps = fps

    def get_position(self):
        return self._pos

    def set_position(self, x, y):
        self._pos = (x, y)

    def add_velocity(self, x, y):
        self._vel[0] += x
        self._vel[1] += y

    def stop_animation(self):
        self._anim_paused = True

    def start_animation(self):
        self._anim_paused = False

    def is_animation_playing(self):
        return not self._anim_paused

    def set_velocity(self, x, y):
        self._vel = (x, y)

    def update(self):
        self._pos[0] += self._vel[0]
        self._pos[1] += self._vel[1]

        cur_ticks = pygame.time.get_ticks()
        anim_diff = (cur_ticks - self._time_since_last_anim_update) / float(gameconstants.ticks_per_second) + self._anim_update_diff - self._anim_fps
        if anim_diff > 0:
            self._time_since_last_anim_update = cur_ticks
            if not self._anim_paused:
                self._anim_pos += int(anim_diff) + 1
                self._anim_update_diff = anim_diff - int(anim_diff)
                if self._anim_pos >= self._num_sprites:
                    self._anim_pos -= self._num_sprites

    def render(self, surface, dt):
        x = self._pos[0] + self._vel[0] * dt
        y = self._pos[1] + self._vel[1] * dt
        ssize = self._sprite_size
        aposx = (self._anim_pos % self._num_sprites_width) * ssize
        aposy = int(self._anim_pos / self._num_sprites_width) * ssize

        anim_coords = (aposx, aposy, ssize, ssize)
        surface.blit(self._image, (x, y), anim_coords)
