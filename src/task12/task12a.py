# Importing necessary libraries
import os, shutil
import matplotlib.pyplot as plt
import numpy as np
from PyLTSpice import Trace, RawWrite, RawRead
from PyLTSpice import SimRunner, SpiceCircuit, SpiceEditor, AscEditor
from PyLTSpice import LTspice

task_name = "task12"
run_file_list = []

# Select spice model
LTC = SimRunner(output_folder='./temp', simulator=LTspice)                         # Location for saving the simualtion files
netlist = AscEditor("../base/neuro_memristor_3x3.asc")                                     # Creating Netlist from .asc file

# Set default parameters
netlist.set_parameters(x0=0.1)

# Simulation time period to run for 200 seconds
netlist.add_instructions(
    "; Simulation Settings",
    ".tran 1m",
)

# Sweeping Parameters
run_count = 0
for voltage in [1]:                                                   # Switching Pseudo-Memcapacitor ON/OFF
    for t_on in [2]:                                                  # Switching the voltage source between 0.8V, 1.2V and 1.5V
        for t_period in [10]:                                         # Switching the t_on period
            for x1 in [0.1, 0.192, 0.284]:                            # Switching the time period
                for x2 in [0.1, 0.192, 0.284]:                        # Switching the time period
                    for x3 in [0.1, 0.192, 0.284]:                    # Switching the time period
                        netlist.set_parameters(x11=x1)
                        netlist.set_parameters(x12=x1)
                        netlist.set_parameters(x13=x1)
                        netlist.set_parameters(x21=x2)
                        netlist.set_parameters(x22=x2)
                        netlist.set_parameters(x23=x2)
                        netlist.set_parameters(x31=x3)
                        netlist.set_parameters(x32=x3)
                        netlist.set_parameters(x33=x3)
                        run_count += 1
                        config_volt = "PULSE(" + "0 " + str(voltage) + " 0 100n 100n " + str(t_on) + "u " + str(t_period) + "u)"
                        netlist.set_component_value('Vpulse1', config_volt)
                        netlist.set_component_value('Vpulse2', config_volt)
                        netlist.set_component_value('Vpulse3', config_volt)
                        run_file_list.append("Run_" + str(run_count) + "_Volt_" + str(voltage) + "V_Ton_" + str(t_on) + "u_T_" + str(t_period) + "u_State1_" + str(x1) + "_State2_" + str(x2) + "_State3_" + str(x3)+"_Col")
                        run_netlist_file = "Run_{}_Volt_{}V_Ton_{}u_T_{}u_State1_{}_State2_{}_State3_{}_Col.net".format(run_count, voltage, t_on, t_period, x1, x2, x3)  # File Naming
                        print("Simulating: " + run_netlist_file)
                        LTC.run_now(netlist, run_filename=run_netlist_file+".asc")

# Delete previous run results
try:
    if os.path.isdir("empty-dir"):
        os.rmdir("result_task12a")
    else:
        shutil.rmtree("result_task12a")
except Exception as e:
    print("result folder doesn't exist Error :",e)

# Create the directory
directory_name = "result_task12a"
try:
    os.mkdir(directory_name)
    print(f"Directory '{directory_name}' created successfully.")
except FileExistsError:
    print(f"Directory '{directory_name}' already exists.")
except PermissionError:
    print(f"Permission denied: Unable to create '{directory_name}'.")
except Exception as e:
    print(f"An error occurred: {e}")

# plot waveforms
for raw in run_file_list:
    pwd = os.getcwd()  # present working directory
    file_name = os.path.join(pwd, "temp", raw + ".net.raw")
    print("RAW File : ",raw)

    # Plot
    px = 1 / plt.rcParams['figure.dpi']  # pixel in inches
    fig, axs = plt.subplots(nrows=5, ncols=1, layout='constrained', figsize=(1080*px, 720*px))    # Create the canvas for plotting

    raw_file = RawRead(file_name)
    #print(raw_file.get_trace_names())                                 # Get and print a list of all the traces
    trace_names = ('V(Vpulse1)', 'V(Vpulse2)', 'V(Vpulse3)', 'V(Vg1)', 'V(Vg2)', 'V(Vg3)', 'I(R1)')                     # Parameters to be plotted

    time = raw_file.get_trace('time')
    y = list()
    steps = None

    # getting the values for plotting
    for trace in trace_names:
        y.append(raw_file.get_trace(trace))
        steps = raw_file.get_steps()

    for step in range(len(steps)):
        xdata = time.get_wave(step)
        ydata1 = y[0].get_wave(step)
        ydata2 = y[1].get_wave(step)
        ydata3 = y[2].get_wave(step)
        ydata4 = y[3].get_wave(step)
        ydata5 = y[4].get_wave(step)
        ydata6 = y[5].get_wave(step)
        ydata7 = y[6].get_wave(step)

    fig.suptitle(str(raw))
    axs[0].set_ylabel("Vpulse1 (V)")
    axs[1].set_ylabel("Vg1 (V)")
    axs[2].set_ylabel("Vg2 (V)")
    axs[3].set_ylabel("Vg3 (V)")
    axs[4].set_ylabel("IR1 (uA)")
    axs[4].set_xlabel("Time (s)")
    axs[0].plot(xdata, ydata1)
    axs[1].plot(xdata, ydata4, 'r')
    axs[2].plot(xdata, ydata5, 'g')
    axs[3].plot(xdata, ydata6, 'm')
    axs[4].plot(xdata, ydata7*1e+6, 'k')
    axs[0].ticklabel_format(style='plain')
    axs[1].ticklabel_format(style='plain')
    axs[2].ticklabel_format(style='plain')
    axs[3].ticklabel_format(style='plain')
    axs[4].ticklabel_format(style='plain')

    pwd = os.getcwd() # present working directory
    file_name = os.path.join(pwd,"result_task12a",str(raw)+".png")
    print(file_name)
    fig.savefig(file_name)  # save the figure to file
    plt.close(fig)

# Sim Statistics
print('Successful/Total Simulation: ' + str(LTC.okSim) + '/' + str(LTC.runno))

# Deleting generated files during simulation
enter = input("Press 1 to delete created files")
if enter == '1':
    netlist.reset_netlist()
    LTC.file_cleanup()
    print("Deleted all the created files")
else:
    print("Saved all the created files")
print("SIM END")