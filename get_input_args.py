"""
Module for parsing command-line arguments.
This module uses argparse to handle command-line arguments for the image
classification program.
"""

import argparse


def get_input_args():
    """
    Parses and returns command-line arguments.
    
    Creates an ArgumentParser object that accepts three command-line arguments:
    - --dir: Path to the folder of pet images (default: 'pet_images/')
    - --arch: CNN model architecture to use (default: 'resnet')
    - --dogfile: Text file containing valid dog names (default: 'dognames.txt')
    
    Returns:
        argparse.Namespace: An object containing the parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Image Classification for a City Dog Show'
    )
    
    parser.add_argument(
        '--dir',
        type=str,
        default='pet_images/',
        help='path to the folder of pet images'
    )
    
    parser.add_argument(
        '--arch',
        type=str,
        default='resnet',
        help='CNN model architecture to use: resnet, alexnet, or vgg'
    )
    
    parser.add_argument(
        '--dogfile',
        type=str,
        default='dognames.txt',
        help='text file that contains valid dog names'
    )
    
    return parser.parse_args()
