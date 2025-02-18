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

        self.Button1 = Button(self.screen, LIGHT_GREEN, GREEN, "person 1", (self.screen_width//2, self.screen_height-100), 100, 50, 20, self.choose_option())
        self.Button2 = Button(self.screen, LIGHT_GREEN, GREEN, "person 2", (3*self.screen_width//2, self.screen_height-100), 100, 50, 20, self.choose_option())


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

        self.Button1.draw_button(self.screen)
        self.Button2.draw_button(self.screen)



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

    def choose_option(self):
        pass


class Button:
    def __init__(self, screen, inactive_color, active_color, text, position, width, height, text_size, action=None):
        self.screen = screen
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.text = text
        self.position = position
        self.width = width
        self.height = height
        self.text_size = text_size
        self.action = action

        # Calculate the centre of the button
        self.button_center = ((self.position[0] + (self.width//2)), self.position[1] + (self.height//2))

        pygame.draw.rect(screen, self.inactive_color, (self.position[0], self.position[1], self.width, self.height), 0, 15)
        display_text(self.text, self.button_center, self.text_size, BLACK, screen)

        self.last_update = False
        self.current_update = False

    def draw_button(self, screen):
        # Get the position of the mouse and see if the user is clicking
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()


        # Check if user is hovering over button
        if self.position[0] < mouse[0] < self.position[0] + self.width and self.position[1] < mouse[1] < self.position[1] + self.height:
            self.current_update = True
            button_color = self.active_color
            if click[0]:
                # Preform the button's action if the user clicks
                self.action()
        else:
            button_color = self.inactive_color
            self.current_update = False


        if self.current_update != self.last_update:
            # Draw a rectangle for the button
            pygame.draw.rect(screen, button_color, (self.position[0], self.position[1], self.width, self.height), 0, 15)
            
            # Display text on button
            display_text(self.text, self.button_center, self.text_size, BLACK, screen)

        self.last_update = self.current_update


game = mainGame()
game.mainloop()

pygame.quit()
