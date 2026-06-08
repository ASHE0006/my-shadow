import pygame
import sys
from settings import *
from scene import scene_control
from player import Player
from dialog import DialogBox
from npc import NPC
from openai import OpenAI
import time
import subprocess
from shop2 import Shop

map_num = -2
coin = 0


def run():
    global map_num
    global coin
    pygame.init()
    win = pygame.display.set_mode((win_setting.wid, win_setting.high))#屏幕大小设置
    pygame.display.set_caption(win_setting.name)#标题
    scene = scene_control(win, 1, map_num) #格式：win，加载（1）或生成（其他）地图，加载第n张地图

    #创建角色
    sprites = pygame.sprite.Group()
    player = Player(win_setting.wid // 2, win_setting.high // 2, map_num, coin)
    sprites.add(player)

    #创建商店类
    shop = Shop(player)
    
    #npc信息
    npc_present = []
    npc_present.append( NPC(pygame.transform.scale(pygame.image.load(game_path.npc[0]).convert_alpha(), (player_setting.wid, player_setting.high)), ["本层地图需要你寻找三个齿轮才能前往图书馆。", "在你捡起齿轮的同时会获得10金币！","按E可以查看你当前的金币数量。"], (800, 1700))  )
    npc_present.append( NPC(pygame.transform.scale(pygame.image.load(game_path.dynamic_book).convert_alpha(), (player_setting.wid, player_setting.high)), ["嗨，你成功捡到我了。", "现在你可以在我这里买东西了！","按B就可以打开商店了。按Esc退出。（仅限本层地图内）"], (320, 3260)) )
    npc_present.append( NPC(pygame.transform.scale(pygame.image.load(game_path.npc[1]).convert_alpha(), (player_setting.wid, player_setting.high)), ["回答我的问题，否则无法通过。（请查看终端，若未出现谜题则重新尝试对话）"], (330, 400), has_riddle = True)  )#npc2有谜语功能
    npcs = []
    for i in npc_setting.npc_num_for_each_map[map_num]:
        npcs.append(npc_present[i])#npcs里存入第map_num中的npc
    
    dialog_box = DialogBox(win, [])  # 初始没有对话框
    book_conversation = False  # 初始化对话标志
    #场景掉落物
    if map_num == 0:
        gear1 = NPC(pygame.transform.scale(pygame.image.load(game_path.item[0]).convert_alpha(), (item_setting.wid, item_setting.high)), [], (130, 680))  #(130, 680)
        npcs.append(gear1)
        gear2 = NPC(pygame.transform.scale(pygame.image.load(game_path.item[0]).convert_alpha(), (item_setting.wid, item_setting.high)), [], (135, 1840))  #(135, 1840)
        npcs.append(gear2)
        gear3 = NPC(pygame.transform.scale(pygame.image.load(game_path.item[0]).convert_alpha(), (item_setting.wid, item_setting.high)), [], (1840, 1930))  #(1840, 1930)
        npcs.append(gear3)
    
    #小怪
    monster1 = NPC(pygame.transform.scale(pygame.image.load(game_path.monster[0]).convert_alpha(), (player_setting.wid * 2, player_setting.high * 2)), [], (330, 1840))
    monster2 = NPC(pygame.transform.scale(pygame.image.load(game_path.monster[0]).convert_alpha(), (player_setting.wid * 2, player_setting.high * 2)), [], (370, 2840))
    if map_num == 0:
        npcs.append(monster1)


    if map_num == 1:
        book1 = NPC(pygame.transform.scale(pygame.image.load(game_path.item[1]).convert_alpha(), (player_setting.wid, player_setting.high)), [], (1820,1820))  #(1820,1820)(1715,530)
        npcs.append(book1)

    if map_num == 2:
        npcs.append(monster2)

    if map_num == 3:
        boss = NPC(pygame.transform.scale(pygame.image.load(game_path.boss).convert_alpha(), (player_setting.wid * 1.3, player_setting.high * 1.3)), [], (1010,1120))
        npcs.append(boss)


    #让游戏保持运行状态
    while True:




        if map_num == 0 and player.coin == 30:
            dialog_box.is_active = True
            dialog_box.dialogues = ["即将前往图书馆..."]
            dialog_box.render() 
            pygame.display.flip()
            time.sleep(2.5)
            dialog_box.is_active = False                    
            dialog_box.render()
            pygame.display.flip() 
            return 


        player_in_world = player.rect.move(scene.give_camera_x(), scene.give_camera_y())#它的坐标是通过将玩家的 rect 的位置加上当前相机的坐标来计算的。player_in_world就表示了玩家在大世界中的位置，而不影响玩家的实际 rect。
        for event in pygame.event.get():#检测事件
            scene.tick(60)
            if event.type == pygame.KEYUP:  #地图切换
                if event.key == pygame.K_n: 
                    return

            #退出游戏
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if map_num == 2:
                if book_conversation == True:
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_b:
                            shop.open()
                if shop.active == True:
                    shop.handle_event(event)
                    coin = player.coin #更新剩余金币数量
                    win.fill((0,0,0))
                    if shop.active == True :
                        shop.draw(win)
                        
            if event.type == pygame.KEYUP:  

                if map_num == 0:
                    if player_in_world.colliderect(monster1.rect) and monster1 in npcs:#撞到怪物
                        dialog_box.is_active = True
                        dialog_box.dialogues = ["这个齿轮不属于你！"]
                        dialog_box.render() 
                        pygame.display.flip()
                        time.sleep(3)
                        dialog_box.is_active = False
                        dialog_box.render()
                        pygame.display.flip() 
                        result = subprocess.run(
                            ["python", r".\Main2.py", str(2), str(player.HP)], #给Main2.py传参数
                                check = True,
                                capture_output = True,
                                text = True)
                        player.HP = int(result.stdout.strip().splitlines()[-2])
                        result.stdout = result.stdout.strip().splitlines()[-1]
                        if result.stdout == 'Win':
                            npcs.remove(monster1)
                            scene.render(npcs)#确保monster1回去时已经消失
                            pygame.display.flip()
                        else:
                            player.rect.x = player_setting.spawn_x[map_num] - scene.give_camera_x()
                            player.rect.y = player_setting.spawn_y[map_num] - scene.give_camera_y()#回弹到该地图的出生位置

                    #检测掉落物是否被捡起
                    if event.key == pygame.K_f:
                        if player_in_world.colliderect(gear1.rect) and gear1 in npcs:# 如果玩家捡起gear1
                            npcs.remove(gear1)
                            player.coin += 10
                        if player_in_world.colliderect(gear2.rect) and gear2 in npcs:
                            npcs.remove(gear2)
                            player.coin += 10
                        if player_in_world.colliderect(gear3.rect) and gear3 in npcs:
                            npcs.remove(gear3)
                            player.coin += 10
                        coin = player.coin
                if map_num == 1:
                    if event.key == pygame.K_f:
                        if player_in_world.colliderect(book1.rect) and book1 in npcs:
                            dialog_box.is_active = True
                            dialog_box.dialogues = ["请在书静止时捡起它，胜者前进，败者食尘！"]
                            dialog_box.render() 
                            pygame.display.flip()
                            time.sleep(3)
                            dialog_box.is_active = False
                            dialog_box.render()
                            pygame.display.flip() 
                            result = subprocess.run(
                                ["python", r".\Main2.py", str(map_num), str(player.HP)], #给Main2.py传参数
                                    check = True,
                                    capture_output = True,
                                    text = True)
                            print(result.stdout.strip().splitlines())
                            player.HP = int(result.stdout.strip().splitlines()[-2])
                            result.stdout = result.stdout.strip().splitlines()[-1]
                            if result.stdout == 'Win':
                                npcs.remove(book1)
                                scene.render(npcs)#确保book1回去时已经消失
                                pygame.display.flip()
                                return
                            else:
                                player.rect.x = player_setting.spawn_x[map_num] - scene.give_camera_x()
                                player.rect.y = player_setting.spawn_y[map_num] - scene.give_camera_y()#回弹到该地图的出生位置

                if map_num == 2:
                    if player_in_world.colliderect(monster2.rect) and monster2 in npcs:#撞到怪物
                        dialog_box.is_active = True
                        dialog_box.dialogues = ["YOU SHALL NOT PASS！"]
                        dialog_box.render() 
                        pygame.display.flip()
                        time.sleep(3)
                        dialog_box.is_active = False
                        dialog_box.render()
                        pygame.display.flip() 
                        result = subprocess.run(
                            ["python", r".\Main2.py", str(2), str(player.HP)], #给Main2.py传参数
                                check = True,
                                capture_output = True,
                                text = True)
                        player.HP = int(result.stdout.strip().splitlines()[-2])
                        result.stdout = result.stdout.strip().splitlines()[-1]
                        if result.stdout == 'Win':
                            npcs.remove(monster2)
                            scene.render(npcs)#确保monster1回去时已经消失
                            pygame.display.flip()
                        else:
                            player.rect.x = player_setting.spawn_x[map_num] - scene.give_camera_x()
                            player.rect.y = player_setting.spawn_y[map_num] - scene.give_camera_y()#回弹到该地图的出生位置     

                if map_num == 3:
                    if player_in_world.colliderect(boss.rect) and boss in npcs:#撞到怪物
                        dialog_box.is_active = True
                        dialog_box.dialogues = ["自杀，是杀死过去的自己还是未来的自己？现在，做出你的选择，杀死我，或许能逃离这个地方。"]
                        dialog_box.render() 
                        pygame.display.flip()
                        time.sleep(3)
                        dialog_box.is_active = False
                        dialog_box.render()
                        pygame.display.flip() 
                        result = subprocess.run(
                            ["python", r".\Main2.py", str(3), str(player.HP)], #给Main2.py传参数
                                check = True,
                                capture_output = True,
                                text = True)
                        player.HP = int(result.stdout.strip().splitlines()[-2])
                        result.stdout = result.stdout.strip().splitlines()[-1]
                        if result.stdout == 'Win':
                            npcs.remove(boss)
                            scene.render(npcs)#确保boss回去时已经消失
                            pygame.display.flip()
                            #结算画面
                            return










                        else:
                            player.rect.x = player_setting.spawn_x[map_num] - scene.give_camera_x()
                            player.rect.y = player_setting.spawn_y[map_num] - scene.give_camera_y()#回弹到该地图的出生位置            
                                
                #查看金币数量
                if event.key == pygame.K_e:
                    dialog_box.is_active = True
                    dialog_box.dialogues = ["你当前的金币数量是" + str(player.coin)]
                    dialog_box.render() 
                    pygame.display.flip()
                    time.sleep(1)
                    dialog_box.is_active = False
                    dialog_box.render()
                    pygame.display.flip() 

        #获取按键
        key = pygame.key.get_pressed()


        #更新player
        if dialog_box.is_active == False and shop.active == False:  
            player.move(key, scene)
        scene.update_camera(player)

        # 玩家与 NPC 的交互   
        for npc in npcs:
            if player_in_world.colliderect(npc.rect) and key[pygame.K_z] and dialog_box.is_active == False:  # 如果玩家靠近 NPC 并按Z键  
                dialog_box.is_active = True  # 激活对话框  
                dialog_box.dialogues = npc.dialogues  # 设置对话内容  
                dialog_box.current_index = 0  # 从第一条对话开始  
                book_conversation = True
                npc_in_dialog = npc
                break  # 中断循环以避免多个NPC同时激活对话框  
        
       # print(player_in_world)
        
        scene.render(npcs)#渲染场景
        sprites.draw(win)#渲染玩家


        key_flag = False
        # 处理对话框显示  e
        if dialog_box.is_active:  
            for event in pygame.event.get():  # 确保事件循环正常  
                if event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_z and not key_flag:  
                        if dialog_box.current_index < len(dialog_box.dialogues) - 1:  
                            dialog_box.current_index += 1  # 逐条显示对话  
                        else:  
                        # 如果是最后一条对话，检查玩家答案  
                            if npc_in_dialog.has_riddle and npc_in_dialog.riddle_active == False:  
                                npc_in_dialog.generate_riddle()  # 如果有谜语功能，立即生成谜语  
                                if npc_in_dialog.res == True:
                                    return
                                #npc_in_dialog.riddle_active = True
                            #dialog_box.is_active = False 
                            win.fill((0,0,0)) 
                            npc_in_dialog.active = False
                     
                    if event.key == pygame.K_x and not key_flag:  
                        dialog_box.is_active = False  # 关闭对话框  
                        win.fill((0,0,0))
                    
                    key_flag = True  # 设置标志位避免重复处理 

                if event.type == pygame.KEYUP:  
                    key_flag = False  # 重置标志位  
        dialog_box.render() 
        
        
         
        pygame.display.flip()

def run2():
    global map_num
    pygame.init()
    win = pygame.display.set_mode((win_setting.wid2, win_setting.high2))#屏幕大小设置
    pygame.display.set_caption(win_setting.name)#标题
    font = pygame.font.Font(r'.\asset\font\nmsl.ttf',54)
    if map_num == -2:
        image = pygame.transform.scale(pygame.image.load(game_path.title_bg).convert_alpha(),(win_setting.wid2,win_setting.high2))
        win.blit(image,(0,0))#渲染对象,坐标
        pygame.display.flip()
        while map_num == -2:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:
                        map_num += 1
                        break
    if map_num == -1:
        text_num = 0
        text =[font.render('Ashe在钟楼的中心醒来，她缓缓睁开眼睛',True, (0,0,0)),
            font.render('头痛如针刺，脑海中闪过模糊的影像却难以捕捉。',True, (0,0,0)),
            font.render('四周弥漫着潮湿的雾气，旧齿轮散落在地',True, (0,0,0)),
            font.render('仿佛在低声诉说着被遗忘的秘密。',True, (0,0,0)),
            font.render('她的手指触碰到冰冷的瓷砖',True,(0,0,0)),
            font.render('周围是破旧的齿轮和布满尘土的地面',True,(0,0,0)),
            font.render('这似乎是一个空无一人的钟塔顶楼。',True,(0,0,0)),
            font.render('(提示：按Z继续对话，按X关闭对话)',True,(0,0,0)),
            font.render('(按M可回到该地图出生点，按F收集物品)',True,(0,0,0)),
            font.render('(存在自动脱离卡死机制以及底图没抠干净)',True,(0,0,0)),
            font.render('(所以可能会存在闪现现象喵。)',True,(0,0,0)),
            ]
        win.fill((255,255,255))
    if map_num == 0:
        text_num = 0
    pygame.display.flip()
    #让游戏保持运行状态
    while True:
        if map_num == -1:
            if text_num == 11:
                return#退出开场旁白
        if map_num == 0:
            if text_num == 0:
                return 
        text_rect = text[text_num].get_rect(center = (win_setting.wid2 // 2,win_setting.high2 // 2))
        win.blit(text[text_num],text_rect)#对象+位置
        pygame.display.update()
        for event in pygame.event.get():#检测事件
            if event.type == pygame.KEYUP:  
                if event.key == pygame.K_z or event.key == pygame.K_RETURN: 
                    text_num += 1
                    win.fill((255,255,255))
                    pygame.display.update()
                    continue
            #退出游戏
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
def run3():
    global map_num
    pygame.init()
    win = pygame.display.set_mode((1200, 756))#屏幕大小设置
    pygame.display.set_caption(win_setting.name)#标题
    image = pygame.transform.scale(pygame.image.load(game_path.finally_bg).convert_alpha(), (1200, 756))
    win.blit(image, (0,0))
    pygame.display.flip()
    time.sleep(10)
    pygame.quit()
    sys.exit()



if __name__=="__main__":
    if map_num == -2:
        run2()
    while map_num < 4:
        map_num += 1
        if map_num != 4:
            run()
    if map_num == 4:
        run3()
