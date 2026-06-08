import pygame
from settings import *
class DialogBox:  
    def __init__(self, win, dialogues):  
        self.win = win  
        self.dialogues = dialogues  
        self.current_index = 0  
        self.font = game_path.font  # 字体对象  
        self.is_active = False  # 对话框是否激活  

    def render(self):  
        if self.is_active:  
            pygame.draw.rect(self.win, (255, 255, 255), (dialog_setting.box_start_x, dialog_setting.box_start_y, dialog_setting.box_wid, dialog_setting.box_high))  # 对话框背景  
            pygame.draw.rect(self.win, (0, 0, 0), (dialog_setting.box_start_x, dialog_setting.box_start_y, dialog_setting.box_wid, dialog_setting.box_high), 2)  # 对话框边框  

            if self.current_index < len(self.dialogues):  
                text_surface = self.font.render(self.dialogues[self.current_index], True, (0, 0, 0))  
                self.win.blit(text_surface, (dialog_setting.box_start_x + 30, dialog_setting.box_start_y + 30))  # 显示文本  
    