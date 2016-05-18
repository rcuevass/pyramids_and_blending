# GAUSSIAN AND LAPLACE PYRAMIDS AND BLENDING

## General description

This repo contains code that exmplifies the implementation of Gaussian and Laplacian pyramids and how they are used for image blending. The scripts included here itend to show this by exclusively using OpenCV and implementing each algorithm from scratch. The code is executed with `python main.py`

### 1. OpenCV libraries: 

The file `from_openCV.py` contains the module that exclusively uses OpenCV libraries for pyramid generation as well as blending. The sequences of images generated with this module can be found in [this link] (https://github.com/rcuevass/pyramids_and_blending/tree/master/blend_openCV)

A rover’s position is represented by a combination of an x and y co-ordinates and a letter representing one of the four cardinal compass points. The plateau is divided up into a grid to simplify navigation. An example position might be
`0, 0, N` , which means the rover is in the bottom left corner and facing North.

In order to control a rover, NASA sends a simple string of letters. The possible letters are `L` , `R` and `M` . `L` and `R` makes the rover spin 90 degrees left or right respectively, without moving from its current spot. `M` means move forward one grid
point, and maintain the same heading. Assume that the square directly North from `(x,y)` is `(x,y+1)`.

### 1b. Input:

The problem below requires some kind of input. You are free to implement any mechanism for feeding input into your solution.
