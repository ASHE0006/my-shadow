import pygame
import sys
import time

from SceneManager2 import SceneManager
from Settings2 import *
from Player2 import Player2
from Monster2 import Monster
from collision2 import *
from Flying_book2 import Flying_book
from shop2 import *
from Boss2 import Boss


def run_game():

    pygame.init()

    map_num = int(sys.argv[1])
    #map_num = 3

    if map_num == 1:
        window = pygame.display.set_mode((WindowSettings.width, WindowSettings.height))
        pygame.display.set_caption(WindowSettings.name)

        scene = SceneManager(window)
        clock = pygame.time.Clock()

        # 创建Player
        sprites = pygame.sprite.Group()
        player = Player2(WindowSettings.width // 3, WindowSettings.height // 3)
        player.HP = int(sys.argv[2])
        sprites.add(player)
        # 创建飞书
        flying_book = Flying_book(WindowSettings.width // 2, WindowSettings.height // 2)
        sprites.add(flying_book)
        flying_book_picked = False

    if map_num == 2:
        window = pygame.display.set_mode((WindowSettings.width, WindowSettings.height))
        pygame.display.set_caption(WindowSettings.name)

        scene = SceneManager(window)
        clock = pygame.time.Clock()

        # 创建Player
        sprites = pygame.sprite.Group()
        player = Player2(WindowSettings.width // 3, WindowSettings.height // 3)
        player.HP = int(sys.argv[2])
        sprites.add(player)

        # 创建Monster
        monster = Monster(WindowSettings.width // 2 + 100, WindowSettings.height // 2)
        sprites.add(monster)

        # 创建所有弹幕
        all_bullets_M = pygame.sprite.Group()
        all_bullets_P = pygame.sprite.Group()

    if map_num == 3:
        window = pygame.display.set_mode((WindowSettings.width, WindowSettings.height))
        pygame.display.set_caption(WindowSettings.name)

        scene = SceneManager(window)
        clock = pygame.time.Clock()

        # 创建Player
        sprites = pygame.sprite.Group()
        player = Player2(WindowSettings.width // 3, WindowSettings.height // 3)
        player.HP = int(sys.argv[2])
        sprites.add(player)

        # 创建Boss
        boss = Boss(WindowSettings.width // 2 + 100, WindowSettings.height // 2)
        sprites.add(boss)

        # 创建所有弹幕
        all_bullets_M = pygame.sprite.Group()
        all_bullets_P = pygame.sprite.Group()


    
    # 游戏主循环
    while True:
        scene.tick(60) # 控制帧率
        delta_time = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        # 获取按键状态
        keys = pygame.key.get_pressed()


        # 更新Player
        player.update(keys, scene)
        
        # Player弹幕
        mouse = pygame.mouse.get_pos()
        if keys[pygame.K_SPACE]:
            Jus = True
            color = (255, 255, 255) 
        elif keys[pygame.K_q]:
            Jus = True
            color = (0, 255, 0)
        elif keys[pygame.K_e]:
            Jus = True
            color = (255, 0, 0)
        else:
            color = (0, 0, 0)
            Jus = False

        if map_num == 2:
            # 玩家弹幕
            player.shoot_bullet(mouse, Jus, all_bullets_P, color)

        if map_num == 3:
            # 玩家弹幕
            player.shoot_bullet(mouse, Jus, all_bullets_P, color)

        # 渲染场景
        scene.render()

        if map_num == 2:
            # 更新Monster
            if monster.HP > 0 and player.HP > 0:
                monster.update(player)
                monster.shoot_bullet(player, all_bullets_M)

            # 更新弹幕
            all_bullets_M.update()
            all_bullets_P.update()

        if map_num == 1:
            # 更新飞书
            flying_book.update(delta_time)

        if map_num == 3:
            # 更新Boss
            if boss.HP > 0 and player.HP > 0:
                boss.update(player)
                boss.shoot_bullet(player, all_bullets_M)

            # 更新弹幕
            all_bullets_M.update()
            all_bullets_P.update()
        
        # 渲染Player,Monster,Flying_book,弹幕
        sprites.draw(window)

        if map_num == 2:
            if player.HP <= 0:
                all_bullets_P.empty()
            # 渲染所有弹幕
            all_bullets_M.draw(window)
            all_bullets_P.draw(window)

            # 显示怪物血量
            text = 'Monster HP:' + str(monster.HP)
            window.blit(pygame.font.SysFont(None, 30).render(text, True, (255, 255, 255)), (10, 40))

        if map_num == 3:
            if player.HP <= 0:
                all_bullets_P.empty()
            # 渲染所有弹幕
            all_bullets_M.draw(window)
            all_bullets_P.draw(window)

            # 显示怪物血量
            text = 'Boss HP:' + str(boss.HP)
            window.blit(pygame.font.SysFont(None, 30).render(text, True, (255, 255, 255)), (10, 40))

        if map_num == 1:
            if pygame.sprite.collide_rect(player, flying_book):
                if flying_book_picked == False:
                    if flying_book.state == "stopping":
                    # 飞书停下时，允许玩家按 F 键捡起
                        if keys[pygame.K_f]:
                            text = "Ashe get the Flyingbook!"
                            flying_book_picked = True
                            sprites.remove(flying_book)
                            
                    if flying_book.state == "moving":
                        # 飞书移动时，禁止玩家捡起，玩家受到攻击
                        player.HP -= 1
                        print("BOOK HIT PLAYER!")

            if flying_book_picked == True:
                text = "Ashe get the Flyingbook!"
                text_surface = pygame.font.SysFont(None, 80).render(text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(WindowSettings.width // 2, WindowSettings.height // 2))
                window.blit(pygame.font.SysFont(None, 80).render(text, True, (0, 255, 0)), text_rect) 
                pygame.display.flip()
                time.sleep(3)
                return_value = "Win"
                return_HP = str(player.HP)
                print(return_HP)
                print(return_value)#给main.py传回参数
                pygame.quit()
                sys.exit(0)
                # 在这里写一段代码让字在5秒后消失
                # 需要让书在被捡起后消失
                
            
        if map_num == 2:
            for bullet in all_bullets_M:
                if player.HP >= 0:
                    if check_collision(bullet, player) == 3:
                        player.HP -= 30
                        print("Ashe 受到攻击！")
                        all_bullets_M.remove(bullet)
                else:
                    all_bullets_M.remove(bullet)
        
            for bullet in all_bullets_P:
                if monster.HP >= 0:
                    if check_collision(bullet, monster) == 1: # 白色
                        monster.HP -= 10
                        all_bullets_P.remove(bullet)
                    elif check_collision(bullet, monster) == 2: # 蓝色
                        monster.HP -= 30
                        all_bullets_P.remove(bullet)
                    elif check_collision(bullet, monster) == 3: # 红色
                        monster.HP -= 20
                        all_bullets_P.remove(bullet)
                else:
                    all_bullets_P.remove(bullet)
            
            if monster.HP <= 0:
                text = 'Monster is DEAD!'
                text_surface = pygame.font.SysFont(None, 80).render(text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(WindowSettings.width // 2, WindowSettings.height // 2))
                window.blit(pygame.font.SysFont(None, 80).render(text, True, (0, 255, 0)), text_rect)
                sprites.remove(monster)
                all_bullets_M.empty()
                pygame.display.flip()
                time.sleep(3)
                return_value = "Win"
                return_HP = str(player.HP)
                print(return_HP)
                print(return_value)#给main.py传回参数
                pygame.quit()
                sys.exit(0)

        if map_num == 3:
            for bullet in all_bullets_M:
                if player.HP >= 0:
                    if check_collision(bullet, player) == 3:
                        player.HP -= 30
                        all_bullets_M.remove(bullet)
                else:
                    all_bullets_M.remove(bullet)

            for bullet in all_bullets_P:
                if boss.HP >= 0:
                    if check_collision(bullet, boss) == 1: # 白色
                        boss.HP -= 10
                        all_bullets_P.remove(bullet)
                    elif check_collision(bullet, boss) == 2: # 蓝色
                        boss.HP -= 20
                        all_bullets_P.remove(bullet)
                    elif check_collision(bullet, boss) == 3: # 红色
                        boss.HP -= 40
                        all_bullets_P.remove(bullet)
                else:
                    all_bullets_P.remove(bullet)

            if boss.HP <= 0:
                text = 'Boss is DEAD!'
                text_surface = pygame.font.SysFont(None, 80).render(text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(WindowSettings.width // 2, WindowSettings.height // 2))
                window.blit(pygame.font.SysFont(None, 80).render(text, True, (0, 255, 0)), text_rect)
                sprites.remove(boss)
                all_bullets_M.empty()
                pygame.display.flip()
                time.sleep(3)
                return_value = "Win"
                return_HP = str(player.HP)
                print(return_HP)
                print(return_value)#给main.py传回参数
                pygame.quit()
                sys.exit(0)


        text = 'Player HP: ' + str(player.HP)
        window.blit(pygame.font.SysFont(None, 30).render(text, True, (255, 255, 255)), (10, 10))

        if (255, 255, 255) in player.unlocked_bullet_colors:
            text = 'Normal Attack: SPACE'
            window.blit(pygame.font.SysFont(None, 30).render(text, True, (255, 255, 255)), (10, 70))

        if (0, 255, 0) in player.unlocked_bullet_colors:
            text = 'Water Attack: Q'
            window.blit(pygame.font.SysFont(None, 30).render(text, True, (255, 255, 255)), (10, 100))

        if (255, 0, 0) in player.unlocked_bullet_colors:
            text = 'Fire Attack: E'
            window.blit(pygame.font.SysFont(None, 30).render(text, True, (255, 255, 255)), (10, 130))
        
        if player.HP <= 0:
            player.HP = 0
            text = "Ashe is DEAD!"
            text_surface = pygame.font.SysFont(None, 80).render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(WindowSettings.width // 2, WindowSettings.height // 2))
            window.blit(pygame.font.SysFont(None, 80).render(text, True, (255, 0, 0)), text_rect)
            sprites.remove(player)
            pygame.display.flip()
            time.sleep(3)
            return_value = "Ji"
            print(sys.argv[2])
            print(return_value)#给main.py传回参数
            pygame.quit()
            sys.exit(0)



        pygame.display.flip()

if __name__ == "__main__":
    run_game()