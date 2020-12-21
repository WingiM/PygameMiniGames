import pygame
import random as r
import math
import constants as cn


class Stick:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = cn.AH_STICK_RADIUS
        self.speed = cn.AH_STICK_SPEED
        self.mass = cn.AH_STICK_MASS
        self.angle = 0

    def move(self, up, down, left, right, time):
        dx, dy = self.x, self.y
        self.x += (right - left) * self.speed * time
        self.y += (down - up) * self.speed * time
        dx, dy = self.x - dx, self.y - dy
        self.angle = math.atan2(dy, dx)

    def get_pos(self):
        return self.x, self.y

    def set_pos(self, x, y):
        self.x = x
        self.y = y


class Puck:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.radius = cn.AH_PUCK_RADIUS
        self.speed = cn.AH_PUCK_SPEED
        self.mass = cn.AH_PUCK_MASS
        self.angle = 0

    def move(self, time):
        self.x += math.sin(self.angle) * self.speed * time
        self.y -= math.cos(self.angle) * self.speed * time

        self.speed *= cn.AH_FRICTION  # TODO: попробовать без трения

    @staticmethod
    def add_vector(angle1, len1, angle2, len2):
        x = math.sin(angle1) * len1 + math.sin(angle2) * len2
        y = math.cos(angle1) * len1 + math.cos(angle2) * len2
        len0 = math.hypot(x, y)
        angle = math.pi / 2 - math.atan2(y, x)
        return angle, len0

    def check_collision(self, stick):
        dx = self.x - stick.x
        dy = self.y - stick.y
        distance = math.hypot(dx, dy)
        if distance > self.radius + stick.radius:
            return False
        tan = math.atan2(dy, dx)
        temp_angle = math.pi / 2 + tan
        total_mass = self.mass + stick.mass

        vector1 = (self.angle, self.speed * (self.mass - stick.mass) / total_mass)
        vector2 = (temp_angle, 2 * stick.speed * stick.mass / total_mass)

        (self.angle, self.speed) = self.add_vector(*vector1, *vector2)

        self.speed = min(self.speed, cn.AH_SPEED_LIMIT)

        vector1 = (stick.angle, stick.speed * (stick.mass - self.mass) / total_mass)
        vector2 = (temp_angle + math.pi, 2 * self.speed * self.mass / total_mass)

        temp_speed = stick.speed
        stick.angle, stick.speed = self.add_vector(*vector1, *vector2)
        stick.speed = temp_speed

        offset = 0.5 * (self.radius + stick.radius - distance + 1)
        self.x += math.sin(temp_angle) * offset
        self.y -= math.cos(temp_angle) * offset
        stick.x -= math.sin(temp_angle) * offset
        stick.y += math.cos(temp_angle) * offset
        return True

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius)
        # TODO: поменять цвета

    def get_pos(self):
        return self.x, self.y
