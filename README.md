# GAUSSIAN AND LAPLACE PYRAMIDS AND BLENDING

## General description

This repo, **still in progress**,  contains code that exemplifies the implementation of Gaussian and Laplacian pyramids and how they are used for image blending. The scripts included here intend to show this by: 1. Exclusively using OpenCV and 2. Implementing each algorithm from scratch. 
The original images utlized for these tests can be found in the folder [images] (https://github.com/rcuevass/pyramids_and_blending/tree/master/images) of this repository. 
The code is executed with `python main.py`

### 1. OpenCV libraries: 

The file `from_openCV.py` contains the module that exclusively uses OpenCV libraries for pyramid generation as well as blending. The sequences of images generated with this module can be found in [this link.] (https://github.com/rcuevass/pyramids_and_blending/tree/master/blend_openCV)

### 2. From-scratch library

The file `gauss_pyramid.py` contains the module that generates a Gaussian pyramid from scratch; OpenCV is only used to load/write images from/to file. The Gauss pyramid can be found in [this link.] (https://github.com/rcuevass/pyramids_and_blending/tree/master/gauss_scratch) 
File `laplace_pyramid.py` contains module that generates a Laplacian pyramid fromscratch; OpenCV is only used to load/write images from/to file. The Laplacian pyramid can be found in [this link] (https://github.com/rcuevass/pyramids_and_blending/tree/master/laplace_scratch).

Blending function has **still to be implemented.**

#### 2a. Important notes

The function testConvIndx(wHat,yTest,indx) **clearly** needs to be improved. The current one is only for prototyping purposes and **huge** improvement upon it can still be done.

### 3. IPython notebook

The whole progress of this project can be found on the Jupyter notebook `pyramids_blending.ipynb`

### 4. References

The original paper on Laplacian pyramids can be fond in the [References] (https://github.com/rcuevass/pyramids_and_blending/tree/master/References) folder of this repo.
