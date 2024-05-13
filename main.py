from PIL import Image
import os
from concurrent.futures import ThreadPoolExecutor


def split_map_image(image_path, target_width=1216, target_height=1216):
    img = Image.open(image_path)

    if img.width != 9728 or img.height != 9728:
        raise ValueError("Image size is not 9728x9728.")

    splits_width = img.width // target_width
    splits_height = img.height // target_height

    split_images = []

    for i in range(0, splits_height):
        for j in range(0, splits_width):
            box = (
                j * target_width,
                i * target_height,
                (j + 1) * target_width,
                (i + 1) * target_height,
            )
            split_images.append(img.crop(box))

    for index, split_img in enumerate(split_images):
        split_img.save(f"dataset/{index + 128}.png")

    return split_images


def split_clip_image(image_path, target_width=608, target_height=608):
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    os.makedirs(f"tiles/{image_name}", exist_ok=True)
    os.makedirs(f"labels/{image_name}", exist_ok=True)

    img = Image.open(image_path)

    step = 32
    count = 0
    for i in range(0, 608 // step):
        for j in range(0, 608 // step):
            box = (
                j * step,
                i * step,
                j * step + 608,
                i * step + 608,
            )
            split_img = img.crop(box)
            split_img.save(f"tiles/{image_name}/{count}.png")
            with open(f"labels/{image_name}/{count}.txt", "w") as label_file:
                label_file.write(f"{j * step + 304} {i * step + 304}")

            count += 1


if __name__ == "__main__":
    if not os.path.exists("tiles"):
        os.makedirs("tiles")
    if not os.path.exists("labels"):
        os.makedirs("labels")

    directory = "./dataset"
    files = [os.path.join(directory, f"{i}.png") for i in range(61, 99)]

    with ThreadPoolExecutor() as executor:
        executor.map(split_clip_image, files)

    # for i in range(61, 99):
    #     path = os.path.join(directory, f"{i}.png")
    #     split_clip_image(path)
