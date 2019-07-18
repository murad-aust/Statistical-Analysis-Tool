from tkinter import *
from dipy.viz import fvtk
from nibabel import trackvis
from dipy.tracking.utils import length
import numpy as np
import nibabel as nib
import vtk.util.colors as colors
import matplotlib.pyplot as plt
from dipy.tracking import utils
from dipy.tracking.vox2track import streamline_mapping
import AFQ.segmentation as seg
from tkinter import filedialog
import tkinter.messagebox 


def loadtrkfile(T_filename, threshold_short_streamlines=10.0):
    """Load tractogram from TRK file and remove short streamlines with
    length below threshold.
    """
    print("Loading %s" % T_filename)
    T, hdr = trackvis.read(T_filename, as_generator=False)
    T = np.array([s[0] for s in T], dtype=np.object)
   
    return T, hdr



def tract(segmented_tract, color):
    ren = fvtk.ren()           
    fvtk.add(ren, fvtk.line(segmented_tract.tolist(),colors=color, linewidth=2,opacity=0.3))
    fvtk.show(ren)
    fvtk.clear(ren)


def input_tract():
    global T_A,hdr,T_A_filename,color
    T_A_filename= filedialog.askopenfilename()
    threshold_short_streamlines = 0.0     
    T_A, hdr = loadtrkfile(T_A_filename, threshold_short_streamlines=threshold_short_streamlines) 
    color=colors.red
  
    
def input_image():  
    global img
    img= filedialog.askopenfilename()
      

def show_tract():
    tract(T_A, color)



def countstreamlines():
    print("---Number of streamlines---")
    print(( len(T_A)))
    tkinter.messagebox.showinfo("Streamlines", ( len(T_A)))
    
    
def voxelCount():
    tractography,header=trackvis.read(T_A_filename)

    tractography = [streamline[0] for streamline in tractography]

    affine=utils.affine_for_trackvis(voxel_size=np.array([2,2,2]))


    print ("---Number of voxel---")

    print (len(streamline_mapping(T_A,affine=affine).keys())) 
    tkinter.messagebox.showinfo("Voxel", len(streamline_mapping(T_A,affine=affine).keys()))  



def showhistogram():
    print("Histogram...")
    lengths = list(length(T_A))
    fig_hist, ax = plt.subplots()
    ax.hist(lengths, color='burlywood')
    ax.set_xlabel('Length')
    ax.set_ylabel('Count')
    plt.show()
    
    
    
def showAfq():
    FA_img = nib.load(img)
    FA_data = FA_img.get_data()

    print("Tract profiles...")

    fig, ax = plt.subplots(1)
    profile = seg.calculate_tract_profile(FA_data, T_A.tolist())
    ax.plot(profile)
    #ax.set_title('100307_af.left')
    #plt.savefig("F:\Thesis\DATA\\103414_af.left.png")
    plt.show()
    

 

if __name__ == '__main__':
    
    print(__doc__)
    np.random.seed(0)
    
    
    
    root = Tk()
    root.geometry("500x200")
    root.title("TRACTOGRAPHY")
    Frame= Frame(root)
        
     
   
    Frame.pack(fill=X)


    button1=Button(Frame,text="Load Tract",fg="blue",command=input_tract)
    button=Button(Frame,text="Load Image",fg="blue",command=input_image)
    button2=Button(Frame,text="Show Tract",fg="blue",command=show_tract)
    button3=Button(Frame,text="Streamlines Count",fg="blue",command=countstreamlines)
    button4=Button(Frame,text="Voxel Count",fg="blue",command=voxelCount)
    button5=Button(Frame,text="Show Histogram",fg="blue",command=showhistogram)
    button6=Button(Frame,text="Show Profile",fg="blue",command=showAfq)
       
    

    button1.pack(fill=X)
    button.pack(fill=X)
    button2.pack(fill=X)
    button3.pack(fill=X)
    button4.pack(fill=X)
    button5.pack(fill=X)
    button6.pack(fill=X)
    button6.pack(fill=X)
    
   
    
    root.mainloop()
