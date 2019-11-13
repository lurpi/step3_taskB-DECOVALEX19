# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 09:52:34 2015

@author: Luca Urpi
"""


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
def out_arr( outfile,list):
 filename=outfile
 f = open(filename, 'w')
 print >> f, "\n".join(list)
 f.close()
 return;
 
def shear_norm_stress(point, dip, strike): # point is a string, dip and strike angle in degrees
 r=point
 p = pd.read_csv(r, skiprows=2, header=0, names=column_hist3, delimiter=r"\s+") 
 dr=np.pi - np.deg2rad(dip)
 sr=np.deg2rad(strike)
 t= p["TIME"].values
 normal_stress=[]
 shear_stress=[]
 if (strike == 0) or (strike == 180):
     shh=p["STRESS_XX"].values
     sho=p["STRESS_XY"].values
     shz=p["STRESS_XZ"].values
     soo=p["STRESS_YY"].values
     soz=p["STRESS_YZ"].values
     szz=p["STRESS_ZZ"].values
 elif (strike == 90) or (strike == -90):
     soo=p["STRESS_XX"].values
     sho=p["STRESS_XY"].values
     soz=p["STRESS_XZ"].values
     shh=p["STRESS_YY"].values
     shz=p["STRESS_YZ"].values
     szz=p["STRESS_ZZ"].values     
 else:
     sxx=p["STRESS_XX"].values
     sxy=p["STRESS_XY"].values
     sxz=p["STRESS_XZ"].values
     syy=p["STRESS_YY"].values
     syz=p["STRESS_YZ"].values
     szz=p["STRESS_ZZ"].values
     shh=[]
     shz=[]
     for jj in range(0,len(t),1):
       horiz_comp = sxx*np.cos(sr)+syy*np.sin(sr)
       shear_comp = sxz*np.cos(sr)+syz*np.sin(sr)
       shh.append(horiz_comp)
       shz.append(shear_comp)
 for jj in range(0,len(t),1):
   
    norm=0.5*(-shh[jj]-szz[jj])+0.5*(-shh[jj]+szz[jj])*np.cos(2*dr)+shz[jj]*np.sin(2*dr)
    shear=(0.5*(-shh[jj]+szz[jj])*np.sin(2.*dr)-(shz[jj]*np.cos(2*dr)))      
        
    normal_stress.append(-norm)      
    shear_stress.append(shear)      
 
 return t,normal_stress, shear_stress

def stress_to_sn(p,strike):
     sr=np.radians(strike)
     sxx=p["STRESS_XX"].values
     sxy=p["STRESS_XY"].values
     sxz=p["STRESS_XZ"].values
     syy=p["STRESS_YY"].values
     syz=p["STRESS_YZ"].values
     szz=p["STRESS_ZZ"].values
     sn1=[]
     sn2=[]
     shz=[]
     for jj in range(0,len(sxx),1):
       horiz_comp = sxx[jj]*np.cos(sr)+syy[jj]*np.sin(sr)
       shear_comp = sxz[jj]*np.cos(sr)+syz[jj]*np.sin(sr)
       sn1.append(-horiz_comp)
       sn2.append(-szz[jj])
       shz.append(shear_comp)
     return sn1, sn2, shz
 
 
def ogs_to_sn(syy,szz,syz, dr): # dr is dip  in radians
   nor=[]
   she=[]
   dr=np.pi/2.-dr
   for jj in range(0,len(szz),1):
        norm=0.5*(-syy[jj]-szz[jj])+0.5*(-syy[jj]+szz[jj])*np.cos(2*dr)+syz[jj]*np.sin(2*dr)
        #(((syy[jj])*np.sin(dr)*np.sin(dr))-2*syz[jj]*(np.sin(dr)*np.cos(dr))+(szz[jj])*(np.cos(dr)*np.cos(dr)))
        shear=(0.5*(-syy[jj]+szz[jj])*np.sin(2.*dr)-(syz[jj]*np.cos(2*dr)))
        #(0.5*(szz[jj]-syy[jj])*np.cos(-2.*dr)-(syz[jj]*np.sin(2*dr)))
        nor.append(norm)
        she.append(shear)        

   return nor,she

r0="..\\taskB-step3-2d_time_INJ_POINT_00.tec"
r1="..\\taskB-step3-2d_time_MONITORING3.tec"
r2="..\\taskB-step3-2d_time_MONITORING3.tec"
r3="..\\taskB-step3-2d_time_MP_18below.tec"
r3="..\\taskB-step3-2d_time_INJ_POINT_00.tec"
#r3="..\\taskB-2d_time_MONITORING3.tec"
strike = 90
dip = 60

column_hist1 = ("TIME","STRAIN_PLS","PRESSURE1","STRESS_XX","STRESS_YY","STRESS_ZZ","STRESS_XY","STRESS_XZ","STRESS_YZ","VELOCITY_X1","VELOCITY_Y1","VELOCITY_Z1","DISPLACEMENT_X1","DISPLACEMENT_Y1","DISPLACEMENT_Z1","p_(1st_Invariant)","q_(2nd_Invariant)","Effective_Strain")
column_hist0 = ("TIME","PRESSURE1","p_(1st_Invariant)","q_(2nd_Invariant)"," Effective_Strain")
column_hist3 = ("TIME","STRAIN_PLS","PRESSURE1","STRESS_XX","STRESS_YY","STRESS_ZZ","STRESS_XY","STRESS_XZ","STRESS_YZ","VELOCITY_X1","VELOCITY_Y1","VELOCITY_Z1","DISPLACEMENT_X1","DISPLACEMENT_Y1","DISPLACEMENT_Z1","p_(1st_Invariant)","q_(2nd_Invariant)","Effective_Strain")
column_hist4 = ("TIME","STRAIN_PLS","VELOCITY_X1","VELOCITY_Y1","VELOCITY_Z1","DISPLACEMENT_X1","DISPLACEMENT_Y1","DISPLACEMENT_Z1","PRESSURE1","STRESS_XX","STRESS_YY","STRESS_ZZ","STRESS_XY","STRESS_XZ","STRESS_YZ","p_(1st_Invariant)","q_(2nd_Invariant)"," Effective_Strain")

p0 = pd.read_csv(r0, skiprows=2, header=0, names=column_hist0, delimiter=r"\s+")  

p1 = pd.read_csv(r1, skiprows=2, header=0, names=column_hist1, delimiter=r"\s+")  
p2 = pd.read_csv(r2, skiprows=2 ,header=0, names=column_hist1, delimiter=r"\s+")  
p3 = pd.read_csv(r3, skiprows=2, header=0, names=column_hist3, delimiter=r"\s+") 
 
#p3 = pd.read_csv(r3, skiprows=[0,1,2,3,4,5,6,7,8,9,10,11,12,18,19,20,21,22,23,24,25,26,27,28] ,header=0,skipfooter=1, names=column_hist3, delimiter=r"\s+")  
Elementthickness = 0.02331/4
X= p0["TIME"].values
X1= p1["TIME"].values
X2= p2["TIME"].values
X_f2= p3["TIME"].values
P_inj = p0["PRESSURE1"].values
P1 = p1["PRESSURE1"].values
P2 = p2["PRESSURE1"].values
P_f2 = p3["PRESSURE1"].values
S1 = p1["STRAIN_PLS"].values * Elementthickness
S2 = p2["STRAIN_PLS"].values * Elementthickness
S_f2 = p3["STRAIN_PLS"].values * Elementthickness


T3=p3["TIME"].values
shh, szz, shz = stress_to_sn(p2, strike) 
N3,S3= ogs_to_sn(shh,szz,shz, np.pi-np.deg2rad(dip))
tx = -1.*np.arange(-9., 9e6, 1e5)
ty = np.arange(-9., 9e6, 1e5)

plt.figure(figsize=(8,5))
plt.scatter(N3, S3, c=T3, s=75, edgecolors='black', alpha=0.75)
plt.plot(tx,np.tan(np.deg2rad(22))*ty, 'b--')
plt.plot(tx,-1.0*np.tan(np.deg2rad(22))*ty, 'b--')
plt.plot(tx,np.tan(np.deg2rad(22))*ty+1.e6, 'r--')
plt.plot(tx,-1.0*np.tan(np.deg2rad(22))*ty-1.e6, 'r--')
plt.plot(tx,np.tan(np.deg2rad(22))*ty+2.5e6, 'g--')
plt.plot(tx,-1.0*np.tan(np.deg2rad(22))*ty-2.5e6, 'g--')
plt.axis([-6.75e6, -0., -2.e6, 2e6])
plt.annotate('Time 0',
                   xy=(N3[0],S3[0]), xycoords='data',
                   xytext=(10, -35), textcoords='offset points',
                   arrowprops=dict(arrowstyle="->", edgecolor='green',shrinkB=0., 
                                   connectionstyle="angle3", lw=2.5), bbox=dict(boxstyle="square", fc="w"))
plt.annotate('Time :'+np.str(np.trunc(T3[-1])),
                   xy=(N3[-1],S3[-1]), xycoords='data',
                   xytext=(10, +35), textcoords='offset points',
                   arrowprops=dict(arrowstyle="->", edgecolor='green',shrinkB=0., 
                                   connectionstyle="angle3", lw=2.5), bbox=dict(boxstyle="square", fc="w"))
if len(T3)>43:                                   
   plt.annotate('Time :'+np.str(np.trunc(T3[43]))+' Pressure :'+np.str(np.trunc(P_f2[43]/1.e3)/1.e3)+' MPa',
                   xy=(N3[43],S3[43]), xycoords='data',
                   xytext=(-200, -35), textcoords='offset points',
                   arrowprops=dict(arrowstyle="->", edgecolor='green',shrinkB=0., 
                                   connectionstyle="angle3", lw=2.5), bbox=dict(boxstyle="square", fc="w"))
if len(T3)>95:                                   
    plt.annotate('Time :'+np.str(np.trunc(T3[95]))+' Pressure :'+np.str(np.trunc(P_f2[95]/1.e3)/1.e3)+' MPa',
                   xy=(N3[95],S3[95]), xycoords='data',
                   xytext=(-150, -47.5), textcoords='offset points',
                   arrowprops=dict(arrowstyle="->", edgecolor='green',shrinkB=0., 
                                   connectionstyle="angle3", lw=2.5), bbox=dict(boxstyle="square", fc="w"))
if len(T3)>174:                                   
    plt.annotate('Time :'+np.str(np.trunc(T3[174]))+' Pressure :'+np.str(np.trunc(P_f2[174]/1.e3)/1.e3)+' MPa',
                   xy=(N3[174],S3[174]), xycoords='data',
                   xytext=(-100, -60), textcoords='offset points',
                   arrowprops=dict(arrowstyle="->", edgecolor='green',shrinkB=0., 
                                   connectionstyle="angle3", lw=2.5), bbox=dict(boxstyle="square", fc="w"))

if len(T3)>188:                                   
    plt.annotate('Time :'+np.str(np.trunc(T3[188]))+' Pressure :'+np.str(np.trunc(P_f2[188]/1.e3)/1.e3)+' MPa',
                   xy=(N3[188],S3[188]), xycoords='data',
                   xytext=(-100, -60), textcoords='offset points',
                   arrowprops=dict(arrowstyle="->", edgecolor='green',shrinkB=0., 
                                   connectionstyle="angle3", lw=2.5), bbox=dict(boxstyle="square", fc="w"))
plt.title('Stress evolution in the fault, point %s' %r3, fontsize=24)
plt.xlabel('Normal stress (MPa)', fontsize=20)
plt.ylabel('Shear stress (MPa)', fontsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
#set_ylabel('treatment')
cb=plt.colorbar()
cb.set_label('Injection time', fontsize=14)
#leg=plt.legend()
plt.grid()
plt.show()

