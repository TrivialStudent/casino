import pathlib

import pygame, pymunk, random, json, os
from board import Board
from ball import Ball
from Multi import multi_group, prev_multi_group, HEIGHT, WIDTH  # groups live in Multi.py

class Plinko:
    def __init__(self):
        pygame.init()

        self.base_dir = pathlib.Path(__file__).resolve().parent
        self.user_file = (self.base_dir.parent / 'user_data.json').resolve()

        users = json.loads(self.user_file.read_text()) if self.user_file.exists() else []
        uname = os.environ.get('PLINKO_USER') or "guest"

        pygame.mixer.init()
        pygame.mixer.music.load(str(self.base_dir / "audio" / "Take_care.mp3"))
        self.ball_sound = pygame.mixer.Sound(str(self.base_dir / "audio" / "pop.mp3"))
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1)

        self.user = next((u for u in users if u.get('name') == uname), None) \
                    or next((u for u in users if u.get('name') == 'test'), None) \
                    or (users[0] if users else {'name': uname, 'balance': 0.0, 'balance_history': []})

        try:
            bal_dollars = float(self.user.get('balance', 0) or 0)
        except (TypeError, ValueError):
            bal_dollars = 0.0
        self.balance_cents = int(round(bal_dollars * 100))
        self.start_balance_cents = self.balance_cents
        self.lock_dir = (self.base_dir / ".locks")
        self.lock_dir.mkdir(exist_ok=True)
        self.lock_path = (self.lock_dir / f"{self.user.get('name', 'guest')}.lock")

        self.turns_total = max(0, self.balance_cents // 100)
        self.turns_left = self.turns_total
        self.session_winnings_cents = 0
        self.balls_in_play = 0

        self.font = pygame.font.SysFont(None, 30)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Plinko")
        self.clock = pygame.time.Clock()
        self.delta_time = 0.0

        self.space = pymunk.Space()
        self.space.gravity = (0, 1000)

        self.plinko_balls = pygame.sprite.Group()
        self.board = Board(self.space)

        try:
            # atomic create; fails if file exists
            self.lock_fd = os.open(self.lock_path, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            os.write(self.lock_fd, str(os.getpid()).encode())
        except FileExistsError:
            # Already running for this user
            print(f"Plinko already running for user {self.user.get('name')}.")
            pygame.quit()
            raise SystemExit

    def handle_score(self, multiplier):
        payout_cents = int(round(float(multiplier) * 100))
        self.session_winnings_cents += payout_cents
        self.balance_cents += payout_cents
        self.turns_left = self.balance_cents // 100

    def save_and_quit(self):

        users = json.loads(self.user_file.read_text()) if self.user_file.exists() else []
        key = self.user.get('name') or 'guest'


        rec = next((x for x in users if x.get('name') == key), None)
        if not rec:
            rec = {'name': key, 'balance': 0.0, 'balance_history': [], 'total_winnings': 0.0}
            users.append(rec)


        file_cents = int(round(float(rec.get('balance', 0.0)) * 100))


        delta_cents = int(self.balance_cents - self.start_balance_cents)
        merged_cents = file_cents + delta_cents
        merged_dollars = round(merged_cents / 100.0, 2)


        rec['balance'] = merged_dollars
        bh = rec.get('balance_history') or []
        if not bh or float(bh[-1]) != merged_dollars:
            bh.append(merged_dollars)
        rec['balance_history'] = bh

        # Aggregate session winnings
        rec['total_winnings'] = round(
            float(rec.get('total_winnings', 0.0)) + round(self.session_winnings_cents / 100.0, 2),
            2
        )

        tmp = self.user_file.with_suffix(".tmp")
        tmp.write_text(json.dumps(users, indent=4))
        tmp.replace(self.user_file)

        # Release lock, ping Flask, and exit
        try:
            os.close(self.lock_fd)
            os.unlink(self.lock_path)
        except Exception:
            pass

        pygame.quit()
        try:
            import urllib.request
            urllib.request.urlopen("http://127.0.0.1:5000/_refresh_cache", data=b"")  # POST
        except Exception:
            pass
        raise SystemExit

    def cents_to_str(self, cents: int) -> str:
        sign = '-' if cents < 0 else ''
        cents = abs(int(cents))
        return f"{sign}${cents // 100}.{cents % 100:02d}"

    def draw_hud(self):
        lines = [
            f"User: {self.user.get('pref_name', '?')}",
            f"Balance: {self.cents_to_str(self.balance_cents)}   Turns left: {self.turns_left}",
            f"Winnings: {self.cents_to_str(self.session_winnings_cents)}",
            "[SPACE] drop ball   [Q] save+quit"
        ]

        x, y = 20, 12  # top-left corner
        line_gap = 6  # vertical spacing between lines

        for line in lines:
            surf = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(surf, (x, y))
            y += surf.get_height() + line_gap

    def start(self):
        while True:
            self.delta_time = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_and_quit()
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    self.save_and_quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self.balance_cents >= 100:
                        self.turns_left -= 1
                        self.balance_cents -= 100  # $1 per ball
                        self.turns_left = self.balance_cents // 100

                        self.ball_sound.play()
                        random_x = WIDTH // 2 + random.choice([random.randint(-10, -1), random.randint(1, 10)])
                        ball = Ball((random_x, 20), self.space, self.board, self.delta_time, on_score=self.handle_score)
                        self.plinko_balls.add(ball)

            self.screen.fill((0, 0, 0))
            self.space.step(self.delta_time)

            self.board.update()
            multi_group.update()
            prev_multi_group.update()

            self.plinko_balls.update()
            multi_group.draw(self.screen)
            self.plinko_balls.draw(self.screen)
            self.draw_hud()

            pygame.display.flip()

if __name__ == "__main__":
    Plinko().start()
