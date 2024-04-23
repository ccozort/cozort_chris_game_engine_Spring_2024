import pygame

# Initialize Pygame
pygame.init()

# Set up the display surface
screen = pygame.display.set_mode((800, 600))

# Load an image
image = pygame.image.load('path_to_image.png')

# The main loop of the game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Draw the image onto the display surface
    screen.blit(image, (50, 50))  # Blit the image at coordinates (50, 50)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()