# Объявление констант, определяющих работу игр
SIZE = WIDTH, HEIGHT = 800, 800
FPS = 60
SOUND_DIR = 'Sounds'
LOAD_DIR = 'data'
COLORS = {'red': (255, 102, 102),
          'blue': (0, 153, 255)}

# Константы для игры в крестики-нолики
TTT_CLICK_SOUND = 'click.mp3'
TTT_WIN_SOUND = 'ttt_win.mp3'
TTT_CELL_CIZE = 100

# Константы для игры в сумо
SUMO_WIN_SOUND = 'sumo_victory.mp3'
SUMO_PLAYER1 = (300, 190)
SUMO_PLAYER2 = (300, 410)
SUMO_MOVES = (0, 30)  # Перемещение в сумо по оси x и y соответственно

# Константы для игры в "Украсть бриллиант"
STD_TIME_RANGE = (2000, 4000)  # От 2х до 6и миллисекунд
STD_DELAY = 100
STD_EVENT_TYPE = 32775
STD_HAND1_EVENT = 32776
STD_HAND2_EVENT = 32777
STD_HAND_DELAY = 50
STD_HAND_SPEED = 200  # Желательно не ставить высокие значения
