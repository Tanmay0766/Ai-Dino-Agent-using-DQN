import pygame
import random

# Initialize Pygame
pygame.init()

last_speed_increase = pygame.time.get_ticks()

# Font setup
font = pygame.font.SysFont(None, 36)
start_time = pygame.time.get_ticks()  
game_over = False
final_time = 0

# Screen Setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load Ground Image
ground_img = pygame.image.load("D:/dinobot/ai_dinobot/dino/Chromium_T-Rex-horizon.png")  
ground_img = pygame.transform.scale(ground_img, (SCREEN_WIDTH, 20))

# Ground Position
GROUND_Y = SCREEN_HEIGHT - 40
ground_x = 0
ground_speed = 5  # Speed of ground movement

#load clouds
cloud_img = pygame.image.load("D:/dinobot/ai_dinobot/dino/Chromium_T-Rex-cloud.png"),(50, 50)

cld_y = SCREEN_HEIGHT - 150
cld_x = 0
cld_speed = 2

# Load Cactus Images
cactus_images = [
    pygame.transform.scale(pygame.image.load("D:/dinobot/ai_dinobot/dino/1_Cactus_Chrome_Dino.webp"), (50, 90)),
    pygame.transform.scale(pygame.image.load("D:/dinobot/ai_dinobot/dino/1_Cactus_Chrome_Dino.webp"), (35, 90)),
    pygame.transform.scale(pygame.image.load("D:/dinobot/ai_dinobot/dino/3_Cactus_Chrome_Dino.webp"), (80, 90))
]

# Store multiple cacti
cacti = []
cactus_speed = 5
spawn_delay = random.randint(80, 150) # Random delay for cactus spawn

# Load Dino Images (Animation Frames)
dino_images = [
    pygame.transform.scale(pygame.image.load("D:/dinobot/ai_dinobot/dino/Chrome_T-Rex_Left_Run.webp"), (50, 50)), 
    pygame.transform.scale(pygame.image.load("D:/dinobot/ai_dinobot/dino/Chrome_T-Rex_Right_Run.webp"), (50, 50)),
]
dino_index = 0  # Track current frame
frame_count = 50  # Control speed of animation

# Dino Physics
DINO_X = 50
DINO_Y = GROUND_Y - 40
Gravity = 0.98
jump_speed = -18
y_velocity = 0
is_jumping = False

# Game Loop
running = True
while running:
    screen.fill((255, 255, 255)) 

    # Move ground & clouds
    ground_x -= ground_speed
    if ground_x <= -SCREEN_WIDTH:
        ground_x = 0

    screen.blit(ground_img, (ground_x, GROUND_Y))
    screen.blit(ground_img, (ground_x + SCREEN_WIDTH, GROUND_Y))

    cld_x -= cld_speed
    if cld_x <= -50:
        cld_x = SCREEN_WIDTH + random.randint(0, 100)
    screen.blit(cloud_img[0], (cld_x, cld_y))

    # Animate Dino
    frame_count += 2
    if frame_count % 10 == 0:
        dino_index = (dino_index + 1) % 2 

    screen.blit(dino_images[dino_index], (DINO_X, DINO_Y))

    # Spawn cacti at random intervals
    spawn_delay -= 2
    if spawn_delay <= 0:
        cactus_type = random.choice(cactus_images)  # Randomly pick a cactus type
        cacti.append([SCREEN_WIDTH, GROUND_Y - 70, cactus_type])  # Append new cactus
        spawn_delay = random.randint(80, 150)  # Reset spawn delay

    # Move and remove cacti
    for cactus in cacti[:]:  # Iterate over a copy of the list to allow removal
        cactus[0] -= cactus_speed  # Move left
        if cactus[0] < -50:  # If off-screen, remove it
            cacti.remove(cactus)

    # Draw cacti
    for cactus in cacti:
        screen.blit(cactus[2], (cactus[0], cactus[1]))

    # Gravity
    DINO_Y += y_velocity
    y_velocity += Gravity
    if DINO_Y >= GROUND_Y - 40:  # Check if dino is on the ground
        DINO_Y = GROUND_Y - 40
        y_velocity = 0
        is_jumping = False

    # Increase difficulty over time
    if not game_over and pygame.time.get_ticks() - last_speed_increase > 1500:
        cactus_speed += 1
        ground_speed += 1
        last_speed_increase = pygame.time.get_ticks()

    # Calculate elapsed time
    if not game_over:
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    else:
        if final_time == 0:
            final_time = (pygame.time.get_ticks() - start_time) // 1000
        elapsed_time = final_time

    # Render timer text
    timer_text = font.render(f"Time: {elapsed_time}s", True, (0, 0, 0))
    screen.blit(timer_text, (10, 10))

    # Create dino rect for collision
    dino_rect = pygame.Rect(DINO_X + 5, DINO_Y + 5, 40, 40)

    for cactus in cacti:
        cactus_rect = pygame.Rect(cactus[0], cactus[1], cactus[2].get_width(), cactus[2].get_height())
        if dino_rect.colliderect(cactus_rect) and not game_over:
            print("Collision Detected!")
            ground_speed = 0
            cactus_speed = 0
            jump_speed = 0
            game_over = True
            final_time = (pygame.time.get_ticks() - start_time) // 1000
            break

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not is_jumping:
                y_velocity = jump_speed
                is_jumping = True
    if game_over:
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 20))

    pygame.display.update()
    clock.tick(30)

pygame.quit()