# Importing necessary libraries
import os, shutil
import matplotlib.pyplot as plt
import numpy as np
from PyLTSpice import Trace, RawWrite, RawRead
from PyLTSpice import SimRunner, SpiceCircuit, SpiceEditor, AscEditor
from PyLTSpice import LTspice

task_name  = "task4a"

# Select spice model
LTC = SimRunner(output_folder='./temp', simulator=LTspice)                         # Location for saving the simualtion files
netlist = AscEditor("../base/mem_circuit.asc")                                     # Creating Netlist from .asc file

# Generate PWL file for -3V, 10ms 100 pulse and -2.7, 10ms 100 pulse
with open ("./temp/task4_input.txt", "w") as f:
    vtime = 0
    for i in range(100):
        f.writelines(f"{vtime}u 0\n")
        vtime += 9990
        f.writelines(f"{vtime}u 0\n")
        vtime += 1
        f.writelines(f"{vtime}u -3\n")
        vtime += 8
        f.writelines(f"{vtime}u -3\n")
        vtime += 1
    for i in range(100):
        f.writelines(f"{vtime}u 0\n")
        vtime += 9990
        f.writelines(f"{vtime}u 0\n")
        vtime += 1
        f.writelines(f"{vtime}u 2.7\n")
        vtime += 8
        f.writelines(f"{vtime}u 2.7\n")
        vtime += 1
    f.writelines(f"{vtime}m 0\n")

# Set default parameters
netlist.set_parameters(x0=0.1)
netlist.set_component_value('V', "PWL file=task4_input.txt")

# Simulation time period to run for 200 seconds
netlist.add_instructions(
    "; Simulation Settings",
    ".tran 2",
)
LTC.run(netlist,run_filename=task_name+".asc")

# plot waveforms
for raw, log in LTC:
    print("Raw File: %s, Log Files: %s" % (raw, log))
    raw_file = RawRead(raw)
    print(raw_file.get_trace_names())  # Get and print a list of all the traces
    print(raw_file.get_raw_property())  # Print all the properties found in the Header section
    steps = raw_file.get_steps()  # Get list of step numbers ([0,1,2]) for sweeped simulations
    print("Steps :", steps)  # Returns [0] if there is just 1 step

    # Plot
    fig, axs = plt.subplots(nrows=1, ncols=1, layout='constrained')  # Create the canvas for plotting

    # plot 1 : voltage vs time
    vm = raw_file.get_trace('V(n001)')             # Get the trace data of voltage source
    pulse =list(range(0,200,1))                    # Get the trace data of no of pulses
    time = raw_file.get_trace('time')              # Get the trace data of time
    xdata0 = time.get_wave()                       # Get the X-axis data (time)
    vmdata = vm.get_wave()                         # Get all the values for the 'vin' trace
    im = raw_file.get_trace('Ix(u1:TE)')           # Get the trace data of memristor current
    imdata = im.get_wave()                         # Get all the values for the 'im' trace
    ydata0 = np.divide((imdata), abs(vmdata), out=np.zeros_like(imdata), where=vmdata!=0)                      # Compute conductance im/vin of memristor

    print("Cond",len(ydata0),"time",len(xdata0))
    # find conductance at discrete time points
    vtime = 9999
    cond = []
    for cnd in range (200):
        index = np.argmin(np.abs(xdata0 - vtime))
        print("index",index)
        print(vtime, ydata0[index])
        # print(ydata1[list(xdata0).index(vtime)])
        # print(list(xdata0).index(vtime))
        cond.append(ydata0[index])
        vtime += 10000

    axs.plot(pulse, cond,'^')                # Do an X/Y plot on second subplot
    axs.set_ylabel("Conductance (S)")

    fig.savefig('./{}.png'.format(task_name))  # save the plot as png
    plt.close(fig)  # close plot

# Sim Statistics
print('Successful/Total Simulation: ' + str(LTC.okSim) + '/' + str(LTC.runno))

# Deleting generated files during simulation
enter = input("Press 1 to delete created files")
if enter == '1':
    netlist.reset_netlist()
    LTC.file_cleanup()

