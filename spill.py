import pygame
from random import randint


WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
screen_height = 1000
screen_width = 1000


class Tower:
    width = 60
    height = 90

    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)
        self.name = name
        self.image = pygame.image.load("tower.png")
        self.scaled_image = pygame.transform.scale(self.image, (self.width, self.height))

    def __str__(self):
        return self.name

    __repr__ = __str__

    def draw(self):
        self.rec = screen.blit(self.scaled_image, (self.x, self.y))

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
        print(self.x, self.y)

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

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = x
        self.speed = 5
        self.last_pos = [(self.x, self.y)]
        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)

    def __str__(self):
        return self.name

    __repr__ = __str__

    def update_pose(self, objects):
        new_background = False
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

            elif isinstance(obj, Tower):
                if self.rec.colliderect(obj.rec):
                        print(self, "collided with", obj)
                        new_background = True


            else:
                print("problem!", obj)
        return new_background

    def draw(self):
        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, RED, self.rec)

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



def create_world(name: str):

    print("creating world")
    kart = open(name, "r")
    all_objects = []
    enemies = []
    walls = []
    chests = []
    towers = []
    print(kart)
    x = 0
    y = 0
    print(x, y)
    player = None

    if name.startswith("tower"):
        background_image = pygame.image.load("bagrunn_tower.png")
    else:
        background_image = pygame.image.load("main_backgrunn.jpg")

    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))


    for line in kart.readlines():
        y += 30
        x = 0
        for col in line:
            x += 30
            if col == ".":
                continue
            elif col == "P":
                player = Player("player" + str(x) + str(y), x, y)
                all_objects.append(player)
            elif col == "X":
                wall = Wall("wall " + str(x) + str(y), x, y)
                walls.append(wall)
                all_objects.append(wall)
            elif col == "C":
                chest = Chest("chest " + str(x) + str(y), x, y)
                chests.append(chest)
                all_objects.append(chest)
            elif col == "E":
                enemy = Enemy("enemy " + str(x) + str(y), x, y)
                enemies.append(enemy)
                all_objects.append(enemy)
            elif col == "T":
                tower = Tower("tower " + str(x) + str(y), x, y)
                towers.append(tower)
                all_objects.append(tower)
    if player is None:
        raise RuntimeWarning("player must be in the map")
    return enemies, walls, chests, all_objects, player, towers, kart, background_image


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    new_background = False

    enemies, walls, chests, all_objects, player, towers, kart, background_image = create_world("world.map")

    crashable_objects = walls + chests + towers

    running = True
    while running:

        if new_background:

            enemies, walls, chests, all_objects, player, towers, kart, background_image= create_world("tower.map")
            crashable_objects = walls + chests + towers
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
        for tower in towers:
            tower.draw()

        new_background = player.update_pose(crashable_objects)
        player.draw()

        pygame.display.flip()
        pygame.time.Clock().tick(20)
