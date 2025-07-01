import csv
import glob


images = []
num_images = 0


for filepath in glob.glob("teacher_photos/*.png") + glob.glob("teacher_photos/*.jpg") + glob.glob("teacher_photos/*.jpeg") + glob.glob("teacher_photos/*.jfif"):
    images.append(filepath.split("/")[-1])
    num_images += 1

with open("teacher_stats.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)

    # add a number 1, 2, 3... for first column
    # add the image name in the second column
    # add 1000 in the third column

    
    for i in range(1, num_images):
        writer.writerow([i, images[i], 1000])


