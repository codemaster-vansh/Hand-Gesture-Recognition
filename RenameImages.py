import os
import glob

def rename_images(base_dir):
    # Get a list of all subdirectories in the base directory
    subdirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    
    for subdir in subdirs:
        subdir_path = os.path.join(base_dir, subdir)
        images = glob.glob(os.path.join(subdir_path, '*'))
        
        for i, img_path in enumerate(images):
            # Extract the file extension
            _, ext = os.path.splitext(img_path)
            new_name = f"{subdir}_{i+200}{ext}"
            new_path = os.path.join(subdir_path, new_name)
            
            os.rename(img_path, new_path)
            print(f"Renamed {img_path} to {new_path}")

# Replace 'your_base_directory_path' with the path to your base directory
base_directory = r"F:\AI and ML\AIMS\Projects\NEW\data1\Augmented"
rename_images(base_directory)
