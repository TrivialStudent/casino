import pygame, pymunk, random
from board import *
from ball import *



class Plinko:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Plinko")
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        self.space = pymunk.Space()
        self.space.gravity = (0,1000)

        self.plinko_balls = pygame.sprite.Group()
        self.board = Board(self.space)

    def start(self):
        while True:
            self.delta_time = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        random_x = 1920 // 2 + random.choice([random.randint(-10,-1), random.randint(1,10)])
                        self.ball = Ball((random_x, 20), self.space, self.board, self.delta_time)
                        self.plinko_balls.add(self.ball)



            self.screen.fill((0, 0, 0))


            self.space.step(self.delta_time)


            self.board.update()
            self.plinko_balls.update()
            self.plinko_balls.draw(self.screen)

            pygame.display.flip()


if __name__ == "__main__":
    plinko = Plinko()
    plinko.start()

