
import pygame


WHITE = (255,255,255)
RED = (255,0,0)
screen_height = 500
screen_width = 500




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
    background_image = pygame.image.load("test.jpg")
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    player = Player()

    
    
    running = True
    while running:
        screen.blit(background_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update_pose()
        player.draw()
        pygame.display.flip()
        pygame.time.Clock().tick(20)


