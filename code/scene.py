from settings import *
import pygame
import Map
from player import Player
from block import Block
import pygame  

class scene_control:
    def __init__(self, win, map_load_or_gen, num):
        self.state = 0
        self.win = win
        self.opt = map_load_or_gen
        self.num = num
        if map_load_or_gen != 1 :
            self.map = Map.build_map()
        else :
            self.map = Map.load_map(num)
        self.clock = pygame.time.Clock()
        self.camera_x = player_setting.spawn_x[num] - win_setting.wid / 2
        self.camera_y = player_setting.spawn_y[num] - win_setting.high / 2
    
    

    def tick(self, fps):
        self.clock.tick(fps)

    def get_wid(self):
        return scene_setting.wid[self.num]
    
    def get_high(self):
        return scene_setting.high[self.num]


    def update_camera(self, player):#更新摄像头
        if player.rect.x > win_setting.wid // 4 * 3:
            self.camera_x += player.speed
            if self.camera_x < self.get_wid() - win_setting.wid -75:
                player.fix_to_middle(player.speed, 0)
            else:
                self.camera_x = self.get_wid() - win_setting.wid -75
        if player.rect.x < win_setting.wid // 4:
            self.camera_x -= player.speed
            if self.camera_x > 0 :
                player.fix_to_middle(-player.speed, 0)
            else:
                self.camera_x = 0
        if player.rect.y > win_setting.high // 4 * 3:
            self.camera_y += player.speed
            if self.camera_y < self.get_high() - win_setting.high -75 :
                player.fix_to_middle(0, player.speed)
            else:
                self.camera_y = self.get_high() - win_setting.high -75
        if player.rect.y < win_setting.high // 4:
            self.camera_y -= player.speed
            if self.camera_y > 0 :
                player.fix_to_middle(0, -player.speed)
            else:
                self.camera_y = 0


    def render(self, npcs):#渲染
        if self.opt == 1:#整个的
            self.win.blit(self.map, (- self.camera_x, - self.camera_y))
        else :
            for i in range(scene_setting.tile_x[self.num]):
                for j in range(scene_setting.tile_y[self.num]):
                    self.win.blit(self.map[i][j],(scene_setting.tile_wid[self.num] * i - self.camera_x, scene_setting.tile_high[self.num] * j - self.camera_y))

        # 渲染 NPC  
        for npc in npcs:  
            npc.draw(self.win, self.camera_x, self.camera_y)  # 传递摄像头位置 
    

    def give_camera_x(self):
        return self.camera_x
    def give_camera_y(self):
        return self.camera_y