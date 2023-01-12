import pygame
import sys
import random
from pygame.locals import *

width = 1000
height = 800

class Particle:
    def __init__(self, x_start=0, y_start=0):
        self.color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.size = random.randint(2, 10)
        if x_start == 0 and y_start == 0:
            self.position_x = int(width / 2)
            self.position_y = int(height / 2)
        else:
            self.position_x = x_start
            self.position_y = y_start
        self.velocity_x = random.randint(0, 20) / 10 - 1
        self.velocity_y = - random.randint(10, 20) / 10 - 1                                #prema gore
        self.time = 0

def main():

    mainClock = pygame.time.Clock()
    pygame.init()
    display = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Racunalna animacija: 2. laboratorijska vjezba")

    particles = []
    step_size = -0.02
    step_velocity = 0.02
    step_time = 0.02
    x_start, y_start = 0, 0

    while True:

        display.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            #detekcija klika mišem - pozicija izvora ovisi o koordinatama miša
            if event.type == MOUSEBUTTONDOWN:
                x_start, y_start = pygame.mouse.get_pos()


        #provjera gdje se nalazi izvor čestica
        if x_start == 0 and y_start == 0:
            particle = Particle()
        else:
            particle = Particle(x_start, y_start)

        particles.append(particle)

        for particle in particles:
            particle.position_x += particle.velocity_x * particle.time
            particle.position_y += particle.velocity_y * particle.time
            particle.size += step_size
            particle.velocity_y += step_velocity
            particle.time += step_time

            pygame.draw.circle(display, particle.color, (int(particle.position_x), int(particle.position_y)), int(particle.size), width=1)

            if particle.size < 0:
                particles.remove(particle)


        pygame.display.update()
        mainClock.tick(30)          #FPS=100

if __name__ == '__main__':
    main()
