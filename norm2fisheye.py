import cv2
import numpy as np
import time


def numpy_func(udst,vdst,w,h,rc,f0,fc):
    u,v = udst-rc ,vdst-rc
    r = np.sqrt(u**2+v**2)
    r0 = f0*np.tan(r/fc)
    p_theta = np.arctan2(u,v)
    x,y = r0*np.cos(p_theta),r0*np.sin(p_theta)
    x = x+w/2
    y = y+h/2
    return x,y

def norm2fisheye(img):
    f0 = 300 #f0 gets bigger, distortion gets smaller
    fc = 300 #fisheye focal length
    rc = fc+100 #image size
    w,h=img.shape[1],img.shape[0]
    u=v=np.linspace(0,2*rc,2*rc)
    udst,vdst = np.meshgrid(u,v)
    map_x,map_y = numpy_func(vdst,udst,w,h,rc,f0,fc)
    map_y = np.array(map_y,dtype=np.float32)
    map_x = np.array(map_x,dtype=np.float32)
    fimg = cv2.remap(img,map_x,map_y,cv2.INTER_LINEAR)
    return fimg
    

if __name__ == "__main__":
    start = time.time()
    img = cv2.imread("tuebingen00.png")
    fimg = norm2fisheye(img)
    end = time.time()
    print(f"spent:{end-start}s")
    # cv2.imwrite("out.png",fimg)
    cv2.imshow('',fimg)
    cv2.waitKey(3000)
