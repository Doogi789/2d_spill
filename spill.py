import pygame
from random import randint
from enum import Enum, auto


WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1000


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


def knockback(obj, x, y, game):
    knockback = 25
    if obj.direction == "x+":
        x += knockback
    if obj.direction == "x-":
        x -= knockback
    if obj.direction == "y+":
        y += knockback
    if obj.direction == "x-":
        y -= knockback

    return (x, y)


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
        self.speed = 2
        self.target_y = randint(0, SCREEN_HEIGHT - self.height)
        self.target_x = randint(0, SCREEN_WIDTH - self.width)
        self.life = 50
        # knockback
        self.direction = "x+"

    def __str__(self):
        return self.name

    __repr__ = __str__

    def update_pose(self, objects, p_x, p_y):
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
                    self.direction = "x+"
                else:
                    self.x -= self.speed
                    self.direction = "x-"
            else:
                if distance_y > 0:
                    self.y += self.speed
                    self.direction = "y+"
                else:
                    self.y -= self.speed
                    self.direction = "y-"
        else:
            self.target_y = randint(0, SCREEN_HEIGHT - self.height)
            self.target_x = randint(0, SCREEN_WIDTH - self.width)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        for obj in objects:
            if isinstance(obj, (Wall, Chest, Tower)):
                if self.rect.colliderect(obj.rect):
                    dx = self.rect.centerx - obj.rect.centerx
                    dy = self.rect.centery - obj.rect.centery

                    if abs(dx) > abs(dy):
                        if dx > 0:
                            self.x = obj.rect.right
                        else:
                            self.x = obj.rect.left - self.rect.width
                    else:
                        if dy > 0:
                            self.y = obj.rect.bottom
                        else:
                            self.y = obj.rect.top - self.rect.height

            if isinstance(obj, (PlayerSword)):
                if self.rect.colliderect(obj.rect):
                    print("COLLIDE")
                    self.life -= 10
                    self.x, self.y = knockback(obj, self.x, self.y, game)

                    #  print(self, "collided with ", obj)


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
        self.screen = screen
        self.x = x
        self.y = y
        self.life = 12
        self.max_life = self.life
        self.name = name
        self.rec = (self.x, self.y, self.width, self.height)
        self.hearts = [
            pygame.image.load(f"heart_{i}.png").convert_alpha() for i in range(5)
        ]
        self.dead: bool = False

    def increase(self):
        self.life += 1
        self.life = min(self.max_life, self.life)

    def decrease(self):
        self.life -= 1
        if self.life < 0:
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
            pygame.image.load("sword_x+.png"), 0.3
        )
        self.image_xminus = pygame.transform.scale_by(
            pygame.image.load("sword_x-.png"), 0.3
        )
        self.image_ypluss = pygame.transform.scale_by(
            pygame.image.load("sword_y+.png"), 0.3
        )
        self.image_yminus = pygame.transform.scale_by(
            pygame.image.load("sword_y-.png"), 0.3
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
            print("SHOW SWORD", self.timer, player.rect)
            if player.direction == "x+":
                self.image = self.image_xpluss
                self.rect = self.image.get_rect(midleft=player.rect.midleft)

            elif player.direction == "x-":
                self.image = self.image_xminus
                self.rect = self.image.get_rect(midright=player.rect.midright)

            elif player.direction == "y+":
                self.image = self.image_ypluss
                self.rect = self.image.get_rect(midtop=player.rect.midtop)

            elif player.direction == "y-":
                self.image = self.image_yminus
                self.rect = self.image.get_rect(midbottom=player.rect.midbottom)

            else:
                raise RuntimeError("BAD DIRCTION", player.direction)

            if self.timer == 10:
                print("DELETE SWORD")
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
        self.speed = 5
        self.colliding = []
        self.hearts = PlayerLife(self.screen, "Life: " + self.name, 30, 30)
        self.keydown = False
        # variabler for å tegne
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(RED)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.topleft = (x, y)
        self.direction = "x+"

    def __str__(self):
        return self.name

    __repr__ = __str__

    def update_life(self, objects):
        for obj in objects:
            if isinstance(obj, Enemy):
                if self.rect.colliderect(obj.rect) and not game.player_imunity:
                    game.player_imunity = True
                    # print(self, "collided with", obj)
                    (
                        self.x,
                        self.y,
                    ) = knockback(obj, self.x, self.y, game)

                    if obj not in self.colliding:
                        self.hearts.decrease()
                        self.colliding.append(obj)

                else:
                    if obj in self.colliding:
                        self.colliding.remove(obj)

            if isinstance(obj, Chest):
                if self.rect.colliderect(obj.rect):
                    # print(self, "collidedage.get_rect with ", obj)

                    if obj not in self.colliding:
                        self.hearts.increase()
                        self.colliding.append(obj)

                else:
                    if obj in self.colliding:
                        self.colliding.remove(obj)

        return self.hearts.life

    def update_pose(self, objects, game):
        button = pygame.key.get_pressed()

        if button[pygame.K_a]:
            self.x -= self.speed
            self.direction = "x-"
        if button[pygame.K_d]:
            self.x += self.speed
            self.direction = "x+"
        if button[pygame.K_w]:
            self.y -= self.speed
            self.direction = "y-"
        if button[pygame.K_s]:
            self.y += self.speed
            self.direction = "y+"

        self.rect.x = self.x
        self.rect.y = self.y

        for obj in objects:
            if isinstance(obj, (Wall, Nothing)):
                if self.rect.colliderect(obj.rect):
                    dx = self.rect.centerx - obj.rect.centerx
                    dy = self.rect.centery - obj.rect.centery

                    if abs(dx) > abs(dy):
                        if dx > 0:
                            self.x = obj.rect.right
                        else:
                            self.x = obj.rect.left - self.rect.width
                    #  print(self, "collided with ", obj)
                    else:
                        if dy > 0:
                            self.y = obj.rect.bottom
                        else:
                            self.y = obj.rect.top - self.rect.height
                    # print(self, "collided with ", obj)

            elif isinstance(obj, Tower):
                if self.rect.colliderect(obj.rect):
                    print(self, "collided with", obj)
                    game.new_background = True

        # print(self, "collided with ", obj)


class Game:
    def __init__(self):
        pygame.init()
        # tekst
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.tekst_size = pygame.font.Font(None, 60)
        self.new_background = False
        # creating world
        self.all_objects = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.chests = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.nothings = pygame.sprite.Group()
        self.crashable_objects = pygame.sprite.Group()
        self.crashable_objects.add(self.walls, self.chests, self.towers, self.nothings)

        self.create_world("world.map")
        self.player_imunity = False
        self.imunity_timer = 0

    def create_world(self, name: str):
        kart = open(name, "r")
        x = 0
        y = 0
        player = None
        sword = None
        self.all_objects = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.chests = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.nothings = pygame.sprite.Group()

        if name.startswith("tower"):
            self.background_image = pygame.image.load("tower.background.png")
        else:
            self.background_image = pygame.image.load("main.background.jpg")

        self.background_image = pygame.transform.scale(
            self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        for line in kart.readlines():
            y += 30
            x = 0
            for col in line:
                x += 30
                if col == ".":
                    continue
                elif col == "N":
                    nothing = Nothing(self.screen, "nothing" + str(x) + str(y), x, y)
                    self.nothings.add(nothing)
                    self.all_objects.add(nothing)
                elif col == "P":
                    player = Player(self.screen, "player" + str(x) + str(y), x, y)
                    sword = PlayerSword()
                    self.all_objects.add(sword)
                    self.all_objects.add(player)
                elif col == "X":
                    wall = Wall(self.screen, "wall " + str(x) + str(y), x, y)
                    self.walls.add(wall)
                    self.all_objects.add(wall)
                elif col == "C":
                    chest = Chest(self.screen, "chest " + str(x) + str(y), x, y)
                    self.chests.add(chest)
                    self.all_objects.add(chest)
                elif col == "E":
                    enemy = Enemy(self.screen, "enemy " + str(x) + str(y), x, y)
                    self.enemies.add(enemy)
                    self.all_objects.add(enemy)
                elif col == "T":
                    tower = Tower(self.screen, "tower " + str(x) + str(y), x, y)
                    self.towers.add(tower)
                    self.all_objects.add(tower)

        if player is None or sword is None:
            raise RuntimeWarning("player must be in the map")

        self.player = player
        self.sword = sword

    def step(self):
        self.screen.blit(self.background_image, (0, 0))
        tekst = self.tekst_size.render(
            f"imunity_timer, {self.imunity_timer}", True, RED
        )
        tekst_rect = tekst.get_rect(center=(240, 30))
        self.screen.blit(tekst, tekst_rect)

        if self.new_background:
            self.create_world("tower.map")
            self.new_background = False

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

        for obj in self.all_objects:
            if isinstance(obj, Enemy):
                if obj.life <= 0:
                    pygame.sprite.Sprite.kill(obj)

        for self.enemy in self.enemies:
            self.enemy.update_pose(self.all_objects, self.player.x, self.player.y)

        self.player.update_life(self.all_objects)
        self.player.update_pose(self.all_objects, game)

        self.sword.update_pos(self.player)
        self.sword.attack()

        self.all_objects.draw(self.screen)
        self.player.hearts.draw()
        pygame.display.flip()
        pygame.time.Clock().tick(60)


if __name__ == "__main__":
    game = Game()

    running = True
    while running:
        game.step()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            #   if event.type == pygame.KEYDOWN:
            #   print("KEYDOWN",event)
