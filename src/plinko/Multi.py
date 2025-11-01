import pygame
HEIGHT = 720
WIDTH  = 1280

OBSTACLE_RAD = int(WIDTH / 240)
OBSTACLE_PAD = int(HEIGHT / 19) + 20

SCORE_RECT = 120
multi_group = pygame.sprite.Group()
clock = pygame.time.Clock()
delta_time = clock.tick(60) / 1000.0

#sound = pygame.mixer.Sound("src/plinko/audio/money.mp3")

class Multi(pygame.sprite.Sprite):
    def __init__(self, position, color, multi_amt):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.SysFont(None, 26)
        self.color = color
        self.border_radius = 10
        self.position = position
        self.rect_width = OBSTACLE_PAD - (OBSTACLE_PAD / 14)
        self.rect_height = 56
        self.image = pygame.Surface((self.rect_width, self.rect_height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.color, self.image.get_rect(), border_radius=self.border_radius)
        self.rect = self.image.get_rect(midbottom=position)
        self.multi_amt = multi_amt
        self.prev_multi = int(WIDTH / 21.3)
        self.animated_frames = 0
        self.animation_frames = max(1, int(0.25 / max(1e-6, delta_time)))
        self.is_animating = False
        self.render_multi()

    def animate(self, color, amount):
        half = self.animation_frames // 2
        if self.animated_frames < half:
            self.rect.bottom += 2
        else:
            self.rect.bottom -= 2
        self.animated_frames += 1
        if self.animated_frames >= half * 2:
            self.is_animating = False
            self.animated_frames = 0
    def render_multi(self):
        text_surface = self.font.render(f"{self.multi_amt}x", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.image.get_rect().center)
        self.image.blit(text_surface, text_rect)


    def update(self):
        global delta_time
        delta_time = clock.get_time() / 1000.0
        target_frames = max(1, int(0.25 / max(1e-6, delta_time)))
        if abs(target_frames - self.animation_frames) > 2:
            self.animation_frames = target_frames
        if self.is_animating:
            self.animate(self.color, self.multi_amt)



class PrevMulti(pygame.sprite.Sprite):
    def __init__(self, multi_amt, rgb_tuple):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.multi_amt = multi_amt
        self.font = pygame.font.SysFont(None, 36)
        self.rect_width = 150
        self.rect_height = 120
        self.prev_surf = pygame.Surface((self.rect_width, self.rect_height), pygame.SRCALPHA)
        self.rgb = rgb_tuple
        pygame.draw.rect(self.prev_surf, self.rgb, (0, 0, self.rect_width, self.rect_height))
        self.prev_rect = self.prev_surf.get_rect(midbottom=(int(WIDTH * 0.85), (HEIGHT / 2) - (SCORE_RECT * 2)))
        self.y_traverse = 0
        self.traveled = 0
        self.render_multi()

    def render_multi(self):
        text_surface = self.font.render(f"{self.multi_amt}x", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.prev_surf.get_rect().center)
        self.prev_surf.blit(text_surface, text_rect)

    def update(self):
        if self.prev_rect.bottom > (HEIGHT - (SCORE_RECT * 2)):
            self.kill()
            return

        global delta_time
        delta_time = clock.get_time() / 1000.0

        if self.traveled < self.y_traverse:
            total_distance = SCORE_RECT
            distance_per_second = 1800
            distance_per_frame = distance_per_second * delta_time
            divisor = max(1, int(total_distance / max(1e-6, distance_per_frame)))
            step = int(total_distance / divisor)
            self.prev_rect.bottom += step
            self.traveled += step

        self.display_surface.blit(self.prev_surf, self.prev_rect)


class PrevMultiGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def update(self):
        super().update()
        if len(self) > 5:
            self.remove(self.sprites().pop(0))
        sprites = self.sprites()
        n = len(sprites)
        if n:
            for i, spr in enumerate(sprites):
                spr.y_traverse = SCORE_RECT * (n - i)

prev_multi_group = PrevMultiGroup()
