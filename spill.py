import pygame


WHITE = (255, 255, 255)
RED = (255, 0, 0)
screen_height = 500
screen_width = 500


class Chest:
    def __init__(self, name, x, y):
        self.name = name
        self.width = 30
        self.height = 30
        self.x = x
        self.y = y
        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = pygame.image.load("chest.png")

    def draw(self):
        # self.rec = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rec = screen.blit(self.image, (self.x, self.y))
        # pygame.draw.rect(screen, "chest.png", self.rec)

    def __str__(self):
        return self.name

    __repr__ = __str__


class Player:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height // 2 - self.height // 2
        self.speed = 10
        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)

    def __str__(self):
        return "Player"

    __repr__ = __str__

    def update_pose(self):
        button = pygame.key.get_pressed()

        if button[pygame.K_a]:
            self.x -= self.speed
        if button[pygame.K_d]:
            self.x += self.speed
        if button[pygame.K_w]:
            self.y -= self.speed
        if button[pygame.K_s]:
            self.y += self.speed

    def draw(self):
        self.rec = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, RED, self.rec)

    def koliderer(self, objects):
        collide = False
        for obj in objects:
            if self.rec.colliderect(obj.rec):
                print(self, "collidered with ", obj)
                collide = True
        if not collide:
            print("No collisino")


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    background_image = pygame.image.load("backgrunn.jpg")
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    player = Player()
    chest = Chest("chest 1", 100, 100)
    chest_2 = Chest("chest 2", 200, 200)
    print(type(chest), type(player))

    running = True
    while running:
        screen.blit(background_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        chest.draw()
        chest_2.draw()
        player.update_pose()
        player.draw()
        player.koliderer([chest, chest_2])

        pygame.display.flip()
        pygame.time.Clock().tick(20)
