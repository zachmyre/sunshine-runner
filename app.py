import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() - 100)  # Starting position at the bottom center
player_speed = 300

# Load the flower images for left and right directions
flower_left_image = pygame.image.load("assets/flower_left.png")
flower_right_image = pygame.image.load("assets/flower_right.png")

# Load the missile image
missile_image = pygame.image.load("assets/missile.png")

# Initial image will be the right-facing one
current_image = flower_right_image

missiles = []  # Use a list to keep track of multiple missiles

# Timer for missile shooting
time_since_last_missile = 0
missile_cooldown = 0.5  # Half a second cooldown

# Platform properties
platform_y = screen.get_height() - 50
platform_width = screen.get_width()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from the last frame
    screen.fill("purple")

    keys = pygame.key.get_pressed()

    # Horizontal Movement
    if keys[pygame.K_a]:
        player_pos.x -= player_speed * dt
        # Switch to the left-facing image when moving left
        current_image = flower_left_image
    if keys[pygame.K_d]:
        player_pos.x += player_speed * dt
        # Switch to the right-facing image when moving right
        current_image = flower_right_image

    # Shooting Missiles
    time_since_last_missile += dt
    if keys[pygame.K_SPACE] and time_since_last_missile >= missile_cooldown:
        # Shoot a missile to the right
        missiles.append({
            'position': player_pos + pygame.Vector2(current_image.get_width() / 2, 0),
            'speed': 500  # Adjust the missile speed as needed
        })
        time_since_last_missile = 0  # Reset the timer

    # Update the missile positions and remove them if they go off the screen
    missiles = [missile for missile in missiles if missile['position'].x < screen.get_width()]
    for missile in missiles:
        missile['position'].x += missile['speed'] * dt

    # Make sure the player stays within the screen boundaries
    player_pos.x = max(player_pos.x, 0)
    player_pos.x = min(player_pos.x, screen.get_width())

    # Check for platform collision to restrict vertical movement
    if player_pos.y < platform_y - current_image.get_height() / 2:
        player_pos.y = platform_y - current_image.get_height() / 2

    # Blit the current image at the player's position
    screen.blit(current_image, player_pos - pygame.Vector2(current_image.get_width() / 2, current_image.get_height() / 2))

    # Draw the platform
    pygame.draw.rect(screen, "yellow", (0, platform_y, platform_width, 50))

    # Blit the missiles
    for missile in missiles:
        screen.blit(missile_image, missile['position'] - pygame.Vector2(missile_image.get_width() / 2, missile_image.get_height() / 2))

    # flip() the display to put your work on the screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is the delta time in seconds since the last frame, used for framerate-independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
