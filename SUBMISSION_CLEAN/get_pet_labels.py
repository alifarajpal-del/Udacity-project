"""
Module for creating pet image labels from filenames.
This module processes image filenames to extract and format pet labels.
"""

from os import listdir


def get_pet_labels(image_dir):
    """
    Creates labels from filenames in the pet_images folder.
    
    Processes filenames to extract pet names and formats them as lowercase
    with words separated by spaces. Ignores numbers and file extensions.
    Skips hidden files (starting with ".").
    
    Args:
        image_dir (str): Path to the folder containing pet images
    
    Returns:
        dict: Dictionary with filename as key and list containing the
              formatted pet label as value
              Example: {"Boston_terrier_02259.jpg": ["boston terrier"]}
    """
    pet_image_labels = {}
    
    # Get list of filenames in the directory
    image_filenames = listdir(image_dir)
    
    for filename in image_filenames:
        # Skip hidden files
        if filename.startswith("."):
            continue
        
        # Remove file extension
        filename_without_ext = filename.split(".")[0]
        
        # Split filename by underscores
        words = filename_without_ext.split("_")
        
        # Filter out numbers and join alphabetic words
        pet_label = ""
        for word in words:
            if word.isalpha():
                pet_label += word.lower() + " "
        
        # Strip trailing space and store in dictionary
        pet_label = pet_label.strip()
        pet_image_labels[filename] = [pet_label]
    
    return pet_image_labels
