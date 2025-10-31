
import pygame, pymunk, os, random
from pathlib import *
from Multi import *
BALL_RAD = 16

class Ball(pygame.sprite.Sprite):
    def __init__(self, pos, space, board, delta_time, on_score=None):
        super().__init__()
        audio_dir = Path(__file__).resolve().parent / "audio"
        self.money_sound = pygame.mixer.Sound(str(audio_dir / "money.mp3"))
        self.display_surface = pygame.display.get_surface()
        self.space = space
        self.on_score = on_score
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
        self.scored =False

    def update(self):
        pos_x, pos_y = int(self.body.position.x), int(self.body.position.y)
        self.rect.centerx = pos_x
        self.rect.centery = pos_y

        for multi in multi_group:
            if pygame.sprite.collide_rect(self, multi):

                multi.animate(multi.color, multi.multi_amt)
                multi.is_animating = True
                self.money_sound.play()

                prev_rgb = multi.color
                prev_multi = PrevMulti(str(multi.multi_amt), prev_rgb)
                prev_multi_group.add(prev_multi)
                if callable(self.on_score):
                    try:
                        self.on_score(multi.multi_amt)
                    except Exception:
                        pass

                self.kill()
