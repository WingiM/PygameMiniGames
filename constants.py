# Объявление констант, определяющих работу игр
SIZE = WIDTH, HEIGHT = 1200, 800  # Большое разрешение экрана лучше не ставить
FPS = 120
SOUND_DIR = 'Sounds'
LOAD_DIR = 'data'
COLORS = {'red': (255, 102, 102),
          'blue': (0, 153, 255),
          'white': (255, 255, 255),
          'green': (102, 204, 0),
          'orange': (255, 102, 51),
          'dark green': (0, 102, 0),
          'black': (12, 12, 12)}  # Цвета, используемые в играх

# Константы для игры в крестики-нолики
TTT_CLICK_SOUND = 'click.mp3'
TTT_WIN_SOUND = 'ttt_win.mp3'
TTT_CELL_SIZE = WIDTH // 10

# Константы для игры в сумо
SUMO_WIN_SOUND = 'sumo_victory.mp3'
SUMO_PLAYER1 = (300, 190)
SUMO_PLAYER2 = (300, 410)
SUMO_MOVES = (0, 30)  # Перемещение игроков по оси x и y соответственно

# Константы для игры в "Украсть бриллиант"
STD_TIME_RANGE = (2000, 4000)  # От 2х до 6и секунд
STD_DELAY = 100
STD_EVENT_TYPE = 32775
STD_HAND1_EVENT = 32776
STD_HAND2_EVENT = 32777
STD_HAND_DELAY = 50
STD_HAND_SPEED = 200  # Желательно не ставить высокие значения

# Константы для игры в Аэро хоккей
AH_STICK_RADIUS = 40
AH_STICK_SPEED = 400
AH_STICK_MASS = 2000
AH_PUCK_RADIUS = 30
AH_PUCK_SPEED = 1000  # Рекомендуется задавать начальную скорость не равную нулю во избежание нечестной игры
AH_PUCK_MASS = 500
AH_FRICTION = 0.998
AH_SPEED_LIMIT = 1500
AH_STICK1X = 20
AH_STICK1Y = HEIGHT // 2
AH_STICK2X = WIDTH - 20
AH_STICK2Y = HEIGHT // 2
AH_GOAL_WIDTH = 180
AH_GOAL_Y1 = HEIGHT // 2 - AH_GOAL_WIDTH // 2
AH_GOAL_Y2 = HEIGHT // 2 + AH_GOAL_WIDTH // 2
AH_STICK1_COLOR = COLORS['red']
AH_STICK2_COLOR = COLORS['blue']
AH_FIELD_COLOR = COLORS['green']
AH_PUCK_COLOR = COLORS['orange']
AH_BORDER_COLOR = COLORS['dark green']
AH_GOAL_COLOR = COLORS['black']
