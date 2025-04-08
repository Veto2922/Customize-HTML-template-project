import os
import shutil
import random

# TODO : make uint test for this function , add logging , exception handling and try to make it as class
def select_random_image_and_move_it_to_Html_src(src_root_folder, dest_folder, image_placeholder, html_template, image_extensions={'.jpg', '.jpeg', '.png', '.bmp', '.gif'}):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    for key, value in image_placeholder.items():
        k = html_template.count(key)
        
        image_folder = os.path.join(src_root_folder, value['size'])
        
        images = [f for f in os.listdir(image_folder) if os.path.splitext(f)[1].lower() in image_extensions]
        
        for _ in range(k):
            selected_image = random.choice(images)
            selected_image_path = os.path.join(image_folder, selected_image)
            
            shutil.copy2(selected_image_path, os.path.join(dest_folder, selected_image))
            
            asset_path = f'"assets/img/temp/{selected_image}"'
            print(asset_path)
            html_template = html_template.replace(key, asset_path, 1)
    
    return html_template