import pygame
from random import randint
import random


WHITE = (255, 255, 255)
RED = (255, 0, 0)
screen_height = 500
screen_width = 500


class Enemies:
    def __init__(self, name, x, y):
        self.name = name
        self.width = 30
        self.height = 30
        self.x = x
        self.y = y
        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)
        self.last_pos = [(self.x, self.y)]

    def __str__(self):
        return self.name

    __repr__ = __str__

    def draw(self):
        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, WHITE, self.rec)

    def update_pose(self, objects):
        self.last_pos.append((self.x, self.y))
        dx = random.choice([-5, 0, 5])
        dy = random.choice([-5, 0, 5])

        self.x += dx
        self.y += dy

        for obj in objects:
            if isinstance(obj, Wall):
                if self.rec.colliderect(obj.rec):
                    if len(self.last_pos) >= 3:
                        self.x, self.y = self.last_pos[-3]
                    else:
                        self.x, self.y = self.last_pos[0]
                    print(self, "collided with ", obj)


class Wall:
    def __init__(self, name, x, y):
        self.name = name
        self.width = 30
        self.height = 30
        self.x = x
        self.y = y
        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = pygame.image.load("wall.png")
        self.scaled_image = pygame.transform.scale(self.image, (self.width, self.height))

    def __str__(self):
        return self.name

    __repr__ = __str__

    def draw(self):
        self.rec = screen.blit(self.scaled_image, (self.x, self.y))


class Chest:
    def __init__(self, name, x, y):
        self.name = name
        self.width = 30
        self.height = 30
        self.x = x
        self.y = y
        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = pygame.image.load("chest.png")
        self.scaled_image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self):
        self.rec = screen.blit(self.scaled_image, (self.x, self.y))

    def __str__(self):
        return self.name

    __repr__ = __str__


class Player:
    def __init__(self):
        self.width = 30
        self.height = 30
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height // 2 - self.height // 2
        self.speed = 3
        self.last_pos = [(self.x, self.y)]
        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)

    def __str__(self):
        return "Player"

    __repr__ = __str__

    def update_pose(self, objects):
        button = pygame.key.get_pressed()
        self.last_pos.append((self.x, self.y))

        if button[pygame.K_a]:
            self.x -= self.speed
        if button[pygame.K_d]:
            self.x += self.speed
        if button[pygame.K_w]:
            self.y -= self.speed
        if button[pygame.K_s]:
            self.y += self.speed

        for obj in objects:
            if isinstance(obj, Chest):
                if self.rec.colliderect(obj.rec):
                    print(self, "collided with ", obj)

            elif isinstance(obj, Wall):
                if self.rec.colliderect(obj.rec):
                    if len(self.last_pos) >= 3:
                        self.x, self.y = self.last_pos[-3]
                    else:
                        self.x, self.y = self.last_pos[0]
                    print(self, "collided with ", obj)

            else:
                print("problem!", obj)

    def draw(self):
        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, RED, self.rec)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    background_image = pygame.image.load("backgrunn.jpg")
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    enemies = [Enemies("enemy" + str(i), randint(0, 300), randint(0, 300)) for i in range(1)]
    player = Player()
    walls = [Wall("wall" + str(i), randint(0, 300), randint(0, 300)) for i in range(5)]
    chests = [Chest("chest " + str(i), randint(0, 400), randint(0, 400)) for i in range(5)]

    all_objects = walls + chests

    running = True
    while running:
        screen.blit(background_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for chest in chests:
            chest.draw()
        for wall in walls:
            wall.draw()
        for enemy in enemies:
            enemy.update_pose(all_objects)
            enemy.draw()

        player.update_pose(walls)
        player.update_pose(all_objects)
        player.draw()

        pygame.display.flip()
        pygame.time.Clock().tick(20)
