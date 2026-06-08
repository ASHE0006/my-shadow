from Settings2 import *
import pygame
import random

class Flying_book(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(GamePath.flying_book_2).convert_alpha() , (Flying_bookSettings.flying_bookwidth, Flying_bookSettings.flying_bookheight))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = Flying_bookSettings.flying_bookSpeed

        self.timer = 0
        self.state = "moving"
        self.direction = [0, 0]
        

    def update(self, delta_time):
            # 更新计时器
            self.timer += delta_time

            if self.state == "moving":
                # 如果移动状态持续超过 3 秒，切换到停止状态
                if self.timer > 6000:  # 3 秒
                    self.state = "stopping"
                    self.timer = 0  # 重置计时器
                    self.direction = [0, 0]  # 停止移动
                    self.image = pygame.transform.scale(pygame.image.load(GamePath.flying_book_1).convert_alpha(), (Flying_bookSettings.flying_bookwidth, Flying_bookSettings.flying_bookheight))
                else:
                    # 随机移动
                    if random.random() < 0.02:  # 每帧有 2% 概率改变方向
                        self.direction = [
                            random.choice([-1, 0, 1]),  # 水平方向：左、停止、右
                            random.choice([-1, 0, 1]),  # 垂直方向：上、停止、下
                        ]
                    
                    # 根据方向移动怪物
                    self.rect.x += self.direction[0] * Flying_bookSettings.flying_bookSpeed
                    self.rect.y += self.direction[1] * Flying_bookSettings.flying_bookSpeed

                    # 水平方向碰到边界就反向
                    if self.rect.left < 0:
                        self.rect.left = 0
                        self.direction[0] = -self.direction[0]  # 反弹
                    elif self.rect.right > WindowSettings.width:
                        self.rect.right = WindowSettings.width
                        self.direction[0] = -self.direction[0]

                    # 垂直方向碰到边界就反向
                    if self.rect.top < 0:
                        self.rect.top = 0
                        self.direction[1] = -self.direction[1]
                    elif self.rect.bottom > WindowSettings.height:
                        self.rect.bottom = WindowSettings.height
                        self.direction[1] = -self.direction[1]

            elif self.state == "stopping":
                # 如果停止状态持续超过 3 秒，切换到移动状态
                if self.timer > 3000:
                    self.state = "moving"
                    self.timer = 0  # 重置计时器
                    self.image = pygame.transform.scale(pygame.image.load(GamePath.flying_book_2).convert_alpha(), (Flying_bookSettings.flying_bookwidth, Flying_bookSettings.flying_bookheight))
