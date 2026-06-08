from Settings2 import *
import pygame
import math

clock = pygame.time.Clock()

class Bullet_M(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((BulletSettings.bulletradiu_M * 2 , BulletSettings.bulletradiu_M * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (BulletSettings.bulletradiu_M, BulletSettings.bulletradiu_M), BulletSettings.bulletradiu_M)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = BulletSettings.bulletSpeed_M
        self.angle = angle

    def update(self):
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)

class Bullet_P(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, color):
        super().__init__()
        self.image = pygame.Surface((BulletSettings.bulletradiu_P * 2, BulletSettings.bulletradiu_P * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (color), (BulletSettings.bulletradiu_P, BulletSettings.bulletradiu_P), BulletSettings.bulletradiu_P)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = BulletSettings.bulletSpeed_P
        self.angle = angle
        self.color = color

    def update(self):
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)