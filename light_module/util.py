from PIL import Image
import shutil
import os

def clear_folder(folder_path):
    if not os.path.exists(folder_path):
        print("no folder")
        return

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        except Exception as e:
            print("error in deleting")

    print("clear")


def diffusion_preprocessing(Image_path, __Image):
    width, height = __Image.size
    size = max(width, height)

    new_img = Image.new("RGB", size=(size, size), color=(0, 0, 0))

    paste_x = (size - width) // 2
    paste_y = (size - height) // 2

    new_img.paste(__Image, (paste_x, paste_y))

    new_img.save(Image_path)