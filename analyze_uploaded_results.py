#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse Results Analyzer for Uploaded Images
Reads the output files from batch run and generates structured report
"""

import re
import os
from collections import defaultdict

def parse_results_file(filename):
    """
    Parse a results output file and extract classification results.
    
    Returns:
        dict: {image_filename: {pet_label, classifier_label, is_dog_truth, is_dog_pred, breed_match}}
    """
    results = {}
    
    if not os.path.exists(filename):
        print(f"WARNING: {filename} not found!")
        return results
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract image classification results
    # Look for patterns like: filename: Real: label  Classifier: label
    # Or parse the statistics section
    
    # Try to find individual image results
    lines = content.split('\n')
    
    current_image = None
    for i, line in enumerate(lines):
        # Look for image filename patterns
        if '.jpg' in line.lower() or '.jpeg' in line.lower():
            # Try to extract structured data
            # Pattern: might have Real: and Classifier: on same or nearby lines
            if 'Real:' in line and 'Classifier:' in line:
                # Parse format: Real: <label>   Classifier: <label>
                match = re.search(r'Real:\s+(\S+.*?)\s+Classifier:\s+(\S+.*?)(?:\s|$)', line)
                if match:
                    pet_label = match.group(1).strip()
                    classifier_label = match.group(2).strip()
                    
                    # Find filename in the line or previous lines
                    filename_match = re.search(r'([a-zA-Z0-9_-]+\.jpe?g)', line, re.IGNORECASE)
                    if filename_match:
                        img_name = filename_match.group(1)
                        results[img_name] = {
                            'pet_label': pet_label,
                            'classifier_label': classifier_label,
                            'is_dog_truth': None,
                            'is_dog_pred': None,
                            'breed_match': None
                        }
    
    return results


def analyze_model_results(model_name, filename):
    """
    Analyze results for a specific model.
    """
    print(f"\n{'='*80}")
    print(f"MODEL: {model_name.upper()}")
    print(f"{'='*80}")
    
    results = parse_results_file(filename)
    
    if not results:
        print(f"No results parsed from {filename}")
        return None
    
    # Print table
    print(f"\n{'Image':<25} {'Pet Label':<20} {'Classifier Label':<30}")
    print('-' * 80)
    
    for img, data in sorted(results.items()):
        print(f"{img:<25} {data['pet_label']:<20} {data['classifier_label']:<30}")
    
    return results


def answer_questions(resnet_results, alexnet_results, vgg_results):
    """
    Answer the 4 required questions based on parsed results.
    """
    print(f"\n\n{'='*80}")
    print("ANSWERS TO REQUIRED QUESTIONS")
    print(f"{'='*80}")
    
    # Find Dog_01.jpg results
    dog01_resnet = None
    dog01_alexnet = None
    dog01_vgg = None
    dog02_resnet = None
    dog02_alexnet = None
    dog02_vgg = None
    
    for key in resnet_results:
        if 'dog_01' in key.lower():
            dog01_resnet = resnet_results[key]
        if 'dog_02' in key.lower():
            dog02_resnet = resnet_results[key]
    
    for key in alexnet_results:
        if 'dog_01' in key.lower():
            dog01_alexnet = alexnet_results[key]
        if 'dog_02' in key.lower():
            dog02_alexnet = alexnet_results[key]
    
    for key in vgg_results:
        if 'dog_01' in key.lower():
            dog01_vgg = vgg_results[key]
        if 'dog_02' in key.lower():
            dog02_vgg = vgg_results[key]
    
    # Q1: Do the 3 models classify Dog_01 as the same breed?
    print("\n" + "Q1: Did the three models classify Dog_01 as the same breed?")
    print("-" * 80)
    if dog01_resnet and dog01_alexnet and dog01_vgg:
        resnet_breed = dog01_resnet['classifier_label']
        alexnet_breed = dog01_alexnet['classifier_label']
        vgg_breed = dog01_vgg['classifier_label']
        
        print(f"  ResNet:  {resnet_breed}")
        print(f"  AlexNet: {alexnet_breed}")
        print(f"  VGG:     {vgg_breed}")
        
        if resnet_breed == alexnet_breed == vgg_breed:
            print(f"  ✓ YES - All three models classified Dog_01 as: {resnet_breed}")
        else:
            print(f"  ✗ NO - Models classified Dog_01 differently")
    else:
        print("  ⚠ Dog_01.jpg not found in results")
    
    # Q2: For each model, did Dog_01 and Dog_02 get the same breed?
    print("\n" + "Q2: For each model, did Dog_01 and Dog_02 get the same breed?")
    print("-" * 80)
    
    if dog01_resnet and dog02_resnet:
        match = dog01_resnet['classifier_label'] == dog02_resnet['classifier_label']
        print(f"  ResNet:  Dog_01={dog01_resnet['classifier_label']}, Dog_02={dog02_resnet['classifier_label']}")
        print(f"           {'✓ MATCH' if match else '✗ DIFFERENT'}")
    
    if dog01_alexnet and dog02_alexnet:
        match = dog01_alexnet['classifier_label'] == dog02_alexnet['classifier_label']
        print(f"  AlexNet: Dog_01={dog01_alexnet['classifier_label']}, Dog_02={dog02_alexnet['classifier_label']}")
        print(f"           {'✓ MATCH' if match else '✗ DIFFERENT'}")
    
    if dog01_vgg and dog02_vgg:
        match = dog01_vgg['classifier_label'] == dog02_vgg['classifier_label']
        print(f"  VGG:     Dog_01={dog01_vgg['classifier_label']}, Dog_02={dog02_vgg['classifier_label']}")
        print(f"           {'✓ MATCH' if match else '✗ DIFFERENT'}")
    
    # Q3: Did models correctly classify Animal_* and Object_* as NOT dogs?
    print("\n" + "Q3: Did models correctly classify Animal_* and Object_* as NOT dogs?")
    print("-" * 80)
    print("  (Analysis based on classifier labels containing 'dog' keyword)")
    
    for results, model_name in [(resnet_results, 'ResNet'), (alexnet_results, 'AlexNet'), (vgg_results, 'VGG')]:
        print(f"\n  {model_name}:")
        for img, data in results.items():
            if 'animal' in img.lower() or 'object' in img.lower():
                has_dog = 'dog' in data['classifier_label'].lower()
                status = '✗ MISCLASSIFIED as dog' if has_dog else '✓ Correctly NOT a dog'
                print(f"    {img}: {data['classifier_label']} - {status}")
    
    # Q4: Select best model
    print("\n" + "Q4: Which model performed best on uploaded images?")
    print("-" * 80)
    print("  Based on analysis:")
    print("  - Breed accuracy for dog images")
    print("  - Correct dog/not-dog classification")
    print("  - Consistency between similar images (Dog_01 vs Dog_02)")
    print("\n  RECOMMENDATION: [To be determined based on actual results above]")
    print("  The best model should:")
    print("    1. Correctly identify dogs as dogs")
    print("    2. Correctly identify non-dogs as non-dogs")
    print("    3. Provide consistent breed classifications")


def main():
    """Main execution function."""
    print("="*80)
    print("UPLOADED IMAGES CLASSIFICATION ANALYSIS")
    print("="*80)
    
    # Step 1: Check for uploaded images
    print("\nSTEP 1: Checking uploaded_images folder...")
    uploaded_dir = "uploaded_images"
    
    if os.path.exists(uploaded_dir):
        images = [f for f in os.listdir(uploaded_dir) if f.lower().endswith(('.jpg', '.jpeg'))]
        print(f"✓ Found {len(images)} image(s) in {uploaded_dir}/")
        for img in sorted(images):
            print(f"  - {img}")
        
        if len(images) != 4:
            print(f"  ⚠ WARNING: Expected 4 images but found {len(images)}")
    else:
        print(f"✗ {uploaded_dir}/ folder not found!")
        return
    
    # Step 2: Check for output files
    print("\nSTEP 2: Checking for model output files...")
    output_files = [
        ('resnet', 'resnet_uploaded-images.txt'),
        ('alexnet', 'alexnet_uploaded-images.txt'),
        ('vgg', 'vgg_uploaded-images.txt')
    ]
    
    missing = []
    for model, fname in output_files:
        if os.path.exists(fname):
            print(f"✓ {fname}")
        else:
            print(f"✗ {fname} - NOT FOUND")
            missing.append(fname)
    
    if missing:
        print(f"\n⚠ Missing output files. Run: run_models_batch_uploaded.bat")
        return
    
    # Step 3: Parse results
    print("\nSTEP 3: Parsing model results...")
    
    resnet_results = analyze_model_results('ResNet', 'resnet_uploaded-images.txt')
    alexnet_results = analyze_model_results('AlexNet', 'alexnet_uploaded-images.txt')
    vgg_results = analyze_model_results('VGG', 'vgg_uploaded-images.txt')
    
    # Step 4: Answer questions
    if resnet_results or alexnet_results or vgg_results:
        answer_questions(resnet_results or {}, alexnet_results or {}, vgg_results or {})
    else:
        print("\n✗ No results could be parsed from output files")
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()
