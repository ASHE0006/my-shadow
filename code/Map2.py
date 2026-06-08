from Settings2 import *
import pygame

def gen_map():
    image = GamePath.groundTiles
    image = pygame.transform.scale(pygame.image.load(image), (WindowSettings.width, WindowSettings.height))

    bg_map = image
    return bg_map
