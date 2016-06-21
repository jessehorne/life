import math
import random
import pygame
from pygame.locals import *

class Life:
    def __init__(self):
        self._running = True
        self._display_surf = None

        # life init

        self.cells_x = 30
        self.cells_y = 30
        self.cells_size = 1000/self.cells_x

        self.bg_color = (20,11,34)
        self.line_color = (17,29,50)
        self.cells_color = (42,42,126)
        self.cells_color_dark = (42,100,126)

        self.life_mode = "plant"

        self.nodes = []

        for y in xrange(self.cells_y):
            for x in xrange(self.cells_x):
                node = {}
                node["start_x"] = (x * self.cells_size)
                node["start_y"] = (y * self.cells_size)
                node["alive"] = False

                self.nodes.append(node)

        # keys to change self.life_mode
        self.plant_key = pygame.K_ESCAPE
        self.play_key = pygame.K_p

        self.life_time_interval = .1 # seconds in between each generation
        self.life_time_clock = 0

        # end life init

        self.getTicksLastFrame = 0

        self.size = self.width, self.height = (self.cells_x*self.cells_size), (self.cells_y*self.cells_size)

    def find_node(self, start_x, start_y):
        for node in self.nodes:
            if node["start_x"] == start_x and node["start_y"] == start_y:
                return node
                break
        return False

    # will calculate 'gens' generations
    def calc_generation(self, gens):
        for i in xrange(gens):
            alives = []
            deads = []
            for node in self.nodes:
                neighbor_count = 0 # number of alive neighbors for alive cells_y

                # up-left
                up_left = self.find_node(node["start_x"] - self.cells_size, node["start_y"] - self.cells_size)

                if up_left != False:
                    if up_left["alive"] == True:
                        neighbor_count += 1

                # up
                up = self.find_node(node["start_x"], node["start_y"] - self.cells_size)

                if up != False:
                    if up["alive"] == True:
                        neighbor_count += 1

                # up-right
                up_right = self.find_node(node["start_x"] + self.cells_size, node["start_y"] - self.cells_size)

                if up_right != False:
                    if up_right["alive"] == True:
                        neighbor_count += 1

                # left
                left = self.find_node(node["start_x"] - self.cells_size, node["start_y"])

                if left != False:
                    if left["alive"] == True:
                        neighbor_count += 1

                # right
                right = self.find_node(node["start_x"] + self.cells_size, node["start_y"])

                if right != False:
                    if right["alive"] == True:
                        neighbor_count += 1

                # down-left
                down_left = self.find_node(node["start_x"] - self.cells_size, node["start_y"] + self.cells_size)

                if down_left != False:
                    if down_left["alive"] == True:
                        neighbor_count += 1

                # down
                down = self.find_node(node["start_x"], node["start_y"] + self.cells_size)

                if down != False:
                    if down["alive"] == True:
                        neighbor_count += 1

                # down-right
                down_right = self.find_node(node["start_x"] + self.cells_size, node["start_y"] + self.cells_size)

                if down_right != False:
                    if down_right["alive"] == True:
                        neighbor_count += 1

                if node["alive"]:
                    if neighbor_count < 2:
                        deads.append(node)

                    if neighbor_count == 2 or neighbor_count == 3:
                        alives.append(node)

                    if neighbor_count > 3:
                        deads.append(node)
                else:
                    if neighbor_count == 3:
                        alives.append(node)

            for node in self.nodes:
                for alive in alives:
                    if alive == node:
                        node["alive"] = True

                for dead in deads:
                    if dead == node:
                        node["alive"] = False

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)

        pygame.display.set_caption("Life")

        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.life_mode == "plant":
                start_x = math.floor(self.mouse_x/self.cells_size*self.cells_size)
                start_y = math.floor(self.mouse_y/self.cells_size*self.cells_size)

                for node in self.nodes:
                    if node["start_x"] == start_x and node["start_y"] == start_y:
                        node["alive"] = not node["alive"]
                        break

        elif event.type == pygame.KEYUP:
            if event.key == self.plant_key:
                self.life_mode = "plant"
            elif event.key == self.play_key:
                self.life_mode = "play"
            elif event.key == pygame.K_MINUS:
                if self.life_time_interval > 0.0:
                    self.life_time_interval -= 0.1
            elif event.key == pygame.K_EQUALS:
                self.life_time_interval += 0.1
            elif event.key == pygame.K_c:
                for node in self.nodes:
                    node["alive"] = False

        self.font = pygame.font.SysFont("monospace", 15)
    def on_loop(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        t = pygame.time.get_ticks()
        # deltaTime in seconds.
        deltaTime = (t - self.getTicksLastFrame) / 1000.0
        self.getTicksLastFrame = t

        if self.life_mode == "play":
            self.life_time_clock += deltaTime

            # generation clock
            if self.life_time_clock > self.life_time_interval:
                self.calc_generation(1)
                self.life_time_clock = 0

    def on_render(self):
        # background color
        self._display_surf.fill(self.bg_color)

        # draw mouse square
        if self.life_mode == "plant":
            start_x = math.floor(self.mouse_x/self.cells_size)*self.cells_size
            start_y = math.floor(self.mouse_y/self.cells_size)*self.cells_size

            end_x = self.cells_size
            end_y = self.cells_size

            pygame.draw.rect(self._display_surf, self.cells_color_dark, (start_x, start_y, end_x, end_y))

        # draw nodes
        for node in self.nodes:
            if node["alive"]:
                pygame.draw.rect(self._display_surf, self.cells_color, (node["start_x"], node["start_y"], self.cells_size, self.cells_size))

        # grid lines
        for y in xrange(0, self.cells_y-1):
            start_x = 0
            start_y = y * self.cells_size + self.cells_size

            end_x = self.height
            end_y = y * self.cells_size + self.cells_size

            pygame.draw.line(self._display_surf, self.line_color, (start_x, start_y), (end_x, end_y), 1)

        for x in xrange(0, self.cells_x-1):
            start_x = x * self.cells_size + self.cells_size
            start_y = 0

            end_x = x * self.cells_size + self.cells_size
            end_y = self.width

            pygame.draw.line(self._display_surf, self.line_color, (start_x, start_y), (end_x, end_y), 1)

        # print details to screen
        speed_label = self.font.render("[-, +] Speed = {} seconds".format(self.life_time_interval), 1, (255, 255, 255))
        self._display_surf.blit(speed_label, (20, 20))

        mode_label = self.font.render("['p' for Play, 'escape' for 'Plant'] Mode = {}".format(self.life_mode.capitalize()), 1, (255, 255, 255))
        self._display_surf.blit(mode_label, (20, 40))

        clear_label = self.font.render("['c' to clear]", 1, (255, 255, 255))
        self._display_surf.blit(clear_label, (20, 60))

        # update display
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__":
    life = Life()
    life.on_execute()
