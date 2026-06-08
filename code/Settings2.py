from enum import Enum

class WindowSettings:
    name = "战斗, 爽!"
    width = 1280
    height = 720
    outdoorScale = 1.5

class PlayerSettings:
    playerspeed = 5
    playerwidth = 100
    playerheight = 100

class MonsterSettings:
    monsterSpeed = 1.5
    monsterwidth = 100
    monsterheight = 100

class Flying_bookSettings:
    flying_bookSpeed = 4
    flying_bookwidth = 100
    flying_bookheight = 70

class BulletSettings:
    bulletSpeed_M = 5
    bulletradiu_M = 15
    bulletSpeed_P = 7
    bulletradiu_P = 10

class SceneSettings:
    tileXnum = 48
    tileYnum = 27
    tileWidth = tileHeight = 40

class GamePath:
    player = r'.\assets\9F1031A9DF932FE2E203690232CC59A8.png'
    groundTiles = r'.\assets\background3-720.png'
    monster = r'.\assets\小怪.png'
    flying_book_1 = r'.\assets\静态书.PNG'
    flying_book_2 = r'.\assets\动态书.PNG'
    boss = r'.\assets\boss.png'

class GameState(Enum):
    GameStart = 0
    GameOver = 1
    GameWin = 2
    GamePause = 3
    GameRun = 4