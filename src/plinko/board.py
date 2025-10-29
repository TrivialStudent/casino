import pygame, pymunk

HEIGHT = 1080
WIDTH = 1920
OBSTACLE_RAD = int(WIDTH / 240)
OBSTACLE_PAD = int(HEIGHT / 19)



class Board():
    def __init__(self, space):
        self.space = space
        self.display = pygame.display.get_surface()

        self.first_row = 3
        self.final_row = 20

        self.obstacles = []
        self.obstacle_sprites = pygame.sprite.Group()
        self.updated_coords = (int((WIDTH / 2) - OBSTACLE_PAD), int((HEIGHT - (HEIGHT * 0.9))))
        self.create_obstacle()
    def create_obstacle(self):
        while self.first_row <= self.final_row:
            for i in range(self.first_row):
                self.obstacles.append(self.spawn_obstacle(self.updated_coords, self.space))
                self.updated_coords = (int(self.updated_coords[0] + OBSTACLE_PAD), self.updated_coords[1])
            self.updated_coords = (int(WIDTH - self.updated_coords[0] + (0.5 * OBSTACLE_PAD)), int(self.updated_coords[1] + OBSTACLE_PAD))
            self.first_row += 1
    def draw_obstacles(self,obstacles):
        for obstacle in obstacles:
            posx, posy = int(obstacle.body.position.x), int(obstacle.body.position.y)
            pygame.draw.circle(self.display,(175,200,255), (posx, posy), OBSTACLE_RAD)
    def spawn_obstacle(self, pos, space):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Circle(body, OBSTACLE_RAD)
        shape.elasticity = 0.9
        shape.friction = 0.5
        shape.filter = pymunk.ShapeFilter(categories=2, mask = pymunk.ShapeFilter.ALL_MASKS())
        self.space.add(body, shape)
        #obstacle = Obstacles(body.position.x, body.position.y)
        # self.obstacle_sprites(obstacle)
        return shape
    def update(self):
        self.draw_obstacles(self.obstacles)
