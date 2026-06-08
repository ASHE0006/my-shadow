import pygame
import numpy as np

# 检测像素级碰撞的函数
def check_collision(bullet, project):

    if not bullet.rect.colliderect(project.rect):
        return False

    overlap_rect = bullet.rect.clip(project.rect)
    if overlap_rect.width == 0 or overlap_rect.height == 0:
        return False

    # 计算重叠区域在各自图像中的偏移
    bx = overlap_rect.x - bullet.rect.x
    by = overlap_rect.y - bullet.rect.y
    px = overlap_rect.x - project.rect.x
    py = overlap_rect.y - project.rect.y
    w = overlap_rect.width
    h = overlap_rect.height

    # 用surfarray批量获取像素数据，避免逐像素循环
    bullet_array = pygame.surfarray.pixels3d(bullet.image)
    bullet_alpha = pygame.surfarray.pixels_alpha(bullet.image)
    project_alpha = pygame.surfarray.pixels_alpha(project.image)

    # 截取重叠区域
    b_rgb = bullet_array[bx:bx+w, by:by+h]
    b_alpha = bullet_alpha[bx:bx+w, by:by+h]
    p_alpha = project_alpha[px:px+w, py:py+h]

    # 找到两者都不透明的区域
    overlap_mask = (b_alpha > 0) & (p_alpha > 0)

    if not np.any(overlap_mask):
        return False

    # 取第一个碰撞像素的颜色判断子弹类型
    positions = np.argwhere(overlap_mask)
    if len(positions) == 0:
        return False

    fx, fy = positions[0]
    r, g, b = b_rgb[fx, fy]

    if r == 255 and g == 255 and b == 255:  # 白色
        return 1
    elif r == 0 and g == 255 and b == 0:    # 绿色
        return 2
    elif r == 255 and g == 0 and b == 0:    # 红色
        return 3

    return False
