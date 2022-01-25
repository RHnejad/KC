import matplotlib.pyplot as plt
import numpy as np 
import csv
import os
directory = 'kc_new'
directory2='kc_new/new'


def rename():
    # #renameing the files which have Ant. in their name
    for file_name in os.listdir(directory):
        # print(file_name)
        f = os.path.join(directory, file_name) 
        try:
            file_name_new=file_name.replace(". ", "")
            file_name_new=file_name_new.replace(" ", "")
            file_name_new=file_name_new.replace("-", "_")

            file_name_new=file_name_new.replace(".", "")#carefull with these 
            file_name_new=file_name_new.replace("csv", ".csv")#carefull with these 

            os.rename(f, os.path.join(directory, file_name_new) )
            print("done")
            # checking if it is a file
        except : pass


def scsv2csv():
    for file_name in os.listdir(directory):
        if file_name!="new":
            f = os.path.join(directory, file_name)
            f2= os.path.join(directory, "new")
            f2=os.path.join(f2, file_name)
            data = ""
            with open(f) as file:
                data = file.read().replace(";", ",")
                file.close()
            with open(f2,'w') as file:
                file.write(data)

def process(f):
    file = open(f)
    csvreader = csv.reader(file)
    header = next(csvreader)
    rows = []

    for row in csvreader:
        rows.append(row)

    file.close()
    N=18000
    array=np.array(rows)
    pic=np.zeros((N,4))
    # print(array)

    for i in range(N):
        for j in range(4):
            pic[i][j]=float(array[i+1][j])

    elevation=pic.T[3]

    n=50
    Z=np.zeros((361,n))
    # Create the mesh in polar coordinates and compute corresponding Z.
    r = np.linspace(0.1, 5.0, 50)
    p = np.linspace(0,360, 361)
    p=np.multiply(p,np.pi/180)
    R, P = np.meshgrid(r, p)
    j=0
    for i in range(180):
        Z[i]=elevation[j*n:(j+1)*n]
        Z[i+180]=elevation[(j+1)*n : (j+2)*n]
        j+=2

    Z[360]=Z[0]
    X, Y = R*np.cos(P), R*np.sin(P)
    return X,Y,Z
   

def plot():
    labels=["0Axial_CURV_ant","1Total_POWER","2Axial_CURV_post","3PostElevationBFS"]
    pat_name=""
    list_dir=os.listdir(directory2)
    list_dir.sort()
    for file_name in list_dir:
        last_p=pat_name
        pat_name=""
        for k in file_name:
            pat_name+=k
            if k=="_":
                eye="OS"
                if "OD" in file_name: eye="OD"
                pat_name+=eye
                break
        if pat_name!=last_p:
            done=0
            try:plt.close(fig)
            except:pass
            fig,ax= plt.subplots(2, 2)

        for label in labels:
            if label[1:] in file_name: 
                f = os.path.join(directory2, file_name) 
                try: 
                    X,Y,Z=process(f)
                
                    r,c=int(label[0])//2,int(label[0])%2
                    ax[r,c].title.set_text("Axial_CURV_ant")
                    surf=ax[r,c].contourf(X,Y,Z,30,cmap=plt.cm.nipy_spectral)  #,list(range(38,58))
                    cbar=fig.colorbar(surf,ax=ax[r,c])
                    done+=1
                    # cbar.mappable.set_clim(-85,100)
                    if done==4 :
                        fig.suptitle(pat_name)
                        plt.savefig("./p3/"+pat_name+".png")
                        print(pat_name+" saved")
            
                except: print("!",file_name)

def process_pcam(f,n):
    file = open(f)
    csvreader = csv.reader(file)
    pic=np.zeros((143*n,143))

    j=0
    c=0
    for row in csvreader:
        if len(row)==143 and j<143*n:    
            c+=1
            for i in range(143):
                print(n)
                try:
                    if row[i]=="":
                        pic[j][i]=None
                    else:
                        pic[j][i]=float(row[i])
                except:
                    pic[j][i]=None
                    print(row[i])
            j+=1

    print("_____C______:",c)
    file.close()
    return pic


def plot_pcam():
    thisdict = {
  "PAC.csv": 1,
  "ELE_BFS.csv": 2,
  "ELE.csv": 5,
  'CUR.csv':5,
  'ACD.csv':1}
  
    list_dir=os.listdir(directory2)
    for file_name in list_dir:
        f = os.path.join(directory2, file_name) 

        n=thisdict[file_name]
        pic=process_pcam(f,n)
        X=pic[0][1:142]
        Y=pic.T[0][1:142]
        Pic = pic[1:143*n-1].T[1:142].T 

        c=0
        for i in range(n):
            plt.figure(figsize=[6,5])
            Pic=pic[142*c+1:142*(c)+1+141].T[1:142].T
            surf=plt.contourf(X,Y,Pic,30,cmap=plt.cm.nipy_spectral)  #,list(range(38,58))
            plt.title(file_name+str(c))
            plt.colorbar(surf)
            plt.savefig(file_name+str(c)+'.png', format='png')
            #plt.show()
            c+=1

        
if __name__=="__main__":
    # rename()
    # scsv2csv()
    plot()
