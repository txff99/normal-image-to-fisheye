import cv2
import numpy as np
import time
import sys
np.set_printoptions(threshold=sys.maxsize)

def numpy_func(udst,vdst,w,h,rc,f0,fc,gamma):
    v,u = udst-1.65*rc ,vdst-rc #image position
    # rotate the sphere
    r1 = np.sqrt(fc**2-u**2)
    yc = r1*np.cos(np.arccos(v/r1)+gamma)
    # convert the proxy to raw image
    r = np.sqrt(u**2+yc**2)
    r0 = f0*np.tan(np.arcsin(r/fc))
    p_theta = np.arctan2(yc,u)
    x,y = r0*np.cos(p_theta),r0*np.sin(p_theta)
    x = x+w/2
    y = y+h/2
    return x,y

def norm2fisheye(img):
    gamma = -0.6 #angle of fisheye camera
    f0 = 1400 #f0 gets bigger, distortion gets smaller
    fc = 600 #fisheye focal length
    rc = int(0.65*fc) #image size
    # rc = fc
    w,h=img.shape[1],img.shape[0]
    u=v=np.linspace(0,2*rc,2*rc)
    udst,vdst = np.meshgrid(u,v)
    map_x,map_y = numpy_func(vdst,udst,w,h,rc,f0,fc,gamma)
 
    map_y = np.array(map_y,dtype=np.float32)
    map_x = np.array(map_x,dtype=np.float32)
    fimg = cv2.remap(img,map_x,map_y,cv2.INTER_LINEAR)
    return fimg
    

if __name__ == "__main__":
    start = time.time()
    img = cv2.imread("koeln00.png")
    fimg = norm2fisheye(img)
    end = time.time()
    print(f"spent:{end-start}s")
    cv2.imwrite("out.png",fimg)
    cv2.imshow('',fimg)
    cv2.waitKey(5000)
