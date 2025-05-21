import os
import shutil
import random

# ===== USER CONFIGURATION =====
AUGMENTED_DIR = r"F:\PROJECTS\AI PROJECTS\data\Augmented"       # Update with your actual path
NON_AUGMENTED_DIR = r"F:\PROJECTS\AI PROJECTS\data\PRIMARY"  # Update with your actual path
NEW_PARENT_DIR = r"F:\PROJECTS\AI PROJECTS\data\Grouped_Pics"       # Update with your destination path
# ==============================

# Verify source directories exist
if not all(os.path.exists(d) for d in [AUGMENTED_DIR, NON_AUGMENTED_DIR]):
    raise FileNotFoundError("One or more source directories don't exist")

# Create new parent directory if needed
os.makedirs(NEW_PARENT_DIR, exist_ok=True)

# Process each subdirectory
for subdir in os.listdir(NON_AUGMENTED_DIR):
    # Path setup
    orig_path = os.path.join(NON_AUGMENTED_DIR, subdir)
    aug_path = os.path.join(AUGMENTED_DIR, subdir)
    combined_path = os.path.join(NEW_PARENT_DIR, subdir)
    
    # Create combined subdirectory
    os.makedirs(combined_path, exist_ok=True)

    all_images = []

    # Copy non-augmented images (0-199)
    for i in range(200):
        src = os.path.join(orig_path, f"{subdir}_{i}.jpg")
        dest = os.path.join(combined_path, f"{subdir}_{i}.jpg")
        if os.path.exists(src):
            shutil.copy(src, dest)
            all_images.append(dest)

    # Copy augmented images (200-399)
    for j in range(200, 400):
        src = os.path.join(aug_path, f"{subdir}_{j}.jpg")
        dest = os.path.join(combined_path, f"{subdir}_{j}.jpg")
        if os.path.exists(src):
            shutil.copy(src, dest)
            all_images.append(dest)

    # Shuffle the images randomly
    random.shuffle(all_images)

    # Rename sequentially
    for index, file_path in enumerate(all_images, 1):
        new_name = f"{subdir}_shuffled_{index}.jpg"
        new_path = os.path.join(combined_path, new_name)
        os.rename(file_path, new_path)

print("Combination, shuffling, and renaming complete! Verify results in:", NEW_PARENT_DIR)
