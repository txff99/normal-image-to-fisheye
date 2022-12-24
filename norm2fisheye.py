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
        self.w,self.h=img.shape[1],img.shape[0]
        try:
            with open("para.txt","r") as f:
                for line in f:
                    line=line.replace('\n','')
                    para.append(line)
                self.pitch = float(para[0])
                self.yaw= float(para[1])
                self.trans_x=float(para[2])
                self.trans_y=float(para[3])
                self.f0 = int(para[4])
                self.zoom = int(para[5])
                self.position_y = float(para[6])
                self.position_x = float(para[7])
                self.size_x = int(para[8])
                self.size_y = int(para[9])
                self.model = int(para[10])

                    
        except:
            print("no exiting para.txt")
            self.pitch = -0.6 
            self.yaw=0
            self.trans_x=1
            self.trans_y=1
            self.f0 = 1400
            self.zoom = 1
            self.position_y = 1
            self.position_x = 1
            self.size_x = 400
            self.size_y = 350
            self.model=1



    def adjust(self):
       
        win =tk.Tk()
        win.title("make your ideal fisheye image!")
        win.geometry('400x650')

        def show_img():
            if self.fimg is None:
                pass
            else:
                cv2.imshow('',self.fimg)
            win.after(50,show_img)

        def pitch_set(value):
            self.pitch = float(value)
            self.norm2fisheye()

        def yaw_set(value):
            self.yaw = float(value)
            self.norm2fisheye()

        def transx_set(value):
            self.trans_x = float(value)
            self.norm2fisheye()

        def transy_set(value):
            self.trans_y = float(value)
            self.norm2fisheye()

        def f0_set(value):
            self.f0 = int(value)
            self.norm2fisheye()

        # def fc_set(value):
        #     self.fc = int(value)
        #     self.norm2fisheye() 

        def zoom_set(value):
            self.zoom = float(value)
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
            para=[self.pitch,self.f0,self.zoom,self.position_x,self.position_y,self.size_x,self.size_y,self.model]
            with open("para.txt","w") as f:
                for i in para:
                    f.writelines(str(i)+'\n')
            print("parameters saved in para.txt")
        
        def set_model1():
            self.model=1
            self.norm2fisheye()
            print("using Orthographic")

        def set_model2():
            self.model=2
            self.norm2fisheye()
            print("using Equidistant")
      
        def set_model3():
            self.model=3
            self.norm2fisheye()
            print("using Stereographic")

        pitch=tk.Scale(win, from_ =-1, to =1,resolution =0.1,orient=tk.HORIZONTAL,length =250,sliderlength= 20,label ='pitch',command=pitch_set)
        yaw=tk.Scale(win, from_ =-1, to =1,resolution =0.1,orient=tk.HORIZONTAL,length =250,sliderlength= 20,label ='yaw',command=yaw_set)
        trans_x=tk.Scale(win, from_ =0, to =2,resolution =0.1,orient=tk.HORIZONTAL,length =250,sliderlength= 20,label ='trans_x',command=(transx_set))
        trans_y=tk.Scale(win, from_ =0, to =2,resolution =0.1,orient=tk.HORIZONTAL,length =250,sliderlength= 20,label ='trans_y',command=transy_set)
        f0=tk.Scale(win, from_ =0, to =2000,resolution =10,orient=tk.HORIZONTAL,length =250,sliderlength= 20,label ='f0',command=f0_set) 
        
        zoom=tk.Scale(win, from_ =0, to =3,resolution =0.1,orient=tk.HORIZONTAL,length =250,sliderlength= 20,label ='zoom',command=zoom_set)
        position_y=tk.Scale(win, from_ =0, to =4,resolution =0.2,orient=tk.HORIZONTAL,length =250,sliderlength= 20,label ='position_y',command=position_set_y)
        position_x=tk.Scale(win, from_ =0, to =4,resolution =0.2,orient=tk.HORIZONTAL,length =250,sliderlength= 20,label ='position_x',command=position_set_x)
        size_x=tk.Scale(win, from_ =100, to =800,resolution =10,orient=tk.HORIZONTAL,length =250,sliderlength= 20,label ='size_x',command=size_set_x)
        size_y=tk.Scale(win, from_ =100, to =800,resolution =10,orient=tk.HORIZONTAL,length =250,sliderlength= 20,label ='size_y',command=size_set_y)
        
        save = tk.Button(win,text='save',bg='#7CCD7C',width=5, height=2,command=save_para)
        model1 = tk.Button(win,text='Orthographic',bg='yellow',width=12, height=2,command=set_model1)
        model2 = tk.Button(win,text='Equidistant',bg='yellow',width=12, height=2,command=set_model2)
        model3 = tk.Button(win,text='Stereographic',bg='yellow',width=12, height=2,command=set_model3)
        
        pitch.set(value=self.pitch)
        yaw.set(value=self.yaw)
        trans_x.set(value=self.trans_x)
        trans_y.set(value=self.trans_y)
        f0.set(value=self.f0)
        zoom.set(value=self.zoom)    
        position_x.set(value=self.position_x)
        position_y.set(value=self.position_y)
        size_x.set(value=self.size_x)
        size_y.set(value=self.size_y)
        
        pitch.grid(row=1)
        yaw.grid(row=2)
        trans_x.grid(row=3)
        trans_y.grid(row=4)
        f0.grid(row=5)
        position_x.grid(row=6)
        position_y.grid(row=7)
        size_x.grid(row=8)
        size_y.grid(row=9)
        zoom.grid(row=10)
        save.grid(row=7, column=1,sticky="ne", padx=50, pady=0)
        model1.grid(row=1, column=1,sticky="ne", padx=50, pady=0)
        model2.grid(row=2, column=1,sticky="ne", padx=50, pady=0)
        model3.grid(row=3, column=1,sticky="ne", padx=50, pady=0)
        show_img()
        win.mainloop()

    def norm2fisheye(self):
        if self.model==1:
            self.model1()
        elif self.model==2:
            self.model2()
        elif self.model==3:
            self.model3()

    def model1(self):
        # Orthographic
        fc = int(self.zoom*350/np.sin(np.arctan(self.w/(2*self.f0))))
        img= self.img
        trans_x = self.trans_x
        trans_y = self.trans_y
        yaw = self.yaw
        pitch = self.pitch #pitch angle of fisheye camera
        f0 = self.f0 #f0 gets bigger, distortion gets smaller
        # fc = self.fc #fisheye focal length
        rx = self.size_x #image size
        ry = self.size_y
  
        ##build the transform map
        u=np.linspace(0,2*rx,2*rx)
        v=np.linspace(0,2*ry,2*ry)
        udst,vdst = np.meshgrid(u,v)
        v,u = vdst-self.position_y*ry+fc*np.sin(pitch)+450*fc*(1-trans_y)/f0 ,\
            udst-self.position_x*rx+fc*np.sin(yaw)+800*fc*(1-trans_x)/f0 #get proxy
        
        # rotate the fisheye sphere
        r1 = np.sqrt(fc**2-u**2)
        yc = r1*np.sin(np.arcsin(v/r1)-pitch)

        r1 = np.sqrt(fc**2-yc**2)
        filter2 = np.arcsin(u/r1)-yaw
        # filter2[filter2>np.pi/2]=None
        # filter2[filter2<-np.pi/2]=None
        xc = r1*np.sin(filter2) 

        # convert the proxy into raw image
        r = np.sqrt(xc**2+yc**2)
        r0 = f0*np.tan(np.arcsin(r/fc))
        p_theta = np.arctan2(yc,xc)
        x,y = r0*np.cos(p_theta),r0*np.sin(p_theta)

        map_x = x+self.w/2*trans_x
        map_y = y+self.h/2*trans_y
        map_y = np.array(map_y,dtype=np.float32)
        map_x = np.array(map_x,dtype=np.float32)

        #transform
        self.fimg = cv2.remap(img,map_x,map_y,cv2.INTER_LINEAR)

    def model2(self):    
        # Equidistant
        fc = int(self.zoom*300/np.arctan(self.w/(2*self.f0)))
        # fc=1000
        img= self.img
        trans_x = self.trans_x
        trans_y = self.trans_y
        yaw = self.yaw
        pitch = self.pitch #pitch angle of fisheye camera
        f0 = self.f0 #f0 gets bigger, distortion gets smaller
        # fc = self.fc #fisheye focal length
        rx = self.size_x #image size
        ry = self.size_y
  
        ##build the transform map
        u=np.linspace(0,2*rx,2*rx)
        v=np.linspace(0,2*ry,2*ry)
        udst,vdst = np.meshgrid(u,v)
        v,u = vdst-self.position_y*ry+fc*np.sin(pitch)+450*fc*(1-trans_y)/f0 ,\
            udst-self.position_x*rx+fc*np.sin(yaw)+800*fc*(1-trans_x)/f0 #get proxy
        
        rp = np.sqrt(u**2+v**2)
        filter = rp/fc
        filter[filter > np.pi/2]=None
        orth = np.sin(filter)
        x0 = fc*orth*u/rp #equidistant to Orthographic
        y0 = fc*orth*v/rp

        # rotate the fisheye sphere
        #rotate in direction of y
        r1 = np.sqrt(fc**2-x0**2)
        filter2 = np.arcsin(y0/r1)-pitch
        filter2[filter2>np.pi/2]=None
        filter2[filter2<-np.pi/2]=None
        yc = r1*np.sin(filter2) 

        #rotate in direction of x
        r1 = np.sqrt(fc**2-y0**2)
        filter2 = np.arcsin(x0/r1)-yaw
        filter2[filter2>np.pi/2]=None
        filter2[filter2<-np.pi/2]=None
        xc = r1*np.sin(filter2) 

        
        # convert the proxy into raw image
        r = np.sqrt(xc**2+yc**2)
        r0 = f0*np.tan(np.arcsin(r/fc))
        p_theta = np.arctan2(yc,xc)
        x,y = r0*np.cos(p_theta),r0*np.sin(p_theta)

        map_x = x+self.w/2*trans_x
        map_y = y+self.h/2*trans_y
        map_y = np.array(map_y,dtype=np.float32)
        map_x = np.array(map_x,dtype=np.float32)

        #transform
        self.fimg = cv2.remap(img,map_x,map_y,cv2.INTER_LINEAR)

    def model3(self):    
        # Stereographic
        fc = int(self.zoom*150/np.tan(0.5*np.arctan(self.w/(2*self.f0))))
        img= self.img
        trans_x = self.trans_x
        trans_y = self.trans_y
        yaw = self.yaw
        pitch = self.pitch #pitch angle of fisheye camera
        f0 = self.f0 #f0 gets bigger, distortion gets smaller
        # fc = self.fc #fisheye focal length
        rx = self.size_x #image size
        ry = self.size_y
  
        ##build the transform map
        u=np.linspace(0,2*rx,2*rx)
        v=np.linspace(0,2*ry,2*ry)
        udst,vdst = np.meshgrid(u,v)
        v,u = vdst-self.position_y*ry+fc*np.sin(pitch)+450*fc*(1-trans_y)/f0 ,\
            udst-self.position_x*rx+fc*np.sin(yaw)+800*fc*(1-trans_x)/f0 #get proxy

        rp = np.sqrt(u**2+v**2)
        filter = 2*np.arctan(rp/(2*fc))
        filter[filter > np.pi/2]=None
        orth = np.sin(filter)
        x0 = fc*orth*u/rp #Stereographic to Orthographic
        y0 = fc*orth*v/rp

        
        # rotate the fisheye sphere
        r1 = np.sqrt(fc**2-x0**2)
        filter2 = np.arcsin(y0/r1)-pitch
        filter2[filter2>np.pi/2]=None
        filter2[filter2<-np.pi/2]=None
        yc = r1*np.sin(filter2)  #rotate in direction of y

        r1 = np.sqrt(fc**2-yc**2)
        filter2 = np.arcsin(x0/r1)-yaw
        filter2[filter2>np.pi/2]=None
        filter2[filter2<-np.pi/2]=None
        xc = r1*np.sin(filter2) 
        

        # convert the proxy into raw image
        r = np.sqrt(xc**2+yc**2)
        r0 = f0*np.tan(np.arcsin(r/fc))
        p_theta = np.arctan2(yc,xc)
        x,y = r0*np.cos(p_theta),r0*np.sin(p_theta)

        map_x = x+self.w/2*trans_x
        map_y = y+self.h/2*trans_y
        map_y = np.array(map_y,dtype=np.float32)
        map_x = np.array(map_x,dtype=np.float32)

        #transform
        self.fimg = cv2.remap(img,map_x,map_y,cv2.INTER_LINEAR)




    

if __name__ == "__main__":
    img = cv2.imread("zuerich00.png")
    f = fisheye(img)
    f.adjust()