# Importing necessary libraries
import os, shutil
import matplotlib.pyplot as plt
import numpy as np
from PyLTSpice import Trace, RawWrite, RawRead
from PyLTSpice import SimRunner, SpiceCircuit, SpiceEditor, AscEditor
from PyLTSpice import LTspice

task_name = "task9"
run_file_list = []

# Select spice model
LTC = SimRunner(output_folder='./temp', simulator=LTspice)                         # Location for saving the simualtion files
netlist = AscEditor("../base/neuro_memristor.asc")                                     # Creating Netlist from .asc file

# Set default parameters
netlist.set_parameters(x0=0.1)
netlist.set_component_value('Vpulse', "PULSE(0 1 0 100n 100n 2u 4u)")

# Simulation time period to run for 200 seconds
netlist.add_instructions(
    ".tran 2m",
)

run_count = 0
# Sweeping Parameters
for voltage in [0.8, 1.0, 1.2]:                                # Switching Pseudo-Memcapacitor ON/OFF
    for t_on in [1, 2, 3]:                                    # Switching the voltage source between 0.8V, 1.2V and 1.5V
        for t_period in [10, 50, 100]:                         # Switching the t_on period
            for x in [0.1, 0.284]:                             # Switching the time period
                netlist.set_parameters(x0=x)
                run_count += 1
                config_volt = "PULSE(" + "0 " + str(voltage) + " 0 100n 100n " + str(t_on) + "u " + str(t_period) + "u)"
                netlist.set_component_value('Vpulse', config_volt)
                run_file_list.append("Run_"+str(run_count)+"_Volt_"+str(voltage)+"V_Ton_"+str(t_on)+"u_T_"+str(t_period)+"u_State_"+str(x))
                run_netlist_file = "Run_{}_Volt_{}V_Ton_{}u_T_{}u_State_{}.net".format(run_count, voltage, t_on, t_period, x)          # File Naming
                print("Simulating: " + run_netlist_file)
                LTC.run_now(netlist, run_filename=run_netlist_file+".asc")

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
for raw in run_file_list:
    pwd = os.getcwd()  # present working directory
    file_name = os.path.join(pwd, "temp", raw + ".net.raw")
    print("File : ",raw)

    # Plot
    px = 1 / plt.rcParams['figure.dpi']  # pixel in inches
    fig, axs = plt.subplots(nrows=3, ncols=1, layout='constrained', figsize=(1080*px, 720*px))    # Create the canvas for plotting
    raw_file = RawRead(file_name)

    #print(raw_file.get_trace_names())                                 # Get and print a list of all the traces
    trace_names = ('V(Vpulse)', 'V(Vg)', 'I(R1)')                     # Parameters to be plotted

    time_data = raw_file.get_trace('time')
    y = list()
    steps = None

    # getting the values for plotting
    for trace in trace_names:
        y.append(raw_file.get_trace(trace))
        steps = raw_file.get_steps()

    for step in range(len(steps)):
        xdata = time_data.get_wave(step)
        ydata1 = y[0].get_wave(step)
        ydata2 = y[1].get_wave(step)
        ydata3 = y[2].get_wave(step)

    fig.suptitle(str(raw))
    axs[0].set_ylabel("Vpulse (V)")
    axs[1].set_ylabel("Vg (V)")
    axs[2].set_ylabel("IR1 (uA)")
    axs[2].set_xlabel("Time (s)")
    axs[0].plot(xdata, ydata1)
    axs[1].plot(xdata, ydata2, 'm')
    axs[2].plot(xdata, ydata3*1e+6, 'g')
    axs[0].ticklabel_format(style='plain')
    axs[1].ticklabel_format(style='plain')
    axs[2].ticklabel_format(style='plain')

    pwd = os.getcwd() # present working directory
    file_name = os.path.join(pwd,"result",str(raw)+".png")
    # print(file_name)
    fig.savefig(file_name)  # save the figure to file
    plt.close(fig)

    if (state_change == 1):
        id_data1 = ydata3
        t_data1 = xdata
        state_change = 2
    # elif (state_change == 2):
    #     id_data2 = ydata3
    #     t_data2 = xdata
    #     state_change = 3
    else:
        id_data3 = ydata3
        t_data3 = xdata
        state_change = 1
        # merge all the time data
        # t_data = np.unique(np.concatenate((t_data1,t_data2,t_data3),0))
        t_data = np.unique(np.concatenate((t_data1,t_data3),0))
        count = 0
        for t in t_data:
            if t not in t_data1:
                id_data1 = np.insert(id_data1,count, id_data1[count-1], axis=0)
            # if t not in t_data2:
            #     id_data2 = np.insert(id_data2,count, id_data2[count-1], axis=0)
            if t not in t_data3:
                id_data3 = np.insert(id_data3,count, id_data3[count-1], axis=0)
            count += 1
        # Plot
        px = 1 / plt.rcParams['figure.dpi']  # pixel in inches
        fig, axs = plt.subplots(nrows=3, ncols=1, layout='constrained', figsize=(1080 * px, 720 * px))  # Create the canvas for plotting
        f_name = str(raw).split("_")
        f_name_len = len(f_name)
        f_name = "_".join(f_name[2:-2])
        fig.suptitle(f_name)
        axs[0].set_ylabel("Vpulse (V)")
        axs[1].set_ylabel("Vg (V)")
        axs[2].set_ylabel("IR1 (uA)")
        axs[2].set_xlabel("Time (s)")
        axs[0].plot(xdata, ydata1)
        axs[1].plot(xdata, ydata2, 'm')
        axs[2].plot(t_data, id_data1*1e+6, 'g', label="x=0.1")
        # axs[2].plot(t_data, id_data2*10e+6, 'c', label="x=0.192")
        axs[2].plot(t_data, id_data3*1e+6, 'r', label="x=0.284")
        fig.legend(loc='outside right lower')
        axs[0].ticklabel_format(style='plain')
        axs[1].ticklabel_format(style='plain')
        axs[2].ticklabel_format(style='plain')

        pwd = os.getcwd()  # present working directory
        file_name = os.path.join(pwd, "comparison", f_name + ".png")
        # print(file_name)
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