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
from pygame import locals
from player import Player
import gameconstants


class Game(object):

    def __init__(self):
        self.screen_width = 640
        self.screen_height = 480
        self._run_game = True

    def quit(self):
        self._run_game = False

    def handle_events(self):
        events = pygame.event.get()
        vel = [0, 0]
        speed = 3
        for event in events:
            if event.type == locals.QUIT:
                self.quit()
            elif event.type == locals.KEYDOWN:
                if event.key == locals.K_ESCAPE:
                    self.quit()
                elif event.key == locals.K_LEFT:
                    vel[0] -= speed
                elif event.key == locals.K_RIGHT:
                    vel[0] += speed
                elif event.key == locals.K_UP:
                    vel[1] -= speed
                elif event.key == locals.K_DOWN:
                    vel[1] += speed
                elif event.key == locals.K_SPACE:
                    if self._player.is_animation_playing():
                        self._player.stop_animation()
                    else:
                        self._player.start_animation()
            elif event.type == locals.KEYUP:
                if event.key == locals.K_LEFT:
                    vel[0] += speed
                elif event.key == locals.K_RIGHT:
                    vel[0] -= speed
                elif event.key == locals.K_UP:
                    vel[1] += speed
                elif event.key == locals.K_DOWN:
                    vel[1] -= speed

        self._player.add_velocity(vel[0], vel[1])

    def init(self):
        pygame.init()
        self._screen = pygame.display.set_mode([self.screen_width, self.screen_height], pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._player = Player()
        self._bgcolor = [0, 0, 0]

    def update(self):
        self._player.update()

    def render(self, dt):
        self._screen.fill(self._bgcolor)
        self._player.render(self._screen, dt)
        pygame.display.flip()

    def main(self):
        self.init()

        skip_ticks = gameconstants.ticks_per_second / gameconstants.time_step
        next_tick = pygame.time.get_ticks()
        while(self._run_game):

            loops = 0
            while(pygame.time.get_ticks() > next_tick and loops < gameconstants.frameskip_threshold):
                self.handle_events()
                self.update()

                next_tick += skip_ticks
                loops += 1
            dt = float(pygame.time.get_ticks() + skip_ticks - next_tick) / float(skip_ticks)
            self.render(dt)


if __name__ == '__main__':
    game = Game()
    game.main()
