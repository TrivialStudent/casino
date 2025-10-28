import pygame, pymunk
from board import *


class Plinko:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Plinko")
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        self.space = pymunk.Space()
        self.space.gravity = (100,1000)

        self.plinko_balls = pygame.sprite.Group()
        self.board = Board(self.space)

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.delta_time = self.clock.tick(60) / 1000.0

            self.screen.fill((0, 0, 0))

            # Update physics
            self.space.step(self.delta_time)

            # Draw everything
            self.board.update()
            self.plinko_balls.draw(self.screen)

            # NOW flip
            pygame.display.flip()


if __name__ == "__main__":
    plinko = Plinko()
    plinko.start()

