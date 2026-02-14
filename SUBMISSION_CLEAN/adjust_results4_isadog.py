"""
Module for adjusting classification results to classify labels as dogs or not dogs.
This module reads dog names from a file and updates results with dog classifications.
"""


def adjust_results4_isadog(results_dic, dogfile):
    """
    Adjusts results_dic to include whether pet and classifier labels are dogs.
    
    Reads dog names from dogfile and updates results_dic with two new values:
    - pet_is_dog: 1 if pet label is in dog names, 0 otherwise
    - classifier_is_dog: 1 if any dog name appears in classifier label, 0 otherwise
    
    Args:
        results_dic (dict): Dictionary with results from classification
        dogfile (str): Path to text file containing dog names (one per line)
    
    Returns:
        None (modifies results_dic in place)
    
    Side effects:
        Prints warning if duplicate dog names are found in dogfile.
        Updates each results_dic[filename] to include two new values:
        [pet_label, classifier_label, match, pet_is_dog, classifier_is_dog]
    """
    # Create dictionary of dog names from dogfile
    dognames_dic = {}
    
    # Read dogfile and populate dognames_dic
    with open(dogfile, 'r') as f:
        for line in f:
            dog_name = line.rstrip()
            if dog_name in dognames_dic:
                print(f"Warning: Dog name '{dog_name}' appears more than once in {dogfile}")
            dognames_dic[dog_name] = 1
    
    # Adjust results_dic for each image
    for filename in results_dic:
        # Extract existing values
        pet_label = results_dic[filename][0]
        classifier_label = results_dic[filename][1]
        
        # Determine if pet label is a dog
        pet_is_dog = 1 if pet_label in dognames_dic else 0
        
        # Determine if classifier label contains any dog name
        classifier_is_dog = 0
        for dog_name in dognames_dic:
            if dog_name in classifier_label:
                classifier_is_dog = 1
                break
        
        # Append both values to results_dic[filename]
        results_dic[filename].extend([pet_is_dog, classifier_is_dog])
