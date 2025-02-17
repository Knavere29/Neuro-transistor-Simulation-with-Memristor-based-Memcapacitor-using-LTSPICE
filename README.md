# Neuro-transistor-Simulation-with-Memristor-based-Memcapacitor-using-LTSPICE
Realization of the neuron functionality with a pseudo-memcapacitive transistor using LTSPICE.

#  Memristor spice model source
R. Schroedter et al., "SPICE Compact Model for an Analog Switching Niobium Oxide Memristor," 
2022 11th International Conference on Modern Circuits and Systems Technologies (MOCAST), 
2022, pp. 1-4, doi: 10.1109/MOCAST54814.2022.9837726.

## Task overview 
--- Semester project for Neural Networks and Memristive Hardware Accelerators course @ Technische Universität Dresden
Implement a single memristor-based memcapacitor at the gate of a MOSFET transistor in LTSPICE and find a pulse input 
setting which realizes the neuron firing after integration through the transistor. 
Extend the simulation to a 3x3 multi-channel neuro-transistor as shown in Figure 1 and test the correct functionality. 
Finally, sweep and find optional parameters for capacitances and pulse timing by using the LTSPICE in a loop via python

## Folder Structure
|--> doc                                       : documents folder
|    |--> groupK_project3.pptx                 : final presentation ppt
|--> ref                                       : reference materials folder
|    |--> Project3_Neurotransistor_SPICE.pdf   : describes details of task of this projects
|--> src                                       : source code folder
|    |--> base                                 : folder contains memristor spice models, symbols and pseudo-memcapacitor circuits
|    |    |--> neuro_memristor.asc             : LTSPICE single pseudo-memcapacitor circuit
|    |    |--> neuro_memristor_3x1.asc         : LTSPICE 3x1 pseudo-memcapacitor circuit
|    |    |--> neuro_memristor_3x3.asc         : LTSPICE 3x3 pseudo-memcapacitor circuit
|    |--> task3                        
|    |    |--> task3.py                        : python file : To run memristor simulation via python and plot state and conductance graph 
|    |    |--> task3.png                       : task3 plot
|    |--> task4                              
|    |    |--> task4a                     
|    |    |    |--> task4a.py                  : python file : To plot potentiation and depression curve of memristor
|    |    |    |--> task4a.png                 : task4a plot
|    |    |--> task4b               
|    |    |    |--> mem_drm.asc                : LTSPICE memristor circuit to plot DRM
|    |--> task9        
|    |    |--> comparison                      : folder contains combined plot of single pseudo-memcapacitor output for different memristor state 
|    |    |--> result                          : folder contains plot of single pseudo-memcapacitor output for different memristor state run
|    |    |--> task9.py                        : python file : To find the input setting of single pseudo-memcapacitor with different parameters sweeped via python
|    |--> task10
|    |    |--> result_task10a                  : folder contains plot of 3x1 pseudo-memcapacitor output for different memristor state 
|    |    |--> result_task10b                  : folder contains plot of 3x1 pseudo-memcapacitor output for different memristor state with ttfs
|    |    |--> task10a.py                      : python file : To find the input setting of 3X1 pseudo-memcapacitor with different parameters sweeped via python
|    |    |--> task10b.py                      : python file : To find the input setting of 3X1 pseudo-memcapacitor with different parameters for ttfs input; sweeped via python
|    |--> task12
|    |    |--> result_task12a                  : folder contains plot of 3x3 pseudo-memcapacitor output for different memristor state (Column-wise)
|    |    |--> result_task12b                  : folder contains plot of 3x3 pseudo-memcapacitor output for different memristor state (Row-wise)
|    |    |--> task12a.py                      : python file : To find the input setting of 3X3 pseudo-memcapacitor with different parameters (Column-wise) sweeped via python
|    |    |--> task12b.py                      : python file : To find the input setting of 3X3 pseudo-memcapacitor with different parameters (Row-wise) sweeped via python
|    |--> task14
|    |    |--> task14.asc                      : LTSPICE circuit realising cascading of pseudo-memcapacitor blocks using transimpedence amplifier
|    |--> requirements.txt                     : lists the required python modules to run python file