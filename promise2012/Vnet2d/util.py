import SimpleITK as sitk
import numpy as np
import cv2

'''
This funciton reads a '.mhd' file using SimpleITK and return the image array, origin and spacing of the image.
read_Image_mask fucntion get image and mask
'''


def load_itk(filename):
    # Reads the image using SimpleITK
    itkimage = sitk.ReadImage(filename)
    # Convert the image to a  numpy array first and then shuffle the dimensions to get axis in the order z,y,x
    ct_scan = sitk.GetArrayFromImage(itkimage)
    # Read the origin of the ct_scan, will be used to convert the coordinates from world to voxel and vice versa.
    origin = np.array(itkimage.GetOrigin())
    # Read the spacing along each dimension
    spacing = np.array(itkimage.GetSpacing())
    return ct_scan, origin, spacing


def read_Image_mask(filespath, outpath, ind=4):
    number = 0
    for index in range(ind):
        for i in range(10):
            if ind == 1:
                imgs, ori, spac = load_itk(filespath + 'Case' + str(index) + str(i) + '.mhd')
                masks, maskori, maskspac = load_itk(filespath + 'Case' + str(index) + str(i) + '_segmentation.mhd')
            else:
                imgs, ori, spac = load_itk(filespath + 'Case' + str(index + 1) + str(i) + '.mhd')
                masks, maskori, maskspac = load_itk(filespath + 'Case' + str(index + 1) + str(i) + '_segmentation.mhd')
            maxvalue, minvalue = np.max(imgs), np.min(imgs)
            imgs = imgs.astype(np.float32)
            imgs = (imgs - minvalue) / (maxvalue - minvalue)
            imgs = imgs * 255.
            imgs = imgs.astype(np.uint8)

            maxmaskvalue, minmaskvalue = np.max(masks), np.min(masks)
            masks = masks.astype(np.float32)
            masks = (masks - minmaskvalue) / (maxmaskvalue - minmaskvalue)
            masks = masks * 255.
            masks = masks.astype(np.uint8)
            for x in range(np.shape(masks)[0]):
                if np.max(masks[x]) == 255:
                    cv2.imwrite(outpath + 'Image\\' + str(number + 1) + '.bmp', cv2.resize(imgs[x], (512, 512)))
                    cv2.imwrite(outpath + 'Mask\\' + str(number + 1) + '.bmp', cv2.resize(masks[x], (512, 512)))
                    number = number + 1


read_Image_mask(filespath='D:\Data\PROMISE2012\\train\\', outpath='D:\Data\PROMISE2012\\train_Vnet\\')
read_Image_mask(filespath='D:\Data\PROMISE2012\\test\\', outpath='D:\Data\PROMISE2012\\test_Vnet\\', ind=1)
