import sys
import os
import pygame
import Structures


class GameWorld(pygame.sprite.Sprite):

    def __init__(self, screen_width, screen_height, fps, object_size, list_coordinates):
        pygame.sprite.Sprite.__init__(self)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fps = fps
        self.object_size = object_size
        self.list_coordinates = list_coordinates
        self.pause = False
        self.bottom_structure = pygame.sprite.Group()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (900, 150)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 0, 32)
        self.clock = pygame.time.Clock()
        pygame.init()

    def run(self):
        self._spawn_initial_blocks()
        ctr = 0
        while ctr < 5:
            if not self.pause:
                pygame.display.flip()
                self.screen.fill((0, 0, 0))
                self._motion()
                self.bottom_structure.draw(self.screen)
                self._process()
                self.clock.tick(self.fps)
            else:
                self.pause_process()

    def _spawn_initial_blocks(self):
        for data in self.list_coordinates:
            for pos in range(0, len(data), 2):
                self.bottom_structure.add(Structures.UnitObject(data[pos], data[pos + 1], "./images/unit_square_01.png"))

    def _process(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause = not self.pause

    def _pause_process(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause = not self.pause

    def _destroy(self, x_pos, y_pos):
        for block in self.bottom_structure:
            if block.rect.x == x_pos and block.rect.y == y_pos:
                self.bottom_structure.remove(block)
                break

    def _block_birth(self, x_pos, y_pos):
        self.bottom_structure.add(Structures.UnitObject(x_pos, y_pos, "./images/unit_square_01.png"))

    def _chk_surrounding(self, x_pos, y_pos, x_y_list):
        live_counter = 0
        living = False

        if ((x_pos-10), (y_pos - 10)) in x_y_list:
            live_counter += 1
        if ((x_pos - 10), y_pos) in x_y_list:
            live_counter += 1
        if ((x_pos - 10), (y_pos + 10)) in x_y_list:
            live_counter += 1
        if (x_pos, (y_pos - 10)) in x_y_list:
            live_counter += 1
        if (x_pos, (y_pos + 10)) in x_y_list:
            live_counter += 1
        if ((x_pos + 10), (y_pos - 10)) in x_y_list:
            live_counter += 1
        if ((x_pos + 10), y_pos) in x_y_list:
            live_counter += 1
        if ((x_pos + 10), (y_pos + 10)) in x_y_list:
            live_counter += 1

        for block in self.bottom_structure:
            if block.rect.x == x_pos and block.rect.y == y_pos:
                living = True
                break

        if living and (live_counter < 2 or live_counter > 3):
            self._destroy(x_pos, y_pos)
        elif not living and live_counter == 3:
            self._block_birth(x_pos, y_pos)

    def _motion(self):
        x_y_list = [(block.rect.x,block.rect.y) for block in self.bottom_structure]

        for x_pos in range(0, self.screen_width, self.object_size):
            for y_pos in range(0, self.screen_width, self.object_size):
                self._chk_surrounding(x_pos, y_pos, x_y_list)
