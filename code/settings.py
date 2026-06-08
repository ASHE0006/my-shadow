import pygame
import sys

class win_setting:
    name = "shadow"
    wid = 1280
    high = 720
    outdoor_scale = 1.5
    wid2 = 1260
    high2 = 944

class player_setting:
    speed = 5
    wid = 80
    high = 80
    #每张图对应出生点
    spawn_x = [970,1715,320,970]
    spawn_y = [1730,535,3460,1730]

class npc_setting:
    npc_num_for_each_map = [[0],[],[1,2],[]]#配置每个地图对应的npc序号

class item_setting:
    wid = 50
    high = 50

class scene_setting:#长宽的格子
    #每张图对应长宽高
    tile_x = [140,140,50,140]
    tile_y = [140,140,280,140]
    tile_wid = tile_high = 15
    wid = []
    high = []
    for i in tile_x:
        wid.append(i * tile_wid)
    for i in tile_y:
        high.append(i * tile_high)

class game_path:#素材路径
    pygame.init()
    player_s_l = r'.\asset\player\player_s_l.PNG'
    player_d = r'.\asset\player\player_d.PNG'
    ground_tile = [r'.\asset\map\map1.PNG',r'.\asset\map\map2.PNG',r'.\asset\map\map3.PNG']
    npc = [r'.\asset\npc\ghost.PNG', r'.\asset\npc\ghost.PNG']
    whole_map = [r'.\asset\map\tower.png',r'.\asset\map\library.png',r'.\asset\map\gallery.png',r'.\asset\map\cathedral.png']
    block = [r'.\asset\block\tower.png',r'.\asset\block\library.png',r'.\asset\block\gallery.png',r'.\asset\block\cathedral.png']
    font = pygame.font.Font(r'.\asset\font\nmsl.ttf',20)
    item = [r'.\asset\item\gear.png',r'.\assets\静态书.PNG']
    monster = [r'.\asset\npc\小怪.png']
    boss = r'.\assets\boss.png'
    dynamic_book = r'.\assets\动态书.png'
    title_bg = r'.\asset\title.jpg'
    finally_bg = r'.\asset\finally.png'


class dialog_setting:
    text_size = 20
    text_color = (255, 255, 255)
    box_alpha = 10 #对话框透明度
    box_wid = 800
    box_high = 100
    npc_wid = 100
    npc_high = 500
    box_start_x = win_setting.wid - box_wid
    box_start_y = win_setting.high - box_high
    npc_coord_x = (win_setting.wid - npc_wid) // 2
    npc_coord_y = win_setting.high - npc_high
    text_start_x = box_start_x + 30
    text_start_y = box_start_y + 30
    text_vertical_dist = text_size // 3
 
class game_state:#游戏状态标识
    main_menu = 1
    loading = 2
    over = 3
    win = 4
    pause = 5 