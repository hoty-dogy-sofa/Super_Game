import pygame
import os
import sys
pygame.init()
size = width, height = 1200, 650
screen = pygame.display.set_mode(size)
sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


class Menu_screen:
    def __init__(self):
        fon = pygame.transform.scale(load_image('fon2.jpg'), size)
        screen.blit((fon), (0, 0))
        font = pygame.font.Font(None, 50)
        text_coord = 0
        intro_text = ['Рекорды', 'Новая игра', 'Обучение', "Информация о врагах/персонажах"]
        for line in range(len(intro_text)):
            string_rendered = font.render(intro_text[line], 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 90
            intro_rect.top = text_coord
            intro_rect.x = (1200 - intro_rect.width)//2
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    Menu_screen.on_click(self, event.pos)
            pygame.display.flip()

    def on_click(self, cell_coords):
        x = cell_coords[0]
        y = cell_coords[1]
        if 520 < x < 680 and 85 < y < 120:
            Records()
        if 500 < x < 700 and 215 < y < 245:
            New_Game()
        if 510 < x < 685 and 340 < y < 375:
            Education()
        if 295 < x < 900 and 460 < y < 495:
            Information()


class Records: #рекорды
    def __init__(self):
        print('рекорды')


class New_Game: #настройки игры
    def __init__(self):
        fon = pygame.transform.scale(load_image('fon_settings.jpg'), size)
        screen.blit((fon), (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), (900, 550, 280, 80))
        font = pygame.font.Font(None, 60)
        line = "Начать игру"
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 570
        intro_rect.x = 920
        screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    New_Game.on_click(self, event.pos)
            pygame.display.flip()

    def on_click(self, cell_coords):
        x = cell_coords[0]
        y = cell_coords[1]
        if 900 < x < 1180 and 550 < y < 630:
            Game()


sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
tile_images = {'wall': load_image('box.png'),
              'empty': load_image('grass.png'),
               'end': load_image('end.jpg')}
player_image = load_image('mar.png')
tile_width = tile_height = 60


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                level[y][x] = '.'
            elif level[y][x] == '*':
                Tile('end', x, y)
    return new_player, x, y


class SpriteGroup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for i in self:
            i.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                               tile_height * self.pos[1] + 5)


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = 'data/' + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


level_map = None
player, max_x, max_y = None, None, None


def Dvech(hero, xod):
    x, y = hero.pos
    if xod == 'up':
        if y > 0 and level_map[y - 1][x] == '.':
            hero.move(x, y - 1)
        elif y > 0 and level_map[y - 1][x] == '*':
            hero.move(x, y - 1)
            End()
    elif xod == 'down':
        if y < max_y - 1 and level_map[y + 1][x] == '.':
            hero.move(x, y + 1)
        elif y < max_y - 1 and level_map[y + 1][x] == '*':
            hero.move(x, y + 1)
            End()
    elif xod == 'left':
        if x > 0 and level_map[y][x - 1] == '.':
            hero.move(x - 1, y)
        elif x > 0 and level_map[y][x - 1] == '*':
            hero.move(x - 1, y)
            End()
    elif xod == 'right':
        if x < max_x - 1 and level_map[y][x + 1] == '.':
            hero.move(x + 1, y)
        elif x < max_x - 1 and level_map[y][x + 1] == '*':
            hero.move(x + 1, y)
            End()


class Game:
    def __init__(self):
        player = None
        running = True
        global level_map, max_x, max_y
        level_map = load_level('map')
        player, max_x, max_y = generate_level(level_map)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        Dvech(player, 'up')
                    if event.key == pygame.K_DOWN:
                        Dvech(player, 'down')
                    if event.key == pygame.K_RIGHT:
                        Dvech(player, 'right')
                    if event.key == pygame.K_LEFT:
                        Dvech(player, 'left')
            screen.fill(pygame.Color('black'))
            sprite_group.draw(screen)
            hero_group.draw(screen)
            pygame.display.flip()


class End:
    def __init__(self):
        pass


class Education: #обучение
    def __init__(self):
        print('рекорды')


class Information: #информация о фрагах и персонажах
    def __init__(self):
        print('информация')


def start_screen():
    fon = pygame.transform.scale(load_image('fon1.jpg'), size)
    screen.blit((fon), (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


if __name__ == '__main__':
    pygame.display.set_caption('Побег из хранилища')
    running = True
    start_screen()
    Menu_screen()
