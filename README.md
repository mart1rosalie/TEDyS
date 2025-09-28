# TEDyS — Transposable Elements Dynamical System

## Introduction

**TEDyS** is a Python software to simulate the evolution of **Transposable Elements (TEs)** in a population of genomes under the assumption of **asexual reproduction**. The model implements a system of differential equations solved with a stochastic Gillespie algorithm. Running simulations produces time-resolved distributions of TEs across genomes, which can be analyzed to study departures from classical Poisson expectations and long-term persistence driven by over-dispersed genomic distributions.


---

## Repository structure

```
.
├── creation_of_datasets.sh           # Script to generate input datasets
├── initialization_of_simulations.csv # Example initialization file
├── LICENCE.rst                       # Licence file
├── output_long_data.csv              # Example output file (example output)
├── params_format.csv                 # Formated input (output of simulations.sh)
├── post_treatment.R                  # Post-processing and analysis in R
├── README.md                         # Documentation (this file)
├── simulations.sh                    # Main script to run simulations
└── src                               # Source code
    ├── main.py
    └── elements_transposables
        ├── arguments.py
        ├── file_csv.py
        ├── gillespie.py
        ├── individual.py
        ├── __init__.py
        └── verbose_mode.py
```

- `src/` contains the core Python implementation.
- Shell scripts (`creation_of_datasets.sh`, `simulations.sh`) are provided to create inputs and launch batches of simulations.
- Example parameter and initialization CSV files document expected formats.
- `post_treatment.R` contains example analysis workflows for simulation outputs.
- `output_long_data.csv` is an example of the simulation output format.


---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/mart1rosalie/TEDyS.git
cd TEDyS
```

2. Install dependencies:

Install the usual scientific `numpy` library.

---

## Quick start — Running a simulation

1. Prepare or check the example parameter files: `initialization_of_simulations.csv`. 
2. (Optional) generate datasets with the provided script:

```bash
./creation_of_datasets.sh
```
3. Create a repertory for large files produced by TEDyS (`output`) and update `simulations.sh` accordingly.

4. Run the simulations (single run or batch):

```bash
./simulations.sh
```
The file `params_format.csv` is created by this script to serve as an input for Python script. 


---

## Configuration files

- **`creation_of_datasets.sh`** (Optional) generate datasets with same parameters for stochasticity.
- **`initialization_of_simulations.csv`** - example file specifying initial population of TEs, seeds, or parameters.
- **`simulations.sh`** - specifying duration and initial population of genomes and `output` repository.

Modify these CSVs to suit your experimental setup before running `simulations.sh`.

- **`params_format.csv`** - specific format for parameters used by the simulation script.
---

## Output format

- `output` repository contains long CSV files with raw distributions of TEs.
- The `post_treatment.R` script demonstrates how to compute summary statistics and plot distributions over time.
- `output_long_data.csv` contains time-stamped records of TE counts and distributions fit across individuals.


---

## Code structure and main modules

- `dynamique_elements_transposables.py` — high-level entry point that orchestrates simulations and I/O.
- `elements_transposables/arguments.py` — CLI and configuration parsing utilities.
- `elements_transposables/file_csv.py` — CSV read/write helpers and format validators.
- `elements_transposables/gillespie.py` — Gillespie algorithm implementation adapted to the TE dynamics.
- `elements_transposables/individual.py` — representation of individuals/genomes and per-individual state.
- `elements_transposables/verbose_mode.py` — logging/verbose utilities used for debugging and trace outputs.


---

## Post-processing and analysis

Run the provided R script to reproduce example figures and summary tables:

```bash
Rscript post_treatment.R
```

The script expects `output_long_data.csv` in the working directory (or adjust the path inside the script).


---

## Testing

No formal test suite is included in this release. To verify correct behavior, run the example scripts and compare `output_long_data.csv` to the included example file.


---

## Citation

If you use **TEDyS** in your research, please cite:


---

## Contributing

Contributions are welcome. Please open issues or pull requests on the repository. For major changes, please first open an issue to discuss the proposed changes.


---

## Contact

For questions, contact: Martin ROSALIE — martin.rosalie@univ-perp.fr


---

## Acknowledgements

This software was developed while the author held positions at [LGDP](https://lgdp.univ-perp.fr). Funding/support: 

> This study is set within the framework of the *Laboratoires d'Excellences* (LABEX) TULIP (ANR-10-LABX-41) and of the *Ecole Universitaire de Recherche* (EUR) TULIP-GS (ANR-18-EURE-0019).
