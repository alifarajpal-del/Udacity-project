"""
Module for classifying pet images using a pre-trained CNN model.
This module processes images and stores classification results.
"""

from classifier import classifier


def classify_images(images_dir, results_dic, model):
    """
    Classifies the images in results_dic using a pre-trained CNN model.
    
    Updates results_dic by adding classifier label and match result for each image.
    
    Args:
        images_dir (str): Path to the folder of pet images
        results_dic (dict): Dictionary where keys are filenames and values are lists
                           containing [pet_label] initially
        model (str): Name of CNN model architecture to use
    
    Returns:
        None (modifies results_dic in place)
    
    Side effects:
        Modifies results_dic so each value becomes:
        [pet_label, classifier_label, match]
        where match is 1 if pet_label is in classifier_label, else 0
    """
    # Iterate through each image in results_dic
    for filename in results_dic:
        # Skip hidden files
        if filename.startswith("."):
            continue
        
        # Build full image path
        if images_dir.endswith("/"):
            full_image_path = images_dir + filename
        else:
            full_image_path = images_dir + "/" + filename
        
        # Classify the image using the classifier function
        classifier_label = classifier(full_image_path, model)
        
        # Format classifier label
        classifier_label = classifier_label.lower().strip()
        
        # Get pet label (already in results_dic[filename][0])
        pet_label = results_dic[filename][0]
        
        # Determine if there's a match
        match = 1 if pet_label in classifier_label else 0
        
        # Update results_dic with classifier label and match
        results_dic[filename].extend([classifier_label, match])
