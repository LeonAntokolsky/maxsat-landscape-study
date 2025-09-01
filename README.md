# An Empirical Study of Local Properties in MAX-SAT Landscapes

## 📖 Project Overview

This project accompanies my M.Sc. thesis *"An Empirical Study of Local Properties of the MAX-SAT Landscape"*.

### Motivation and Goal
The **Maximum Satisfiability (MAX-SAT)** problem is a central challenge in combinatorial optimization with applications in artificial intelligence, hardware verification, scheduling, and beyond.  
Despite its importance, the structure of MAX-SAT solution landscapes—especially the behavior and diversity of local optima—remains only partially understood.  
This research aims to fill that gap and provide insights that can guide the development of more effective heuristics and optimization algorithms.

**Goal:**  
To perform an empirical analysis of the structure of local optima in random MAX-SAT instances with varying parameters, focusing on:

- The share of assignments that are local optima.  
- The distribution of optima across different heights (number of satisfied clauses).  
- The fraction of neighbors with the same quality as a local optimum.  
- The Hamming distances between local optima at different heights.

### Key Definitions
- **Instance** – a specific set of clauses over a fixed set of variables.  
- **Configuration** – a truth assignment (True/False) to all variables in an instance.  
- **Height** – the number of satisfied clauses (a measure of solution quality).  
- **Neighbor** – a configuration differing in exactly one variable.  
- **Local optimum** – a configuration that cannot be improved by moving to any neighbor.  
- **Hamming distance** – the number of differing variable positions between two configurations.  

### Landscape Analysis
We treat each possible solution as a point in a high-dimensional landscape, where the “height” is the number of satisfied clauses.  
Local optima appear as peaks. By analyzing their distribution, heights, and mutual distances, we can better understand how rugged or smooth the landscape is.  
This helps predict the difficulty of search and informs the design of algorithms capable of navigating the landscape effectively.

### Research Methodology
- Generate random instances and random configurations.  
- Count satisfied clauses for each configuration.  
- Generate neighbors by flipping one variable at a time.  
- Identify local optima among all configurations.  
- Analyze distributions of local optima by height.  
- Compute Hamming distances between pairs of local optima.  

### Outcomes
Our experiments show clear structural patterns:
- The ratio and distribution of local optima strongly depend on problem parameters.  
- More complex instances exhibit greater diversity and larger Hamming distances.  
- Stable patterns appear within problem families with similar parameters.  

**Conclusion:**  
The study provides new quantitative insights into the landscapes of MAX-SAT problems and highlights how landscape-

## 🎯 Research Focus

- **Local optima ratio**: proportion of locally optimal assignments among all assignments.
- **Same-height neighbors**: fraction of neighbors with equal quality.
- **Hamming distance analysis**: diversity and distribution of local optima across problem families.
- **Statistical metrics**: mean/median heights, standard deviation, mean absolute deviation.

## 📂 Repository Structure

- `thesis/` — PDF of the full thesis.
- `experiments/` — Python scripts for each experiment.
This repository contains separate Python scripts for each experiment:

1. **Exp1 – Local Optimum Ratio**  
   Calculates the percentage of locally optimal assignments.

2. **Exp2 – Clause Satisfaction Count**  
   Counts the number of satisfied clauses for given configurations.

3. **Exp3 – Metrics for Percentages**  
   Computes summary statistics (mean, median, standard deviation, MAD) of local optima.

4. **Exp4 – Neighbor Analysis**  
   Evaluates the percentage of neighbors with the same quality (height).

5. **Exp5 – 100 Local Optima for Neighbors**  
   Studies 100 local optima and analyzes their neighborhood structures.

6. **Exp6 – Pairwise Distance Between 100 Local Optima**  
   Computes Hamming distances between local optima to measure diversity.

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
