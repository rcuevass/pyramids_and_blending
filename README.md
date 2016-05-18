# GAUSSIAN AND LAPLACE PYRAMIDS AND BLENDING

## 1. General description

This repo contains code that exmplifies the implementation of Gaussian and Laplacian pyramids and how they are used for image blending. The scripts included here itend to show this by:

a. Exclusively using OpenCV
b. Implementing each algorithm from scratch


### 1a. Description: 

A squad of robotic rovers are to be landed by NASA on a plateau on Mars. This plateau, which is curiously rectangular, must be navigated by the rovers so that their on board cameras can get a complete view of the surrounding terrain to send back to Earth.

A rover’s position is represented by a combination of an x and y co-ordinates and a letter representing one of the four cardinal compass points. The plateau is divided up into a grid to simplify navigation. An example position might be
`0, 0, N` , which means the rover is in the bottom left corner and facing North.

In order to control a rover, NASA sends a simple string of letters. The possible letters are `L` , `R` and `M` . `L` and `R` makes the rover spin 90 degrees left or right respectively, without moving from its current spot. `M` means move forward one grid
point, and maintain the same heading. Assume that the square directly North from `(x,y)` is `(x,y+1)`.

### 1b. Input:

The problem below requires some kind of input. You are free to implement any mechanism for feeding input into your solution.
