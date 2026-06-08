from Settings2 import *
import pygame
from Bullets2 import Bullet_P
import math

class Player2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        image = pygame.image.load(GamePath.player).convert_alpha()
        
        self.image = pygame.transform.scale(image, (PlayerSettings.playerwidth, PlayerSettings.playerheight))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = PlayerSettings.playerspeed
        self.time = 0
        self.HP = 100
        self.coin = 0

         # 新增：已解锁的子弹颜色(初始只解锁白色)
        self.unlocked_bullet_colors = {(255, 255, 255)}
        # 当前要使用的子弹颜色
        self.current_bullet_color = (255, 255, 255)


    def update(self, keys, scene):
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < WindowSettings.height:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < WindowSettings.width:
            self.rect.x += self.speed

    def fix_to_middle(self, dx, dy):
        self.rect.x -= dx
        self.rect.y -= dy



    def shoot_bullet(self, mouse, Jus, all_bullets_P, color):
        self.time += 1
        if self.time >= 60 and Jus == True:
            self.time = 0
            player_x, player_y = self.rect.center
            mouse_x, mouse_y = mouse
            angle = math.atan2(mouse_y - player_y, mouse_x - player_x)

             # 这里做一个判断：若 color 不在已解锁列表，则无效
            if color not in self.unlocked_bullet_colors:
                return

            bullet = Bullet_P(player_x, player_y, angle, color)
            all_bullets_P.add(bullet)
            