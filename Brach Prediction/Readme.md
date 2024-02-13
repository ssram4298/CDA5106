# CDA 5106: Advanced Computer Architecture - Fall 2023
## Machine Problem 2 - Branch Prediction

Welcome to the Machine Problem 2 repository for the Advanced Computer Architecture course (CDA 5106) at the University of Central Florida, Fall 2023. This project involves the implementation of a branch predictor simulator and use it to design branch predictors well suited to the SPECint95 benchmarks.


## Repository Structure

### Directories
- **validation_runs:** Similar to `debug_runs`, this directory holds output files used for validation. It assists in verifying the correctness and accuracy of the program.
- **outputs:** The `outputs` directory stores the generated output files from the program. These files represent the results and metrics obtained during the simulation runs.
- **traces:** This directory includes trace files that serve as input to the program. Traces are essential for simulating memory access patterns.
- **commands.txt:** A text file providing relevant commands to run the program in various configurations. It serves as a quick reference for executing the simulation with different parameters.

### Program Files
- **debug.py:** This Python program is responsible for generating output in a debug-friendly format. The resulting file format aligns with those found in the `debug_runs` folder, facilitating debugging processes.
- **run.py:** A Python script designed to execute the program with all required configurations. It streamlines the process of running the simulation under different scenarios.
- **sim.py:** The main cache simulator file. `run.py` invokes this Python program to obtain all necessary outputs. The file is the core implementation of a multilevel cache simulation.
- **validate.py:** This Python script runs `sim.py` with validation configurations and prints a diff with the given validation files. It aids in ensuring the accuracy of the simulation results.


## How to Run sim_cache.py
To execute the `sim_cache.py` program, use the following command format:

```bash
python sim.py smith <B> <tracefile>
python sim.py bimodal <M2> <tracefile>
python sim.py gshare <M1> <N> <tracefile>
python sim.py hybrid <K> <M1> <N> <M2> <tracefile>
```

- **B** Positive integer. Number of counter bits used for prediction.
- **M1** Positive integer. Number of PC bits used to index the gshare table.
- **M2:** Positive integer. Number of PC bits used to index the bimodal table.
- **N:** Positive integer. Number of global branch history bits.
- **K:** Positive integer. Number of PC bits used to index the chooser table.
