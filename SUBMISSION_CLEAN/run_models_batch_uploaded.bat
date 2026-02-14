@echo off
echo Running ResNet model on uploaded images...
C:/Users/PH-User/Udacity-project/.venv/Scripts/python.exe check_images.py --dir uploaded_images/ --arch resnet --dogfile dognames.txt > resnet_uploaded-images.txt

echo Running AlexNet model on uploaded images...
C:/Users/PH-User/Udacity-project/.venv/Scripts/python.exe check_images.py --dir uploaded_images/ --arch alexnet --dogfile dognames.txt > alexnet_uploaded-images.txt

echo Running VGG model on uploaded images...
C:/Users/PH-User/Udacity-project/.venv/Scripts/python.exe check_images.py --dir uploaded_images/ --arch vgg --dogfile dognames.txt > vgg_uploaded-images.txt

echo.
echo All models completed. Output files created:
echo - resnet_uploaded-images.txt
echo - alexnet_uploaded-images.txt
echo - vgg_uploaded-images.txt
echo.
pause
