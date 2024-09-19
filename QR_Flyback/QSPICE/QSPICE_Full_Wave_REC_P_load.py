#This file was autogenerated on 2024-09-17 00:49:00
import os
import subprocess
import pandas as pd

def QSPICE_Full_Wave_REC_P_load(Cf, ESR, freq, fwd, Pin, rdiff, VAC_rms, export_traces = None):
    if export_traces is None:
         export_traces = [] 
    #### Create circuit file ####
    f = open("Full_Wave_REC_P_load.cir", "w", encoding="ascii", newline="\n")

    #### Circuit Definition ####
    f.write("* Auto-Generated Netlist File" + "\n")
    f.write("D1 N01 out REC" + "\n")
    f.write("D2 N02 out REC" + "\n")
    f.write("D3 0 N02 REC" + "\n")
    f.write("D4 0 N01 REC" + "\n")
    f.write("V1 N01 N02 SIN 0 {sqrt(2)*VAC_rms} {freq}" + "\n")
    f.write("C1 N03 0 {Cf}" + "\n")
    f.write("B1 out 0 R=if(time>2/freq,(V(out)*V(out))/{Pin},0)" + "\n")
    f.write("R1 out N03 {ESR}" + "\n")

    #### Parameters ####
    f.write(".param Pin=" + str(Pin) + "\n")
    f.write(".param Cf=" + str(Cf) + "\n")
    f.write(".param VAC_rms=" + str(VAC_rms) + "\n")
    f.write(".param fwd=" + str(fwd) + "\n")
    f.write(".param rdiff=" + str(rdiff) + "\n")
    f.write(".param freq=" + str(freq) + "\n")
    f.write(".param ESR=" + str(ESR) + "\n")
    f.write(".param TSTEP = {(1/freq)/1000}" + "\n")
    f.write(".param TSTOP = {600*1/freq}" + "\n")
    f.write(".param TSTART = {TSTOP-6/freq}" + "\n")

    #### Models ####
    f.write(".model REC D(Vfwd={fwd},Ron={rdiff},Cjo=10p)" + "\n")

    #### Spice Options ####
    f.write(".options savepowers=1" + "\n")
    f.write(".options trtol=1" + "\n")

    #### Measurement Definition ####
    f.write(".meas I_AC_RMS rms I(V1)" + "\n") # results[0]
    f.write(".meas I_D_RMS rms I(D1)" + "\n") # results[1]
    f.write(".meas I_D_AVG avg I(D1)" + "\n") # results[2]
    f.write(".meas Pd avg P(D1)" + "\n") # results[3]
    f.write(".meas I_Cin_RMS rms I(C1)" + "\n") # results[4]
    f.write(".meas VOUT_AVG AVG V(out)" + "\n") # results[5]

    #### SPICE Analysis ####
    f.write(".tran 0 TSTOP TSTART TSTEP" + "\n")

    f.write(".end")

    f.close()
    results = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    # Assume that QSPICE is installed in its default path for non-Admin user
    exe_qspice64 = os.path.expanduser(r"~\QSPICE\QSPICE64.exe")
    exe_qpost = os.path.expanduser(r"~\QSPICE\QPOST.exe")
    exe_qux = os.path.expanduser(r"~\QSPICE\QUX.exe")

    # run QSPICE Simulation
    run_qspice64 = subprocess.run([exe_qspice64, "Full_Wave_REC_P_load.cir"])

    # Run postprocess measurement
    run_qpost = subprocess.run([exe_qpost, "Full_Wave_REC_P_load.cir", "-o", "results.txt"])

    f = open("results.txt", "r")
    results_lines = f.readlines()
    f.close()

    # Run postprocess waveforms extraction
    df = 0 
    if export_traces:
        run_qux = subprocess.run([exe_qux, "-Export", "Full_Wave_REC_P_load.qraw", export_traces, "all", "CSV"])
        df = pd.read_csv("Full_Wave_REC_P_load.csv") 
        df.columns = df.columns.str.lower() 

        #Delete Exported Waveforms CSV File 
        subprocess.run(["del", "Full_Wave_REC_P_load.csv"], shell=True) 

    # Delete Results
    subprocess.run(["del", "Full_Wave_REC_P_load.qraw"], shell=True)

    # Delete Netlist
    subprocess.run(["del", "Full_Wave_REC_P_load.cir"], shell=True)

    # Delete QPOST Results
    subprocess.run(["del", "results.txt"], shell=True)
    for i, line in enumerate(results_lines):
        stripped_line = line.strip()
        match stripped_line:
            case ".meas i_ac_rms rms i(v1):": 
                results[0] = float(results_lines[i + 1])

            case ".meas i_d_rms rms i(d1):": 
                results[1] = float(results_lines[i + 1])

            case ".meas i_d_avg avg i(d1):": 
                results[2] = float(results_lines[i + 1])

            case ".meas pd avg p(d1):": 
                results[3] = float(results_lines[i + 1])

            case ".meas i_cin_rms rms i(c1):": 
                results[4] = float(results_lines[i + 1])

            case ".meas vout_avg avg v(out):": 
                results[5] = float(results_lines[i + 1])

    return [df,results]