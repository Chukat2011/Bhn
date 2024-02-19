import pygame
from pygame.locals import *
import tkinter as tk
from tkinter import filedialog

# Инициализация Pygame
pygame.init()

# Размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.original_image = image
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.selected = False

    def scale(self, factor):
        width = max(int(self.original_image.get_width() * factor), 1)
        height = max(int(self.original_image.get_height() * factor), 1)
        self.image = pygame.transform.scale(self.original_image, (width, height))
        self.rect = self.image.get_rect(center=self.rect.center)

class Player(Sprite):
    def update(self, keys):
        if keys[pygame.K_w]:
            self.rect.y -= 5
        if keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_s]:
            self.rect.y += 5
        if keys[pygame.K_d]:
            self.rect.x += 5

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("2D Game Engine")

        self.sprites = pygame.sprite.Group()

        # Создаем кнопку для загрузки изображений
        self.load_button = pygame.Rect(10, 10, 100, 50)
        self.play_button = pygame.Rect(10, 70, 100, 50)
        self.font = pygame.font.Font(None, 36)

        self.selected_sprite = None
        self.players = []
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            image = pygame.image.load(file_path)
            sprite = Sprite(image, 0, 0)
            self.sprites.add(sprite)

    def create_player(self):
        if self.selected_sprite:
            player = Player(self.selected_sprite.image, 100, 100)
            self.players.append(player)

    def scale_selected_sprite(self, factor):
        if self.selected_sprite:
            self.selected_sprite.scale(factor)

    def run(self):
        running = True
        while running:
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.load_button.collidepoint(mouse_pos):
                            self.load_image()
                        elif self.play_button.collidepoint(mouse_pos):
                            self.create_player()

                        for sprite in self.sprites:
                            if sprite.rect.collidepoint(mouse_pos):
                                self.selected_sprite = sprite
                                self.offset_x = sprite.rect.x - mouse_pos[0]
                                self.offset_y = sprite.rect.y - mouse_pos[1]
                                self.dragging = True
                                break

                    elif event.button == 4:  # Прокрутка колесика вверх
                        self.scale_selected_sprite(0.9)  # Уменьшаем размер спрайта на 10%
                    elif event.button == 5:  # Прокрутка колесика вниз
                        self.scale_selected_sprite(1.1)  # Увеличиваем размер спрайта на 10%

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.dragging = False

            if self.dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.selected_sprite.rect.x = mouse_x + self.offset_x
                self.selected_sprite.rect.y = mouse_y + self.offset_y

            self.screen.fill(WHITE)

            # Отображаем кнопки
            pygame.draw.rect(self.screen, (0, 255, 0), self.load_button)
            text_surface = self.font.render("Load", True, (0, 0, 0))
            self.screen.blit(text_surface, (25, 25))

            pygame.draw.rect(self.screen, (0, 255, 0), self.play_button)
            text_surface = self.font.render("Play", True, (0, 0, 0))
            self.screen.blit(text_surface, (25, 85))

            # Отображаем спрайты
            self.sprites.draw(self.screen)

            # Обновляем игроков
            for player in self.players:
                player.update(keys)
                self.screen.blit(player.image, player.rect)

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
