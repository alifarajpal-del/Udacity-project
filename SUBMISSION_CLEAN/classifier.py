#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# */AIPND-revision/intropyproject-classify-pet-images/classifier.py
#
# PROGRAMMER: Jennifer S. (Udacity Instructor)
# DATE CREATED: 02/20/2018
# REVISED DATE: 02/27/2018 - added try/except to handle PyTorch problems
# PURPOSE: Classifies pet images using a pretrained CNN model, compares labels,
#          and creates a dictionary of results (text and statistics)
#
##

import ast
from PIL import Image
import torchvision.transforms as transforms
from torch.autograd import Variable
import torchvision.models as models
from torch import __version__


# obtain ImageNet labels - this only needs to be done once
with open('imagenet1000_clsid_to_human.txt') as imagenet_classes_file:
    imagenet_classes_dict = ast.literal_eval(imagenet_classes_file.read())


def classifier(img_path, model_name):
    """
    Classifies images using a pretrained CNN model.
    
    Parameters:
        img_path - path to the image file (str)
        model_name - CNN model architecture to use for classification. 
                     Must be one of: resnet, alexnet, vgg (str)
    Returns:
        breed - The classifier label as a string
    """
    # check model name is one we can use
    if model_name not in ['resnet', 'alexnet', 'vgg']:
        print("Model name '{}' not recognized. Acceptable values: resnet, alexnet, vgg".format(model_name))
        return None
    
    # Load ONLY the requested model (lazy loading)
    if model_name == 'resnet':
        model = models.resnet18(pretrained=True)
    elif model_name == 'alexnet':
        model = models.alexnet(pretrained=True)
    elif model_name == 'vgg':
        model = models.vgg16(pretrained=True)
    
    # Set model to evaluation mode
    model.eval()
    
    # Process image
    img = Image.open(img_path)
    
    # Image preprocessing
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                           std=[0.229, 0.224, 0.225])
    ])
    
    img_tensor = preprocess(img)
    img_tensor.unsqueeze_(0)
    
    # PyTorch pretrained models require the data type to be a variable
    pytorch_ver = __version__.split('.')
    
    # Check for version 0.4.0 or higher
    if int(pytorch_ver[0]) > 0 or int(pytorch_ver[1]) >= 4:
        img_tensor = img_tensor
    else:
        # Older PyTorch versions
        data = Variable(img_tensor, volatile=True) if pytorch_ver[0] < '0.4.0' else Variable(img_tensor)
        img_tensor = data
    
    # Apply model to get predictions
    output = model(img_tensor)
    
    # Get the predicted label
    pred_idx = output.data.numpy().argmax()
    
    return imagenet_classes_dict[pred_idx]
