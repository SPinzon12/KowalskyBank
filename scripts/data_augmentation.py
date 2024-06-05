import Augmentor
import os

def augment_images_in_folder(folder_path, num_samples=50):
    """Augment images in the specified folder."""
    p = Augmentor.Pipeline(folder_path)

    # Define augmentation operations
    p.rotate(probability=0.7, max_left_rotation=10, max_right_rotation=10)
    p.flip_left_right(probability=0.5)
    p.flip_top_bottom(probability=0.5)
    p.random_contrast(probability=0.5, min_factor=0.7, max_factor=1.3)
    p.random_brightness(probability=0.5, min_factor=0.7, max_factor=1.3)
    p.random_color(probability=0.5, min_factor=0.7, max_factor=1.3)
    p.random_distortion(probability=0.5, grid_width=4, grid_height=4, magnitude=8)
    p.zoom_random(probability=0.5, percentage_area=0.8)
    p.crop_random(probability=0.5, percentage_area=0.8)
    p.resize(probability=1.0, width=2992, height=2992)

    # Sample and save augmented images
    p.sample(num_samples)


def augment_images_in_directories(base_path, num_samples=50):
    """Augment images in specified directories."""
    categories = ["2k", "5k", "10k", "20k", "50k"]
    subfolders = ["frontal", "posterior"]

    for category in categories:
        for subfolder in subfolders:
            folder_path = os.path.join(base_path, category, subfolder)
            if os.path.exists(folder_path):
                print(f"Augmenting images in: {folder_path}")
                augment_images_in_folder(folder_path, num_samples)
            else:
                print(f"Folder does not exist: {folder_path}")


if __name__ == "__main__":
    base_path = "./"  # Update this with the actual path
    augment_images_in_directories(base_path, num_samples=50)
