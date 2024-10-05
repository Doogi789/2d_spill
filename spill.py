import pygame
from random import randint


WHITE = (255, 255, 255)
RED = (255, 0, 0)
screen_height = 500
screen_width = 500


class Enemy:
    width = 30
    height = 30

    def __init__(self, name, x, y):
        self.name = name

        self.x = x
        self.y = y
        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)
        self.last_pos = [(self.x, self.y)]
        self.speed = 2
        self.target_y = randint(0, screen_height - self.height)
        self.target_x = randint(0, screen_width - self.width)

    def __str__(self):
        return self.name

    __repr__ = __str__

    def draw(self):
        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, WHITE, self.rec)

    def movement_enemy(self, objects):
        self.last_pos.append((self.x, self.y))
        distance_x = self.target_x - self.x
        distance_y = self.target_y - self.y

        if abs(distance_x) > self.speed / 2 and abs(distance_y) > self.speed / 2:
            if abs(distance_x) >= abs(distance_y):
                if distance_x > 0:
                    self.x += self.speed
                else:
                    self.x -= self.speed
            else:
                if distance_y > 0:
                    self.y += self.speed
                else:
                    self.y -= self.speed
        else:
            self.target_y = randint(0, screen_height - self.height)
            self.target_x = randint(0, screen_width - self.width)

        for obj in objects:
            if isinstance(obj, Wall):
                if self.rec.colliderect(obj.rec):
                    if len(self.last_pos) >= 3:
                        self.x, self.y = self.last_pos[-3]

                    else:
                        self.x, self.y = self.last_pos[0]
                    print(self, "collided with ", obj)


class Wall:
    width = 30
    height = 30

    def __init__(self, name, x, y):
        self.name = name
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
    width = 30
    height = 30

    def __init__(self, name, x, y):
        self.name = name
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
    width = 30
    height = 30

    def __init__(self):
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height // 2 - self.height // 2
        self.speed = 3
        self.last_pos = [(self.x, self.y)]
        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)

    def __str__(self):
        return "Playmovement_enemyer"

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


class recipies:
    def house():
        chests = []
        walls = []
        enemis = []

        return walls, chests, enemies


def has_collision(x, y, width, height, all_objects):
    for obj in all_objects:
        print(
            x,
            y,
            obj.x,
            obj.y,
            type(obj),
        )
        if x - obj.width < obj.x < x + obj.width and y - obj.height < obj.y < y + obj.height:
            print("collision")
            return True
        print("ok")
    print("NO COLLISIOk")
    return False


def find_available_x_y(width, height, all_objects):
    while True:
        x = randint(0, 500)
        y = randint(0, 500)
        if not has_collision(x, y, width, height, all_objects):
            return x, y


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    background_image = pygame.image.load("backgrunn.jpg")
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    player = Player()
    all_objects = [player]

    enemies = []
    for i in range(2):
        x, y = find_available_x_y(Enemy.width, Enemy.height, all_objects)
        enemy = Enemy("Enemy" + str(i), x, y)
        enemies.append(enemy)
        all_objects.append(enemy)

    walls = []
    for i in range(5):
        x, y = find_available_x_y(Wall.width, Wall.height, all_objects)
        wall = Wall("wall" + str(i), x, y)
        print(x, y, wall)
        walls.append(wall)
        all_objects.append(wall)

    chests = []
    for i in range(5):
        x, y = find_available_x_y(Chest.width, Chest.height, all_objects)
        chest = Chest("chest" + str(i), x, y)
        print(x, y, chest)
        chests.append(chest)
        all_objects.append(chest)

    crashable_objects = walls + chests
    print(type(crashable_objects))

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
            enemy.movement_enemy(crashable_objects)
        enemy.draw()

        player.update_pose(crashable_objects)

        player.draw()

        pygame.display.flip()
        pygame.time.Clock().tick(20)
