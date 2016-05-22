import cv2
import numpy as np
import utilities as util
from gauss_pyramid import MatrixGaussPyramid 
import math as mt

"""
This module generates a Laplacian pyramid from scratch. OpenCV is only used
to load/write images from/to file.
"""

# Needs improvement

def testConvIndx(wHat,yTest,indx):
    """
    This function finds the ith component of the extended vector that resuluts from convoluting
    yTest with kernel wHat
    wHat: kernel
    yTest: Vector to be extended
    indx: component of resulting extended vector
    returns: ith component of extended vector resulting from the convolution wHat*yTest
    """
    if len(yTest)%2==0:
        max_ = len(yTest) + 1
    else:
        max_ = len(yTest)
    
    yExtended = np.insert(yTest,[i for i in range(1,max_)],0)
    
    if indx == 0:
        yReduced = yExtended[:3]
        wPrime = [0 if yReduced[i]==0 else wHat[i+2] for i in range(len(yReduced))]
        wPrime = wPrime/sum(wPrime)
        return np.dot(wPrime,yReduced)
    
    if indx == 1:
        yReduced = yExtended[:4]
        wPrime = [0 if yReduced[i]==0 else wHat[i+1] for i in range(len(yReduced))]
        wPrime = wPrime/sum(wPrime)
        return np.dot(wPrime,yReduced)
    
    
    if (indx>=2) and (indx<=(len(yExtended))-3):
        yReduced = yExtended[indx-2:indx+3]
        wPrime = [0 if yReduced[i]==0 else wHat[i] for i in range(len(yReduced))]
        wPrime = wPrime/sum(wPrime)
        return round(np.dot(wPrime,yReduced),1)
    
        
    if indx == len(yExtended)- 2:
        yReduced = yExtended[len(yExtended)-4:]
        wPrime = [0 if yReduced[i]==0 else wHat[len(wHat)-1-i] for i in range(len(yReduced))]
        wPrime = wPrime/sum(wPrime)
        return np.dot(wPrime,yReduced)
        
    if indx == len(yExtended)- 1:
        yReduced = yExtended[len(yExtended)-3:]
        wPrime = [0 if yReduced[i]==0 else wHat[len(wHat)-1-i] for i in range(len(yReduced))]
        wPrime = wPrime/sum(wPrime)
        return np.dot(wPrime,yReduced)



def extendVect(yTest,wHat):
    """
    Function that determines the vector resulting from the convolution of yTest and wHat
    yTest: vector to be extended
    wHat: kernel vector
    returns: vector resulting from the convolution yTest*wHat
    """
    # Since the size of the image is given by 2^N + 1  or 2^N we find the power N
    len_ = int(mt.floor(mt.log(len(yTest),2)))
    # According to the oddity of length of the image we extend it by changing 
    # the power from N to N + 1
    if len(yTest)%2 == 0:
        len_ = 2**(len_+1)
    else:
        len_ = (2**(len_+1)) + 1
    # Set a list of the resulting dimension 2^(N+1) + 1
    xOut = [0]*len_
    # We compute every component of the convolution...
    for i in range(len_):
        # ... and store it in the recently created list
        xOut[i] = testConvIndx(wHat,yTest,i)
    # Return list turned into a np array
    return np.array(xOut)


def convExpandMatrix(A,wHat):
    """
    This function extends the capabilities of extendVect(yTest,wHat) to
    make it useful for matrices 
    A: image matrix to be reduced
    wHat: kernel to perform the convolution
    returns: matrix representing the extended image
    NOTE. This function assumes the matrix A is two-dimensional
    """
    # We get number of rows and columns of given matrix A ...
    rowsA,colsA = A.shape[:2]
    # Extend the dimensions accordingly ...
    finalRows = util.incrDim(rowsA); finalCols = util.incrDim(colsA)
    # ... and set a matrix of zeros with the same shape
    Afinal = np.ones((finalRows,finalCols))

    # WE FIRST CONVOLUTE ROWS:
    for k in range(rowsA):
        # Get the row in turn and store temporarily ...
        vec_ =  np.array(A[k,:])
        # ... to convolute with kernel and store result in row of extended matrix
        Afinal[k,:] = extendVect(vec_,wHat)
    
    # Introduce an auxiliary intermediate matrix 
    Ainter = Afinal[:rowsA,:finalCols]
        
    
    # WE NOW CONVOLUTE COLUMNS:
    for k in range(finalCols):
        # We proceed in a similar fashion as before, this time 
        # using columns of the resulting matrix Afinal
        vec_ = np.array(Ainter[:rowsA,k])
        Afinal[:,k] = extendVect(vec_,wHat)
            
    return Afinal


def LaplPyr3D(A,a_):
    """
    This function uses the previosuly implemented function, convExpandMatrix(A,wHat),
    to apply it to a three-dimensional matrix as the ones provided by OpenCV.
    Remember that the third index in matrix A is related with BGR of the pixel (x,y)
    A: three-dimensional matrix representation of an image
    a_: Parameter that uniquely defines the kernel
    returns: three-dimensional matrix representing reduced image
    """
    # The kernel is defined
    wHat = np.array([0.25 - (a_/2),0.25,a_,0.25,0.25-(a_/2)])
   
    # Apply the "two-dimensional" function to the "B" color, index 0
    auxL = convExpandMatrix(A[:,:,0],wHat)
    
    # Get shape of resulting matrix and set a three-dimensional
    # matrix of zeros accordingly
    rows,cols = auxL.shape
    Afin = np.zeros((rows,cols,3))
    # Store result in the corresponding "B" color of reduced matrix
    Afin[:,:,0] = auxL
    # Repeat the same process but this time for "G" and "R" color indices
    for k in range(1,3):
        auxL = convExpandMatrix(A[:,:,k],wHat)
        Afin[:,:,k] = auxL
    return Afin



def LapPyr(name,a_,size):
    """
    This function generates a Laplacian pyramid of an image accesed by the name of file containing it
    name: name of file containing image
    a_: parameter that defines kernel
    size: size of pyramid; number of levels in pyramid
    """
    # Get gaussian pyramid
    GPyr = MatrixGaussPyramid(name,a_,size+1)
    # Initialize list that will contain laplacian pyramid as an empty list
    Lapl = []
    # Loop over all levels in pyramid...
    for k in range(size+1,0,-1):
        # ... and get the level in turn as the difference between two consecutive Gaussian pyramids ...
        aux_ = GPyr[k-1] - LaplPyr3D(GPyr[k],a_)
        # ... and append it to the list 
        Lapl.append(aux_)
    return Lapl



def ImagesLaplPyramid(name,size):
    # Set parameter for kernel
    a_ = 0.4
    # Generate the list containing Laplacian pyramid...
    lapPyr = LapPyr(name,a_,size)
    # ... and save each imagein list to file 
    for k in range(len(lapPyr)):
        name_ = 'Laplace_0' + str(k) + '.jpg'
        print name_
        cv2.imwrite(name_,lapPyr[k])
