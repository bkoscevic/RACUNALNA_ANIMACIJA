import sys

import pygame
import random
import math

WIDTH = 1200
HEIGHT = 800

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
fps = 30


class Sun:
    def __init__(self, radius, x, y, color=(255, 255, 0)):
        self.radius = radius
        self.position_x = x
        self.position_y = y
        self.color = color

    def draw_sun(self):
        pygame.draw.circle(window, self.color, (self.position_x, self.position_y), self.radius)


class Star:
    def __init__(self, color=(255, 255, 255), step_time=0.5):
        self.color = color
        self.radius = random.randint(0, 1)
        self.position_x = random.randint(0, WIDTH)
        self.position_y = random.randint(0, HEIGHT)
        self.time = random.randint(1, 1000)
        self.step_time = step_time

    def draw_star(self):
        pygame.draw.circle(window, self.color, (self.position_x, self.position_y), self.radius)


class Planet:
    def __init__(self, radius, speed, color, x_radius, y_radius, rings=False):
        self.radius = radius
        self.speed = speed
        self.color = color
        self.x_radius = x_radius
        self.y_radius = y_radius
        self.rings = rings
        self.angle = 0

    def draw_planet(self):
        x = math.cos(self.angle * math.pi / 180) * self.x_radius + WIDTH / 2
        y = math.sin(self.angle * math.pi / 180) * self.y_radius + HEIGHT / 2
        pygame.draw.circle(window, self.color, (x, y), self.radius)

        if self.rings:
            pygame.draw.line(window, (125, 125, 125), (x - 35, y), (x + 35, y), width=3)

        self.angle += self.speed

    def draw_orbit(self):
        pygame.draw.ellipse(window, (255, 255, 255), [WIDTH / 2 - self.x_radius, HEIGHT / 2 - self.y_radius, 2 * self.x_radius,
                                                      2 * self.y_radius], 1)


def run(planets, sun, stars):
    clock = pygame.time.Clock()

    while True:

        window.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for star in stars:
            star.draw_star()

            star.time -= star.step_time
            if star.time < 0:
                stars.remove(star)

                new_star = Star()
                stars.append(new_star)

        sun.draw_sun()

        for planet in planets:
            planet.draw_orbit()
            planet.draw_planet()

        pygame.display.update()
        clock.tick(fps)


def main():
    pygame.display.set_caption("Sunčev sustav")

    sun = Sun(40, WIDTH / 2, HEIGHT / 2, (255, 255, 0))
    mercury = Planet(5, 2.25, (125, 125, 125), 90, 45)
    venus = Planet(10, 2, (255, 205, 0), 140, 70)
    earth = Planet(15, 1.5, (0, 255, 155), 180, 90)
    mars = Planet(8, 1.25, (255, 0, 0), 230, 115)
    jupiter = Planet(30, 0.6, (255, 230, 130), 300, 150)
    saturn = Planet(25, 0.5, (180, 120, 0), 400, 200, True)
    uranus = Planet(20, 0.3, (50, 170, 255), 500, 250)
    neptune = Planet(15, 0.25, (0, 0, 255), 580, 290)

    planets = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    stars = []
    for i in range(500):
        star = Star()
        stars.append(star)

    run(planets, sun, stars)


if __name__ == '__main__':
    main()
