import time
import math
import numpy as np
from matplotlib import pyplot as plt
import sys
import tkinter as tk
from tkinter import *
from os import system
from tkinter import ttk
import ctypes
plt.ion()
class Aircraft():
    def __init__(self, vehicle_ID = 0, vehicle_type = 0 , max_speed = 0 , min_speed=0 , vehicle_range = 0.05,fuel_trans=0):
        self.vehicle_ID = vehicle_ID
        self.vehicle_type = vehicle_type # drone veya duramayan araç
        self.max_speed = max_speed
        self.min_speed = min_speed # hedef araç duramayan bir araç ise düşebileceği min hız
        self.vehicle_range = vehicle_range 
        self.fuel_trans = fuel_trans # % yakıt aktarımı

    def __str__(self):
        return "Vehicle ID : {}\nVehicle Type : {}\nMax Speed : {} km/h \nMin Speed : {} km/h \nVehicle Signal Range : {} m\nFuel Transfer : {} m".format(self.vehicle_ID,self.vehicle_type,self.max_speed,self.min_speed,self.vehicle_range,self.fuel_trans)

class Flight(Aircraft):
    def __init__(self, vehicle_ID = 0, vehicle_type = 0, max_speed = 0,min_speed = 0, vehicle_range = 0.05 ,fuel_trans=0, x_axis = 0, y_axis = 0,fuel =0, vehicle_speed = 0, base_x_axis=0 , base_y_axis=0 , direct_x=0 , direct_y=0 ):
        super().__init__(vehicle_ID, vehicle_type , max_speed , min_speed , vehicle_range , fuel_trans)
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.fuel = fuel # kalan % yakıt
        self.vehicle_speed = vehicle_speed
        self.base_x_axis = base_x_axis
        self.base_y_axis = base_y_axis
        self.direct_x = direct_x # yön bilgisi
        self.direct_y = direct_y 
        
        
    def __str__(self):
        return "\nGPS-x : {}\nGPS-y : {}\nSpeed : {} km/h\n".format(self.x_axis,self.y_axis,self.vehicle_speed)





    
    
def follow(target,tanker,t_rem):
    global turn_back
    if(tanker.max_speed < target.vehicle_speed):
        print("tanker not able to fly side by side with target")
        control=1
        turn_back=1
        return 
    control=0
    tanker.vehicle_speed=target.vehicle_speed
    xb=tanker.base_x_axis-target.x_axis
    yb=tanker.base_y_axis-target.y_axis
    xc=target.direct_x-target.x_axis
    yc=target.direct_y-target.y_axis
    xx=1
    xy=0
    
    arcX3=round(((xc*xx)+(yc*xy))/(math.sqrt(xx**2+xy**2)*math.sqrt(xc**2+yc**2)),4)
    angX3 = math.degrees(np.arccos(arcX3))
    
    vekx=target.direct_x-target.x_axis
    veky=target.direct_y-target.y_axis
           
        # positioning for A
    if vekx<0:
        idenx = -1
    else:
        idenx = 1
            
    if veky<0:
        ideny = -1
    else:
        ideny = 1
        
    tanker.direct_x= tanker.x_axis+(  idenx* abs(np.cos(math.radians(angX3))) * (tanker.vehicle_speed*t_rem/3600))
    tanker.direct_y= tanker.y_axis+(  ideny* abs(np.sin(math.radians(angX3))) * (tanker.vehicle_speed*t_rem/3600))
    

def prt_graph(target,tanker):
    plt.plot([tanker.x_axis,tanker.direct_x], [tanker.y_axis,tanker.direct_y], 'k',[target.x_axis,target.direct_x], [target.y_axis,target.direct_y], 'k',[tanker.x_axis],[tanker.y_axis], 'bo',[target.direct_x],[target.direct_y],'rD',[tanker.direct_x],[tanker.direct_y],'gD',[target.x_axis],[target.y_axis],'ro',[99,-99],[0,0],'k-',[0,0],[99,-99],'k-')
    plt.axis([-3, 3, -3, 3])#going to fix that graph 
    plt.grid(True)
    plt.pause(0.000001)
    plt.draw()
    plt.clf()
    
def vehicle_move(target , tanker , control,trgt_ctrl):
    # positioning vectors for f
    xx=1#ierde bitiş noktası için x exseni vektörü
    xy=0
    xc=target.direct_x-target.x_axis
    yc=target.direct_y-target.y_axis
    xf=tanker.direct_x-tanker.x_axis
    yf=tanker.direct_y-tanker.y_axis
    

            

            #adding vectors to A
    if trgt_ctrl==0:
        arcX=round((((xc*xx)+(yc*xy))/(math.sqrt(xx**2+xy**2)*math.sqrt(xc**2+yc**2))),4)
        angX = math.degrees(np.arccos(arcX))
           
        vekx=target.direct_x-target.x_axis
        veky=target.direct_y-target.y_axis
          
        # positioning for A
        if vekx<0:
            idenx = -1
        else:
            idenx = 1
            
        if veky<0:
            ideny = -1
        else:
            ideny = 1
        target.x_axis= target.x_axis+(  idenx* abs(np.cos(math.radians(angX))) * (target.vehicle_speed/3600))
        target.y_axis= target.y_axis+(  ideny* abs(np.sin(math.radians(angX))) * (target.vehicle_speed/3600)) 
        
            
            # positioning for B
    if control==0:
        arcX2=round((((xf*xx)+(yf*xy))/(math.sqrt(xx**2+xy**2)*math.sqrt(xf**2+yf**2))),4)
        angX2 = math.degrees(np.arccos(arcX2))
        
        vekox=tanker.direct_x-tanker.x_axis
        vekoy=tanker.direct_y-tanker.y_axis
        if vekox<0:
            idenox = -1
        else:
            idenox = 1
            
        if vekoy<0:
            idenoy = -1
        else:
            idenoy = 1
                
                
         #adding vectors to B
        
        tanker.x_axis= tanker.x_axis+(  idenox* abs(np.cos(math.radians(angX2))) * (tanker.vehicle_speed/3600))  
        tanker.y_axis= tanker.y_axis+(  idenoy* abs(np.sin(math.radians(angX2))) * (tanker.vehicle_speed/3600)) 
        
    


def short_way(target , tanker):
    #global control
    #veriables
    global T
    global control
    # vectors for finding angles
    xb=tanker.x_axis-target.x_axis
    yb=tanker.y_axis-target.y_axis#hedef araç ile kontrol edilen araç
    xc=target.direct_x-target.x_axis
    yc=target.direct_y-target.y_axis#hedef araç ile referans noktası
    xx=1#ierde bitiş noktası için x exseni vektörü
    xy=0
    control=0
    
    # finding angles
    arcA=round(((xc*xb)+(yc*yb))/(math.sqrt(xb**2+yb**2)*math.sqrt(xc**2+yc**2)),4)
    angA = math.degrees(np.arccos(arcA))#referans noktası-hedef araç -kontrol edilen araç
    
    ## angle between AC/AF and x axis
    arcX=round((((xc*xx)+(yc*xy))/(math.sqrt(xx**2+xy**2)*math.sqrt(xc**2+yc**2))),4)
    angX = math.degrees(np.arccos(arcX))
    # referans noktası - hedef araç- x exseni
      
    #finding B angle
    dik = np.sin(math.radians(angA))*(target.vehicle_speed/3600)#*T
    
    #istisnalar
    if tanker.vehicle_speed == 0:
        print("out of reach")
        control=control+1
        return
    
    if dik/(tanker.vehicle_speed/3600) > 1 or dik/(tanker.vehicle_speed/3600) <-1:
        print("out of reach")
        control=control+1
        return
    
    ## last point of anles
    angB = math.degrees(np.arcsin(dik/(tanker.vehicle_speed/3600)))#bitiş-kullanılan araç -hedef araç
    
    angC=180.00-angA-angB#bitiş-hedef araç - kontrol edilen araç
    
    #distance between A and B
    dist=math.sqrt((tanker.y_axis-target.y_axis)**2+(tanker.x_axis-target.x_axis)**2)#hedef araç ile kontor edilen araç
    # finding time T for distance
    if(  (np.cos(math.radians(angA))*(target.vehicle_speed/3600) ) +(  np.cos(math.radians(angB))*(tanker.vehicle_speed/3600))==0):
        print("out of reach")
        control=control+1
        return
    T = dist / (  (np.cos(math.radians(angA))*(target.vehicle_speed/3600) ) +(  np.cos(math.radians(angB))*(tanker.vehicle_speed/3600)  )  )
    
    #istisnalar
    if T<0:
        print("out of reach")
        control=control+1
        return
     
    #positioning the axis 1/2 bölge 
    if xc<0:
        idenx = -1
    else:
        idenx = 1
    
    if yc<0:
        ideny = -1
    else:
        ideny = 1
    
    #finding reach points for F 
    x= target.x_axis+(  idenx*abs(np.cos(math.radians(angX))) * (target.vehicle_speed*T/3600))# referans noktası - hedef araç- x exseni
    y= target.y_axis+(  ideny*abs(np.sin(math.radians(angX))) * (target.vehicle_speed*T/3600))
    
    #menzil istisna 
    
    if T*tanker.vehicle_speed/3600>500:
        print("out of reach")
        control=control+1
        return  
    
    #tracking prints for console

    #giving x and y to global veriable
    tanker.direct_x=x
    tanker.direct_y=y
      
    
    
   
def simulation():
    #this function need to track path for both vehicle
    #veriables
    #veriables should get here then run func
    global T
    global control
    global trgt_ctrl
    global turn_back
    #vehicle_ID = 0, vehicle_type = 0, max_speed = 0,min_speed = 0, vehicle_range = 0.05 ,fuel_trans=0, x_axis = 0, y_axis = 0,fuel =0, vehicle_speed = 0, base_x_axis=0 , base_y_axis=0 , direct_x=0 , direct_y=0 
    tanker = Flight(1,0,0,0,0.05,0,0,0,0,0,0,0,0,0)
    target = Flight(2,0,0,0,0.05,0,0,0,0,0,0,0,0,0)
    try:
        #target.x_axis=float(e1.get())
        #target.y_axis=float(e2.get())
        tanker.x_axis=float(e3.get())
        tanker.y_axis=float(e4.get())
        target.vehicle_speed =float(e7.get())
        tanker.vehicle_speed=float(e8.get())
    except ValueError:
        ctypes.windll.user32.MessageBoxW(0, "Type should be number", "Input error", 1)
        return
    tanker.max_speed=tanker.vehicle_speed
    c=0
    ct_time=0
    turn_back=0
    tanker.base_x_axis=tanker.x_axis
    tanker.base_y_axis=tanker.y_axis
    control=0
    trgt_ctrl=0
    t_rem=50
    percent=t_rem
    lineCounter=1
   
    try:
        file1 = open('cordinates.txt','r')
        lines = file1.readlines()
    except:
        ctypes.windll.user32.MessageBoxW(0, "file not found", "Input error", 1)
        return

    if(typeVehicle.get()=='type1'):
        target.vehicle_type=0
    elif(typeVehicle.get()=='type2'):
        target.vehicle_type=1
    else:
        ctypes.windll.user32.MessageBoxW(0, "Type cannot be empty", "Input error", 1)
        return
    coordinates = lines[0].split('\t')
    target.x_axis= float(coordinates[0])
    target.y_axis= float(coordinates[1])
    
    while(1):
     
        coordinates = lines[lineCounter].split('\t')
        target.direct_x=float(coordinates[0])
        target.direct_y=float(coordinates[1])
        dista=math.sqrt((tanker.x_axis-target.x_axis)**2+(tanker.y_axis-target.y_axis)**2)
        c=c+1
        if(dista>target.vehicle_range and turn_back==0):
            print("going to target vehicle")
            short_way(target, tanker)
            if c==60 :
                print("mission aboard!!!")
                break
            if control==0:
                c=0
        elif(dista<=target.vehicle_range and turn_back==0):
            print ("inside the range of target . following...")
            #choice 1 function after ending make turn_back 1 so turn back functin can start
            if(target.vehicle_type==0):
                follow(target,tanker,t_rem)
                t_rem=t_rem-1
                if(t_rem<=0):
                    turn_back=1
                    print ("fuel :% 100")
                    
            if(target.vehicle_type==1):
                trgt_ctrl=1
                control=1
                t_rem=t_rem-1
                if(t_rem<=0):
                    turn_back=1
                    print ("fuel :% 100")
            per100=round(((percent-t_rem)/percent)*100,2)
            print ("fuel :% " ,per100)
        

        elif(turn_back==1):
            print("turning back to base position")
            turn_back=1
            control=0
            trgt_ctrl=0
            tanker.vehicle_speed=tanker.max_speed
            tanker.direct_x=tanker.base_x_axis
            tanker.direct_y=tanker.base_y_axis
            distb = math.sqrt((tanker.x_axis-tanker.base_x_axis)**2+(tanker.y_axis-tanker.base_y_axis)**2)
            if distb < tanker.vehicle_range :
                print("reached to base.mission time:",ct_time)
                break
            #turning back function
        
        vehicle_move(target , tanker , control,trgt_ctrl)
        prt_graph(target,tanker)
        

        print("flying time:",ct_time,"target vehicle:",round(target.x_axis,2),round(target.y_axis,2),"tanker vehicle:",round(tanker.x_axis,2),round(tanker.y_axis,2))
        print("tanker drone destination:",round(tanker.direct_x,2),round(tanker.direct_y,2))
        ct_time = ct_time+1
        target.direct_x= target.direct_x+0.05
        targetDistance=math.sqrt((target.x_axis-target.direct_x)**2+(target.y_axis-target.direct_y)**2)
        if(targetDistance<0.1):
            if(len(lines)<=lineCounter+1):
                trgt_ctrl=1
            else:
                lineCounter=lineCounter+1
            
        time.sleep(0.05)




root = Tk()

#lab1=Label(root,text="Target")
lab2=Label(root,text="Tanker")
lab3=Label(root,text="Type of target")
lab4=Label(root,text="Target V")
lab5=Label(root,text="Tanker V")
lab6=Label(root,text="X")
lab7=Label(root,text="Y")
lab8=Label(root,text="                               ")


#e1=Entry(root,width=10)
#e2=Entry(root,width=10)
e3=Entry(root,width=10)
e4=Entry(root,width=10)
e5=Entry(root,width=10)
e6=Entry(root,width=10)
e7=Entry(root,width=10)
e8=Entry(root,width=10)

myButton = Button(root,text="Run",command=simulation)

#lab1.grid(row=0,column=1)
lab2.grid(row=0,column=2)
lab3.grid(row=0,column=4)
lab4.grid(row=0,column=5)
lab5.grid(row=0,column=6)
lab6.grid(row=1,column=0)
lab7.grid(row=2,column=0)
lab7.grid(row=2,column=0)
lab8.grid(row=1,column=4)

#e1.grid(row=1,column=1)
#e2.grid(row=2,column=1)
e3.grid(row=1,column=2)
e4.grid(row=2,column=2)
e7.grid(row=1,column=5)
e8.grid(row=1,column=6)

n = tk.StringVar() 
typeVehicle = ttk.Combobox(root, width = 7, textvariable = n) 
  
# Adding combobox drop down list 
typeVehicle['values'] = ('type1','type2') 
  
typeVehicle.grid(column = 4, row = 1) 
typeVehicle.current() 
myButton.grid(row=2,column=6)

root.mainloop()




