# Importing necessary libraries
import os, shutil
import matplotlib.pyplot as plt
import numpy as np
from PyLTSpice import Trace, RawWrite, RawRead
from PyLTSpice import SimRunner, SpiceCircuit, SpiceEditor, AscEditor
from PyLTSpice import LTspice
from ttfs_encoding import *

# Objective : To find the input setting of 3X1 pseudo-memcapacitor with different parameters for ttfs input; sweeped via python
task_name = "task10b"
run_file_list = []

# generate pwl file for ttfs encoding of image
image_path = "./img_src/A/A1.png"                   # Replace with your image
T_max = 30e-6                                       # Maximum spike delay (1ms)

pixel_data = read_image(image_path)
print("Pixel Matrix (Grayscale):\n", pixel_data)

spike_times = normalize_ttfs(pixel_data, T_max)
print("Spike Times (seconds):\n", spike_times)

generate_pwl_files(spike_times)

# Select spice model
LTC = SimRunner(output_folder='./temp', simulator=LTspice)                         # Location for saving the simualtion files
netlist = AscEditor("../base/neuro_memristor_3x1.asc")                             # Creating Netlist from .asc file

# Set default parameters
netlist.set_parameters(x0=0.1)

# Simulation time period to run for 200 seconds
netlist.add_instructions(
    ".tran 0.1m",
)

# Sweeping Parameters
run_count = 0
for voltage in [1]:                                                   # Switching Pseudo-Memcapacitor ON/OFF
    for t_on in [2]:                                                  # Switching the voltage source between 0.8V, 1.2V and 1.5V
        for t_period in [10]:                                         # Switching the t_on period
            for x1 in [0.1, 0.284]:                                   # Switching the time period
                for x2 in [0.1, 0.284]:                               # Switching the time period
                    for x3 in [0.1, 0.284]:                           # Switching the time period
                        netlist.set_parameters(x1=x1)
                        netlist.set_parameters(x2=x2)
                        netlist.set_parameters(x3=x3)
                        run_count += 1
                        netlist.set_component_value('Vpulse1', "PWL file=../spikes_V1.txt")
                        netlist.set_component_value('Vpulse2', "PWL file=../spikes_V2.txt")
                        netlist.set_component_value('Vpulse3', "PWL file=../spikes_V3.txt")
                        run_file_list.append("Run_" + str(run_count) + "_Volt_" + str(voltage) + "V_Ton_" + str(t_on) + "u_T_" + str(t_period) + "u_State1_" + str(x1)+"_State2_"+str(x2)+"_State3_"+str(x3))
                        run_netlist_file = "Run_{}_Volt_{}V_Ton_{}u_T_{}u_State1_{}_State2_{}_State3_{}.net".format(run_count, voltage, t_on, t_period, x1, x2, x3)  # File Naming
                        print("Simulating: " + run_netlist_file)
                        LTC.run_now(netlist, run_filename=run_netlist_file+".asc")

# Delete previous run results
try:
    if os.path.isdir("empty-dir"):
        os.rmdir("result_task10b")
    else:
        shutil.rmtree("result_task10b")
except Exception as e:
    print("result folder doesn't exist Error :",e)

# Create the directory
directory_name = "result_task10b"
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
    #print(raw_file.get_trace_names())                                                            # Get and print a list of all the traces
    trace_names = ('V(Vpulse1)', 'V(Vpulse2)', 'V(Vpulse3)', 'V(Vg)', 'I(Rd)')                    # Parameters to be plotted

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

    fig.suptitle(str(raw), weight='bold')
    axs[0].set_ylabel("Vpulse1 (V)", weight='bold')
    axs[1].set_ylabel("Vpulse2 (V)", weight='bold')
    axs[2].set_ylabel("Vpulse3 (V)", weight='bold')
    axs[3].set_ylabel("Vg (V)", weight='bold')
    axs[4].set_ylabel("Id (uA)", weight='bold')
    axs[4].set_xlabel("Time (ms)", weight='bold')
    axs[0].plot(xdata*1e+3, ydata1)
    axs[1].plot(xdata*1e+3, ydata2, 'm')
    axs[2].plot(xdata*1e+3, ydata3, 'g')
    axs[3].plot(xdata*1e+3, ydata4, 'r')
    axs[4].plot(xdata*1e+3, ydata5*1e+6, 'k')
    axs[0].ticklabel_format(style='plain')
    axs[1].ticklabel_format(style='plain')
    axs[2].ticklabel_format(style='plain')
    axs[3].ticklabel_format(style='plain')
    axs[4].ticklabel_format(style='plain')

    pwd = os.getcwd() # present working directory
    file_name = os.path.join(pwd,"result_task10b",str(raw)+".png")
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