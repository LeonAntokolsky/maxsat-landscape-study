# An Empirical Study of Local Properties in MAX-SAT Landscapes

This repository contains the source code and supporting material for my M.Sc. thesis:

📄 **An Empirical Study of Local Properties of the Landscape of the Maximum Satisfiability Problem**  
Sami Shamoon College of Engineering, 2025.

The project explores the structure of local optima in random MAX-SAT instances through computational experiments and statistical analysis.

## 🎯 Research Focus

- **Local optima ratio**: proportion of locally optimal assignments among all assignments.
- **Same-height neighbors**: fraction of neighbors with equal quality.
- **Hamming distance analysis**: diversity and distribution of local optima across problem families.
- **Statistical metrics**: mean/median heights, standard deviation, mean absolute deviation.

## 📂 Repository Structure

- `thesis/` — PDF of the full thesis.
- `experiments/` — Python scripts for each experiment.
  - `exp1_local_optima_ratio.py` — overall/local optima distribution.
  - `exp2_neighbors_same_height.py` — analysis of neighbors at equal heights.
  - `exp3_hamming_distance.py` — pairwise distances between local optima.
  - `utils.py` — shared helper functions (instance generation, evaluation, etc.).
- `data/` — optional folder for generated instances or stored results.
- `results/` — plots and aggregated statistics.
- `requirements.txt` — Python dependencies.

## ⚙️ Requirements

- Python 3.10+
- Libraries:
  ```text
  numpy
  matplotlib
  seaborn
  tqdm

📊 Example Outputs

Distribution of local optima ratios across instances.

Histograms of neighbor similarity.

Hamming distance statistics visualized by family parameters.

📄 Thesis

The full text of the thesis can be found in:

thesis/An_Empirical_Study_of_Local_Properties.pdf
