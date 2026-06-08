import pygame
from settings import *

SHOP_ITEMS = [
    {
        "name": "增加血量(+50HP)",
        "type": "hp",
        "price": 30,
        "amount": 50
    },
    {
        "name": "解锁圣水攻击",
        "type": "bullet",
        "price": 50,
        "color": (0, 255, 0)
    },
    {
        "name": "解锁火焰攻击",
        "type": "bullet",
        "price": 80,
        "color": (255, 0, 0)
    },
]
class Shop:
    def __init__(self, player):
        """
        :param player: 传入 Player 对象，用于金币判断、解锁弹幕、加血等
        """
        self.player = player
        self.items = SHOP_ITEMS  # 也可以在外面再传进来
        self.selected_index = 0  # 当前在商店中选中的商品序号
        self.font = game_path.font

        # active 判断商店是否处于“打开”状态
        self.active = False

    def open(self):
        """ 打开商店 """
        self.active = True
        self.selected_index = 0

    def close(self):
        """ 关闭商店 """
        self.active = False

    def handle_event(self, event):
        """
        当商店处于打开状态时，在主循环里把事件(event)传给它,
        以监听玩家的按键操作。
        """
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                # 按 ESC 退出商店
                self.close()
            elif event.key == pygame.K_UP:
                # 向上移动选择
                self.selected_index = (self.selected_index - 1) % len(self.items)
            elif event.key == pygame.K_DOWN:
                # 向下移动选择
                self.selected_index = (self.selected_index + 1) % len(self.items)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # 回车或空格执行购买
                self.buy_item(self.selected_index)

    def buy_item(self, index):
        """ 购买指定序号的商品 """
        item = self.items[index]
        price = item["price"]
        if self.player.coin < price:
            print("金币不足，无法购买！")
            return

        # 扣除金币
        self.player.coin -= price
        print(f"成功购买：{item['name']}，花费 {price} 金币！剩余金币: {self.player.coin}")

        # 根据商品类型给予不同效果
        if item["type"] == "hp":
            self.player.HP += item["amount"]
            print(f"当前HP:{self.player.HP}")
        elif item["type"] == "bullet":
            # 加入到已解锁的子弹颜色集合
            self.player.unlocked_bullet_colors.add(item["color"])
            print(f"解锁子弹颜色：{item['color']}，已解锁列表：{self.player.unlocked_bullet_colors}")

        # 购买完毕后也可以选择自动退出商店
        # self.close()

    def update(self):
        """
        如果有需要在商店里做一些动画或其他逻辑，可以写在这里。
        """
        pass

    def draw(self, surface):
        """
        渲染商店界面
        """
        # 先把屏幕涂成半透明/纯色背景，突出商店界面
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # 半透明黑
        surface.blit(overlay, (0, 0))

        # 显示标题
        title_text = self.font.render("商店", True, (255, 255, 0))
        surface.blit(title_text, (00, 50))

        # 依次绘制商品列表
        start_y = 120
        gap = 50
        for i, item in enumerate(self.items):
            # 如果是当前选中的，就给一个特殊颜色或前缀
            prefix = ">> " if i == self.selected_index else "   "
            text_content = f"{prefix}{item['name']} - 价格: {item['price']}"
            text_render = self.font.render(text_content, True, (255, 255, 255))
            surface.blit(text_render, (30, start_y + i * gap))

        # 显示玩家当前金币
        coin_text = f"当前金币: {self.player.coin}"
        coin_render = self.font.render(coin_text, True, (255, 255, 0))
        surface.blit(coin_render, (30, start_y + len(self.items) * gap + 30))
