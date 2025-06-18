import pygame
import random

class DinoGameEnv:
    def __init__(self):
        pygame.init()

        # Font setup
        self.font = pygame.font.SysFont(None, 36)

        # Screen Setup
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 450
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Dino RL Game")
        self.clock = pygame.time.Clock()

        # Ground
        self.ground_img = pygame.image.load("D:/dinobot/ai_dinobot/dino/Chromium_T-Rex-horizon.png")
        self.ground_img = pygame.transform.scale(self.ground_img, (self.SCREEN_WIDTH, 20))
        self.GROUND_Y = self.SCREEN_HEIGHT - 40
        self.ground_x = 0
        self.ground_speed = 5

        # Clouds
        self.cloud_img = pygame.image.load("D:/dinobot/ai_dinobot/dino/Chromium_T-Rex-cloud.png")
        self.cloud_img = pygame.transform.scale(self.cloud_img, (50, 50))
        self.cld_y = self.SCREEN_HEIGHT - 150
        self.cld_x = 0
        self.cld_speed = 2

        # Cactus
        self.cactus_images = [
            pygame.transform.scale(pygame.image.load("D:/dinobot/ai_dinobot/dino/1_Cactus_Chrome_Dino.webp"), (50, 90)),
            pygame.transform.scale(pygame.image.load("D:/dinobot/ai_dinobot/dino/1_Cactus_Chrome_Dino.webp"), (35, 90)),
            pygame.transform.scale(pygame.image.load("D:/dinobot/ai_dinobot/dino/3_Cactus_Chrome_Dino.webp"), (80, 90))
        ]
        self.cacti = []
        self.cactus_speed = 5
        self.spawn_delay = random.randint(80, 150)

        # Dino
        self.dino_images = [
            pygame.transform.scale(pygame.image.load("D:/dinobot/ai_dinobot/dino/Chrome_T-Rex_Left_Run.webp"), (50, 50)),
            pygame.transform.scale(pygame.image.load("D:/dinobot/ai_dinobot/dino/Chrome_T-Rex_Right_Run.webp"), (50, 50)),
        ]
        self.dino_index = 0
        self.frame_count = 0

        self.DINO_X = 50
        self.DINO_Y = self.GROUND_Y - 40
        self.Gravity = 0.98
        self.jump_speed = -18
        self.y_velocity = 0
        self.is_jumping = False

        self.game_over = False
        self.score = 0
        self.start_time = pygame.time.get_ticks()

        # Speed increase logic
        self.last_speed_increase = pygame.time.get_ticks()

    def reset(self):
        self.__init__()
        return self.get_state()

    def get_state(self):
        next_cactus = None
        for cactus in self.cacti:
            if cactus[0] > self.DINO_X:
                next_cactus = cactus
                break

        if next_cactus:
            distance = next_cactus[0] - self.DINO_X
            cactus_height = next_cactus[2].get_height()
            cactus_width = next_cactus[2].get_width()
        else:
            distance = self.SCREEN_WIDTH
            cactus_height = 0
            cactus_width = 0

        return [
            self.DINO_Y,
            self.y_velocity,
            distance,
            cactus_height,
            cactus_width,
            self.cactus_speed,
            len(self.cacti)
        ]

    def step(self, action, frame_skip=4): # Frame skipping logic
        total_reward = 0
        done = False
        final_state = None

        for _ in range(frame_skip):
            # Jump logic
            if action == 1 and not self.is_jumping:
                self.y_velocity = self.jump_speed
                self.is_jumping = True

            # Gravity update
            self.DINO_Y += self.y_velocity
            self.y_velocity += self.Gravity
            if self.DINO_Y >= self.GROUND_Y - 40:
                self.DINO_Y = self.GROUND_Y - 40
                self.y_velocity = 0
                self.is_jumping = False

            # Ground movement
            self.ground_x -= self.ground_speed
            if self.ground_x <= -self.SCREEN_WIDTH:
                self.ground_x = 0

            # Cloud movement
            self.cld_x -= self.cld_speed
            if self.cld_x <= -50:
                self.cld_x = self.SCREEN_WIDTH + random.randint(0, 100)

            # Dino animation
            self.frame_count += 2
            if self.frame_count % 10 == 0:
                self.dino_index = (self.dino_index + 1) % 2

            # Cactus spawning
            self.spawn_delay -= 2
            if self.spawn_delay <= 0:
                cactus_type = random.choice(self.cactus_images)
                self.cacti.append([self.SCREEN_WIDTH, self.GROUND_Y - 70, cactus_type])
                self.spawn_delay = random.randint(80, 150)

            # Cactus movement
            for cactus in self.cacti[:]:
                cactus[0] -= self.cactus_speed
                if cactus[0] < -50:
                    self.cacti.remove(cactus)

            # Collision detection
            dino_rect = pygame.Rect(self.DINO_X + 5, self.DINO_Y + 5, 40, 40)
            for cactus in self.cacti:
                cactus_rect = pygame.Rect(cactus[0], cactus[1], cactus[2].get_width(), cactus[2].get_height())
                if dino_rect.colliderect(cactus_rect):
                    self.game_over = True
                    total_reward -= 100
                    done = True
                    break

            # Speed increase over time
            if not done and pygame.time.get_ticks() - self.last_speed_increase > 1500:
                self.cactus_speed += 1
                self.ground_speed += 1
                self.last_speed_increase = pygame.time.get_ticks()

            # Reward and state
            self.score += 1
            total_reward += 1  # Small reward per frame survived

            final_state = self.get_state()

            if self.game_over:
                break

        return final_state, total_reward, self.game_over

    def render(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.ground_img, (self.ground_x, self.GROUND_Y))
        self.screen.blit(self.ground_img, (self.ground_x + self.SCREEN_WIDTH, self.GROUND_Y))
        self.screen.blit(self.cloud_img, (self.cld_x, self.cld_y))
        self.screen.blit(self.dino_images[self.dino_index], (self.DINO_X, self.DINO_Y))

        for cactus in self.cacti:
            self.screen.blit(cactus[2], (cactus[0], cactus[1]))

        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        timer_text = self.font.render(f"Time: {elapsed_time}s", True, (0, 0, 0))
        self.screen.blit(timer_text, (10, 10))

        if self.game_over:
            game_over_text = self.font.render("Game Over!", True, (255, 0, 0))
            self.screen.blit(game_over_text, (self.SCREEN_WIDTH // 2 - 80, self.SCREEN_HEIGHT // 2 - 20))

        pygame.display.update()
        self.clock.tick(30)

    def close(self):
        pygame.quit()
