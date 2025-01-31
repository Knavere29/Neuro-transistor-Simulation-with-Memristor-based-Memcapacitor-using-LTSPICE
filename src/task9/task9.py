# Importing necessary libraries
import os, shutil
import matplotlib.pyplot as plt
import numpy as np
from PyLTSpice import Trace, RawWrite, RawRead
from PyLTSpice import SimRunner, SpiceCircuit, SpiceEditor, AscEditor
from PyLTSpice import LTspice

task_name = "task9"

# Select spice model
LTC = SimRunner(output_folder='./temp', simulator=LTspice)                         # Location for saving the simualtion files
netlist = AscEditor("../base/neuro_memristor.asc")                                     # Creating Netlist from .asc file

# Set default parameters
netlist.set_parameters(x0=0.1)
netlist.set_component_value('Vpulse', "PULSE(0 1 0 100n 100n 2u 4u)")

# Simulation time period to run for 200 seconds
netlist.add_instructions(
    "; Simulation Settings",
    ".tran 1m",
)

run_count = 0
# Sweeping Parameters
for voltage in [0.5, 1, 1.5]:                           # Switching Pseudo-Memcapacitor ON/OFF
    for t_on in [1, 2, 3]:                            # Switching the voltage source between 0.8V, 1.2V and 1.5V
        for t_period in [10, 50, 100]:                       # Switching the t_on period
            for x in [0.1, 0.192, 0.284]:                    # Switching the time period
                netlist.set_parameters(x0=x)
                run_count += 1
                config_volt = "PULSE(" + "0 " + str(voltage) + "V 0 100n 100n " + str(t_on) + "u " + str(t_period) + "u)"
                netlist.set_component_value('Vpulse', config_volt)
                run_netlist_file = "Run_{}_Volt_{}_Ton_{}_T_{}_State_{}.net".format(run_count, voltage, t_on, t_period, x)          # File Naming
                print("Simulating: " + run_netlist_file)
                LTC.run(netlist, run_filename=run_netlist_file+".asc")

# Delete previous run results
try:
    if os.path.isdir("empty-dir"):
        os.rmdir("result")
        os.rmdir("comparison")
    else:
        shutil.rmtree("result")
        shutil.rmtree("comparison")
except Exception as e:
    print("result folder doesn't exist Error :",e)

# Create the directory
directory_name1 = "result"
directory_name2 = "comparison"
try:
    os.mkdir(directory_name1)
    os.mkdir(directory_name2)
    print(f"Directory '{directory_name1}' or '{directory_name2}' created successfully.")
except FileExistsError:
    print(f"Directory '{directory_name1}' or '{directory_name2}' already exists.")
except PermissionError:
    print(f"Permission denied: Unable to create '{directory_name1}' or '{directory_name2}'.")
except Exception as e:
    print(f"An error occurred: {e}")

# plot waveforms
state_change = 1
for raw, log in LTC:
    print("Raw File: %s, Log Files: %s" % (raw, log))

    # Plot
    px = 1 / plt.rcParams['figure.dpi']  # pixel in inches
    fig, axs = plt.subplots(nrows=3, ncols=1, layout='constrained', figsize=(1080*px, 720*px))    # Create the canvas for plotting

    raw_file = RawRead(raw)
    #print(raw_file.get_trace_names())                                 # Get and print a list of all the traces
    trace_names = ('V(Vpulse)', 'V(Vg)', 'Id(M1)')                     # Parameters to be plotted

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

    fig.suptitle(str(raw)[5:-8])
    axs[0].set_ylabel("Vpulse (V)")
    axs[1].set_ylabel("Vg (V)")
    axs[2].set_ylabel("Id (A)")
    axs[2].set_xlabel("Time (s)")
    axs[0].plot(xdata, ydata1)
    axs[1].plot(xdata, ydata2)
    axs[2].plot(xdata, ydata3)
    axs[0].ticklabel_format(style='plain')
    axs[1].ticklabel_format(style='plain')
    axs[2].ticklabel_format(style='plain')

    pwd = os.getcwd() # present working directory
    file_name = os.path.join(pwd,"result",str(raw)[5:-8]+".png")
    print(file_name)
    fig.savefig(file_name)  # save the figure to file
    plt.close(fig)

    if (state_change == 1):
        id_data1 = ydata3
        t_data1 = xdata
        state_change = 2
    elif (state_change == 2):
        id_data2 = ydata3
        t_data2 = xdata
        state_change = 3
    else:
        id_data3 = ydata3
        t_data3 = xdata
        state_change = 1
        # merge all the time data
        t_data = np.unique(np.concatenate((t_data1,t_data2,t_data3),0))
        count = 0
        for t in t_data:
            if t not in t_data1:
                id_data1 = np.insert(id_data1,count, id_data1[count-1], axis=0)
            if t not in t_data2:
                id_data2 = np.insert(id_data2,count, id_data2[count-1], axis=0)
            if t not in t_data3:
                id_data3 = np.insert(id_data3,count, id_data3[count-1], axis=0)
            count += 1
        # Plot
        px = 1 / plt.rcParams['figure.dpi']  # pixel in inches
        fig, axs = plt.subplots(nrows=3, ncols=1, layout='constrained', figsize=(1080 * px, 720 * px))  # Create the canvas for plotting
        f_name = str(raw)[5:-8].split("_")
        f_name_len = len(f_name)
        f_name = "_".join(f_name[2:-2])
        fig.suptitle(f_name)
        axs[0].set_ylabel("Vpulse (V)")
        axs[1].set_ylabel("Vg (V)")
        axs[2].set_ylabel("Id (uA)")
        axs[2].set_xlabel("Time (s)")
        axs[0].plot(xdata, ydata1)
        axs[1].plot(xdata, ydata2)
        axs[2].plot(t_data, id_data1*10e+6, 'g', label="x=0.1")
        axs[2].plot(t_data, id_data2*10e+6, 'c', label="x=0.192")
        axs[2].plot(t_data, id_data3*10e+6, 'r', label="x=0.284")
        axs[2].legend(loc='lower right')
        axs[0].ticklabel_format(style='plain')
        axs[1].ticklabel_format(style='plain')
        axs[2].ticklabel_format(style='plain')

        pwd = os.getcwd()  # present working directory
        file_name = os.path.join(pwd, "comparison", f_name + ".png")
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