import csv
import glob
import os


images = []
num_images = 0


# This all just basically resets the files for distriburttion, so that the game starts fresh


# clear the teacher_stats.csv file if it exists
try:
    with open("teacher_stats.csv", "w", newline='') as csvfile:
        pass
except FileNotFoundError:
    pass


# Write zero as the only item in the "User_data.txt" file
with open("User_data.txt", "w") as file:
    file.write("0")


for filepath in glob.glob("teacher_photos/*.png") + glob.glob("teacher_photos/*.jpg") + glob.glob("teacher_photos/*.jpeg") + glob.glob("teacher_photos/*.jfif"):
    filename = os.path.basename(filepath)  # Safely gets just the file name
    images.append(filename)
    num_images += 1

with open("teacher_stats.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(["Number", "Photo", "Score"])

    # add a number 1, 2, 3... for first column
    # add the image name in the second column
    # add 1000 in the third column

    
    for i in range(1, num_images):
        writer.writerow([i, images[i], 1000])


