#QSPICE Circuit Generators
#This script contains collection of SPICE circuit generators
#Each generator creates netlist file compatible with Qorvo QSPICE. 
#It assumes that QSPICE is installed in its default path for non-Admin user

#Update: 25-Aug-2023

import os
import subprocess

# This function generates Full Wave AC rectifier with constant power load.It uses simplified diode model.

#Input parameters:
#VAC_rms - RMS value of Input AC source
#Cf - value of filter capacitor
#Pin - value of constant power load. It should be equal to expected input power of connected DC/DC converter
#fwd - Estimated rectifier diode threshold voltage
#rdiff - estimated rectifier diode differential resistance
#freq - Input AC line frequency

#Output:
#list index
    #[0] - Total Power Dissipation
    #[1] - Diode AVG current
    #[2] - Diode RMS current
    #[3] - AC source RMS current
    #[4] - Output voltage AVG value
    #[5] - Input Capacitor RMS ripple current

def QSPICE_Input_REC(VAC_rms, Cf, Pin, fwd, rdiff, freq):

    #### Generate cir File
    f = open("Input_REC.cir", "w", encoding='ascii', newline='\n')

    #### Circuit Definition ###
    f.write("* Input Rectifier Auto-Generated Netlist File"+"\n")
    f.write("D1 N01 out REC"+"\n")
    f.write("D2 N02 out REC"+"\n")
    f.write("D3 0 N02 REC"+"\n")
    f.write("D4 0 N01 REC"+"\n")
    f.write("V1 N01 N02 SIN 0 {sqrt(2)*VAC_rms} {freq}"+"\n")
    f.write("C1 out 0 {Cf}"+"\n")
    f.write("B1 out 0 R=if(time>{1/freq},V(out)*V(out)/{Pin},0)"+"\n")
    
    #### Models Definition ####
    f.write(".model REC D(Vfwd={fwd}, Ron={rdiff}, Cjo=10p)"+"\n")
    f.write(".lib Diode.txt"+"\n")
    
    #### Spice Options ####
    f.write(".tran 0 {12*1/freq} {6*1/freq} 10e-6"+"\n")
    f.write(".options savepowers=1"+"\n")
    f.write(".options trtol=1"+"\n")

    #### Parameters ####
    f.write(".param Pin="+str(Pin)+"\n")
    f.write(".param Cf="+str(Cf)+"\n")
    f.write(".param VAC_rms="+str(VAC_rms)+"\n")
    f.write(".param rdiff="+str(rdiff)+"\n")
    f.write(".param freq="+str(freq)+"\n")
    f.write(".param fwd="+str(fwd)+"\n")
    
    #### Measurement Definition ####
    f.write(".meas Pd avg P(V1)"+"\n")
    f.write(".meas I_C1_RMS rms I(C1)"+"\n")
    f.write(".meas Vout_AVG avg V(out)"+"\n")
    f.write(".meas I_AC_RMS rms I(V1)"+"\n")
    f.write(".meas I_D_RMS rms I(D1)"+"\n")
    f.write(".meas I_D_AVG avg I(D1)"+"\n")
    
   
    f.write(".end")
       
    f.close()
    
    
    #Assume that QSPICE is installed in its default path for non-Admin user
    exe_qspice64=os.path.expanduser(r"~\QSPICE\QSPICE64.exe")
    exe_qpost=os.path.expanduser(r"~\QSPICE\QPOST.exe")
    
    #run QSPICE Simulation
    result=subprocess.run([exe_qspice64, "Input_REC.cir"])
  #  print(result)
    
    #Run postprocess measurement
    result=subprocess.run([exe_qpost, "Input_REC.cir", "-o","results.txt"])
    #print(result.stdout)

    f = open("results.txt", "r")
    Lines = f.readlines()
    f.close()
    
    #Delete Results
    subprocess.run(["del", "Input_REC.qraw"], shell=True)
  #  print(result)
    
    #Delete Netlist
    subprocess.run(["del", "Input_REC.cir"], shell=True)
  #  print(result)

    #Delete QPOST Results
    subprocess.run(["del", "results.txt"], shell=True)
  #  print(result)
    results = [0, 0, 0, 0, 0, 0]

    for line in Lines:
        # Assign results in required order into the list
        if line.find('.meas pd avg p(v1):') != -1:
            index=Lines.index(line)
            results[0]=(float(Lines[index+1])*-1)-Pin
        elif line.find('.meas i_d_avg avg i(d1):') != -1:
            index=Lines.index(line)
            results[1]=float(Lines[index+1])
        elif line.find('.meas i_d_rms rms i(d1):') != -1:
            index=Lines.index(line)
            results[2]=float(Lines[index+1])           
        elif line.find('.meas i_ac_rms rms i(v1):') != -1:
            index=Lines.index(line)
            results[3]=float(Lines[index+1])
        elif line.find('.meas vout_avg avg v(out):') != -1:
            index=Lines.index(line)
            results[4]=float(Lines[index+1])
        elif line.find('.meas i_c1_rms rms i(c1):') != -1:
            index=Lines.index(line)
            results[5]=float(Lines[index+1])
        
    
    return results


