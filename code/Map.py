from settings import *
import pygame
from random import random,randint

def build_map():
    image = [pygame.image.load(tile).convert_alpha() for tile in game_path.ground_tile]#把所有的格子放进来
    image = [pygame.transform.scale(images, (scene_setting.tile_wid, scene_setting.tile_high)).convert_alpha() for images in image]#让所有图片适应场景大小

    mapp = []
    for i in range(scene_setting.tile_x):
        tmp = []
        for j in range(scene_setting.tile_y):
            tmp.append(image[randint(0, len(image)-1)])
        mapp.append(tmp)#生成随机地图
    
    return mapp

def load_map(num):
    image = pygame.image.load(game_path.whole_map[num]).convert_alpha()
    image = pygame.transform.scale(image, (scene_setting.wid[num], scene_setting.high[num])).convert_alpha()
    return image