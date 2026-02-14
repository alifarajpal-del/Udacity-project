# PROGRAMMER: Ali Faraj
# DATE CREATED: 12/02/2026
#
# PURPOSE: Image Classification for a City Dog Show
"""
Main script for image classification.
This module contains the main function that uses a pre-trained CNN model
to classify images of pets from a folder.
"""

from time import time
from get_input_args import get_input_args
from get_pet_labels import get_pet_labels
from classify_images import classify_images
from adjust_results4_isadog import adjust_results4_isadog
from calculates_results_stats import calculates_results_stats
from print_results import print_results


def main():
    """
    Performs classification of images using a pre-trained CNN model.
    
    This function:
    1. Gets command-line arguments
    2. Classifies images in the specified directory
    3. Records and prints the total runtime
    """
    # TODO: 0 - Record the start time
    start_time = time()
    
    # Get command-line arguments
    in_arg = get_input_args()
    
    # Get pet image labels
    pet_image_labels = get_pet_labels(in_arg.dir)
    
    # Classify the images
    classify_images(in_arg.dir, pet_image_labels, in_arg.arch)
    
    # Adjust results to classify labels as dogs or not dogs
    adjust_results4_isadog(pet_image_labels, in_arg.dogfile)
    
    # Calculate results statistics
    results_stats = calculates_results_stats(pet_image_labels)
    
    # Print results
    print_results(pet_image_labels, results_stats, in_arg.arch)
    
    # TODO: 0 - Record the end time
    end_time = time()
    
    # TODO: 0 - Compute total runtime in seconds
    tot_time = end_time - start_time
    
    # TODO: 0 - Print the runtime formatted as hh:mm:ss
    hours = int(tot_time // 3600)
    minutes = int((tot_time % 3600) // 60)
    seconds = int(tot_time % 60)
    
    print(f"\nTotal Time Elapsed: {hours:02d}:{minutes:02d}:{seconds:02d}")


if __name__ == "__main__":
    main()
