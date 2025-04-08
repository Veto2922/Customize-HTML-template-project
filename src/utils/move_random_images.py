import os
import shutil
import random

def move_random_images(src_root_folder, dest_folder, image_extensions={'.jpg', '.jpeg', '.png', '.bmp', '.gif'}):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for folder_name in os.listdir(src_root_folder):
        folder_path = os.path.join(src_root_folder, folder_name)
        if os.path.isdir(folder_path):
            # List image files only
            images = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in image_extensions]
            if images:
                selected_image = random.choice(images)
                src_image_path = os.path.join(folder_path, selected_image)
                extension = os.path.splitext(selected_image)[1]
                dest_image_path = os.path.join(dest_folder, f"{folder_name}{extension}")
                
                shutil.copy2(src_image_path, dest_image_path)
                print(f"Moved: {selected_image} -> {dest_image_path}")
            else:
                print(f"No images found in folder: {folder_name}")


