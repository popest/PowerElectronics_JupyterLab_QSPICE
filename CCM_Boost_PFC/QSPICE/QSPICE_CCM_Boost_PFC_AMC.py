#This file was autogenerated on 2024-11-28 22:01:00
import os
import subprocess
import pandas as pd
import re

def QSPICE_CCM_Boost_PFC_AMC(Cfp_I, Cfp_V, Cfz_I, Cfz_V, Cout, eff, ESR, freq, fsw, L, Pout, Rf_I, Rf_V, Vin_rms, Vout, export_traces = None):
    if export_traces is None:
         export_traces = [] 
    #### Create circuit file ####
    f = open("CCM_Boost_PFC_AMC.cir", "w", newline="\n")

    #### Circuit Definition ####
    f.write("* Auto-Generated Netlist File" + "\n")
    f.write("D1 N01 N04 REC" + "\n")
    f.write("V1 N03 N02 SIN 0 {Vin_rms*sqrt(2)} {freq}" + "\n")
    f.write("D2 N02 N04 REC" + "\n")
    f.write("D3 N05 N01 REC" + "\n")
    f.write("D4 N05 N02 REC" + "\n")
    f.write("L1 N14 N06 {L}" + "\n")
    f.write("D5 N06 OUT boostD" + "\n")
    f.write("D6 N04 OUT REC" + "\n")
    f.write("C1 OUT N12 {Cout} IC=0" + "\n")
    f.write("S1 N06 0 PWM 0 MODSW" + "\n")
    f.write("R2 N10 N08 1K" + "\n")
    f.write("R3 N08 N07 {Rf_I}" + "\n")
    f.write("C2 N07 N09 {Cfz_I}" + "\n")
    f.write("C3 N08 N09 {Cfp_I}" + "\n")
    f.write("V3 VCC 0 15" + "\n")
    f.write("V4 VEE 0 0" + "\n")
    f.write("¥3 VLOG 0 PWM ¥ N09 SAW VLOG ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ ¥ HMITT TTOL={I_ttol_factor/fsw} VH=2m" + "\n")
    f.write("V7 VLOG 0 1" + "\n")
    f.write("C7 N04 N15 1µ" + "\n")
    f.write("D7 0 N06 ideal" + "\n")
    f.write("B2 0 N11 I=V(LINE_FWD)*V(Verr)" + "\n")
    f.write("R4 N12 0 {ESR}" + "\n")
    f.write("G1 0 LINE_FWD N04 N05 I_kVin" + "\n")
    f.write("R5 LINE_FWD 0 1" + "\n")
    f.write("G2 0 N13 OUT 0 {I_Vref/Vout}" + "\n")
    f.write("R8 N13 0 1" + "\n")
    f.write("R1 OUT 0 {Vout*Vout/(Pout/eff)}" + "\n")
    f.write("V2 N03 N01 0" + "\n")
    f.write("V8 SAW 0 PULSE {1/I_kMOD} 0 0 {(I_ttol_factor*10)/fsw} {(1-I_ttol_factor*10)/fsw} 0 {1/fsw}" + "\n")
    f.write("R10 N04 N14 {I_Res_L}" + "\n")
    f.write("R11 N15 N05 1m" + "\n")
    f.write("H1 N10 0 L1 {I_Ri}" + "\n")
    f.write("R6 N11 0 1" + "\n")
    f.write("R12 N13 N16 10K" + "\n")
    f.write("R13 N16 N17 {Rf_V}" + "\n")
    f.write("C6 N17 Verr {Cfz_V}" + "\n")
    f.write("C8 N16 Verr {Cfp_V}" + "\n")
    f.write("D8 Verr VCC ideal" + "\n")
    f.write("D9 0 Verr ideal" + "\n")
    f.write("D10 N09 VCC ideal" + "\n")
    f.write("D11 0 N09 ideal" + "\n")
    f.write("G3 0 N09 N11 N08 100K" + "\n")
    f.write("R14 N09 0 1" + "\n")
    f.write("C4 N09 0 100K/10Meg/2/pi" + "\n")
    f.write("G4 0 Verr N18 N16 100K" + "\n")
    f.write("R9 Verr 0 1" + "\n")
    f.write("C5 Verr 0 100K/10Meg/2/pi" + "\n")
    f.write("I1 0 N18 1µ" + "\n")
    f.write("R15 N18 0 {I_Vref/1e-6}" + "\n")
    f.write("C9 N18 0 20n IC=0" + "\n")
    f.write("V5 0 N05 0" + "\n")

    #### Parameters ####
    f.write(".param eff=" + str(eff) + "\n")
    f.write(".param Pout=" + str(Pout) + "\n")
    f.write(".param Vout=" + str(Vout) + "\n")
    f.write(".param fsw=" + str(fsw) + "\n")
    f.write(".param ESR=" + str(ESR) + "\n")
    f.write(".param Cout=" + str(Cout) + "\n")
    f.write(".param L=" + str(L) + "\n")
    f.write(".param Vin_rms=" + str(Vin_rms) + "\n")
    f.write(".param freq=" + str(freq) + "\n")
    f.write(".param Cfp_I=" + str(Cfp_I) + "\n")
    f.write(".param Rf_I=" + str(Rf_I) + "\n")
    f.write(".param Cfz_I=" + str(Cfz_I) + "\n")
    f.write(".param Cfp_V=" + str(Cfp_V) + "\n")
    f.write(".param Rf_V=" + str(Rf_V) + "\n")
    f.write(".param Cfz_V=" + str(Cfz_V) + "\n")
    f.write(".param I_kVin={1.5/(sqrt(2)*Vin_RMS)}" + "\n")
    f.write(".param I_kMOD=0.2" + "\n")
    f.write(".param I_fwd_REC=0" + "\n")
    f.write(".param I_rdiff_REC=0.1e-3" + "\n")
    f.write(".param I_ron_SW=0.1e-3" + "\n")
    f.write(".param I_fwd_boost=0" + "\n")
    f.write(".param I_rdiff_boost=0.1e-3" + "\n")
    f.write(".param TSTART={TSTOP-1/freq}" + "\n")
    f.write(".param TSTOP={1}" + "\n")
    f.write(".param TSTEP={(1/fsw)/50}" + "\n")
    f.write(".param I_ttol_factor = 0.0001" + "\n")
    f.write(".param I_Res_L=0.1m" + "\n")
    f.write(".param I_Vref = 2.5" + "\n")
    f.write(".param I_D = -Vin_rms / Vout + 1" + "\n")
    f.write(".param I_IL_peak = sqrt(2) * Pout * (1 + (-sqrt(2) * Vin_RMS ** 3 + Vin_RMS ** 2 * Vout) / L / Pout / Vout / fsw / 2) / eff / Vin_RMS" + "\n")
    f.write(".param I_Ri = 1/I_IL_peak" + "\n")

    #### Models ####
    f.write(".model REC D(Vfwd={I_fwd_REC},Ron={I_rdiff_REC}, Roff = 10Meg, Cjo=10p)" + "\n")
    f.write(".model ideal D(Vfwd=0,Ron=1m, Roff=10Meg)" + "\n")
    f.write(".model boostD D(Vfwd={I_fwd_boost},Ron={I_rdiff_boost}, Roff = 10Meg)" + "\n")
    f.write(".model MODSW SW(ron={I_ron_SW} roff=10Meg vt=0.5 vh=-0.05 )" + "\n")

    #### Spice Options ####
    f.write(".options trtol=1" + "\n")

    #### Measurement Definition ####
    f.write(".meas I_L_RMS rms I(L1)" + "\n") # results[0]
    f.write(".meas I_Dboost_RMS rms I(D5)" + "\n") # results[1]
    f.write(".meas I_L_PEAK max I(L1)" + "\n") # results[2]
    f.write(".meas I_FET_RMS rms I(S1)" + "\n") # results[3]
    f.write(".meas I_Dboost_AVG avg I(D5)" + "\n") # results[4]
    f.write(".meas I_Cout_RMS rms I(C1)" + "\n") # results[5]
    f.write(".meas I_REC_RMS rms I(D1)" + "\n") # results[6]
    f.write(".meas I_REC_AVG avg I(D1)" + "\n") # results[7]
    f.write(".meas V_Cout_MAX max V(out)" + "\n") # results[8]
    f.write(".meas I_IN_RMS rms I(V1)" + "\n") # results[9]
    f.write(".meas I_RSENSE_RMS rms I(V5)" + "\n") # results[10]

    #### SPICE Analysis ####
    f.write(".tran 0 {TSTOP} {TSTART} {TSTEP}" + "\n")

    f.write(".end")

    f.close()
    results = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    # Assume that QSPICE is installed in its default path for non-Admin user
    exe_qspice64 = os.path.expanduser(r"~\QSPICE\QSPICE64.exe")
    exe_qpost = os.path.expanduser(r"~\QSPICE\QPOST.exe")
    exe_qux = os.path.expanduser(r"~\QSPICE\QUX.exe")

    # run QSPICE Simulation
    run_qspice64 = subprocess.run([exe_qspice64, "CCM_Boost_PFC_AMC.cir"])

    # Run postprocess measurement
    run_qpost = subprocess.run([exe_qpost, "CCM_Boost_PFC_AMC.cir", "-o", "results.txt"])

    f = open("results.txt", "r")
    results_lines = f.readlines()
    f.close()

    # Run postprocess waveforms extraction
    df = 0 
    if export_traces:
        run_qux = subprocess.run([exe_qux, "-Export", "CCM_Boost_PFC_AMC.qraw", export_traces, "all", "CSV"])
        df = pd.read_csv("CCM_Boost_PFC_AMC.csv") 
        df.columns = df.columns.str.lower() 

        #Delete Exported Waveforms CSV File 
        subprocess.run(["del", "CCM_Boost_PFC_AMC.csv"], shell=True) 

    # Delete Results
    subprocess.run(["del", "CCM_Boost_PFC_AMC.qraw"], shell=True)

    # Delete Netlist
    subprocess.run(["del", "CCM_Boost_PFC_AMC.cir"], shell=True)

    # Delete QPOST Results
    subprocess.run(["del", "results.txt"], shell=True)
    for i, line in enumerate(results_lines):
        stripped_line = line.strip()
        match stripped_line:
            case ".meas i_l_rms rms i(l1):": 
                results[0] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas i_dboost_rms rms i(d5):": 
                results[1] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas i_l_peak max i(l1):": 
                results[2] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas i_fet_rms rms i(s1):": 
                results[3] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas i_dboost_avg avg i(d5):": 
                results[4] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas i_cout_rms rms i(c1):": 
                results[5] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas i_rec_rms rms i(d1):": 
                results[6] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas i_rec_avg avg i(d1):": 
                results[7] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas v_cout_max max v(out):": 
                results[8] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas i_in_rms rms i(v1):": 
                results[9] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas i_rsense_rms rms i(v5):": 
                results[10] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

    return [df,results]