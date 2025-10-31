import pygame, pymunk
from Multi import Multi, multi_group
from Multi import WIDTH, HEIGHT

OBSTACLE_RAD = int(WIDTH / 240)
OBSTACLE_PAD = int(HEIGHT / 19)
MULTI_HEIGHT = int(HEIGHT / 19)
NUM_MULTIS = 17

multi_rgb = {
    (0, 1000): (255,  77,  77),
    (1,  130): (255, 107,  74),
    (2,   26): (255, 138,  71),
    (3,    9): (255, 166,  70),
    (4,    4): (255, 195,  76),
    (5,    2): (255, 218,  98),
    (6,  0.2): (244, 239, 135),
    (7,  0.2): (214, 240, 161),
    (8,  0.2): (185, 242, 187),
    (9,  0.2): (214, 240, 161),
    (10, 0.2): (244, 239, 135),
    (11,   2): (255, 218,  98),
    (12,   4): (255, 195,  76),
    (13,   9): (255, 166,  70),
    (14,  26): (255, 138,  71),
    (15, 130): (255, 107,  74),
    (16,1000): (255,  77,  77),
}


class Board:
    def __init__(self, space):
        self.space = space
        self.display = pygame.display.get_surface()
        self.first_row = 3
        self.final_row = 20
        self.obstacles = []
        self.updated_coords = (int((WIDTH / 2) - OBSTACLE_PAD), int(HEIGHT * 0.05))
        self.create_obstacle()
        self.spawn_multi()

    def create_obstacle(self):
        r = self.first_row
        x, y = self.updated_coords
        while r <= self.final_row:
            for _ in range(r):
                self.obstacles.append(self.spawn_obstacle((x, y)))
                x += OBSTACLE_PAD
            x = int(WIDTH - x + (0.4 * OBSTACLE_PAD))
            y += OBSTACLE_PAD * 0.95
            r += 1

    def draw_obstacles(self):
        for shape in self.obstacles:
            posx, posy = int(shape.body.position.x), int(shape.body.position.y)
            pygame.draw.circle(self.display, (175, 200, 255), (posx, posy), OBSTACLE_RAD)

    def spawn_obstacle(self, pos):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Circle(body, OBSTACLE_RAD)
        shape.elasticity = 0.9
        shape.friction = 0.5
        shape.filter = pymunk.ShapeFilter(categories=2, mask=pymunk.ShapeFilter.ALL_MASKS())
        self.space.add(body, shape)
        return shape

    def spawn_multi(self):
        entries = sorted(multi_rgb.items(), key=lambda kv: kv[0][0])  # by index 0..16
        start_x = int(WIDTH / 2 - (OBSTACLE_PAD * (NUM_MULTIS - 1)) / 2) - 82
        y = HEIGHT - (MULTI_HEIGHT // 2)
        for i, (idx_amt, color) in enumerate(entries):
            _, amount = idx_amt
            x = start_x + i * (OBSTACLE_PAD + 10)
            multi_group.add(Multi((x, y), color, amount))

    def update(self):
        self.draw_obstacles()
