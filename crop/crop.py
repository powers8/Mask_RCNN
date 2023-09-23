from PIL import Image, ImageOps
import os

large_image = Image.open("大样地1.png")

image_gray = large_image.convert("L")
image_gray.save("image_gray.png")

small_width = 224
small_height = 224

large_width, large_height = large_image.size

num_horizontal = large_width / small_width
num_vertical = large_height / small_height

# small_width = large_width / num_horizontal
# small_height = large_height / num_vertical

if not os.path.exists("small images"):
    os.makedirs("small images")

for i in range(int(num_vertical)):
    for j in range(int(num_horizontal)):
        left = j * small_width
        top = i * small_height
        right = (j + 1) * small_width
        bottom = (i + 1) * small_height

        small_image = large_image.crop((left, top, right, bottom))

        # if small_image.width < 224 or small_image.height < 224:
        #     small_image = ImageOps.pad(small_image, (224, 224), color="white")
        #     small_image.show()
        small_image.save(f"small images/small_{i}_{j}.png")

print("切割完成")
