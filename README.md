# GAUSSIAN AND LAPLACE PYRAMIDS AND BLENDING

## General description

This repo contains code that exmplifies the implementation of Gaussian and Laplacian pyramids and how they are used for image blending. The scripts included here itend to show this by exclusively using OpenCV and implementing each algorithm from scratch. The code is executed with `python main.py`

### 1. OpenCV libraries: 

The file `from_openCV.py` contains the module that exclusively uses OpenCV libraries for pyramid generation as well as blending. The sequences of images generated with this module can be found in [this link.] (https://github.com/rcuevass/pyramids_and_blending/tree/master/blend_openCV)

### 2. From-scratch library

The file `gauss_pyramid.py` contains the module that generates a Gaussian pyramid from scratch; OpenCV is only used to load/write images from/to file. The Gauss pyramid can be found in [this link.] (https://github.com/rcuevass/pyramids_and_blending/tree/master/gauss_scratch)


### 3. IPython notebook

The whole progress of this project can be found on the Jupyter notebook `pyramids_blending.ipynb`
