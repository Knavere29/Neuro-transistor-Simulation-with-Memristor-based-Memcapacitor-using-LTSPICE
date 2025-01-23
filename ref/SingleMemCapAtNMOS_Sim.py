# Importing necessary libraries
import os
import matplotlib.pyplot as plt
import numpy as np
from PyLTSpice import RawRead
from PyLTSpice import SimRunner, SpiceEditor
from PyLTSpice import LTspice

# Directory of the Program File
directory = os.getcwd()

# Select spice model
LTC = SimRunner(output_folder='./temp', simulator=LTspice)                         # Location for saving the simualtion files
LTC.create_netlist('./MEM_NAMLAB_Project_Circuit/SingleMemCapAtNMOS.asc')          # Creating Netlist
netlist = SpiceEditor('./MEM_NAMLAB_Project_Circuit/SingleMemCapAtNMOS.net')

# Set default parameters
netlist.set_parameters(x0=0.1)
netlist.set_component_value('Vpulse', "PULSE(0 1 0 0 0 1u 50u)")

# Simulation time period
netlist.add_instructions(
    "; Simulation Settings",
    ".tran 1m",
)

# Sweeping Parameters
for x in [0.1, 0.28]:                           # Switching Memcapacitors ON/OFF
    netlist.set_parameters(x0=x)

    for voltage in [0.8, 1.2, 1.5]:             # Switching the voltage source between 0.8V, 1.2V and 1.5V
        for t_on in np.arange(0, 10, 0.5):      # Switching the t_on period
            for t_period in [10, 25, 50, 100]:  # Switching the time period
                config_volt = "PULSE(" + "0 " + str(voltage) + "V 0 35n 35n " + str(t_on) + "u " + str(t_period) + "u)"
                netlist.set_component_value('Vpulse', config_volt)
                run_netlist_file = "Volt_{}_Ton_{}_T_{}_State_{}.net".format(voltage, t_on, t_period, x)  # File Naming
                print("Simulating: " + run_netlist_file)
                LTC.run(netlist, run_filename=run_netlist_file)
                # LTC.run(netlist)

# Reading .raw files and plotting datapoints
for raw, log in LTC:
    print("Raw File: %s, Log Files: %s" % (raw, log))
    # raw_file_paths.append(raw)
    # raw_file_paths = glob.glob("./temp/*.raw")
    # print(raw_file_paths)

    raw_filename = raw
    trace_names = ('V(input)', 'V(gate)', 'I(R3)')  # Parameters to be plotted

    file_ = RawRead(raw_filename)

    x = file_.get_trace('time')
    y = list()
    steps = None

    # getting the values for plotting
    for trace in trace_names:
        y.append(file_.get_trace(trace))
        steps = file_.get_steps()

    for step in range(len(steps)):
        xdata = x.get_wave(step)
        # xdata = raw.get_axis(step)
        y1_data = y[0].get_wave(step)
        y2_data = y[1].get_wave(step)
        y3_data = y[2].get_wave(step)

    # Plotting figures
    fig = plt.figure()

    fig.suptitle(raw_filename)

    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)
    ax1.set_title("V(In)")
    ax2.set_title("V(Gate)")
    ax3.set_title("I(R3)")
    ax1.plot(xdata, y1_data)
    ax2.plot(xdata, y2_data)
    ax3.plot(xdata, y3_data)

    #plt.savefig(raw_filename + '.png')
    fig.savefig('./{}.png'.format(raw_filename))  # save the figure to file
    plt.close(fig)

netlist.reset_netlist()

# Sim Statistics
print('Successful/Total Simulation: ' + str(LTC.okSim) + '/' + str(LTC.runno))

# Deleting generated files during simulation
enter = input("Press enter to delete created files")
if enter == '':
    LTC.file_cleanup()
