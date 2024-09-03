import pygame


WHITE = (255, 255, 255)
RED = (255, 0, 0)
screen_height = 500
screen_width = 500


class Chest:
    def __init__(self, x, y):
        self.width = 30
        self.height = 30
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30

    def draw(self):
        rec = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, WHITE, rec)


class Player:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height // 2 - self.height // 2
        self.speed = 1

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
        rec = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, RED, rec)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    background_image = pygame.image.load("backgrunn.jpg")
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    player = Player()
    chest = Chest(100, 100)
    chest2 = Chest(200, 200)
    running = True
    while running:
        screen.blit(background_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        chest.draw()
        chest2.draw()
        player.update_pose()
        player.draw()
        pygame.display.flip()
        pygame.time.Clock().tick(20)
