import cv2
import numpy as np
import time
import sys
import tkinter as tk

# np.set_printoptions(threshold=sys.maxsize)

class fisheye(object):
    def __init__(self,img) -> None:
        self.img = img 
        self.fimg = None
        para = []
        # try:
        #     with open("data.txt","a") as f:
        #         f.readline()
        # except:
        #     print("no exiting para.txt")
        # else:
        self.pitch = -0.6 
        self.f0 = 1400
        self.fc = 600
        self.position_y = 1.5
        self.position_x = 1
        self.size_x = 400
        self.size_y = 400



    def adjust(self):
       
        win =tk.Tk()
        win.title("make your ideal fisheye image!")
        win.geometry('400x500')

        def show_img():
            if self.fimg is None:
                pass
            else:
                cv2.imshow('',self.fimg)
                # cv2.waitKey(20)
            win.after(50,show_img)

        def pitch_set(value):
            self.pitch = float(value)
            self.norm2fisheye()
        
        def f0_set(value):
            self.f0 = int(value)
            self.norm2fisheye()

        def fc_set(value):
            # print(type(value))
            # print(self.fc)
            self.fc = int(value)
            self.norm2fisheye()
        
        def position_set_x(value):
            self.position_x = float(value)
            self.norm2fisheye()

        def position_set_y(value):
            self.position_y = float(value)
            self.norm2fisheye()

        def size_set_x(value):
            self.size_x = int(value)
            self.norm2fisheye()

        def size_set_y(value):
            self.size_y = int(value)
            self.norm2fisheye()

        
        def save_para():
            para=[self.f0,self.fc,self.pitch,self.position,self.size_x,self.size_y]
            with open("para.txt","a") as f:
                for i in para:
                    f.writelines(i)


            
        pitch=tk.Scale(win, from_ =-1, to =1,resolution =0.1,orient=tk.HORIZONTAL,length =200,sliderlength= 20,label ='pitch',command=pitch_set)
        f0=tk.Scale(win, from_ =0, to =2000,resolution =10,orient=tk.HORIZONTAL,length =200,sliderlength= 20,label ='f0',command=f0_set)
        fc=tk.Scale(win, from_ =300, to =1200,resolution =10,orient=tk.HORIZONTAL,length =200,sliderlength= 20,label ='fc',command=fc_set)
        position_y=tk.Scale(win, from_ =0, to =4,resolution =0.2,orient=tk.HORIZONTAL,length =200,sliderlength= 20,label ='position_y',command=position_set_y)
        position_x=tk.Scale(win, from_ =0, to =4,resolution =0.2,orient=tk.HORIZONTAL,length =200,sliderlength= 20,label ='position_x',command=position_set_x)
        size_x=tk.Scale(win, from_ =100, to =800,resolution =10,orient=tk.HORIZONTAL,length =200,sliderlength= 20,label ='size_x',command=size_set_x)
        size_y=tk.Scale(win, from_ =100, to =800,resolution =10,orient=tk.HORIZONTAL,length =200,sliderlength= 20,label ='size_y',command=size_set_y)
        save = tk.Button(win,text='save',bg='#7CCD7C',width=5, height=2,command=save_para)

        pitch.set(value=self.pitch)
        f0.set(value=self.f0)
        fc.set(value=self.fc)    
        position_x.set(value=self.position_x)
        position_y.set(value=self.position_y)
        size_x.set(value=self.size_x)
        size_y.set(value=self.size_y)
        
        pitch.grid(row=1)
        f0.grid(row=2)
        fc.grid(row=3)
        position_x.grid(row=4)
        position_y.grid(row=5)
        size_x.grid(row=6)
        size_y.grid(row=7)
        save.grid(row=8, column=1,sticky="ne", padx=100, pady=0)
        show_img()
        win.mainloop()

    def norm2fisheye(self):
        img= self.img
        pitch = self.pitch #pitch angle of fisheye camera
        f0 = self.f0 #f0 gets bigger, distortion gets smaller
        fc = self.fc #fisheye focal length
        rx = self.size_x #image size
        ry = self.size_y
        w,h=img.shape[1],img.shape[0]
  
        ##build the transform map


        u=np.linspace(0,2*rx,2*rx)
        v=np.linspace(0,2*ry,2*ry)
        udst,vdst = np.meshgrid(u,v)
        v,u = vdst-self.position_y*rx ,udst-self.position_x*ry #image position
        
        # rotate the fisheye sphere
        r1 = np.sqrt(fc**2-u**2)
        yc = r1*np.cos(np.arccos(v/r1)+pitch)

        # convert the proxy into raw image
        r = np.sqrt(u**2+yc**2)
        r0 = f0*np.tan(np.arcsin(r/fc))
        p_theta = np.arctan2(yc,u)
        x,y = r0*np.cos(p_theta),r0*np.sin(p_theta)
        map_x = x+w/2
        map_y = y+h/2
        map_y = np.array(map_y,dtype=np.float32)
        map_x = np.array(map_x,dtype=np.float32)

        #transform
        self.fimg = cv2.remap(img,map_x,map_y,cv2.INTER_LINEAR)

    

if __name__ == "__main__":
    # start = time.time()
    img = cv2.imread("zuerich00.png")
    # fimg = norm2fisheye(img)
    # end = time.time()
    # print(f"spent:{end-start}s")
    # cv2.imwrite("out.png",fimg)
    # cv2.imshow('',fimg)
    # cv2.waitKey(500)
    f = fisheye(img)
    f.adjust()