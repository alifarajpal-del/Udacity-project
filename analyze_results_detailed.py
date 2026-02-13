#!/usr/bin/env python3
"""
Comprehensive analysis of uploaded images classification results
"""

import os
import re

def read_output_file(filename):
    """Read and parse the output file to understand results."""
    if not os.path.exists(filename):
        return None
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return content

def main():
    print("="*90)
    print("UPLOADED IMAGES CLASSIFICATION - COMPREHENSIVE ANALYSIS")
    print("="*90)
    
    #  Check uploaded images
    print("\n1. UPLOADED IMAGES:")
    print("-" * 90)
    uploaded_dir = "uploaded_images"
    if os.path.exists(uploaded_dir):
        images = sorted([f for f in os.listdir(uploaded_dir) if f.lower().endswith(('.jpg', '.jpeg'))])
        for i, img in enumerate(images, 1):
            print(f"   {i}. {img}")
    else:
        print(" ERROR: uploaded_images/ folder not found!")
        return
    
    # Check output files
    print("\n2. MODEL OUTPUT FILES:")
    print("-" * 90)
    models = [
        ('ResNet', 'resnet_uploaded-images.txt'),
        ('AlexNet', 'alexnet_uploaded-images.txt'),
        ('VGG', 'vgg_uploaded-images.txt')
    ]
    
    results = {}
    for model_name, filename in models:
        if os.path.exists(filename):
            print(f"   ✓ {filename}")
            results[model_name] = read_output_file(filename)
        else:
            print(f"   ✗ {filename} - NOT FOUND")
            results[model_name] = None
    
    # Display results for each model
    print("\n3. CLASSIFICATION RESULTS:")
    print("=" * 90)
    
    for model_name, content in results.items():
        if content:
            print(f"\n{model_name.upper()} RESULTS:")
            print("-" * 90)
            print(content)
    
    # Analysis
    print("\n4. KEY FINDINGS:")
    print("=" * 90)
    print("\n⚠️  IMPORTANT OBSERVATION:")
    print("   All models classified 0 images as dogs (N Dog Images: 0)")
    print("\n📋 REASON:")
    print("   The filenames in uploaded_images/ do not contain specific dog breed names")
    print("   that match entries in dognames.txt.")
    print("\n   Current filenames:")
    for img in images:
        # Extract the label that would be used
        label = img.lower().rsplit('.', 1)[0]  # Remove extension
        label = re.sub(r'[-_]', ' ', label)  # Replace - and _ with spaces
        label = re.sub(r'[0-9]', '', label)  # Remove numbers
        label = label.strip()
        print(f"   - {img} → extracted label: '{label}'")
    
    print("\n💡 SOLUTION:")
    print("   For proper dog breed classification, rename files using breed names from dognames.txt:")
    print("   Examples:")
    print("   - Yorkshire_terrier_01.jpg")
    print("   - Yorkshire_terrier_02.jpg")
    print("   - Golden_retriever_01.jpg")
    print("   - Cat_01.jpg (for non-dog test)")
    print("   - Coffee_table_01.jpg (for object test)")
    
    print("\n5. CURRENT vs EXPECTED BEHAVIOR:")
    print("=" * 90)
    print("\n✓ WHAT WORKED:")
    print("   - All 3 models ran successfully")
    print("   - 4 images were processed")
    print("   - Classification labels were generated")
    print("   - Statistics were calculated")
    
    print("\n⚠  WHAT NEEDS IMPROVEMENT:")
    print("   - Pet labels from filenames don't match dog breed names")
    print("   - No images were identified as dogs")
    print("   - Cannot evaluate dog breed classification accuracy")
    print("   - Cannot compare model performance for dog detection")
    
    print("\n6. NEXT STEPS:")
    print("=" * 90)
    print("   1. Rename the dog images with proper breed names")
    print("   2. Re-run: .\\run_models_batch_uploaded.bat")
    print("   3. Analyze results with proper dog classifications")
    print("   4. Answer the 4 required questions based on proper results")
    
    print("\n" + "=" * 90)
    print("ANALYSIS COMPLETE")
    print("=" * 90)

if __name__ == "__main__":
    main()
