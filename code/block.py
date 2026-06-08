import pygame
from settings import *
class Block(pygame.sprite.Sprite):  # 玩家类

    def __init__(self, num, x, y):
        super().__init__()#构造
        self.image = pygame.image.load(game_path.block[num]).convert_alpha()#加载图片
        self.image = pygame.transform.scale(self.image, (scene_setting.wid[num],scene_setting.high[num])).convert_alpha()#大小适应
        self.rect = self.image.get_rect()#获取位置
        self.rect.topleft = (x, y)