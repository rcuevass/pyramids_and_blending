# Module that uses EXCLUSIVELY openCV
import from_openCV as fOCV

# gauss_pyramid is a module written from scratch that generates gaussian pyramid
# only reduceImageSequence is invoked by main program
from gauss_pyramid import reduceImageSequence

# laplace_pyramid is a module written from scratch that generates gaussian pyramid
# only ImagesLaplPyramid is invoked by main program
from laplace_pyramid import ImagesLaplPyramid 


def main():

	# Generates different blendings using OpenCV libraries
	fOCV.makeSequenceBlends('apple.jpg','orange.jpg',8)

	# Generates gaussian pyramid using a module written from scratch
	reduceImageSequence('apple.jpg',7)

	# Generates laplacian pyramid using a module written from scratch
	ImagesLaplPyramid('apple.jpg',4)

if __name__ == '__main__':
    main()
