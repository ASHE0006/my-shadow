import pygame
from block import Block
from settings import *
def pixel_collision(image1, rect1, image2, rect2, scene):  
    # 获取两个图像的重叠区域  
    overlap_rect = rect1.clip(rect2)  
    #print("重叠部分：",overlap_rect,"player位置：",rect1,"block位置：",rect2)
    if overlap_rect.width == 0 or overlap_rect.height == 0:
        #print("没有重叠，不可能发生碰撞  ")  
        return False  # 没有重叠，不可能发生碰撞  

    # 提取两个图各自重叠的部分
    sub_image1 = image1.subsurface(overlap_rect.move(-rect1.x, -rect1.y))  
    sub_image2 = image2.subsurface(overlap_rect.move(-rect2.x, -rect2.y)) 
    #print("sub_image1.rect:",overlap_rect.move(-rect1.x, -rect1.y),"sub_image2.rect:",overlap_rect.move(-rect2.x, -rect2.y)) 


    # 更新显示  
    pygame.display.flip()  

    # 获取每个子图像的透明度
    pixels1 = pygame.surfarray.pixels_alpha(sub_image1)  
    pixels2 = pygame.surfarray.pixels_alpha(sub_image2)  

    # 检查重叠区的每个像素  
    for x in range(overlap_rect.width):  
        for y in range(overlap_rect.height):  
            if pixels1[x, y] > 0 and pixels2[x, y] > 0:  # 如果两个图像的像素均不透明  
                #print("两个图像的像素均不透明  ")
                return True  

    #print("重叠部分透明")
    return False  

class Player(pygame.sprite.Sprite):  # 玩家类

    def __init__(self, x, y, block_num, coin):
        super().__init__()#构造
        # 预加载并缓存两个朝向的图片，避免每帧重复加载
        self.image_left = pygame.transform.scale(
            pygame.image.load(game_path.player_s_l).convert_alpha(),
            (player_setting.wid, player_setting.high)
        ).convert_alpha()
        self.image_right = pygame.transform.scale(
            pygame.image.load(game_path.player_d).convert_alpha(),
            (player_setting.wid, player_setting.high)
        ).convert_alpha()
        self.image = self.image_left  # 默认朝向左
        self.rect = self.image.get_rect()#获取位置
        self.rect.topleft = (x, y)
        self.speed = player_setting.speed
        self.block_num = block_num
        self.coin = coin

        self.time = 0
        self.HP = 100
         # 新增：已解锁的子弹颜色(初始只解锁白色)
        self.unlocked_bullet_colors = {(255, 255, 255)}
        # 当前要使用的子弹颜色
        self.current_bullet_color = (255, 255, 255)


    def move(self, key, scene):
        player_in_world = self.rect.move(scene.give_camera_x(), scene.give_camera_y())
        #print(player_in_world)
        block = Block(self.block_num, -scene.give_camera_x(), -scene.give_camera_y())
        #block = Block(self.block_num, 0, 0)
        if key[pygame.K_m]:
            self.rect.x = player_setting.spawn_x[self.block_num] - scene.give_camera_x()
            self.rect.y = player_setting.spawn_y[self.block_num] - scene.give_camera_y()#回弹到该地图的出生位置
        if (key[pygame.K_w] or key[pygame.K_UP]) and self.rect.top > 0 : 
            pro = self.rect.copy()
            pro.y -= self.speed
            if not pixel_collision(self.image, pro, block.image, block.rect, scene):#按了移动且不撞墙且不在边界
                self.rect.y -= self.speed 
                #背后图片待补充
            else:
                while pixel_collision(self.image, pro, block.image, block.rect, scene):
                    self.rect.y += 1
                    player_in_world = self.rect.move(scene.give_camera_x(), scene.give_camera_y())
                if player_in_world.y > scene_setting.high[self.block_num] :#离开边界
                    self.rect.x = player_setting.spawn_x[self.block_num] - scene.give_camera_x()
                    self.rect.y = player_setting.spawn_y[self.block_num] - scene.give_camera_y()#回弹到该地图的出生位置

        if (key[pygame.K_s] or key[pygame.K_DOWN]) and self.rect.bottom < win_setting.high :
            pro = self.rect.copy()
            pro.y += self.speed
            if not pixel_collision(self.image, pro, block.image, block.rect, scene):
                self.rect.y += self.speed 
                self.image = self.image_left  # 朝向左
            else:
                while pixel_collision(self.image, pro, block.image, block.rect, scene) and self.rect.y > 0:
                    self.rect.y -= 1
                    player_in_world = self.rect.move(scene.give_camera_x(), scene.give_camera_y())
                if player_in_world.y < 0 :#离开边界
                    self.rect.x = player_setting.spawn_x[self.block_num] - scene.give_camera_x()
                    self.rect.y = player_setting.spawn_y[self.block_num] - scene.give_camera_y()#回弹到该地图的出生位置

        if (key[pygame.K_a] or key[pygame.K_LEFT]) and self.rect.left > 0 :
            pro = self.rect.copy()
            pro.x -= self.speed
            if not pixel_collision(self.image, pro, block.image, block.rect, scene):
                self.rect.x -= self.speed 
                self.image = self.image_left  # 朝向左
            else :
                while pixel_collision(self.image, pro, block.image, block.rect, scene):
                    self.rect.x += 1
                    player_in_world = self.rect.move(scene.give_camera_x(), scene.give_camera_y())
                if player_in_world.x > scene_setting.wid[self.block_num] :#离开边界
                    self.rect.x = player_setting.spawn_x[self.block_num] - scene.give_camera_x()
                    self.rect.y = player_setting.spawn_y[self.block_num] - scene.give_camera_y()#回弹到该地图的出生位置

        if (key[pygame.K_d] or key[pygame.K_RIGHT]) and self.rect.right < win_setting.wid :
            pro = self.rect.copy()
            pro.x += self.speed
            if not pixel_collision(self.image, pro, block.image, block.rect, scene):
                self.rect.x += self.speed 
                self.image = self.image_right  # 朝向右
            else :
                while pixel_collision(self.image, pro, block.image, block.rect, scene):
                    self.rect.x -= 1
                    player_in_world = self.rect.move(scene.give_camera_x(), scene.give_camera_y())
                if player_in_world.x < 0 :#离开边界
                    self.rect.x = player_setting.spawn_x[self.block_num] - scene.give_camera_x()
                    self.rect.y = player_setting.spawn_y[self.block_num] - scene.give_camera_y()#回弹到该地图的出生位置

    def fix_to_middle(self, dx, dy):
        self.rect.x -= dx
        self.rect.y -= dy
    
