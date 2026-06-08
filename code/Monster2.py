from Settings2 import *
import pygame
import math
from Bullets2 import Bullet_M

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        image = pygame.image.load(GamePath.monster).convert_alpha()

        self.image = pygame.transform.scale(image , (MonsterSettings.monsterwidth, MonsterSettings.monsterheight))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = MonsterSettings.monsterSpeed
        self.time = 0
        self.HP = 100

    def update(self, player):
        player_x, player_y = player.rect.topleft
        monster_x, monster_y = self.rect.topleft

        # 计算怪物与玩家的距离
        dx = player_x - monster_x   
        dy = player_y - monster_y
        distance = math.sqrt(dx**2 + dy**2)

        # 如果怪物和玩家之间的距离大于0，移动怪物
        if distance > 0:
            dx /= distance
            dy /= distance
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

    # 发射弹幕
    def shoot_bullet(self, player, all_bullets_M):
        self.time += 1
        if self.time >= 60: # 冷却时间
            self.time = 0
            # 找怪物与玩家的角度
            player_x, player_y = player.rect.center
            monster_x, monster_y = self.rect.center
            angle = math.atan2(player_y - monster_y, player_x - monster_x)
            bullt = Bullet_M(monster_x, monster_y, angle)

            for i in range(-1, 2):
                bullet_angle = angle + i * 0.1
                bullt = Bullet_M(monster_x, monster_y, bullet_angle)
                all_bullets_M.add(bullt)