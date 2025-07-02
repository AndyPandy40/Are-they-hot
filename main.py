import pygame
import glob
import random
import csv
from PIL import Image, ImageOps
import io

pygame.init()

GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 200, 0)
RED = (255, 0, 0)
LIGHT_RED = (200, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# TODO
# Fix sideways images
# give buttons functionality
# add text file to save the scores of people

# Simple function to display text on the screen
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
        self.MAX_WIDTH = self.screen_width // 1.5  # 50% of the screen width
        self.MAX_HEIGHT = self.screen_height // 1.5  # 50% of the screen height

        self.num_photos = 0

        self.teacher_stats = []

        # Read the CSV file into a list of dictionaries
        with open('teacher_stats.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.num_photos += 1
                self.teacher_stats.append(row)





        self.generate_new_images()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.run_game = True

        self.rand_num_1 = random.randint(0, self.num_photos - 1)  # Use 0-based indexing
        self.rand_num_2 = random.randint(0, self.num_photos - 1)  # Use 0-based indexing


        self.Button1 = Button(self.screen, GREEN, LIGHT_GREEN, "person 1", (self.screen_width//4 - 225, self.screen_height-100), 450, 100, 40, self.choose_option_1)
        self.Button2 = Button(self.screen, GREEN, LIGHT_GREEN, "person 2", (3*self.screen_width//4 - 225, self.screen_height-100), 450, 100, 40, self.choose_option_2)


    def mainloop(self):
        while self.run_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.KEYDOWN:  # Check for key events
                    if event.key == pygame.K_n:  # If 'n' is pressed, generate new images
                        self.generate_new_images()


            self.display_stuff()

            

            self.clock.tick(60)

    def display_stuff(self):
        self.screen.fill(WHITE)

        self.screen.blit(self.teacher1_photo, (0, 0))
        self.screen.blit(self.teacher2_photo, (self.screen_width // 2, 0))

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
        self.teacher1_photo = pygame.image.load(self.teacher_stats[self.rand_num_1]["Photo"])
        self.teacher2_photo = pygame.image.load(self.teacher_stats[self.rand_num_2]["Photo"])

                
        self.teacher1_photo = self.scale_image(self.teacher_stats[self.rand_num_1]["Photo"])
        self.teacher2_photo = self.scale_image(self.teacher_stats[self.rand_num_2]["Photo"])



    def scale_image(self, path):  # Chat gpt image stuff 
        # Load the image using PIL to respect EXIF orientation
        pil_image = Image.open(path)
        pil_image = ImageOps.exif_transpose(pil_image)  # Rotates image based on EXIF metadata

        # Resize if needed
        width, height = pil_image.size
        if width > self.MAX_WIDTH or height > self.MAX_HEIGHT:
            scale = min(self.MAX_WIDTH / width, self.MAX_HEIGHT / height)
            new_size = (int(width * scale), int(height * scale))
            pil_image = pil_image.resize(new_size, Image.Resampling.LANCZOS)

        # Convert to Pygame surface
        image_bytes = pil_image.convert("RGBA").tobytes()
        return pygame.image.fromstring(image_bytes, pil_image.size, "RGBA")



    def quit(self):
        self.run_game = False
        pygame.quit()
        exit()

    def choose_option_1(self):

        # Open a text file to save the number of times user's have voted
        with open("User_data.txt", "r") as file:
            number = int(file.readline().strip())

        # Increment the number of votes
        number += 1

        # Write the updated number back to the file
        with open("counter.txt", "w") as file:
            file.write(str(number))

        # close the file
        file.close()

        





        self.teacher_stats[self.rand_num_1]["Score"] = int(self.teacher_stats[self.rand_num_1]["Score"]) + 5
        self.teacher_stats[self.rand_num_2]["Score"] = int(self.teacher_stats[self.rand_num_2]["Score"]) - 5

        # Save the updated scores back to the CSV file
        with open('teacher_stats.csv', 'w', newline='') as csvfile:
            fieldnames = self.teacher_stats[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.teacher_stats)


        # Generate new images when a button is clicked
        self.generate_new_images()

    def choose_option_2(self):


        # Open a text file to save the number of times user's have voted
        with open("User_data.txt", "r") as file:
            number = int(file.readline().strip())

        # Increment the number of votes
        number += 1

        # Write the updated number back to the file
        with open("counter.txt", "w") as file:
            file.write(str(number))

        # close the file
        file.close()

        self.teacher_stats[self.rand_num_2]["Score"] = int(self.teacher_stats[self.rand_num_2]["Score"]) + 5
        self.teacher_stats[self.rand_num_1]["Score"] = int(self.teacher_stats[self.rand_num_1]["Score"]) - 5



        # Save the updated scores back to the CSV file
        with open('teacher_stats.csv', 'w', newline='') as csvfile:
            fieldnames = self.teacher_stats[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.teacher_stats)


        # Generate new images when a button is clicked
        self.generate_new_images()


class Button:
    def __init__(self, screen, inactive_color, active_color, text, position, width, height, text_size, action):
        self.screen = screen
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.text = text
        self.position = position
        self.width = width
        self.height = height
        self.text_size = text_size
        self.action = action
        print(self.action)


        # Calculate the centre of the button
        self.button_center = ((self.position[0] + (self.width//2)), self.position[1] + (self.height//2))

        pygame.draw.rect(screen, self.inactive_color, (self.position[0], self.position[1], self.width, self.height), 0, 15)
        display_text(self.text, self.button_center, self.text_size, BLACK, screen)

        self.last_update = False
        self.current_update = False

        self.clicked = False

    def draw_button(self, screen):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        # Check if hovering
        if self.position[0] < mouse[0] < self.position[0] + self.width and self.position[1] < mouse[1] < self.position[1] + self.height:
            button_color = self.active_color
            # Check for click
            if click[0] and not self.clicked:
                self.action()
                self.clicked = True
        else:
            button_color = self.inactive_color

        # Reset click when mouse button is released
        if not click[0]:
            self.clicked = False

        # Draw button
        pygame.draw.rect(screen, button_color, (self.position[0], self.position[1], self.width, self.height), 0, 15)
        display_text(self.text, self.button_center, self.text_size, BLACK, screen)



game = mainGame()
game.mainloop()

pygame.quit()
