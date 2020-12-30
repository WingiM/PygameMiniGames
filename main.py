import sys
import pygame
import pygame_gui
from constants import *  # Переносит все константы, использующиеся в проекте
from TicTacToe import TicTacToeBoard  # Поле для игры в крестики-нолики
from Sumo import SumoGame, Player, SUMO_field  # Поле для игры в сумо, а также класс игрока
from StealTheDiamond import StealTheDiamond, Hand, Diamond  # Экран игры в "Украсть бриллиант"
from AirHockey import Stick, Puck, AirHockey  # Поле для игры в Аэрохоккей
from load_image import load_image  # Для загрузки изображений (используется и в других частях проекта)

# Начало работы с pygame
pygame.init()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
manager = pygame_gui.UIManager(SIZE, 'style.json')

# Настройка игры в крестики нолики
TicTacToe = TicTacToeBoard(screen)
TicTacToe.set_view((WIDTH - TicTacToe.width * TTT_CELL_SIZE) // 2,
                   (HEIGHT - TicTacToe.height * TTT_CELL_SIZE) // 2, TTT_CELL_SIZE)

# Настройка игры в сумо
SUMO_all_sprites = pygame.sprite.Group()
SUMO_all_sprites.add(SUMO_field)
SUMO_player1 = Player(SUMO_all_sprites, pos=SUMO_PLAYER1)
SUMO_player2 = Player(SUMO_all_sprites, pos=SUMO_PLAYER2, transform=180)
Sumo = SumoGame(screen, SUMO_player1, SUMO_player2, SUMO_all_sprites)

# Настройка игры в "Украсть бриллиант"
STD_all_sprites = pygame.sprite.Group()
STD_diamond = Diamond(STD_all_sprites)
STD_hand1 = Hand(STD_all_sprites, number=1, diamond=STD_diamond)
STD_hand2 = Hand(STD_all_sprites, number=2, diamond=STD_diamond)
STD = StealTheDiamond(screen, STD_all_sprites, STD_hand1, STD_hand2, STD_diamond)

# Настройка игры в Аэро Хоккей
AH_stick1 = Stick(AH_STICK1_COLOR, AH_STICK1X, AH_STICK1Y)
AH_stick2 = Stick(AH_STICK2_COLOR, AH_STICK2X, AH_STICK2Y)
AH_puck = Puck(AH_PUCK_COLOR, WIDTH // 2, HEIGHT // 2)
AH = AirHockey(screen, AH_FIELD_COLOR, AH_stick1, AH_stick2, AH_puck)

# Настройка выпадающего списка
# Для добавления новой игры необходимо добавить в словарь ее название и класс
# Также игра должна иметь методы render() и restart()
# Обработку действий в игре можно написать в ф-ии play_game(), если игра статичная
# Если игра требует частых обновлений и проверок, то лучше написать в основной игровой цикл
# Например, как игра в Аэрохоккей
games_dict = {'Tic Tac Toe (Крестики-нолики)': TicTacToe,
              'Sumo (Сумо)': Sumo,
              'Steal The Diamond (Украсть бриллиант)': STD,
              'Air Hockey (Аэрохоккей)': AH}
game_changer = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
    options_list=list(games_dict.keys()),
    starting_option='Air Hockey (Аэрохоккей)',
    manager=manager,
    relative_rect=pygame.Rect((10, 10), (400, 50))
)


def play_game(game, event):  # Выполняет ивенты некоторых игр
    if game == TicTacToe:
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.get_click(event.pos)
    elif game == STD:
        if event.type == STD_EVENT_TYPE:
            game.update()
            if game.active:
                STD_hand1.can_move = True
                STD_hand2.can_move = True
        if event.type == STD_HAND1_EVENT:
            STD_hand1.move()
        if event.type == STD_HAND2_EVENT:
            STD_hand2.move()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                STD_hand1.pressed()
            if event.key == pygame.K_UP:
                STD_hand2.pressed()
    if game == Sumo:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                game.update(1)
            if event.key == pygame.K_UP:
                game.update(2)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('start_screen.png'), (WIDTH, HEIGHT))
    pygame.display.set_caption('Pygame Mini Games')
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def start_game():
    game = AH
    while True:
        time_delta = clock.get_time() / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            play_game(game, event)
            if event.type == pygame.KEYDOWN:
                # Перезапуск любой игры осуществляется через пробел
                if event.key == pygame.K_SPACE:
                    game.restart()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    game.restart()
                    game = games_dict[event.text]
            manager.process_events(event)
        if game == AH:
            keys = pygame.key.get_pressed()
            # Проверка кнопок Игрока 1
            w = keys[pygame.K_w]
            s = keys[pygame.K_s]
            d = keys[pygame.K_d]
            a = keys[pygame.K_a]
            # Проверка кнопок Игрока 2
            up = keys[pygame.K_UP]
            down = keys[pygame.K_DOWN]
            right = keys[pygame.K_RIGHT]
            left = keys[pygame.K_LEFT]
            # Перемещение Игрока 1
            AH_stick1.move(w, s, a, d, time_delta)
            AH_stick1.check_vertical()
            AH_stick1.check_left()
            # Перемещение Игрока 2
            AH_stick2.move(up, down, left, right, time_delta)
            AH_stick2.check_vertical()
            AH_stick2.check_right()
            # Перемещение шайбы
            AH_puck.move(time_delta)
            if game.goal():  # Если шайба попала в ворота - перезапуск игры
                pygame.mixer.Sound.play(AirHockey.goal_sound)
                game.restart()
            AH_puck.check()
            if AH_puck.check_collision(AH_stick1):  # Отскоки
                pygame.mixer.Sound.play(AirHockey.hit_sound)
            if AH_puck.check_collision(AH_stick2):  # Отскоки
                pygame.mixer.Sound.play(AirHockey.hit_sound)
        pygame.display.set_caption(game.caption)
        screen.fill((0, 0, 0))
        manager.update(time_delta)
        game.render()
        manager.draw_ui(screen)
        clock.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    start_screen()
    start_game()
