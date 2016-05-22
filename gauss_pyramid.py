import cv2
import numpy as np

"""
This module generates a Gaussian pyramid from scratch. OpenCV is only used
to load/write images from/to file.
"""

def convPyrA(xTest,wHat):
    """
    Function that performs convolution of a vector with a separable matrix
    xTest: input vector to be convoluted
    wHat: kernel used for convolution
    returns: reduced vector resulting from convolution
    """
    
    # We find the length of resulting convoluted vector according to the
    # lenght of input vector
    if len(xTest)%2 == 0:
        len_ = len(xTest)//2
    else:
        len_ = (len(xTest)//2) + 1
    
    # Set list of zeros with dimension of the resulting vector
    xReduced = [0]*len_
    
    # We first deal with all the entries in the resulting vector that 
    # are NOT the edges
    for i in range(1,len_-1):
        # Subset the input vector according the index of the convoluted
        # vector to be computed and store it in aux_
        # Keep in mind that:
        # a. The ith index of the resulting vector corresponds
        #    to the index 2i of the original vector
        # b. The ith position of resulting vector is the center and
        #    we need to collect two elements before and after the center
        #    This is [i-2,i-1,i,i+1,i+2]
        # c. In order to grab the last element we need to add 1 to the last
        #    index. This is why in the following line we have 3 = 2 + 1
        aux_ = np.array(xTest[2*i - 2 : 2*i + 3])
        # Peform the inner product of kernel with the recently obtained
        # aux_ vector to find the convolution
        xReduced[i] = np.dot(aux_,wHat)
    # We now need to take care of the edges
    # For the first cell (index zero in Python)
    # As before, we need to add 1 at the last index to ensure we are 
    # getting the last element of array: 3 = 2 + 1
    aux_ = np.array(xTest[:3])
    # For the edges the kernel has to be reduced in order to have overlap
    # with the vector; we collect the "right-hand side" of kernel
    # and store it auxiliary variable
    wAux = np.array(wHat[2:])
    # Perform inner product for convultion and correct result 
    # to ensure our reduced kernel was normalized
    xReduced[0] = np.dot(wAux,aux_)/sum(wAux)
    # We proceed in a similar fashion for last index
    aux_ = np.array(xTest[len(xTest)-3:])
    # This time the kernel is same as before but in opposite order, [::-1]
    wAux = wAux[::-1]
    # As before, we compute inner product for convolution and normalize
    # kernel
    xReduced[len_-1] = np.dot(wAux,aux_)/sum(wAux)
    
    return np.array(xReduced)
    


def convPyrMatrix(A,wHat):
    """
    This function extends the capabilities of convPyrA(xTest,wHat) to
    make it useful for matrices 
    A: image matrix to be reduced
    wHat: kernel to perform the convolution
    returns: matrix representing the reduced image
    NOTE. This function assumes the matrix A is two-dimensional
    """
    # We get number of rows and columns of given matrix A ...
    rowsA,colsA = A.shape[:2]
    # ... and set a matrix of zeros with the same shape
    Afinal = np.zeros((rowsA,colsA))

    # WE FIRST CONVOLUTE ROWS:
    for k in range(rowsA):
        # Get the row in turn and store temporarily ...
        vec_ =  np.array(A[k,:])
        # ... to convolute with kernel. Store result in temp. variable
        aux_ = convPyrA(vec_,wHat)
        # Determine length of resulting convolution and store 
        # result in corresponding section of output matrix
        rowsAux =  aux_.shape[0]
        Afinal[k,:rowsAux] = aux_
        
    #lenA = Afinal.shape[1]
    # WE NOW CONVOLUTE COLUMNS:
    for k in range(rowsAux):
        # We proceed in a similar fashion as before, this time 
        # using columns of the resulting matrix Afinal
        vec_ = np.array(Afinal[:,k])
        aux_ = convPyrA(vec_,wHat)
        colsAux =  aux_.shape[0]
        Afinal[:colsAux,k] = aux_
            
    return Afinal[:rowsAux,:colsAux]


def GaussPyr3D(A,a_):
    """
    This function uses the previosuly implemented function, convPyrMatrix(A,wHat),
    to apply it to a three-dimensional matrix as the ones provided by OpenCV.
    Remember that the third index in matrix A is related with BGR of the pixel (x,y)
    A: three-dimensional matrix representation of an image
    a_: Parameter that uniquely defines the kernel
    returns: three-dimensional matrix representing reduced image
    """
    # The kernel is defined
    wHat = np.array([0.25 - (a_/2),0.25,a_,0.25,0.25-(a_/2)])
    #aux = aApple[:,:,0]
    
    # Apply the "two-dimensional" function to the "B" color, index 0
    aux = convPyrMatrix(A[:,:,0],wHat)
    # Get shape of resulting matrix and set a three-dimensional
    # matrix of zeros accordingly
    rows,cols = aux.shape
    Afin = np.zeros((rows,cols,3))
    # Store result in the corresponding "B" color of reduced matrix
    Afin[:,:,0] = aux
    # Repeat the same process but this time for "G" and "R" color indices
    for k in range(1,3):
        aux = convPyrMatrix(A[:,:,k],wHat)
        Afin[:,:,k] = aux
    return Afin


def MatrixGaussPyramid(name,a_,size):
    """
    Function that generates a list containing a Gaussian pyramid from the name of the file containing 
    the image
    name: name of file containing image
    a_: parameter that determines kernel
    size: size of pyramid; number of levels in pyramid
    """
    # Get matrix of image from its file
    Aimg = cv2.imread(name)
    # Initialize list with original image
    GaussPyr = [Aimg]
    # Iterate to determine gaussian pyramid..
    for k in range(size):
        Aimg = GaussPyr3D(Aimg,a_)
        GaussPyr.append(Aimg)
    return GaussPyr


def reduceImage(name_input,name_output):
    """
    Function that takes an image and reduces it by colvolution
    name_input: name if image to be reduced
    name_output: name of resulting image
    returns: None, but saves to file the resulting image
    """
    # Set "customary" value of parameter for kernel
    a_ = 0.4
    # Load matrix corresponding to original image
    Ainput = cv2.imread(name_input)
    # Apply the reduce function to matrix...
    Aoutput = GaussPyr3D(Ainput,a_)
    # ... and save it to file with chose name
    cv2.imwrite(name_output,Aoutput)



def reduceImageSequence(name_input,size):
    """
    This function generates a sequence of reduced images
    name_input: name of original image
    size: size of Gaussian pyramid; number of times the image will be reduced
    returns: none, but writes each image of sequence to file
    """
    # Set value of parameter for kernel
    a_ = 0.4
    # Load matrix corresponding to image
    Aimg = cv2.imread(name_input)
    # For every level in pyramid...
    for k in range(size):
        # Set the name of file...
        name_output = 'reduced_0' + str(k) + '.jpg' 
        # and write to file
        cv2.imwrite(name_output,Aimg)
        print "Image " , name_output , "with size ", Aimg.shape[:2] ,"has been created"
        # reduce matrix
        Aimg = GaussPyr3D(Aimg,a_)