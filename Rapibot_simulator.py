############################################################################
####                    3D printer G code simulator                     ####
####                           by Xiang Zhai                            ####
####                         April 11, 2015                             ####
####                                                                    ####
####                        funofdiy.blogspot.com                       ####
####                        zxzhaixiang@gmail.com                       ####
############################################################################


from Gcode_interpretation_functions import Gcode_interpretation, preprocess
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

#####################################
#####    read configuration       ###
#####################################

config_file = open("simulator_config.txt","r")
Gcode_file  =   'gcodes/squirrel_export.gcode' #G code file name
ns_skip     =   4 #number of sections to skip when plotting
np_skip     =   5 #number of points to skip when plotting
tmp = config_file.readline().split()
dx = 0.075                              #resolution in x,y,z direction
dy = 0.075
dz = 0.075
de = 0.01                               #resolution of extruder

print(Gcode_file, ns_skip, dx, dy, dz, de)
config_file.close()

print("pre-processing..")
[xmin, xmax, ymin, ymax, zmax]=preprocess(Gcode_file)
print("xrange=[{}, {}], yrange=[{}, {}], zrange=[0, {}]".format(xmin,xmax,ymin,ymax,zmax))
print("xstep=[{}, {}], ystep=[{}, {}], zstep=[0, {}]".format(int(xmin/dx),int(xmax/dx),int(ymin/dy),int(ymax/dy), int(zmax/dz)))
xbound = [xmin-(xmax-xmin)/8,xmax+(xmax-xmin)/8]
ybound = [ymin-(ymax-ymin)/8,ymax+(ymax-ymin)/8]
zbound = [0,zmax*(1+1/8)]

#####################################
#####       main program          ###
#####################################
prefix_name=['G','M','X','Y','Z','E','F','S']

ns = -1
x_coord=0
y_coord=0
z_coord=0
e_coord=0

x_origin=0
y_origin=0
z_origin=0
e_origin=0

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_xlim3d(xbound[0],xbound[1])
ax.set_ylim3d(ybound[0],ybound[1])
ax.set_zlim3d(zbound[0],zbound[1])
#ax.set_aspect('equal');
ax.set_xlabel('x (mm)')
ax.set_ylabel('y (mm)')
ax.set_zlabel('z (mm)')

ax.pbaspect = [1.0,(ybound[1]-ybound[0])/(xbound[1]-xbound[0]),(zbound[1]-zbound[0])/(xbound[1]-xbound[0])]
#ax.auto_scale_xyz(xbound,ybound,zbound);
#ax.set_aspect('equal');
                
xlist=[]
ylist=[]
zlist=[]

np=0
try:
    for lines in open(Gcode_file,'r'):
        values=Gcode_interpretation(lines)#[G, M, X, Y, Z, E, F, S]
        if values[0]==21:       #working in millimeter
            print("working in millimeter")
        elif values[0]==20:     #working in inch
            dx/=25.4
            dy/=25.4
            dz/=25.4
            de/=25.4
            print("working in inch")
        elif values[1]==82: #M82
            print("use absolute distances for extrusion")
        elif values[1]==84: #M84
            print("disable motors")
        elif values[1]==106:
            print("fan on")
        elif values[1]==107:
            print("fan off")
        elif values[1]==104:
            print("set temperature to {} C".format(values[7]))
        elif values[1]==109:
            print("wait for temperature {} C to be reached".format(values[7]))            
        elif values[0]==28:  #home axes
            print("home axes")
        elif values[0]==90:  #absolute coordinates
            x_origin=0
            y_origin=0
            z_origin=0
            print("use absolute coordinates")
        elif values[0]==91:  #relative coordinates
            x_origin=x_coord
            y_origin=y_coord
            z_origin=z_coord
            print("use relative coordinates")
        elif values[0]==92:  #zeros position
            counter=0;
            if (values[2]!=-999):
                x_coord=0
                x_origin=0
                counter+=1
                print("set current x location as zero")
            if (values[3]!=-999):
                counter+=1
                y_coord=0
                y_origin=0
                print("set current y location as zero")
            if (values[4]!=-999):
                counter+=1
                z_coord=0
                z_origin=0
                print("set current z location as zero")
            if (values[5]!=-999):
                counter+=1
                e_coord=0
                e_origin=0
                xlist=[]
                ylist=[]
                zlist=[]
                #print "set current e location as zero";
            if(counter==0):
                x_coord=0
                y_coord=0
                z_coord=0
                e_coord=0
                x_origin=0
                y_origin=0
                z_origin=0
                e_origin=0
                print("set current location as zero")
        elif values[0]==1:   #G1
            if((values[2]!=-999) and (values[3]!=-999)):   #xy motion
                x_coord=values[2]
                y_coord=values[3]
            if ((values[5]>=0) and (values[5]<=e_coord)):  #finishing a section
                ns += 1
                if ns % (ns_skip) == 0:                
                    ax.plot(xlist,ylist,zlist)
                    plt.draw()
                    plt.pause(0.0001)
                    xlist=[]
                    ylist=[]
                    zlist=[]
            elif ((values[4]==-999) and (values[5]>e_coord)): #start feeding plastic
                e_coord=values[5]
                np += 1
                if(np % np_skip==0):
                    xlist.append(int(x_coord/dx)*dx)
                    ylist.append(int(y_coord/dy)*dy)
                    zlist.append(int(z_coord/dz)*dz)
                print("move to x={}, y={} ".format(values[2], values[3]))
            elif (values[4]!=-999): #z motion
                z_coord = values[4]
                print("lift to z={}".format(values[4]))


except KeyboardInterrupt:
    pass

raw_input("press enter key to exit");
