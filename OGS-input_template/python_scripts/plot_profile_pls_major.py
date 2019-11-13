# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 10:21:05 2018

% 

calculate magnitude and shear slip from FLAC3d profile output done by Luca Urpi (ETH)

@author: Luca
#################################
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
plt.rcParams['pdf.fonttype'] = 42 # so text can be edited in Illustrator
plt.rcParams['ps.fonttype'] = 42 # so text can be edited in Illustrator

"""
# FUNCTION to read output from flac3d
file has header
 -z_sxx   -z_szz   -z_sxz   z_pp    string(z_vsi(p_z))   string(z_ssi(p_z))   string(tempe)   string(es)   string(et)   string(esj)   string(etj)   string(z_ycen(p_z))   string(z_zcen(p_z))
"""
def read_file(filename):   
  rd_values=[]
  with open(filename, 'r') as data:
    data.seek(0) #goes to the beginning of file, useful if need to iterate multiple times over the file
    data.readline() # skip first line header
    flag_data=0
    flag_line=0
    rd_values=[]
    for line in data: 
             if "ZONE" in line:
                   if flag_data ==0:
                           flag_data=1
                           time=float(line[14:-2])
                   else:        
                           flag_data=0
                           rd_values.append([time, rd_elem])
                           flag_line=0                         
             elif "TITLE" in line:
                           flag_data=0
                           rd_values.append([time, rd_elem])

                           flag_line=0
             else:
              if flag_data ==1:              
                values=line.split()
                if flag_line==0:
                    flag_line=1
                    length=(len(values))
                    rd_elem= [[] for oid in range(length)]
                for jj in range(len(values)):
                    rd_elem[jj].append(float(values[jj]))
  return rd_values

polyline="..\\taskB-step3-2d_ply_DIP_Z_major_t23.tec"
data=read_file(polyline) #array with (time_dd,press_bar,flow_lmin, north_displ, west_displ, vert_displ)

"""
data[i][0] = ## time of i-data
data[i][1][j] = ## value of data. j=0 is x length along polyline, other values depends on .out
this case 
0="DIST" 
1="STRAIN_PLS" 
2="PRESSURE1" 
3="STRESS_XX" 4="STRESS_YY"  5="STRESS_ZZ" 6="STRESS_XY" 7="STRESS_XZ" 8="STRESS_YZ" 
9="VELOCITY_X1" 10="VELOCITY_Y1" 11="VELOCITY_Z1" 
12="DISPLACEMENT_X1"13= "DISPLACEMENT_Y1" 14="DISPLACEMENT_Z1",
15="p_(1st_Invariant)"16="q_(2nd_Invariant)"17="Effective_Strain" 
"""


colormap = plt.get_cmap('coolwarm_r') 
colorst = [colormap(i) for i in np.linspace(0., 1.,len(data)-1)]   
colorst.append((0,0,0,1))

#fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(11, 7.4), sharex=True)
fig3 = plt.figure(figsize=(9,6))
ax1 = fig3.add_subplot(111)
for i in range(len(data)):
 x_val= data[i][1][0]
 y_val =data[i][1][1]
 ax1.plot(x_val,y_val,color=colorst[i],lw=2.5,label="Pls strain at "+str(data[i][0])+"s")
 
ax1.set_xlabel('Distance along polyline', fontsize=28)
ax1.set_ylabel('Pls strain', fontsize=28)
ax1.tick_params(axis='y', labelsize=24)
ax1.tick_params(axis='x', labelsize=24)

 # norm is a class which, when called, can normalize data into the
# [0.0, 1.0] interval.

norm = mpl.colors.Normalize(vmin=0, vmax=data[-1][0])

# create a ScalarMappable and initialize a data structure
cmap = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.coolwarm_r)
cmap.set_array([])

cb=fig3.colorbar(cmap)#, ticks=time_color)
#cb.set_fontsize(24)
cb.ax.tick_params(labelsize=20)
cb.set_label('Time (s)', fontsize=22)

#cb.set_label('Injection time', fontsize=14)
#ax1.set_xlim(0,850)
#ax1.set_ylim(4.9e5,1.1e6)
#plt.legend(loc=2)
#plt.tight_layout()
plt.grid()
#plt.savefig("FM1_upd.png",dpi=600)
plt.show()