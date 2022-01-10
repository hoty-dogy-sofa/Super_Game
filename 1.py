import pygame
import os
import sys


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    return image

pygame.init()
size = width, height = 1200, 650
screen = pygame.display.set_mode(size)
sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()


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
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
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
        pass


class New_Game: #настройки игры
    def __init__(self):
        fon = pygame.transform.scale(load_image('fon_settings.jpg'), size)
        screen.blit((fon), (0, 0))

    def on_click(self, cell_coords):
        x = cell_coords[0]
        y = cell_coords[1]
        print(x, y)


class Education: #обучение
    def __init__(self):
        pass


class Information: #информация о фрагах и персонажах
    def __init__(self):
        pass


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), size)
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
    Menu_screen()print(12)
print(15)
