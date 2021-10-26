import tkinter as tk
from tkinter import filedialog
from tkinter import *
from tkinter import simpledialog
from PIL import ImageTk, Image
import utils
import glob
import os

import kMeans
import DBScan

import time

def show_buttons(file):
    kMeansButton=Button(top,text="KMeans", command=lambda: startKMeans(file), padx=10,pady=5)
    kMeansButton.configure(background='#364156', foreground='white', font=('arial',10,'bold'))
    kMeansButton.place(relx=0.79,rely=0.42)

    EpsLabel = Label(top,text = "Epsilon :")
    EpsLabel.configure(background='#CDCDCD',foreground='#364156')
    EpsLabel.place(relx=0.79,rely=0.58)

    DBScanEps = Entry(top,width=10)
    DBScanEps.configure(font=('arial',10))
    DBScanEps.place(relx=0.79,rely=0.62)
    DBScanEps.insert(END,"8")

    MinPtsLabel = Label(top,text = "MinPts :")
    MinPtsLabel.configure(background='#CDCDCD',foreground='#364156')
    MinPtsLabel.place(relx=0.79,rely=0.66)

    DBScanMinPts = Entry(top,width=10)
    DBScanMinPts.configure(font=('arial',10))
    DBScanMinPts.place(relx=0.79,rely=0.70)
    DBScanMinPts.insert(END,"4")

    DBScanButton=Button(top,text="DBScan", command=lambda: startDBscan(file,float(DBScanEps.get()),int(DBScanMinPts.get())), padx=10,pady=5)
    DBScanButton.configure(background='#364156', foreground='white', font=('arial',10,'bold'))
    DBScanButton.place(relx=0.79,rely=0.52)

def upload_image():
    try:
        file_path=filedialog.askopenfilename(initialdir="./")
        uploaded=Image.open(file_path)
        w, h = uploaded.size
        uploaded.thumbnail((300, int((h*300)/w)))
        im=ImageTk.PhotoImage(uploaded)
        sign_image.configure(image=im)
        sign_image.image=im
        label.configure(text='')
        show_buttons(file_path)
    except:
        pass

def startDBscan(filename,eps,minPts):
    newData = DBScan.process(filename, eps, minPts)
    size = utils.getSize(filename)
    flatData = [int(item) for sublist in newData for item in sublist]
    flatData = bytes(flatData)
    newImage = Image.frombytes('RGB', size, flatData)
    filename = filename[filename.rfind("/") + 1 :]
    distanceType = "euclidienne" if euclidienne else "manhattan"
    newName = "DBScan_" + str(distanceType) + "_" + str(eps) + "_" + str(minPts) + "_" + filename 
    newImage.save("./results/" + newName)
    im = ImageTk.PhotoImage(newImage)
    sign_image.configure(image=im)
    sign_image.image = im

def startKMeans(filename):
    try :
        clusters = simpledialog.askinteger('Parameters','How many clusters are needed ?')
        startTime = time.time()
        newData = kMeans.process(filename,clusters,euclidienne)
        print('Temps pour ' + str(clusters) + " : " + str(time.time()-startTime))
        size = utils.getSize(filename)
        print(str(size))
        flatData = [int(item) for sublist in newData for item in sublist]
        flatData = bytes(flatData)
        newImage = Image.frombytes('RGB', size, flatData)
        filename = filename[filename.rfind("/") + 1 :]
        distanceType = "euclidienne" if euclidienne else "manhattan"
        newName = "KMeans_" + str(clusters) + "_" + str(distanceType) + "_" + filename 
        newImage.save("./results/" + newName)
        newImage.thumbnail((size[0], int((size[1]*300)/size[0])))
        im = ImageTk.PhotoImage(newImage)
        sign_image.configure(image=im)
        sign_image.image = im

        # Si l'on souhaite obtenir le GIF de représentation des centroids
        
        # fp_in = "./centroidsSRC/*.png"
        # filename = filename[:filename.rfind('.')]
        # fp_out = "./centroids/centroids_" + str(clusters) + "_" + str(distanceType) + "_" + filename + ".gif"

        # img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in), key=os.path.getmtime)]
        # img.save(fp=fp_out, format='GIF', append_images=imgs, save_all=True, duration=200, loop=0)

        # for f in glob.glob(fp_in):
        #     os.remove(f)
    
    except :
        pass

def switchDistance():
    global euclidienne
    euclidienne = False if euclidienne else True
    distanceSTR = "Euclidienne" if euclidienne else "Manhattan"
    distanceButton.configure(text=distanceSTR)


if __name__ == "__main__" :
    result = []
    global euclidienne
    euclidienne = True

    #initialise GUI
    top=tk.Tk()
    top.geometry('800x600')
    top.title('TP #2 – CLUSTERING DE COULEURS')
    top.configure(background='#CDCDCD')
    label=Label(top,background='#CDCDCD', font=('arial',15,'bold'))
    sign_image = Label(top)
    upload=Button(top,text="Upload an image",command=upload_image,padx=10,pady=5)
    upload.configure(background='#364156', foreground='white',font=('arial',10,'bold'))
    upload.pack(side=BOTTOM,pady=50)
    sign_image.pack(side=BOTTOM,expand=True)
    label.pack(side=BOTTOM,expand=True)
    heading = Label(top, text="TP #2 – CLUSTERING DE COULEURS",pady=20, font=('arial',20,'bold'))
    heading.configure(background='#CDCDCD',foreground='#364156')
    heading.pack()
    distanceButton = Button(top, text="Euclidienne",command=switchDistance, font=('arial',12))
    distanceButton.configure(background='#364156',foreground='white')
    distanceButton.pack()
    top.mainloop()