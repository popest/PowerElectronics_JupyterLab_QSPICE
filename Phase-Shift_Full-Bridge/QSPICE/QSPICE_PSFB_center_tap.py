#This file was autogenerated on 2025-02-01 00:10:07
import os
import subprocess
import pandas as pd
import re

def QSPICE_PSFB_center_tap(Coss, Cout_ESR, D, deadtime, eff, fsw_p, Iout_max, L_leak, Lout, Lp, Lr, N, Pmax, Rdiff, REC_fwd, Ron_MOS, Vin, Vout, export_traces = None):
    if export_traces is None:
         export_traces = [] 
    #### Create circuit file ####
    f = open("PSFB_center_tap.cir", "w", newline="\n")

    #### Circuit Definition ####
    f.write("* Auto-Generated Netlist File" + "\n")
    f.write("V3 Vlog 0 1" + "\n")
    f.write("S1 VIN CD high_C 0 MODSW" + "\n")
    f.write("S3 CD 0 low_D 0 MODSW" + "\n")
    f.write("S2 VIN AB high_A 0 MODSW" + "\n")
    f.write("S4 AB 0 low_B 0 MODSW" + "\n")
    f.write("L1 N02 N01 {Lp} RSER = {I_Res_Lprim}" + "\n")
    f.write("L2 N14 0 {I_Ls} RSER={I_Res_Lsec}" + "\n")
    f.write("Lout N03 Vout {Lout}" + "\n")
    f.write("R1 N07 0 {Cout_ESR}" + "\n")
    f.write("L5 AB N01 {L_leak}" + "\n")
    f.write("D7 CD VIN ideal_MOS" + "\n")
    f.write("D4 0 CD ideal_MOS" + "\n")
    f.write("D6 AB VIN ideal_MOS" + "\n")
    f.write("D8 0 AB ideal_MOS" + "\n")
    f.write("V´I_SENSE N04 VIN 0" + "\n")
    f.write("¥2 Vlog 0 A B B N06 0 0 ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ D-FLOP TTOL = {I_ttol_factor/fsw_p}" + "\n")
    f.write("¥1 Vlog 0 C D D N05 0 0 ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ D-FLOP TTOL = {I_ttol_factor/fsw_p}" + "\n")
    f.write("V6 N13 0 {1-D}" + "\n")
    f.write("¥3 Vlog 0 N05 N06 N13 RAMP Vlog ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ HMITT VH=2m TTOL={I_ttol_factor/fsw_p}" + "\n")
    f.write("¥4 Vlog 0 low_B ¥ N09 B ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ AND TTOL={I_ttol_factor/fsw_p}" + "\n")
    f.write("¥6 Vlog 0 high_A ¥ A N08 ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ AND TTOL={I_ttol_factor/fsw_p}" + "\n")
    f.write("¥7 Vlog 0 N08 N09 A ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ OR TD={deadtime} TTOL = {I_ttol_factor/fsw_p}" + "\n")
    f.write("¥8 Vlog 0 low_D ¥ N11 D ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ AND TTOL={I_ttol_factor/fsw_p}" + "\n")
    f.write("¥9 Vlog 0 high_C ¥ C N10 ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ AND TTOL={I_ttol_factor/fsw_p}" + "\n")
    f.write("¥10 Vlog 0 N10 N11 C ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ OR TD={deadtime} TTOL = {I_ttol_factor/fsw_p}" + "\n")
    f.write("R3 N12 N03 {I_Res_Lout}" + "\n")
    f.write("V9 N04 0 {Vin}" + "\n")
    f.write("Rload Vout 0 {max(Vout/(Pmax/Vout),Vout/Iout_max)}" + "\n")
    f.write("V1 Vout N07 {Vout}" + "\n")
    f.write("V2 RAMP 0 PULSE 1 0 0 {(I_ttol_factor*10)/(2*fsw_p)} {(1-I_ttol_factor*10)/(2*fsw_p)} 0 {1/(2*fsw_p)}" + "\n")
    f.write("L9 CD N02 {Lr} RSER = {I_Res_Lr} IC=0" + "\n")
    f.write("D1 N14 N12 ideal_REC" + "\n")
    f.write("D3 N15 N12 ideal_REC" + "\n")
    f.write("L3 0 N15 {I_Ls} RSER={I_Res_Lsec}" + "\n")
    f.write("K2 L1 L2 L3 1" + "\n")

    #### Parameters ####
    f.write(".param Lp=" + str(Lp) + "\n")
    f.write(".param N=" + str(N) + "\n")
    f.write(".param fsw_p=" + str(fsw_p) + "\n")
    f.write(".param Lr=" + str(Lr) + "\n")
    f.write(".param Lout=" + str(Lout) + "\n")
    f.write(".param Vout=" + str(Vout) + "\n")
    f.write(".param D=" + str(D) + "\n")
    f.write(".param Vin=" + str(Vin) + "\n")
    f.write(".param Iout_max=" + str(Iout_max) + "\n")
    f.write(".param Pmax=" + str(Pmax) + "\n")
    f.write(".param L_leak=" + str(L_leak) + "\n")
    f.write(".param Ron_MOS=" + str(Ron_MOS) + "\n")
    f.write(".param deadtime=" + str(deadtime) + "\n")
    f.write(".param Rdiff=" + str(Rdiff) + "\n")
    f.write(".param eff=" + str(eff) + "\n")
    f.write(".param Coss=" + str(Coss) + "\n")
    f.write(".param REC_fwd=" + str(REC_fwd) + "\n")
    f.write(".param Cout_ESR=" + str(Cout_ESR) + "\n")
    f.write(".param I_Ls={Lp/N^2}" + "\n")
    f.write(".param TSTEP={(1/(2*fsw_p))/100}" + "\n")
    f.write(".param TSTOP={5000*1/(2*fsw_p)}" + "\n")
    f.write(".param TSTART={TSTOP-6/(2*fsw_p)}" + "\n")
    f.write(".param I_Iout = (Pmax/eff)/Vout" + "\n")
    f.write(".param I_Res_Lr=1m" + "\n")
    f.write(".param I_Res_Lprim=1m" + "\n")
    f.write(".param I_Res_Lsec=1m" + "\n")
    f.write(".param I_ttol_factor = 0.0001" + "\n")
    f.write(".param I_Res_Lout = 1m" + "\n")

    #### Models ####
    f.write(".model ideal_MOS D(Vfwd=0.7,Ron={Ron_MOS}, Roff=10Meg)" + "\n")
    f.write(".model MODSW SW(ron={Ron_MOS} roff=100Meg vt=0.5 vh=-0.05 )" + "\n")
    f.write(".model ideal_REC D(Vfwd={REC_fwd},Ron={Rdiff}, Roff=10Meg)" + "\n")

    #### Spice Options ####
    f.write(".options trtol=1" + "\n")
    f.write(".options maxord=1" + "\n")
    f.write(".options savepowers" + "\n")

    #### Measurement Definition ####
    f.write(".meas I_Lout_AVG avg I(Lout)" + "\n") # results[0]
    f.write(".meas I_Rload_AVG avg I(Rload)" + "\n") # results[1]
    f.write(".meas P_Rload_AVG avg P(Rload)" + "\n") # results[2]
    f.write(".meas P_Vin_AVG avg P(V9)" + "\n") # results[3]
    f.write(".meas V_Vout_AVG avg V(Vout)" + "\n") # results[4]
    f.write(".meas I_S2_RMS rms I(S2)" + "\n") # results[5]
    f.write(".meas I_Lout_PP PP I(Lout)" + "\n") # results[6]
    f.write(".meas V_Vout_PP PP V(Vout)" + "\n") # results[7]
    f.write(".meas I_S1_RMS rms I(S1)" + "\n") # results[8]
    f.write(".meas I_Lprim_AVG avg I(L1)" + "\n") # results[9]
    f.write(".meas I_Lprim_RMS rms I(L1)" + "\n") # results[10]
    f.write(".meas I_Lout_RMS rms I(Lout)" + "\n") # results[11]
    f.write(".meas I_Lsec1_AVG avg I(L2)" + "\n") # results[12]
    f.write(".meas I_Lsec1_RMS rms I(L2)" + "\n") # results[13]
    f.write(".meas I_Lsec2_AVG avg I(L3)" + "\n") # results[14]
    f.write(".meas I_Lsec2_RMS rms I(L3)" + "\n") # results[15]
    f.write(".meas L_res_point FIND I(L9) WHEN V(low_b)=0.5 cross=last" + "\n") # results[16]
    f.write(".meas I_Lprim_pp pp I(L1)" + "\n") # results[17]
    f.write(".meas I_sense_RMS rms I(I_SENSE)" + "\n") # results[18]
    f.write(".meas I_sense_AVG avg I(I_SENSE)" + "\n") # results[19]

    #### SPICE Analysis ####
    f.write(".tran 0 {TSTOP} {TSTART} {TSTEP}" + "\n")

    f.write(".end")

    f.close()
    results = { 
        "I_Lout_AVG": 0,
        "I_Rload_AVG": 0,
        "P_Rload_AVG": 0,
        "P_Vin_AVG": 0,
        "V_Vout_AVG": 0,
        "I_S2_RMS": 0,
        "I_Lout_PP": 0,
        "V_Vout_PP": 0,
        "I_S1_RMS": 0,
        "I_Lprim_AVG": 0,
        "I_Lprim_RMS": 0,
        "I_Lout_RMS": 0,
        "I_Lsec1_AVG": 0,
        "I_Lsec1_RMS": 0,
        "I_Lsec2_AVG": 0,
        "I_Lsec2_RMS": 0,
        "L_res_point": 0,
        "I_Lprim_pp": 0,
        "I_sense_RMS": 0,
        "I_sense_AVG": 0,
    }
    # Assume that QSPICE is installed in its default path for non-Admin user
    exe_qspice64 = os.path.expanduser(r"~\QSPICE\QSPICE64.exe")
    exe_qpost = os.path.expanduser(r"~\QSPICE\QPOST.exe")
    exe_qux = os.path.expanduser(r"~\QSPICE\QUX.exe")

    # run QSPICE Simulation
    run_qspice64 = subprocess.run([exe_qspice64, "PSFB_center_tap.cir"])

    # Run postprocess measurement
    run_qpost = subprocess.run([exe_qpost, "PSFB_center_tap.cir", "-o", "results.txt"])

    f = open("results.txt", "r")
    results_lines = f.readlines()
    f.close()

    # Run postprocess waveforms extraction
    df = 0 
    if export_traces:
        run_qux = subprocess.run([exe_qux, "-Export", "PSFB_center_tap.qraw", export_traces, "all", "CSV"])
        df = pd.read_csv("PSFB_center_tap.csv") 
        df.columns = df.columns.str.lower() 

        #Delete Exported Waveforms CSV File 
        subprocess.run(["del", "PSFB_center_tap.csv"], shell=True) 

    # Delete Results
    subprocess.run(["del", "PSFB_center_tap.qraw"], shell=True)

    # Delete Netlist
    subprocess.run(["del", "PSFB_center_tap.cir"], shell=True)

    # Delete QPOST Results
    subprocess.run(["del", "results.txt"], shell=True)
    for i, line in enumerate(results_lines):
        stripped_line = line.strip()
        match stripped_line:
            case ".meas i_lout_avg avg i(lout):": 
                results['I_Lout_AVG'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas i_rload_avg avg i(rload):": 
                results['I_Rload_AVG'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas p_rload_avg avg p(rload):": 
                results['P_Rload_AVG'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas p_vin_avg avg p(v9):": 
                results['P_Vin_AVG'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas v_vout_avg avg v(vout):": 
                results['V_Vout_AVG'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas i_s2_rms rms i(s2):": 
                results['I_S2_RMS'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas i_lout_pp pp i(lout):": 
                results['I_Lout_PP'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas v_vout_pp pp v(vout):": 
                results['V_Vout_PP'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas i_s1_rms rms i(s1):": 
                results['I_S1_RMS'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas i_lprim_avg avg i(l1):": 
                results['I_Lprim_AVG'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas i_lprim_rms rms i(l1):": 
                results['I_Lprim_RMS'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas i_lout_rms rms i(lout):": 
                results['I_Lout_RMS'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas i_lsec1_avg avg i(l2):": 
                results['I_Lsec1_AVG'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas i_lsec1_rms rms i(l2):": 
                results['I_Lsec1_RMS'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas i_lsec2_avg avg i(l3):": 
                results['I_Lsec2_AVG'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas i_lsec2_rms rms i(l3):": 
                results['I_Lsec2_RMS'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas l_res_point find i(l9) when v(low_b)=0.5 cross=last:": 
                results['L_res_point'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas i_lprim_pp pp i(l1):": 
                results['I_Lprim_pp'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas i_sense_rms rms i(i_sense):": 
                results['I_sense_RMS'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas i_sense_avg avg i(i_sense):": 
                results['I_sense_AVG'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

    return [df,results]