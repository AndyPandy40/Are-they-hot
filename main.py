import pygame
import glob
import random

pygame.init()

GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def display_text(text, position, size, color, screen):

    text = str(text).strip()
    font = pygame.font.Font("freesansbold.ttf", size)
    text = font.render(text, True, color)

    text_rect = text.get_rect(center=(position))

    screen.blit(text, text_rect)


class mainGame:
    def __init__(self):
        self.screen_width = 1440
        self.screen_height = 864

        # Define MAX_WIDTH and MAX_HEIGHT based on the screen size
        self.MAX_WIDTH = self.screen_width // 4  # 25% of the screen width
        self.MAX_HEIGHT = self.screen_height // 4  # 25% of the screen height

        self.num_photos = 0

        self.images = {}
        # Load all PNG and JPG images from teacher_photos folder
        for filepath in glob.glob("teacher_photos/*.png") + glob.glob("teacher_photos/*.jpg") + glob.glob("teacher_photos/*.jpeg") + glob.glob("teacher_photos/*.jfif"):
            filename = filepath.split("/")[-1]  # Extract just the filename

            # Load the image
            image = pygame.image.load(filepath)

            # Get the image's width and height
            width, height = image.get_width(), image.get_height()

            # Check if the image exceeds the max dimensions
            if width > self.MAX_WIDTH or height > self.MAX_HEIGHT:
                # Calculate scale factor to keep the aspect ratio
                scale_factor = 3*min(self.MAX_WIDTH / width, self.MAX_HEIGHT / height)
                new_width = int(width * scale_factor)
                new_height = int(height * scale_factor)

                # Resize the image using smoothscale (better quality, prevents rotation)
                image = pygame.transform.smoothscale(image, (new_width, new_height))


            self.images[filename] = image
            self.num_photos += 1

        self.image_keys = list(self.images.keys())

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.run_game = True

        self.rand_num_1 = random.randint(0, self.num_photos - 1)  # Use 0-based indexing
        self.rand_num_2 = random.randint(0, self.num_photos - 1)  # Use 0-based indexing

        # Ensure both numbers are not the same
        while self.rand_num_1 == self.rand_num_2:
            self.rand_num_2 = random.randint(0, self.num_photos - 1)

        # Get random images based on the random numbers
        self.random_image_1 = self.images[self.image_keys[self.rand_num_1]]
        self.random_image_2 = self.images[self.image_keys[self.rand_num_2]]

    def mainloop(self):
        while self.run_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.KEYDOWN:  # Check for key events
                    if event.key == pygame.K_n:  # If 'n' is pressed, generate new images
                        self.generate_new_images()


            self.display_stuff()

            

            self.clock.tick(120)

    def display_stuff(self):
        self.screen.fill(WHITE)

        self.screen.blit(self.random_image_1, (0, 0))
        self.screen.blit(self.random_image_2, (self.screen_width // 2, 0))

        display_text("Who is hotter?", (self.screen_width//2, 50), 75, BLACK, self.screen)



        pygame.display.update()

    def generate_new_images(self):
        self.rand_num_1 = random.randint(0, self.num_photos - 1)  # Use 0-based indexing
        self.rand_num_2 = random.randint(0, self.num_photos - 1)  # Use 0-based indexing

        # Ensure both numbers are not the same
        while self.rand_num_1 == self.rand_num_2:
            self.rand_num_2 = random.randint(0, self.num_photos - 1)

        # Get random images based on the random numbers
        self.random_image_1 = self.images[self.image_keys[self.rand_num_1]]
        self.random_image_2 = self.images[self.image_keys[self.rand_num_2]]


    def quit(self):
        self.run_game = False
        pygame.quit()
        exit()


game = mainGame()
game.mainloop()

pygame.quit()
