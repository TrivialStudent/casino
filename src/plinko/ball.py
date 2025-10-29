import pygame, pymunk, random
BALL_RAD = 16
class Ball(pygame.sprite.Sprite):
    def __init__(self, pos, space, board, delta_time):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.space = space
        self.board = board
        self.delta_time = delta_time
        self.body = pymunk.Body(body_type = pymunk.Body.DYNAMIC)
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, BALL_RAD)
        self.shape.elasticity = 0.5
        self.shape.density = 10
        self.shape.mass = 1000
        self.shape.filter = pymunk.ShapeFilter(categories=1, mask=pymunk.ShapeFilter.ALL_MASKS() ^ 1)
        self.space.add(self.body, self.shape)
        self.image = pygame.Surface((BALL_RAD * 2, BALL_RAD * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (BALL_RAD, BALL_RAD), BALL_RAD)
        self.rect = self.image.get_rect(topleft=(self.body.position.x, self.body.position.y))

    def update(self):
        pos_x, pos_y = int(self.body.position.x), int(self.body.position.y)
        self.rect.centerx = pos_x
        self.rect.centery = pos_y
