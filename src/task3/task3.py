# Importing necessary libraries
import os
import matplotlib.pyplot as plt
import numpy as np
from PyLTSpice import Trace, RawWrite, RawRead
from PyLTSpice import SimRunner, SpiceCircuit, SpiceEditor, AscEditor
from PyLTSpice import LTspice

task_name = "task3"

# Select spice model
LTC = SimRunner(output_folder='./temp', simulator=LTspice)                         # Location for saving the simualtion files
netlist = AscEditor("../base/mem_circuit.asc")                                     # Creating Netlist from .asc file

# Set default parameters
netlist.set_parameters(x0=0.1)
netlist.set_component_value('Vin', "PWL file=../task3_input.txt")

# Simulation time period to run for 200 seconds
netlist.add_instructions(
    "; Simulation Settings",
    ".tran 200",
)
LTC.run(netlist,run_filename=task_name+".asc")

# plot waveforms
for raw, log in LTC:
    print("Raw File: %s, Log Files: %s" % (raw, log))
    raw_file = RawRead(raw)
    print(raw_file.get_trace_names())            # Get and print a list of all the traces
    print(raw_file.get_raw_property())           # Print all the properties found in the Header section
    steps = raw_file.get_steps()                 # Get list of step numbers ([0,1,2]) for sweeped simulations
    print("Steps :",steps)                       # Returns [0] if there is just 1 step

    # Plot
    fig, axs = plt.subplots(nrows=3, ncols=1, layout='constrained')    # Create the canvas for plotting

    # plot 1 : voltage vs time
    vin = raw_file.get_trace('V(n001)')          # Get the trace data of voltage source
    time1 = raw_file.get_trace('time')           # Get the trace data of time
    xdata0 = time1.get_wave()                    # Get all the values for the 'time' trace
    ydata0 = vin.get_wave()                      # Get all the values for the 'vin' trace
    axs[0].plot(xdata0, ydata0)                  # Do an X/Y plot on first subplot
    axs[0].set_ylabel("Voltage (V)")

    # plot 2 : Conductance vs time
    im = raw_file.get_trace('Ix(u1:TE)')         # Get the trace data of memristor current
    time2 = raw_file.get_trace('time')           # Get the trace data of time
    imdata = im.get_wave()                       # Get all the values for the 'im' trace
    # Compute conductance im/vin of memristor
    ydata1 = np.divide(imdata, ydata0, out=np.zeros_like(imdata), where=ydata0!=0)
    xdata1 = time2.get_wave()                    # Get the X-axis data (time)
    axs[1].plot(xdata1, abs(ydata1))             # Do an X/Y plot on second subplot
    axs[1].set_ylabel("Conductance (S)")
    axs[1].set_yscale("log")

    # plot 3 : state x vs time
    state = raw_file.get_trace('V(x)')           # Get the trace data of state x
    time3 = raw_file.get_trace('time')           # Get the trace data of time
    xdata2 = time3.get_wave()                    # Get all the values for the 'time' trace
    ydata2 = state.get_wave()                    # Get all the values for the 'state' trace
    axs[2].plot(xdata2, ydata2)                  # Do an X/Y plot on first subplot
    axs[2].set_ylabel("State x (V)")
    axs[2].set_xlabel("Time (s)")

    plt.show()                                   # show the plot
    fig.savefig('./{}.png'.format(task_name))    # save the plot as png
    plt.close(fig)                               # close plot

# Sim Statistics
print('Successful/Total Simulation: ' + str(LTC.okSim) + '/' + str(LTC.runno))

# Deleting generated files during simulation
enter = input("Press 1 to delete created files")
if enter == '1':
    netlist.reset_netlist()
    LTC.file_cleanup()
