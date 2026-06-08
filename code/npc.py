import pygame
import sys
from scene import scene_control
from openai import OpenAI
from typing import List, Dict

class NPC(pygame.sprite.Sprite):  
    def __init__(self, image, dialogues, position, has_riddle = False):  
        super().__init__()
        self.image = image  
        self.world_position = position  # 在大地图上的位置  
        self.rect = self.image.get_rect(topleft=self.world_position)  # NPC 位置 
        self.dialogues = dialogues  # 属于这个npc的对话组
        self.dialog_index = 0  
        self.correct_answer = ""  # 存储正确答案  
        self.has_riddle = has_riddle  # 是否有谜语功能  
        self.riddle_active = False

    def generate_riddle(self): 
        client = OpenAI(base_url='http://10.15.88.73:5031/v1',
                            api_key='ollama',) # 初始化 OpenAI 客户端  
        messages: List[Dict] = [
        {"role": "system", "content": "You are a Portrait of a wraith capable of generating riddles. \
         Each time, you will generate a riddle for the player to guess.\
         If the player's answer is correct, you will say YOU ARE CORRECT and sign with relief and disappear.\
         If the answer is incorrect, you will say YOU ARE WRONG and try to kill the player. \
         Your goal is to challenge the player with a riddle,\
         and check if their answer is correct. You know the correct answer.\
         You don't need to wait for me to speak, you can tell the riddle yourself first."}
        ]

        messages.append({"role": "user", "content": "ask me a riddle without starting with 'I have a head'."})

        response1 = client.chat.completions.create(
            model = "llama3.2",
            messages = messages,
        )

        riddle = response1.choices[0].message.content
        print(f"Llama: {riddle}")

        messages.append({"role": "system", "content": riddle})

        user_input = input("Ashe:")

        messages.append({"role": "user", "content": user_input})

        response2 = client.chat.completions.create(
            model="llama3.2",
            messages=messages,
        )

        # 提取模型回复
        assistant_reply = response2.choices[0].message.content
        if "CORRECT" in assistant_reply:
            self.res = True
        else:
            self.res = False  
        print(f"Llama: {assistant_reply}")

    def draw(self, win, camera_x, camera_y):  
        win.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))