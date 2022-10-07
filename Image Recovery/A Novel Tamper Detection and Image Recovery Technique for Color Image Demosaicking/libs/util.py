import imageio
import numpy as np
import cv2

def readImg(image_path, flags=3): 
    tmp = imageio.mimread(image_path)
    if tmp is None:
        return None
    imt = np.array(tmp)
    imt = imt[0]
    if imt.ndim == 3 and flags is not -1:
        im = imt[:, :, 0:3]
    else:
        im = imt
    return im

def mse(imageA, imageB):
	err = np.sum((imageA.astype("float64") - imageB.astype("float64")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	return err

def psnr(imageA, imageB):
    return cv2.PSNR(imageA, imageB)