# CDA 5106: Advanced Computer Architecture - Fall 2023
## Machine Problem 1 - Cache Design, Memory Hierarchy Design

Welcome to the Machine Problem 1 repository for the Advanced Computer Architecture course (CDA 5106) at the University of Central Florida, Fall 2023. This project involves the implementation of a flexible cache and memory hierarchy simulator. The primary objective is to compare the performance, area, and energy of various memory hierarchy configurations using a subset of the SPEC-2000 benchmark suite.

## Repository Structure

### Directories
- **debug_runs:** This directory contains output files intended for debugging purposes. It helps in analyzing and fixing issues within the program.
- **validation_runs:** Similar to `debug_runs`, this directory holds output files used for validation. It assists in verifying the correctness and accuracy of the program.
- **outputs:** The `outputs` directory stores the generated output files from the program. These files represent the results and metrics obtained during the simulation runs.
- **traces:** This directory includes trace files that serve as input to the program. Traces are essential for simulating memory access patterns.
- **commands.txt:** A text file providing relevant commands to run the program in various configurations. It serves as a quick reference for executing the simulation with different parameters.

### Program Files
- **debug.py:** This Python program is responsible for generating output in a debug-friendly format. The resulting file format aligns with those found in the `debug_runs` folder, facilitating debugging processes.
- **run.py:** A Python script designed to execute the program with all required configurations. It streamlines the process of running the simulation under different scenarios.
- **sim_cache.py:** The main cache simulator file. `run.py` invokes this Python program to obtain all necessary outputs. The file is the core implementation of a multilevel cache simulation.
- **validate.py:** This Python script runs `sim_cache.py` with validation configurations and prints a diff with the given validation files. It aids in ensuring the accuracy of the simulation results.


## How to Run sim_cache.py
To execute the `sim_cache.py` program, use the following command format:

```bash
python sim_cache.py <BLOCKSIZE> <L1_SIZE> <L1_ASSOC> <L2_SIZE> <L2_ASSOC> <REPLACEMENT_POLICY> <INCLUSION_PROPERTY> <trace_file>
```

- **BLOCKSIZE:** Positive integer. Block size in bytes (same block size for all caches in the memory hierarchy).
- **L1_SIZE:** Positive integer. L1 cache size in bytes.
- **L1_ASSOC:** Positive integer. L1 set-associativity (1 is direct-mapped).
- **L2_SIZE:** Positive integer. L2 cache size in bytes. L2_SIZE = 0 signifies no L2 cache.
- **L2_ASSOC:** Positive integer. L2 set-associativity (1 is direct-mapped).
- **REPLACEMENT_POLICY:** Positive integer. 0 for LRU, 1 for FIFO.
- **INCLUSION_PROPERTY:** Positive integer. 0 for non-inclusive, 1 for inclusive.
- **trace_file:** Character string. Full name of the trace file, including any extensions.

### Example
```bash
python sim_cache.py 32 8192 4 262144 8 0 0 ./traces/gcc_trace.txt
```
