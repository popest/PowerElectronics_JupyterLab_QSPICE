#QSPICE Circuit Generators
#This script contains collection of SPICE circuit generators
#Each generator creates netlist file compatible with Qorvo QSPICE. 
#It assumes that QSPICE is installed in its default path for non-Admin user

#Update: 18-Oct-2023

import os
import subprocess
import pandas as pd
import re

# This function generates QSPICE netlist with PFC boost converter in CCM mode with ACMC (average current mode control).
# Compensation is fixed and should satisfy all typical cases for CCM PFC (rquires verification from user ). 
# It uses simplified diode models and switch.
# The simulation stop time is 1s which satisfy both 50 and 60Hz AC input
# Load is constant power load what emulates typical use of PFC converter loaded by another DC/DC converter

#Input parameters:
#VAC_rms - RMS value of Input AC source
#Cout - value of output capacitor
#ESR - Cout ESR
#eff - Estimated efficiency
#Vout - desired Vout
#Pout - Constant power load value
#fsw - Main switch switching frequency
#freq - Input AC line frequency
#L - PFC inductor value


#Output:
#list index
    #[0] - Switch current waveform in Pandas format
    #[1][0] - Inductor RMS current
    #[1][1] - Inductor PEAK current
    #[1][2] - FET RMS current
    #[1][3] - Boost diode AVG current
    #[1][4] - Boost diode RMS current
    #[1][5] - Output Capacitor RMS ripple current
    #[1][6] - Input REC AVG current
    #[1][7] - Input REC RMS current
    #[1][8] - Output Voltage AVG value
    #[1][9] - Output Voltage pk-pk value
    #[1][10] - Input RMS current
    #[1][11] - Current-sense resistor RMS current
   

def QSPICE_PFC_CCM_ACMC(VAC_rms, Cout, ESR, eff, fsw, freq, L, Pout, Vout):

    #### Generate cir File
    f = open("PFC_CCM_ACMC.cir", "w", newline='\n')

    #### Circuit Definition ###
    f.write("* Boost PFC in CCM Mode with Average Current Mode COntrol Auto-Generated Netlist File"+"\n")
    f.write("D1 N01 N03 REC"+"\n")
    f.write("V1 N01 N02 SIN 0 {sqrt(2)*VAC_rms} {freq}"+"\n")
    f.write("D2 N02 N03 REC"+"\n")
    f.write("D3 N04 N01 REC"+"\n")
    f.write("D4 N04 N02 REC"+"\n") 
    f.write("L1 N03 N05 {L}"+"\n")
    f.write("D5 N05 OUT boostD"+"\n")
    f.write("D6 N03 OUT REC"+"\n")
    f.write("C1 OUT N13 {Cout}"+"\n")
    f.write("S1 N05 0 PWM 0 MODSW"+"\n")
    f.write("Ã1 VCC VEE N08 N07 N10 ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ RRopAmp Avol=100K GBW=50Meg Slew=5Meg Rload=2K Phi=60"+"\n")
    f.write("R2 0 N07 2.2K"+"\n")
    f.write("R3 N07 N06 2.2K"+"\n")
    f.write("C2 N06 N08 10n"+"\n")
    f.write("C3 N07 N08 220p"+"\n")
    f.write("V3 VCC 0 15"+"\n")
    f.write("V4 VEE 0 0"+"\n")
    f.write("V5 N09 0 2.5"+"\n")
    f.write("¥3 VLOG 0 PWM ¥ N08 SAW VLOG ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ HMITT VT=0 VH=1m TD=1n TRISE=10n TFALL=10n TTOL=1n"+"\n")
    f.write("V6 SAW 0 PULSE 0.1 {1/kMOD} 0 {1/fsw} 1n 1n {1/fsw+2e-9}"+"\n")
    f.write("V7 VLOG 0 1"+"\n")
    f.write("C7 N03 N04 1u"+"\n")
    f.write("D7 0 N05 ideal"+"\n")
    f.write("B2 0 N10 I=V(LINE_FWD)*V(Verr)/3*kMUL"+"\n")
    f.write("R7 N04 N10 {RCS}"+"\n")
    f.write("Ã3 VCC VEE Verr N11 N09 ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ MultGmAmp Gm=10e-6"+"\n")
    f.write("C4 N12 0 1e-6 IC=250m"+"\n")
    f.write("R4 N13 0 {ESR}"+"\n")
    f.write("G1 0 LINE_FWD N03 N04 kVin"+"\n")
    f.write("R5 LINE_FWD 0 1"+"\n")
    f.write("G2 0 N11 OUT 0 {2.5/Vout}"+"\n")
    f.write("R8 N11 0 1"+"\n")
    f.write("R6 N04 0 {RSENSE}"+"\n")
    f.write("B1 OUT 0 R=if(time>1/freq,V(out)*V(out)/{Pout/eff},0)"+"\n")
    f.write("R9 Verr N12 56K"+"\n")
    
    #### Models Definition ####
    f.write(".model MODSW SW(ron={ron_SW} roff=10Meg vt=0.5 vh=-0.05 TTOL=1n)"+"\n")
    f.write(".model REC D(Vfwd={fwd_REC},Ron={rdiff_REC},Cjo=10p)"+"\n")
    f.write(".model ideal D(Vfwd=0,Ron=1m)"+"\n")
    f.write(".model boostD D(Vfwd={fwd_boost},Ron={rdiff_boost})"+"\n")
    f.write(".lib Diode.txt"+"\n")
    
    #### Spice Options ####
    f.write(".tran 0 {TSTOP} {TSTART} {TSTEP}"+"\n")
    f.write(".options savepowers=1"+"\n")
    f.write(".options trtol=1"+"\n")

    #### Parameters ####
    f.write(".param TSTART={TSTOP-1/freq}"+"\n")
    f.write(".param TSTOP=1"+"\n")
    f.write(".param TSTEP={(1/fsw)/30}"+"\n")
    
    f.write(".param kVin=600e-6"+"\n")
    f.write(".param Rsense=50e-3"+"\n")
    f.write(".param RCS=2.8K"+"\n")
    f.write(".param kMUL=0.0035"+"\n")
    f.write(".param kMOD=0.5"+"\n")
    f.write(".param FWD_REC=0"+"\n")
    f.write(".param RDIFF_REC=1m"+"\n")
    f.write(".param FWD_BOOST=0"+"\n")
    f.write(".param RDIFF_BOOST=1m"+"\n")
    f.write(".param RON_SW=1m"+"\n")
    
    f.write(".param eff="+str(eff)+"\n")
    f.write(".param Pout="+str(Pout)+"\n")
    f.write(".param Vout="+str(Vout)+"\n")
    f.write(".param fsw="+str(fsw)+"\n")
    f.write(".param ESR="+str(ESR)+"\n")
    f.write(".param Cout="+str(Cout)+"\n")
    f.write(".param L="+str(L)+"\n")
    f.write(".param VAC_rms="+str(VAC_rms)+"\n")
    f.write(".param freq="+str(freq)+"\n")
    
    #### Measurement Definition ####
    f.write(".meas I_L_RMS rms I(L1)"+"\n")
    f.write(".meas I_L_peak max I(L1)"+"\n")
    f.write(".meas I_FET_RMS rms I(S1)"+"\n")
    f.write(".meas I_BOOST_AVG avg I(D5)"+"\n")
    f.write(".meas I_BOOST_RMS rms I(D5)"+"\n")
    f.write(".meas I_COUT_RMS rms I(C1)"+"\n")
    f.write(".meas I_REC_AVG avg I(D1)"+"\n")
    f.write(".meas I_REC_RMS rms I(D1)"+"\n")
    f.write(".meas Vout_AVG avg V(out)"+"\n")
    f.write(".meas Vout_pk_pk pp V(out)"+"\n")
    f.write(".meas I_VIN_RMS rms I(V1)"+"\n")
    f.write(".meas I_RSENSE rms I(R6)"+"\n")
    
      
    f.write(".end")
       
    f.close()
    
    
    #Assume that QSPICE is installed in its default path for non-Admin user
    exe_qspice64=os.path.expanduser(r"~\QSPICE\QSPICE64.exe")
    exe_qpost=os.path.expanduser(r"~\QSPICE\QPOST.exe")
    exe_qux=os.path.expanduser(r"~\QSPICE\QUX.exe")
    
    #run QSPICE Simulation
    result=subprocess.run([exe_qspice64, "PFC_CCM_ACMC.cir"])
  #  print(result)

    #Run postprocess measurement  
    result=subprocess.run([exe_qpost, "PFC_CCM_ACMC.cir", "-o","results.txt"] )
    #print(result)
    
    #Run postprocess waveform extraction
    result=subprocess.run([exe_qux, "-Export", "PFC_CCM_ACMC.qraw", "V(pwm),I(S1),V(OUT),I(L1)", "all", "CSV"])
  
        
    #print(result.stdout)

    

    df = pd.read_csv('PFC_CCM_ACMC.csv')

    f = open("results.txt", "r")
    Lines = f.readlines()
    f.close()
    
    #Delete Results
    subprocess.run(["del", "PFC_CCM_ACMC.qraw"], shell=True)
  #  print(result)
    
    #Delete Netlist
    subprocess.run(["del", "PFC_CCM_ACMC.cir"], shell=True)
  #  print(result)

    #Delete QPOST Results
    subprocess.run(["del", "results.txt"], shell=True)
  #  print(result)

    #Delete Exported Waveforms
    subprocess.run(["del", "PFC_CCM_ACMC.csv"], shell=True)
  #  print(result)
    results = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for line in Lines:
        # Assign results in required order into the list
        if line.find('.meas i_l_rms rms i(l1):') != -1:
            index=Lines.index(line)
            results[0]=float(Lines[index+1])
        elif line.find('.meas i_l_peak max i(l1):') != -1:
            index=Lines.index(line)
            str_line = Lines[index+1]
            numbers = re.search(r'[-+]?\d*\.\d+|\d+',str_line) #extract first number in string
            results[1]=float(numbers[0])
        elif line.find('.meas i_fet_rms rms i(s1):') != -1:
            index=Lines.index(line)
            results[2]=float(Lines[index+1])           
        elif line.find('.meas i_boost_avg avg i(d5):') != -1:
            index=Lines.index(line)
            results[3]=float(Lines[index+1])
        elif line.find('.meas i_boost_rms rms i(d5):') != -1:
            index=Lines.index(line)
            results[4]=float(Lines[index+1])
        elif line.find('.meas i_cout_rms rms i(c1):') != -1:
            index=Lines.index(line)
            results[5]=float(Lines[index+1])
        elif line.find('.meas i_rec_avg avg i(d1):') != -1:
            index=Lines.index(line)
            results[6]=float(Lines[index+1])
        elif line.find('.meas i_rec_rms rms i(d1):') != -1:
            index=Lines.index(line)
            results[7]=float(Lines[index+1])
        elif line.find('.meas vout_avg avg v(out):') != -1:
            index=Lines.index(line)
            results[8]=float(Lines[index+1])
        elif line.find('.meas vout_pk_pk pp v(out):') != -1:
            index=Lines.index(line)
            results[9]=float(Lines[index+1])
        elif line.find('.meas i_vin_rms rms i(v1):') != -1:
            index=Lines.index(line)
            results[10]=float(Lines[index+1])
        elif line.find('.meas i_rsense rms i(r6):') != -1:
            index=Lines.index(line)
            results[11]=float(Lines[index+1])    
        
    
    return [df, results]


