# Объявление констант, определяющих работу игр
SIZE = WIDTH, HEIGHT = 800, 800
FPS = 60
CELL_SIZE = 100  # Для игр с клетчатым полем (17.12.2020 - TicTacToe)
SOUND_DIR = 'Sounds'
LOAD_DIR = 'data'
COLORS = {'red': (255, 102, 102),
          'blue': (0, 153, 255)}

# Константы для игры в крестики-нолики
TTT_CLICK_SOUND = 'click.mp3'
TTT_WIN_SOUND = 'ttt_win.mp3'

# Константы для игры в сумо
SUMO_WIN_SOUND = 'sumo_victory.mp3'
SUMO_PLAYER1 = (300, 190)
SUMO_PLAYER2 = (300, 410)
SUMO_MOVES = (0, 30)  # Перемещение в сумо по оси x и y соответственно
