# Neuro-transistor-Simulation-with-Memristor-based-Memcapacitor-using-LTSPICE
Realization of the neuron functionality with a pseudo-memcapacitive transistor using LTSPICE.

#  Memristor spice model source
R. Schroedter et al., "SPICE Compact Model for an Analog Switching Niobium Oxide Memristor," 2022 11th International Conference on Modern Circuits and Systems Technologies (MOCAST), 2022, pp. 1-4, doi: 10.1109/MOCAST54814.2022.9837726.

## Task overview 
### Semester project for Neural Networks and Memristive Hardware Accelerators course @ Technische Universität Dresden
Implement a single memristor-based memcapacitor at the gate of a MOSFET transistor in LTSPICE and find a pulse input setting which realizes the neuron firing after integration through the transistor. 
Extend the simulation to a 3x3 multi-channel neuro-transistor as shown in Figure 1 and test the correct functionality. 
Finally, sweep and find optional parameters for capacitances and pulse timing by using the LTSPICE in a loop via python

## Files & Folder Structure
|--> doc                                       
|    |--> groupK_project3.pptx                 
|--> ref                                       
|    |--> Project3_Neurotransistor_SPICE.pdf   
|--> src                                       
|    |--> base                                 
|    |    |--> neuro_memristor.asc             
|    |    |--> neuro_memristor_3x1.asc         
|    |    |--> neuro_memristor_3x3.asc         
|    |--> task3                        
|    |    |--> task3.py                
|    |    |--> task3.png               
|    |--> task4                        
|    |    |--> task4a                  
|    |    |    |--> task4a.py          
|    |    |    |--> task4a.png         
|    |    |--> task4b               
|    |    |    |--> mem_drm.asc        
|    |--> task9        
|    |    |--> comparison              
|    |    |--> result                  
|    |    |--> task9.py                
|    |--> task10
|    |    |--> result_task10a          
|    |    |--> result_task10b          
|    |    |--> task10a.py              
|    |    |--> task10b.py              
|    |--> task12
|    |    |--> result_task12a          
|    |    |--> result_task12b          
|    |    |--> task12a.py              
|    |    |--> task12b.py              
|    |--> task14
|    |    |--> task14.asc              
|    |--> requirements.txt             

## Files and folders details
|--> doc                      : documents                                  
|--> ref                      : reference materials                 
|--> src                      : source code               
|    |--> base                : common LTSPICE files folder                        
|    |--> task3                       
|    |--> task4                              
|    |    |--> task4a                   
|    |    |--> task4b         
|    |--> task9               
|    |    |--> comparison     : contains combined plot of single pseudo-memcapacitor output for different memristor state 
|    |    |--> result         : contains plot of single pseudo-memcapacitor output for different memristor state run
|    |--> task10
|    |    |--> result_task10a : contains plot of 3x1 pseudo-memcapacitor output for different memristor state 
|    |    |--> result_task10b : contains plot of 3x1 pseudo-memcapacitor output for different memristor state with ttfs
|    |--> task12
|    |    |--> result_task12a : contains plot of 3x3 pseudo-memcapacitor output for different memristor state (Column-wise)
|    |    |--> result_task12b : contains plot of 3x3 pseudo-memcapacitor output for different memristor state (Row-wise)
|    |--> task14             

### LTSpice files details
1. neuro_memristor.asc      : LTSPICE single pseudo-memcapacitor circuit
2. neuro_memristor_3x1.asc  : LTSPICE 3x1 pseudo-memcapacitor circuit
3. neuro_memristor_3x3.asc  : LTSPICE 3x3 pseudo-memcapacitor circuit
4. mem_drm.asc              : LTSPICE memristor circuit to plot DRM
5. task14.asc               : LTSPICE circuit realising cascading of pseudo-memcapacitor blocks using transimpedence amplifier

### Python files details
1. task3.py      : To run memristor simulation via python and plot state and conductance graph 
2. task4a.py     : To plot potentiation and depression curve of memristor
3. task9.py      : To find the input setting of single pseudo-memcapacitor with different parameters sweeped via python
4. task10a.py    : To find the input setting of 3X1 pseudo-memcapacitor with different parameters sweeped via python
5. task10b.py    : To find the input setting of 3X1 pseudo-memcapacitor with different parameters for ttfs input; sweeped via python
6. task12a.py    : To find the input setting of 3X3 pseudo-memcapacitor with different parameters (Column-wise) sweeped via python
7. task12b.py    : To find the input setting of 3X3 pseudo-memcapacitor with different parameters (Row-wise) sweeped via python

### Other file details
1. groupK_project3.pptx               : final presentation ppt
2. Project3_Neurotransistor_SPICE.pdf : describes details of task of this projects
3. requirements.txt                   : lists the required python modules to run python file