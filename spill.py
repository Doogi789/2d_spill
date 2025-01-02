"""My 2d topdown game"""

import sys
from random import randint
from enum import Enum, auto

import pygame

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WORLD_HEIGHT = 1000
WORLD_WIDTH = 1000
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500


def split_into_chunks(n, x):
    # Full chunks
    full_chunks = n // x

    # Remainder after full chunks
    remainder = n % x

    # Create the list of chunks
    chunks = [x] * full_chunks  # full chunks of size x

    # Add the remainder chunk
    if remainder > 0:
        chunks.append(remainder)

    # If you want to pad with 0s to match a fixed number of chunks (like in the example of 5)
    while len(chunks) < 3:
        chunks.append(0)

    return chunks


def knockback(obj, x, y):
    force = 25
    # print(obj)
    if obj.direction.x == 1:
        x += force
    if obj.direction.x == -1:
        x -= force
    if obj.direction.y == 1:
        y += force
    if obj.direction.y == -1:
        y -= force

    return (x, y)


def collision(obj, rect):
    dx = rect.centerx - obj.rect.centerx
    dy = rect.centery - obj.rect.centery

    if abs(dx) > abs(dy):
        if dx > 0:
            rect.x = obj.rect.right
        else:
            rect.x = obj.rect.left - rect.width
    else:
        if dy > 0:
            rect.y = obj.rect.bottom
        else:
            rect.y = obj.rect.top - rect.height

    return rect.x, rect.y


class Nothing(pygame.sprite.Sprite):
    width = 30
    height = 30

    def __init__(self, screen, name, x, y):
        super().__init__()
        self.screen = screen
        self.name = name
        self.x = x
        self.y = y
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLACK)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.topleft = (x, y)

    def __str__(self):
        return self.name

    __repr__ = __str__


class Door(pygame.sprite.Sprite):
    width = 30
    height = 30

    def __init__(self, screen, name, x, y):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.name = name
        self.original_image = pygame.image.load("door.png")
        self.image = pygame.transform.scale(
            self.original_image, (self.width, self.height)
        )
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.topleft = (x, y)

    def __str__(self):
        return self.name

    __repr__ = __str__


class House(pygame.sprite.Sprite):
    width = 60
    height = 60

    def __init__(self, screen, name, x, y):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.name = name
        self.original_image = pygame.image.load("house.png")
        self.image = pygame.transform.scale(
            self.original_image, (self.width, self.height)
        )
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.topleft = (x, y)

    def __str__(self):
        return self.name

    __repr__ = __str__


class Tower(pygame.sprite.Sprite):
    width = 60
    height = 90

    def __init__(self, screen, name, x, y):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.name = name
        self.original_image = pygame.image.load("tower.png")
        self.image = pygame.transform.scale(
            self.original_image, (self.width, self.height)
        )
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.topleft = (x, y)

    def __str__(self):
        return self.name

    __repr__ = __str__


class Enemy(pygame.sprite.Sprite):
    width = 30
    height = 30

    def __init__(self, screen, name, x, y):
        super().__init__()
        # variabler som er hentet
        self.name = name
        self.x = x
        self.y = y
        self.screen = screen
        # variabler for å tegne
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((WHITE))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.topleft = (x, y)
        # variabler får å bevege
        self.speed = 0.4
        self.target_y = randint(0, WORLD_HEIGHT - self.height)
        self.target_x = randint(0, WORLD_WIDTH - self.width)
        self.life = 10
        # knockback
        self.direction = pygame.math.Vector2()

    def __str__(self):
        return self.name

    __repr__ = __str__

    def update_pose(self, p_x, p_y, game):
        distance_player = ((self.x - p_x) ** 2 + (self.y - p_y) ** 2) ** 0.5

        if abs(distance_player) < 80 + self.width and not game.player_imunity:
            self.target_x = p_x
            self.target_y = p_y

        distance_x = self.target_x - self.x
        distance_y = self.target_y - self.y

        if abs(distance_x) > self.speed / 2 and abs(distance_y) > self.speed / 2:
            if abs(distance_x) >= abs(distance_y):
                if distance_x > 0:
                    self.x += self.speed
                    self.direction.x = 1
                else:
                    self.x -= self.speed
                    self.direction.x = -1
            else:
                if distance_y > 0:
                    self.y += self.speed
                    self.direction.y = 1
                else:
                    self.y -= self.speed
                    self.direction.y = -1
        else:
            self.target_y = randint(0, WORLD_HEIGHT - self.height)
            self.target_x = randint(0, WORLD_WIDTH - self.width)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def check_collision(self, objects):
        for obj in objects:
            if isinstance(obj, (Chest, Tower, House, Door)):
                if self.rect.colliderect(obj.rect):
                    self.x, self.y = collision(obj, self.rect)

            if isinstance(obj, (Wall)):
                if self.rect.colliderect(obj.rect):
                    self.target_y = randint(0, WORLD_HEIGHT - self.height)
                    self.target_x = randint(0, WORLD_WIDTH - self.width)
                    self.x, self.y = collision(obj, self.rect)

            if isinstance(obj, (PlayerSword)):
                if self.rect.colliderect(obj.rect):
                    self.life -= 10
                    self.x, self.y = knockback(obj, self.x, self.y)

                    #  print(self, "collided with ", obj)

    def update(self, game):
        # print("enemy")
        for enemy in game.enemies:
            enemy.update_pose(game.player.x, game.player.y, game)
            enemy.check_collision(game.all_objects)


class Wall(pygame.sprite.Sprite):
    width = 30
    height = 30

    def __init__(self, screen, name, x, y):
        super().__init__()
        self.screen = screen
        self.name = name
        self.x = x
        self.y = y
        self.original_image = pygame.image.load("wall.png")
        self.image = pygame.transform.scale(
            self.original_image, (self.width, self.height)
        )
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.topleft = (x, y)

    def __str__(self):
        return self.name

    __repr__ = __str__


class Chest(pygame.sprite.Sprite):
    width = 30
    height = 30

    def __init__(self, screen, name, x, y):
        super().__init__()
        self.screen = screen
        self.name = name
        self.x = x
        self.y = y
        self.original_image = pygame.image.load("chest.png")
        self.image = pygame.transform.scale(
            self.original_image, (self.width, self.height)
        )
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def __str__(self):
        return self.name

    __repr__ = __str__


class Direction(Enum):
    XPLUS = auto()
    XMINUS = auto()


class PlayerLife:
    width = 50
    height = 50

    def __init__(self, screen, name, x, y):
        self.direction = 1
        self.screen = screen
        self.x = x
        self.y = y
        self.life = 12
        self.max_life = self.life
        self.name = name
        self.rec = (self.x, self.y, self.width, self.height)
        self.hearts = [
            pygame.image.load(f"hearts/heart_{i}.png").convert_alpha() for i in range(5)
        ]
        self.dead: bool = False

    def increase(self):
        self.life += 1
        self.life = min(self.max_life, self.life)

    def decrease(self):
        self.life -= 1
        if self.life <= 0:
            self.dead = True
        return self.dead

    def __str__(self):
        return self.name

    __repr__ = __str__

    def draw(self):
        for idx, heart_idx in enumerate(split_into_chunks(self.life, 4)):
            image = self.hearts[heart_idx]

            scaled_image = pygame.transform.scale(image, (self.width, self.height))

            x = self.x + (self.width * idx)

            self.rec = self.screen.blit(scaled_image, (x, self.y))


class PlayerSword(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_xpluss = pygame.transform.scale_by(
            pygame.image.load("swords/sword_x+.png"), 0.3
        )
        self.image_xminus = pygame.transform.scale_by(
            pygame.image.load("swords/sword_x-.png"), 0.3
        )
        self.image_ypluss = pygame.transform.scale_by(
            pygame.image.load("swords/sword_y+.png"), 0.3
        )
        self.image_yminus = pygame.transform.scale_by(
            pygame.image.load("swords/sword_y-.png"), 0.3
        )
        self.hidden_image = pygame.Surface(
            self.image_yminus.get_rect().size, pygame.SRCALPHA
        )
        self.hidden_image.fill((0, 0, 0, 0))
        self.image = self.hidden_image
        self.rect = self.image.get_rect()
        self.timer = 0
        self.show_sword = False
        self.can_use_sword = False

    def attack(self):
        button = pygame.key.get_pressed()
        if not button[pygame.K_SPACE]:
            self.can_use_sword = True
        if button[pygame.K_SPACE] and self.can_use_sword:
            self.show_sword = True
            self.timer = 0
            self.can_use_sword = False

    def update_pos(self, player):
        self.direction = player.direction
        if self.show_sword:
            self.timer += 1
            if player.direction == pygame.math.Vector2(0, 0):
                self.image = self.image_xpluss
                self.rect = self.image.get_rect(midleft=player.rect.midleft)
            if player.direction.x == 1:
                self.image = self.image_xpluss
                self.rect = self.image.get_rect(midleft=player.rect.midleft)

            elif player.direction.x == -1:
                self.image = self.image_xminus
                self.rect = self.image.get_rect(midright=player.rect.midright)

            elif player.direction.y == 1:
                self.image = self.image_ypluss
                self.rect = self.image.get_rect(midtop=player.rect.midtop)

            elif player.direction.y == -1:
                self.image = self.image_yminus
                self.rect = self.image.get_rect(midbottom=player.rect.midbottom)

            if self.timer == 10:
                self.image = self.hidden_image
                self.show_sword = False


class Player(pygame.sprite.Sprite):
    width = 30
    height = 30

    def __init__(self, screen, name, x, y):
        super().__init__()
        self.screen = screen
        self.name = name
        self.x = x
        self.y = y
        self.speed = 3
        self.colliding = []
        self.hearts = PlayerLife(self.screen, "Life: " + self.name, 30, 30)
        self.keydown = False
        # variabler for å tegne
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(RED)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.topleft = (x, y)
        self.direction = pygame.math.Vector2()

    def __str__(self):
        return self.name

    __repr__ = __str__

    def update_life(self, objects, game):
        for obj in objects:
            if isinstance(obj, Enemy):
                if self.rect.colliderect(obj.rect) and not game.player_imunity:
                    game.player_imunity = True
                    # print(self, "collided with", obj)
                    self.x, self.y = knockback(obj, self.x, self.y)

                    if obj not in self.colliding:
                        self.hearts.decrease()
                        self.colliding.append(obj)

                else:
                    if obj in self.colliding:
                        self.colliding.remove(obj)

            if isinstance(obj, Chest):
                if self.rect.colliderect(obj.rect):
                    self.x, self.y = collision(obj, self.rect)
                    # print(self, "collidedage.get_rect with ", obj)

                    if obj not in self.colliding:
                        self.hearts.increase()
                        self.colliding.append(obj)

                else:
                    if obj in self.colliding:
                        self.colliding.remove(obj)

        return self.hearts.life

    def update_pose(self):
        button = pygame.key.get_pressed()
        self.direction = pygame.math.Vector2(0, 0)

        if button[pygame.K_a]:
            self.direction.x = -1
        if button[pygame.K_d]:
            self.direction.x = 1
        if button[pygame.K_w]:
            self.direction.y = -1
        if button[pygame.K_s]:
            self.direction.y = 1
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.x += int(self.direction.x * self.speed)
        self.y += int(self.direction.y * self.speed)

        self.x = max(0, self.x)
        self.y = max(0, self.y)
        self.x = min(WORLD_WIDTH, self.x)
        self.y = min(WORLD_HEIGHT, self.y)

        self.rect.x = self.x
        self.rect.y = self.y

    def check_collison(self, objects, game):
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                if isinstance(obj, (Wall, Nothing)):
                    self.x, self.y = collision(obj, self.rect)

                elif isinstance(obj, Tower):
                    # print(self, "collided with", obj)
                    game.new_background_tower = True
                    self.x, self.y = collision(obj, self.rect)

                elif isinstance(obj, House):
                    # print(self, "collided with", obj)
                    game.new_background_house = True
                    self.x, self.y = collision(obj, self.rect)

                elif isinstance(obj, Door):
                    # print(self, "collided with ", obj)
                    if game.in_building:
                        game.in_building = False
                        game.new_background_world = True
                        self.x, self.y = collision(obj, self.rect)

            # print(self, "collided with ", obj)

    def update(self, game):
        # print("player")
        game.player.update_pose()
        game.player.update_life(game.all_objects, game)
        game.player.check_collison(game.all_objects, game)
        game.sword.update_pos(game.player)
        game.sword.attack()
        game.player.hearts.draw()


class Camera:
    def __init__(self):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.camera = pygame.Rect(0, 0, self.width, self.height)

    def apply(self, entity):
        """Apply the camera offset to an entity."""
        x, y = self.camera.topleft
        return entity.rect.move((-x, -y))

    def update(self, player):
        """Update the camera to follow the target."""
        camera_x = max(
            0,
            min(player.x - self.width // 2, WORLD_WIDTH - self.width),
        )
        camera_y = max(
            0,
            min(
                player.y - self.height // 2,
                WORLD_HEIGHT - self.height,
            ),
        )

        self.camera = pygame.Rect(camera_x, camera_y, self.width, self.height)
        # print("CAMERA", camera_x, camera_y, player.x, player.y)


class Game:
    def __init__(self):
        pygame.init()
        self.camera = Camera()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.tekst_size = pygame.font.Font(None, 60)
        # new background
        self.new_background_tower = False
        self.new_background_house = False
        self.new_background_world = False
        self.in_building = False
        # creating world
        self.all_objects = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.chests = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.nothings = pygame.sprite.Group()
        self.houses = pygame.sprite.Group()
        self.crashable_objects = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.crashable_objects.add(
            self.walls, self.chests, self.towers, self.nothings, self.houses, self.doors
        )
        self.player = None
        self.sword = None
        self.create_world("world.map")

        self.player_imunity = False
        self.imunity_timer = 0

        self.buildings = {}

    def check_player(self):
        if self.player.hearts.dead:
            tekst = self.tekst_size.render("GAME OVER", True, RED)
            tekst_rect = tekst.get_rect(center=(240, 30))
            self.screen.blit(tekst, tekst_rect)
            self.create_world("world.map")
            self.player.hearts.dead = False

        if self.player_imunity:
            self.imunity_timer += 1

            if self.imunity_timer == 25:
                self.player_imunity = False
                self.imunity_timer = 0

    def check_background(self):
        # print(self.in_building)
        if self.new_background_tower:
            self.create_world("tower.map")
            self.new_background_tower = False
            self.in_building = True

        if self.new_background_house:
            self.create_world("house.map")
            self.new_background_house = False
            self.in_building = True

        if self.new_background_world:
            self.create_world("world.map")
            self.new_background_world = False
            self.in_building = False

    def move_to_available_x_y(self, object_to_place):
        #        if whatever in self.buildings:
        #            raise RuntimeError(f"{whatever} is already in buldings")
        for _ in range(3000):
            x = randint(0, WORLD_HEIGHT)
            y = randint(0, WORLD_WIDTH)
            object_to_place.rect.move_ip(x, y)
            for obj in self.all_objects:
                if not object_to_place.rect.colliderect(
                    obj.rect
                ):  # og ikke i "home of player"
                    #    if isinstance(object_to_place, (House, Tower)):
                    #        self.buildings[object_to_place] = (x, y)

                    # print(object_to_place, x, y, object_to_place.rect)
                    object_to_place.x = x
                    object_to_place.y = y
                    return object_to_place

    def create_world(self, name: str):
        self.all_objects = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.chests = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.nothings = pygame.sprite.Group()
        self.houses = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()

        if name.startswith("tower"):
            self.background_image = pygame.image.load("tower.background.png")
        elif name.startswith("house"):
            self.background_image = pygame.image.load("tower.background.png")
        else:
            self.background_image = pygame.image.load("main.background.jpg")

            for _ in range(4):
                enemy = Enemy(self.screen, "enemy", 0, 0)
                self.move_to_available_x_y(enemy)
                self.enemies.add(enemy)
                self.all_objects.add(enemy)

        self.background_image = pygame.transform.scale(
            self.background_image, (WORLD_WIDTH, WORLD_HEIGHT)
        )
        self._read_kart(name)

    def _read_kart(self, name):
        x = 0
        y = 0
        player = None
        sword = None
        round_y = 0
        round_x = 0
        with open(name, "r", encoding="utf-8") as kart:
            for line in kart.readlines():
                y = 30 * round_y
                round_x = 0
                for col in line:
                    x = 30 * round_x
                    round_x += 1
                    if col == ".":
                        continue
                    if col == "N":
                        obj = Nothing(self.screen, "nothing" + str(x) + str(y), x, y)
                        self.nothings.add(obj)
                    elif col == "P":
                        player = Player(self.screen, "player" + str(x) + str(y), x, y)
                        sword = PlayerSword()
                    elif col == "X":
                        obj = Wall(self.screen, "wall " + str(x) + str(y), x, y)
                        self.walls.add(obj)
                    elif col == "C":
                        obj = Chest(self.screen, "chest " + str(x) + str(y), x, y)
                        self.chests.add(obj)
                    elif col == "E":
                        obj = Enemy(self.screen, "enemy " + str(x) + str(y), x, y)
                        self.enemies.add(obj)
                    elif col == "H":
                        obj = House(self.screen, "house" + str(x) + str(y), x, y)
                        self.houses.add(obj)
                    elif col == "T":
                        obj = Tower(self.screen, "tower " + str(x) + str(y), x, y)
                        self.towers.add(obj)
                    elif col == "D":
                        obj = Door(self.screen, "door" + str(x) + str(y), x, y)
                        self.doors.add(obj)

                round_y += 1

            if player is None or sword is None:
                raise RuntimeWarning("player must be in the map")

            self.player = player
            self.sword = sword
            self.all_objects.add(
                (
                    self.towers,
                    self.enemies,
                    self.chests,
                    self.walls,
                    self.sword,
                    self.player,
                    self.nothings,
                    self.houses,
                    self.doors,
                )
            )

    def step(self):
        self.screen.blit(self.background_image, (0, 0))
        # Game.camera(self)
        tekst = self.tekst_size.render(
            f"imunity_timer, {self.imunity_timer}", True, RED
        )
        tekst_rect = tekst.get_rect(center=(240, 30))
        self.screen.blit(tekst, tekst_rect)

        for enemy in self.enemies:
            if enemy.life <= 0:
                pygame.sprite.Sprite.kill(enemy)

        self.check_background()
        self.check_player()

        self.enemies.update(self)

        self.camera.update(self.player)
        for sprite in self.all_objects:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        self.player.update(self)

        pygame.display.flip()
        pygame.time.Clock().tick(60)


if __name__ == "__main__":
    mygame = Game()

    while True:
        mygame.step()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            #   if event.type == pygame.KEYDOWN:
            #   print("KEYDOWN",event)
