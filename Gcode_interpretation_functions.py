def Gcode_interpretation(lines):
    #given a G code line, return the value of G, M, X, Y, Z, E, F, S
    #if does not apply, return -1
    #For example, line G1 X10 Y20 E4 F5 will give [1,0,10,20,0,4,5]
    Prefix_list=[ 'G', 'M', 'X', 'Y', 'Z', 'E', 'F', 'S']
    Return_list=[-999,-999,-999,-999,-999,-999,-999,-999]
    k=0
    for Prefix in Prefix_list:
        if (lines.find(Prefix))>=0:         #if letter [Prefix] exists
            char_loc=lines.index(Prefix)   #location of this letter
            i=char_loc+1
            while (47<ord(lines[i])<58)|(lines[i]=='.')|(lines[i]=='-'):
                i+=1
            if(i>char_loc+1):
                Return_list[k]=float(lines[char_loc+1:i])#the number after this letter
        k+=1;
    Return_list[0]=int(Return_list[0]) #int for G
    Return_list[1]=int(Return_list[1]) #int for M    
    return Return_list


def preprocess(Gcode_file):
    xmin=999
    xmax=-999
    ymin=999
    ymax=-999
    zmin=999
    zmax=-999

    lines = open('gcodes/squirrel_export.gcode','r')
    for line in lines:
        values=Gcode_interpretation(line)#[G, M, X, Y, Z, E, F, S]
        if(values[0]==1):
            if(values[2]!=-999):
                xmin=min(xmin,values[2])
                xmax=max(xmax,values[2])
            if(values[3]!=-999):
                ymin=min(ymin,values[3])
                ymax=max(ymax,values[3])
            if(values[4]!=-999):
                zmax=max(zmax,values[4])
    lines.close();

    return [xmin,xmax,ymin,ymax,zmax]