# Module that uses EXCLUSIVELY openCV
import from_openCV as fOCV
# Module written from scratch that generates gaussian pyramid
import gauss_pyramid as gaussPy


def main():

	# Generates different blendings using OpenCV libraries
	fOCV.makeSequenceBlends('apple.jpg','orange.jpg',8)

	# Generates gaussian pyramid using a module written from scratch
	gaussPy.reduceImageSequence('apple.jpg',7)

if __name__ == '__main__':
    main()
