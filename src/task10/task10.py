# Importing necessary libraries
import os, shutil
import matplotlib.pyplot as plt
import numpy as np
from PyLTSpice import Trace, RawWrite, RawRead
from PyLTSpice import SimRunner, SpiceCircuit, SpiceEditor, AscEditor
from PyLTSpice import LTspice

task_name = "task10"

# Select spice model
LTC = SimRunner(output_folder='./temp', simulator=LTspice)                         # Location for saving the simualtion files
netlist = AscEditor("../base/neuro_memristor_3x1.asc")                                     # Creating Netlist from .asc file

# Set default parameters
netlist.set_parameters(x0=0.1)

# Simulation time period to run for 200 seconds
netlist.add_instructions(
    "; Simulation Settings",
    ".tran 1m",
)

# Sweeping Parameters
for x in [0.1, 0.284]:                            # Switching Pseudo-Memcapacitor ON/OFF
    netlist.set_parameters(x0=x)

    for voltage in [1]:                         # Switching the voltage source between 0.8V, 1.2V and 1.5V
        for t_on in [1.5, 2, 2.5]:        # Switching the t_on period
            for t_period in [10, 50, 100]:    # Switching the time period
                config_volt = "PULSE(" + "0 " + str(voltage) + "V 0 100n 100n " + str(t_on) + "u " + str(t_period) + "u)"
                netlist.set_component_value('Vpulse1', config_volt)
                netlist.set_component_value('Vpulse2', config_volt)
                netlist.set_component_value('Vpulse3', config_volt)
                run_netlist_file = "Volt_{}_Ton_{}_T_{}_State_{}.net".format(voltage, t_on, t_period, x)          # File Naming
                print("Simulating: " + run_netlist_file)
                LTC.run(netlist, run_filename=run_netlist_file+".asc")

# Delete previous run results
try:
    if os.path.isdir("empty-dir"):
        os.rmdir("result")
    else:
        shutil.rmtree("result")
except Exception as e:
    print("result folder doesn't exist Error :",e)

# Create the directory
directory_name = "result"
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
for raw, log in LTC:
    print("Raw File: %s, Log Files: %s" % (raw, log))

    # Plot
    fig, axs = plt.subplots(nrows=5, ncols=1, layout='constrained')    # Create the canvas for plotting

    raw_file = RawRead(raw)
    #print(raw_file.get_trace_names())                                 # Get and print a list of all the traces
    trace_names = ('V(Vpulse1)', 'V(Vpulse2)', 'V(Vpulse3)', 'V(Vg)', 'Id(M1)')                     # Parameters to be plotted

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

    fig.suptitle(str(raw)[5:-8])
    axs[0].set_ylabel("Vpulse1 (V)")
    axs[1].set_ylabel("Vpulse2 (V)")
    axs[2].set_ylabel("Vpulse3 (V)")
    axs[3].set_ylabel("Vg (V)")
    axs[4].set_ylabel("Id (A)")
    axs[4].set_xlabel("Time (s)")
    axs[0].plot(xdata, ydata1)
    axs[1].plot(xdata, ydata2)
    axs[2].plot(xdata, ydata3)
    axs[3].plot(xdata, ydata4)
    axs[4].plot(xdata, ydata5)

    file_name = str(raw)[:-8] + ".png"
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