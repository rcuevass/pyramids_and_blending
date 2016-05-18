import cv2
import numpy as np,sys
import os
import math as mt


"""
This module generates pyramids of images for the purpose of image blending. 
The process of generating the pyramids and blending is exeplored using OpenCV exclusively
"""


def get_GaussPyrimid(name,times):
    """
    Function that reduces a given image certain number of times
    name: name of file containing the image
    times: number of times the image will be reduced
    """
    # Read image from file using OpenCV
    img = cv2.imread(name)
    # Create a list of images that initially contains only the original
    # image
    gaussPy = [img]
    # We reduce the image as many times as the user has requested
    for _ in range(times):
        # Notice we updated img every time with the new reduced image...
        img = cv2.pyrDown(img)
        # ... and append to the list of images
        gaussPy.append(img)
    return gaussPy



def get_GaussPyrimids(name1,name2,size):
    """
    Function that reduces two images certain number of times
    name1, name2: names of files containing the images
    times: number of times the image will be reduced
    """
    # Read images from corresponding files
    img1 = cv2.imread(name1); img2 = cv2.imread(name2)
    # Initialize two lists with corresponding images
    gaussPy1 = [img1]; gaussPy2 = [img2]
    # We reduce the image as many times as the user has requested ... 
    for _ in range(size):
        # ... and append to the lists, respectively
        img1 = cv2.pyrDown(img1); gaussPy1.append(img1)
        img2 = cv2.pyrDown(img2); gaussPy2.append(img2)
    return gaussPy1,gaussPy2


def get_LaplacePyramid(name1,name2,size):
    """
    Function that creates Laplacian pyramids of two images
    name1, name2: names of files containing the images
    size: number of levels in the lapalacian pyramid
    """
    # We first get the gaussian pyramids of each image. Notice 
    # the function written before is invoked here
    gaussPy1,gaussPy2 = get_GaussPyrimids(name1,name2,size)
    # We create a list of Laplacian pyramids; we initialize each list 
    # with the deeper level (smallest image) of each Gaussian pyramid
    Lapl1 = [gaussPy1[size]]; Lapl2 = [gaussPy2[size]]
    # We loop over each element of the Gaussian pyramid. Notice the 
    # looping begins with the smallest image in the Gaussian pyramid 
    # (deepest level)
    # For each element of the Gaussian pyramid...
    for k in range(size,0,-1):
        # Increase size of images in turn...
        G1 = cv2.pyrUp(gaussPy1[k]); G2 = cv2.pyrUp(gaussPy2[k])
        #print G1.shape, G2.shape
        # ... take respective differences with images in turn ...
        L1 = cv2.subtract(gaussPy1[k-1],G1); L2 = cv2.subtract(gaussPy2[k-1],G2)
        # ... and append to the list of Laplacian pyramids
        #print k , L1.shape, L2.shape
        Lapl1.append(L1); Lapl2.append(L2)
    return Lapl1,Lapl2


def blendImages(name1,name2,name_blend,size):
    """
    This function genearated the blending of two images.
    The blending takes place the middle part of each image
    name1, name2: files' names containing images
    name_blend: name of file containing the blended image
    size: size of pyramids (number of levels in pyramids) generated
          to do the blending
    """
    # Get Laplacian pyramids
    lpA,lpB = get_LaplacePyramid(name1,name2,size)
    # We intialize an empty list of images
    list_img = []
    # For each tuple in the cartesian product of Laplacian pyramids...
    for la,lb in zip(lpA,lpB):
         #row,col,dpt = la.shape
        # We get dimension of element of Laplacian pyramid in turn ...
        row,col = la.shape[:2]
        # ... grab the left and right halves of corresponding elements...
        left_img = la[:,0:col/2]; right_img = lb[:,col/2:]
        # ... stack them horizontally to do sewing ...
        ls = np.hstack((left_img,right_img))
        # ... append the recently sewed image
        list_img.append(ls)
    # We get the first element of sewed images... 
    ls_ = list_img[0]
    # ... and for the remaining elements in chaing of sewed images...
    for item in list_img[1:]:
        # ... increase the size ...
        ls_ = cv2.pyrUp(ls_)
        # ... and add it to the element in turn..
        ls_ = cv2.add(ls_,item)
            
    cv2.imwrite(name_blend,ls_)



def makeSequenceBlends(name1,name2,max_size):
    """
    Function that generates a sequence of blended images
    name1, name2: names of files containing the images to be blended
    max_size: maximum size of pyramids genereted for blending
    """
    # For all levels of blending ...
    for size in range(max_size):
        # Generate name of file containing blended image in turn
        output_name = 'blend_0'+ str(size) +'.jpg'
        # Show name of file on screen...
        print output_name
        # ... and perform the blending itself
        blendImages(name1,name2,output_name,size)



