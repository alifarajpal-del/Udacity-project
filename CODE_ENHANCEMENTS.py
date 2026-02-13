# ==============================================================================
# CODE ENHANCEMENTS GUIDE
# Professional code improvements with type hints and docstrings
# ==============================================================================
# These enhancements improve code quality while maintaining Udacity requirements
# ==============================================================================

# ============================================================
# FILE: get_input_args.py (Enhanced Version)
# ============================================================

"""
Command-line argument parser for image classification pipeline.

This module provides a clean interface for configuring the classification system
via command-line arguments. Follows ArgumentParser best practices for production
Python applications.
"""

import argparse
from typing import Any


def get_input_args() -> argparse.Namespace:
    """
    Parse and return command-line arguments for the image classifier.
    
    This function creates an ArgumentParser configured with three required
    parameters for the classification pipeline. All arguments have sensible
    defaults to enable quick testing without configuration.
    
    Command-line Arguments:
        --dir (str): Path to folder containing images to classify.
                     Default: 'pet_images/'
                     
        --arch (str): CNN model architecture for classification.
                      Choices: 'resnet', 'alexnet', 'vgg'
                      Default: 'resnet'
                      
        --dogfile (str): Path to text file listing valid dog breed names.
                         Default: 'dognames.txt'
    
    Returns:
        argparse.Namespace: Object containing parsed arguments as attributes
                           accessible via dot notation (e.g., args.dir)
    
    Example:
        >>> args = get_input_args()
        >>> print(f"Processing images from: {args.dir}")
        >>> print(f"Using model architecture: {args.arch}")
        
    Notes:
        - Validates that architecture is one of the supported models
        - File paths are not validated here (handled during execution)
        - Default values enable zero-config quickstart
    
    Raises:
        SystemExit: If invalid arguments provided (handled by argparse)
    """
    parser = argparse.ArgumentParser(
        description='AI-powered image classification for city dog show entries',
        epilog='Example: python check_images.py --dir uploaded_images/ --arch resnet',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--dir',
        type=str,
        default='pet_images/',
        metavar='PATH',
        help='path to the folder of pet images (default: pet_images/)'
    )
    
    parser.add_argument(
        '--arch',
        type=str,
        default='resnet',
        choices=['resnet', 'alexnet', 'vgg'],
        metavar='MODEL',
        help='CNN model architecture: resnet, alexnet, or vgg (default: resnet)'
    )
    
    parser.add_argument(
        '--dogfile',
        type=str,
        default='dognames.txt',
        metavar='FILE',
        help='text file containing valid dog breed names (default: dognames.txt)'
    )
    
    return parser.parse_args()


# ============================================================
# FILE: get_pet_labels.py (Enhanced Version)
# ============================================================

"""
Pet label extraction from image filenames.

This module handles the critical task of extracting ground truth labels from
image filenames for validation purposes. Uses a standardized naming convention
to ensure accurate classification benchmarking.
"""

import os
from typing import Dict, List


def get_pet_labels(image_dir: str) -> Dict[str, List[str]]:
    """
    Extract pet labels from image filenames in the specified directory.
    
    Creates a dictionary mapping each image filename to its extracted label(s).
    The label extraction follows these rules:
    
    1. Filename is converted to lowercase
    2. File extension is removed
    3. Underscores and hyphens are replaced with spaces
    4. Numbers are removed
    5. Leading/trailing whitespace is stripped
    
    Naming Convention:
        Golden_retriever_01.jpg    → "golden retriever"
        Yorkshire_terrier_02.jpg   → "yorkshire terrier"
        Cat_01.jpg                 → "cat"
        Coffee_table_01.jpg        → "coffee table"
    
    Args:
        image_dir: Path to directory containing image files.
                   May or may not include trailing slash.
    
    Returns:
        Dictionary mapping filenames to label lists:
        {
            'Golden_retriever_01.jpg': ['golden retriever'],
            'Cat_01.jpg': ['cat'],
            ...
        }
    
    Example:
        >>> labels = get_pet_labels('uploaded_images/')
        >>> for filename, label_list in labels.items():
        ...     print(f"{filename}: {label_list[0]}")
        Golden_retriever_01.jpg: golden retriever
    
    Notes:
        - Skips hidden files (starting with '.')
        - Expects one label per filename (list contains single element)
        - Label quality directly impacts classification accuracy
        - Case-insensitive to match ImageNet label format
    
    Raises:
        FileNotFoundError: If image_dir does not exist
    """
    results_dic = {}
    
    # Get list of files in directory, skipping hidden files
    filename_list = [f for f in os.listdir(image_dir) if not f.startswith('.')]
    
    for filename in filename_list:
        # Extract label from filename using standardized algorithm
        pet_label = extract_label_from_filename(filename)
        
        # Store in dictionary if not already present
        if filename not in results_dic:
            results_dic[filename] = [pet_label]
        else:
            # Log warning if duplicate filename detected (shouldn't happen)
            print(f"Warning: Duplicate filename '{filename}' found. Skipping.")
    
    return results_dic


def extract_label_from_filename(filename: str) -> str:
    """
    Extract and normalize label from a single filename.
    
    Helper function that applies the label extraction algorithm:
    - Convert to lowercase
    - Remove file extension
    - Replace underscores/hyphens with spaces
    - Remove digits
    - Strip whitespace
    
    Args:
        filename: Image filename (e.g., 'Golden_retriever_01.jpg')
    
    Returns:
        Normalized label string (e.g., 'golden retriever')
    
    Example:
        >>> extract_label_from_filename('Yorkshire_terrier_02.jpg')
        'yorkshire terrier'
    """
    import re
    
    # Convert to lowercase
    label = filename.lower()
    
    # Remove file extension
    label = label.rsplit('.', 1)[0]
    
    # Replace underscores and hyphens with spaces
    label = re.sub(r'[-_]', ' ', label)
    
    # Remove all digits
    label = re.sub(r'[0-9]', '', label)
    
    # Strip leading/trailing whitespace
    label = label.strip()
    
    return label


# ============================================================
# FILE: calculates_results_stats.py (Enhanced Version with Type Hints)
# ============================================================

"""
Statistical analysis module for classification results.

Computes comprehensive performance metrics including accuracy, precision,
and percentages for dog detection, breed classification, and non-dog filtering.
"""

from typing import Dict, List, Union


def calculates_results_stats(results_dic: Dict[str, List[Union[str, int]]]) -> Dict[str, Union[int, float]]:
    """
    Calculate comprehensive statistics from classification results.
    
    Processes the results dictionary to compute counts and percentages for:
    - Total images processed
    - Dog vs. non-dog classification
    - Breed-specific accuracy
    - Overall match rate
    
    Args:
        results_dic: Dictionary with structure:
                     {
                         filename: [
                             pet_label,          # index 0: str
                             classifier_label,   # index 1: str
                             match,              # index 2: int (0 or 1)
                             pet_is_dog,         # index 3: int (0 or 1)
                             classifier_is_dog   # index 4: int (0 or 1)
                         ]
                     }
    
    Returns:
        Statistics dictionary:
        {
            'n_images': int,              # Total images
            'n_dogs_img': int,            # Ground truth dog count
            'n_notdogs_img': int,         # Ground truth non-dog count
            'n_match': int,               # Exact label matches
            'n_correct_dogs': int,        # Correctly classified dogs
            'n_correct_notdogs': int,     # Correctly classified non-dogs
            'n_correct_breed': int,       # Correctly classified breeds (dogs only)
            'pct_match': float,           # % exact matches
            'pct_correct_dogs': float,    # % correct dog classifications
            'pct_correct_breed': float,   # % correct breed classifications
            'pct_correct_notdogs': float  # % correct non-dog classifications
        }
    
    Example:
        >>> results = {
        ...     'Golden_retriever.jpg': ['golden retriever', 'golden retriever', 1, 1, 1],
        ...     'Cat.jpg': ['cat', 'tabby cat', 0, 0, 0]
        ... }
        >>> stats = calculates_results_stats(results)
        >>> print(f"Dog detection accuracy: {stats['pct_correct_dogs']:.1f}%")
        Dog detection accuracy: 100.0%
    
    Notes:
        - Division by zero is guarded (returns 0.0% for empty categories)
        - Percentages are floats in range [0.0, 100.0]
        - Breed accuracy only considers images where ground truth is a dog
    
    Raises:
        KeyError: If results_dic has unexpected structure
    """
    # Initialize results statistics dictionary
    results_stats_dic: Dict[str, Union[int, float]] = {}
    
    # Initialize all counters to 0
    results_stats_dic['n_images'] = 0
    results_stats_dic['n_dogs_img'] = 0
    results_stats_dic['n_notdogs_img'] = 0
    results_stats_dic['n_match'] = 0
    results_stats_dic['n_correct_dogs'] = 0
    results_stats_dic['n_correct_notdogs'] = 0
    results_stats_dic['n_correct_breed'] = 0
    
    # Iterate through results dictionary to count statistics
    for key in results_dic:
        # Count total images processed
        results_stats_dic['n_images'] += 1
        
        # Count exact label matches (index 2)
        if results_dic[key][2] == 1:
            results_stats_dic['n_match'] += 1
        
        # Process dog images (index 3 = pet_is_dog)
        if results_dic[key][3] == 1:
            results_stats_dic['n_dogs_img'] += 1
            
            # Count correctly classified breeds (both say dog AND labels match)
            if results_dic[key][2] == 1:
                results_stats_dic['n_correct_breed'] += 1
            
            # Count correctly classified as dog (index 4 = classifier_is_dog)
            if results_dic[key][4] == 1:
                results_stats_dic['n_correct_dogs'] += 1
        
        # Process non-dog images
        else:
            # Count correctly classified as non-dog
            if results_dic[key][4] == 0:
                results_stats_dic['n_correct_notdogs'] += 1
    
    # Calculate derived count
    results_stats_dic['n_notdogs_img'] = (
        results_stats_dic['n_images'] - results_stats_dic['n_dogs_img']
    )
    
    # Calculate percentage statistics with zero-division guards
    results_stats_dic['pct_match'] = (
        (results_stats_dic['n_match'] / results_stats_dic['n_images']) * 100.0
        if results_stats_dic['n_images'] > 0 else 0.0
    )
    
    results_stats_dic['pct_correct_dogs'] = (
        (results_stats_dic['n_correct_dogs'] / results_stats_dic['n_dogs_img']) * 100.0
        if results_stats_dic['n_dogs_img'] > 0 else 0.0
    )
    
    results_stats_dic['pct_correct_breed'] = (
        (results_stats_dic['n_correct_breed'] / results_stats_dic['n_dogs_img']) * 100.0
        if results_stats_dic['n_dogs_img'] > 0 else 0.0
    )
    
    results_stats_dic['pct_correct_notdogs'] = (
        (results_stats_dic['n_correct_notdogs'] / results_stats_dic['n_notdogs_img']) * 100.0
        if results_stats_dic['n_notdogs_img'] > 0 else 0.0
    )
    
    return results_stats_dic


# ==============================================================================
# USAGE NOTES:
# 
# These enhanced versions can replace the original files WITHOUT breaking
# Udacity grading scripts because:
#
# 1. Function signatures remain identical
# 2. Return types are unchanged
# 3. Logic is preserved exactly
# 4. Only additions are:
#    - Type hints (Python 3.5+ compatible, ignored by runtime)
#    - Comprehensive docstrings
#    - Better comments explaining WHY
#    - Helper functions for clarity
#
# To apply these enhancements:
# 1. Backup original files
# 2. Replace with enhanced versions
# 3. Run Udacity test suite to verify compatibility
# 4. Commit with message: "refactor: Add type hints and professional docstrings"
# ==============================================================================
