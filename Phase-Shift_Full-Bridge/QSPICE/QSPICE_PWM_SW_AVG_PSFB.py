#This file was autogenerated on 2025-04-30 00:12:46
import os
import subprocess
import pandas as pd
import re
import sys

def QSPICE_PWM_SW_AVG_PSFB(Cout, Cout_ESR_max, fc, fsw, Iout_max, Lout, N, Pout_lim, Vin, Vout, export_traces = None):
    if export_traces is None:
         export_traces = [] 
    #### Create circuit file ####
    cir_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "PWM_SW_AVG_PSFB.cir")
    results_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "results.txt")
    csv_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "PWM_SW_AVG_PSFB.csv")
    base_dir = os.path.dirname(os.path.realpath(__file__))
    f = open(cir_file_path, "w", newline="\n")

    #### Circuit Definition ####
    f.write("* Auto-Generated Netlist File" + "\n")
    f.write("V1 N01 0 {Vin}" + "\n")
    f.write("V2 N05 0 AC 1 0" + "\n")
    f.write("L1 N04 OUT {Lout}" + "\n")
    f.write("C1 OUT N02 {Cout}" + "\n")
    f.write("R1 N02 0 {Cout_ESR_max}" + "\n")
    f.write("R2 OUT 0 {max(Vout/(Pout_lim/Vout),Vout/Iout_max)}" + "\n")
    f.write("×1 «N03 0 N04 0» Turns=1 {N}" + "\n")
    f.write("L2 vc N07 1K" + "\n")
    f.write("C2 vc N05 1K" + "\n")
    f.write("G2 0 N06 OUT 0 {I_Vref/Vout}" + "\n")
    f.write("R3 N06 0 1" + "\n")
    f.write("V4 N08 0 2.5" + "\n")
    f.write("E1 N07 0 N08 N06 30000" + "\n")
    f.write("X1 N01 0 vc N03 PWM_SW_AVG_model params: L=I_L f=I_fsec ks=I_ks vr=I_uramp" + "\n")
    f.write("V3 ks 0 AC {I_ks} 0" + "\n")
    f.write("V5 kr 0 AC {I_uramp} 0" + "\n")

    #### Parameters ####
    f.write(".param N=" + str(N) + "\n")
    f.write(".param Lout=" + str(Lout) + "\n")
    f.write(".param Cout=" + str(Cout) + "\n")
    f.write(".param Cout_ESR_max=" + str(Cout_ESR_max) + "\n")
    f.write(".param Vout=" + str(Vout) + "\n")
    f.write(".param Vin=" + str(Vin) + "\n")
    f.write(".param fsw=" + str(fsw) + "\n")
    f.write(".param fc=" + str(fc) + "\n")
    f.write(".param Pout_lim=" + str(Pout_lim) + "\n")
    f.write(".param Iout_max=" + str(Iout_max) + "\n")
    f.write(".param I_fsec= {fsw*2}" + "\n")
    f.write(".param I_L = {Lout/(N*N)}" + "\n")
    f.write(".param I_uramp = if(I_Dccm < I_Ddcm,if(I_Dccm>0.45,I_Se/I_fsec,0),0)" + "\n")
    f.write(".param I_R_load = {max(Vout/(Pout_lim/Vout),Vout/Iout_max)}" + "\n")
    f.write(".param I_Vref = 2.5" + "\n")
    f.write(".param I_Vac = Vin - Vout/N" + "\n")
    f.write(".param I_ic = Vout/I_R_load * N" + "\n")
    f.write(".param I_R = I_R_load / (N*N)" + "\n")
    f.write(".param I_Dccm = (Vout/N)/Vin" + "\n")
    f.write(".param I_K = I_L/I_R*I_fsec" + "\n")
    f.write(".param I_Ddcm = sqrt(0.2e1) * sqrt(I_K / Vin / (Vin - Vout / N)) * Vout / N" + "\n")
    f.write(".param I_D = min(I_Dccm, I_Ddcm)" + "\n")
    f.write(".param I_vc = 1" + "\n")
    f.write(".param I_ks = if(I_Dccm < I_Ddcm, I_ks_ccm, I_ks_dcm)" + "\n")
    f.write(".param I_Vcp = Vout/N" + "\n")
    f.write(".param I_S2 = I_Vcp/I_L * I_ks" + "\n")
    f.write(".param I_Se = 0.5*I_S2" + "\n")
    f.write(".param I_ks_ccm = (2 * I_vc * I_L * I_fsec) / (2 * I_L * I_fsec * I_ic + I_Dccm * I_Vac)" + "\n")
    f.write(".param I_ks_dcm = (I_vc * I_L * I_fsec / I_Ddcm) / I_Vac" + "\n")

    #### Models ####

    #### Libs ####
    f.write(".lib PWM_SW_AVG_model.lib" + "\n")

    #### Spice Options ####

    #### Measurement Definition ####
    f.write(".meas TF_gain db(abs(v(out))) when frequency={fc}" + "\n") # results[0]
    f.write(".meas TF_phase phase(v(out)) when frequency={fc}" + "\n") # results[1]
    f.write(".meas ks V(ks)" + "\n") # results[2]
    f.write(".meas kr V(kr)" + "\n") # results[3]

    #### SPICE Analysis ####
    f.write(".ac dec 100 1 1Meg" + "\n")

    f.write(".end")

    f.close()
    results = { 
        "TF_gain": 0,
        "TF_phase": 0,
        "ks": 0,
        "kr": 0,
    }
    # Assume that QSPICE is installed in its default path for non-Admin user
    exe_qspice64 = os.path.expanduser(r"~\QSPICE\QSPICE64.exe")
    exe_qpost = os.path.expanduser(r"~\QSPICE\QPOST.exe")
    exe_qux = os.path.expanduser(r"~\QSPICE\QUX.exe")

    # run QSPICE Simulation
    try:
        run_qspice64 = subprocess.Popen([exe_qspice64, "PWM_SW_AVG_PSFB.cir"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd = base_dir, bufsize=1, universal_newlines=True)
        for line in run_qspice64.stdout:
            print(line, end="")
            sys.stdout.flush()

        run_qspice64.wait()

        # Check exit code after process is done
        if run_qspice64.returncode == 0:
            print("QSPICE64 simulation completed successfully.")
            print('*************** END ***************')
        else:
            print(f"QSPICE64 simulation failed with exit code {run_qspice64.returncode}.")
            raise SystemExit("Terminating execution because simulation failed.")
    except subprocess.CalledProcessError as e:
        print('QSPICE64 exec output:')
        print(e.stderr)

    # Run postprocess measurement
    try:
        run_qpost = subprocess.run([exe_qpost, "PWM_SW_AVG_PSFB.cir", "-o", "results.txt"], capture_output=True, text=True, check=True, cwd = base_dir)
    except subprocess.CalledProcessError as e:
        print('QPOST exec output:')
        print(e.stderr)

    f = open(results_file_path, "r")
    results_lines = f.readlines()
    f.close()

    # Run postprocess waveforms extraction
    df = 0 
    if export_traces:
        run_qux = subprocess.run([exe_qux, "-Export", "PWM_SW_AVG_PSFB.qraw", export_traces, "all", "CSV"], cwd = base_dir)
        df = pd.read_csv(csv_file_path) 
        df.columns = df.columns.str.lower() 

        #Delete Exported Waveforms CSV File 
        subprocess.run(["del", "PWM_SW_AVG_PSFB.csv"], shell=True, cwd = base_dir) 

    # Delete Results
    subprocess.run(["del", "PWM_SW_AVG_PSFB.qraw"], shell=True, cwd = base_dir)

    # Delete Netlist
    subprocess.run(["del", "PWM_SW_AVG_PSFB.cir"], shell=True, cwd = base_dir)

    # Delete QPOST Results
    subprocess.run(["del", "results.txt"], shell=True, cwd = base_dir)
    for i, line in enumerate(results_lines):
        stripped_line = line.strip()
        match stripped_line:
            case ".meas tf_gain db(abs(v(out))) when frequency={fc}:": 
                results['TF_gain'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas tf_phase phase(v(out)) when frequency={fc}:": 
                results['TF_phase'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas ks v(ks):": 
                results['ks'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

            case ".meas kr v(kr):": 
                results['kr'] = float(re.search(r'[-+]?\d*\.\d+|\d+', results_lines[i + 1])[0])

    return [df,results]