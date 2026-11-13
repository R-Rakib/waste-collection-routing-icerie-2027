# Supplementary Materials: A Two-Stage Clustered MILP Framework for Efficient and Resilient Waste Collection Routing

**Paper ID:** 87  
**Conference:** 9th International Conference on Engineering Research, Innovation, and Education (ICERIE 2027)  
**Authors:** Riasad Rahman Rakib, Hasin Almas Sanim, Md. Mohibul Islam  
**Affiliation:** Department of Industrial & Production Engineering, Rajshahi University of Engineering & Technology (RUET), Rajshahi-6204, Bangladesh

## About

This repository provides supplementary materials for the research paper titled *A Two-Stage Clustered MILP Framework for Efficient and Resilient Waste Collection Routing*.

The study develops a cluster-first, route-second framework for waste collection in Rajshahi City Corporation (RCC). K-means clustering groups 20 Secondary Transfer Stations (STS) into four zones, and a Mixed-Integer Linear Programming (MILP) model optimizes the routing of a heterogeneous fleet of shuttles and sweepers within each zone.

Due to the conference paper's page limit, the complete dataset, cluster assignments, detailed mathematical formulation, and extended results are provided separately in this repository.

## Repository Structure

| Folder/File | Contents |
|---|---|
| `Supplementary Materials/` | Detailed supplementary document |
| `code/` | Python implementation of the MILP model and K-means clustering |
| `dataset/` | Research datasets used in the study |
| `README.md` | Repository documentation |

## Contents of the Supplementary Document

| Section | Topic | Tables and Figures |
|---|---|---|
| 1 | Introduction and abbreviations | |
| 2 | Dataset and STS information | Tables S1–S3 |
| 3 | Clustering method and results | Table S4, Figure S1 |
| 4 | Complete MILP formulation | Tables S5–S6, Equations (1)–(17) |
| 5 | Optimization results by scenario | Table S7 |
| 6 | Economic and sensitivity analysis | Table S8, Figure S2 |
| 7 | Additional figures | Figures S3–S4 |
| 8 | Reproducibility notes and data availability | |

## Relationship with the Conference Paper

| Conference Paper | Supplementary Material |
|---|---|
| Data and clustering (Section 2.2) | Sections 2 and 3 |
| Model formulation (Equations 1–17) | Section 4 |
| Scenario results (Table 2) | Section 5, Table S7 |
| Sensitivity analysis (Table 3, Figure 2) | Section 6, Table S8 |

## Data Summary

- 20 Secondary Transfer Stations (STS) in Rajshahi.
- Four K-means clusters.
- Three vehicle classes: 1.5-tonne sweepers, 3.0-tonne sweepers, and 5.0-tonne shuttles.
- Eleven scenarios (Z0–Z10).
- Total waste generation ranging from 434.68 to 470.60 tonnes per day.
- Daily cost reduction of 10.76%–17.52% compared with traditional dispatch.

## Reproducibility

The optimization model is implemented in Python and solved using Gurobi. The supplementary document provides additional details regarding the mathematical formulation, model inputs, assumptions, and computational results.

## Data and Code Availability

The supplementary materials, including the detailed mathematical formulation, Python implementation of the MILP model and K-means clustering algorithm, research datasets, additional figures, and extended results, are publicly available through Zenodo.

**DOI:** https://doi.org/10.5281/zenodo.24186922

## Citation

Please cite the corresponding ICERIE 2027 conference paper (Paper ID 87) when using this research material.

## Contact

**Corresponding Author:** Md. Mohibul Islam  
Department of Industrial & Production Engineering, RUET  
Email: mohibul@ipe.ruet.ac.bd