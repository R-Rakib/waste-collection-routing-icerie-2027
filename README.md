# Supplementary Materials: A Two-Stage Clustered MILP Framework for Efficient and Resilient Waste Collection Routing

**Paper ID:** 87
**Conference:** 9th International Conference on Engineering Research, Innovation, and Education (ICERIE 2027)
**Authors:** Riasad Rahman Rakib, Hasin Almas Sanim, Md. Mohibul Islam
**Affiliation:** Department of Industrial & Production Engineering, Rajshahi University of Engineering & Technology (RUET), Rajshahi-6204, Bangladesh

## About

This repository extends the paper above. The paper develops a cluster-first, route-second framework for waste collection in the Rajshahi City Corporation (RCC). K-means groups 20 secondary transfer stations (STS) into four zones, and a mixed-integer linear programming (MILP) model routes a heterogeneous fleet of shuttles and sweepers inside each zone. The page limit of the paper left out the full dataset, cluster assignments, the complete model and the extended results. They are provided here.

## Files

| File | Contents |
|:--|:--|
| `Supplementary_Materials_ICERIE2027_Paper87.docx` | Supplementary document (Word) |
| `figs/` | Figures S1 to S4 as image files |

## Contents of the supplementary document

| Section | Topic | Tables and figures |
|:--|:--|:--|
| 1 | Introduction and abbreviations | |
| 2 | Dataset and STS information | Tables S1 to S3 |
| 3 | Clustering method and results | Table S4, Figure S1 |
| 4 | Complete MILP formulation (sets, parameters, variables, objective, constraints, assumptions) | Tables S5 and S6, Eqs. (1) to (17) |
| 5 | Optimization results by scenario | Table S7 |
| 6 | Economic and sensitivity analysis | Table S8, Figure S2 |
| 7 | Additional figures | Figures S3 and S4 |
| 8 | Reproducibility notes and data availability | |

## Where each part connects to the paper

| Paper | Supplementary document |
|:--|:--|
| Data and clustering (Section 2.2) | Section 2 and Section 3 |
| Model formulation (Eqs. 1 to 17) | Section 4 |
| Scenario results (Table 2) | Section 5, Table S7 |
| Sensitivity analysis (Table 3, Fig. 2) | Section 6, Table S8 |

## Data summary

- 20 STS in Rajshahi, with coordinates and daily waste generation of 8 to 31 t/day
- 4 K-means clusters
- 3 vehicle classes: sweepers of 1.5 t and 3.0 t, and a shuttle of 5.0 t
- 11 scenarios (Z0 to Z10), with total waste of 434.68 to 470.60 t/day
- Daily cost reduction of 10.76% to 17.52% against traditional dispatch

## Reproducibility

The model is solved for each cluster with Gurobi. The supplementary document states which model inputs are tabulated and which are not (Section 8.1).

## Citation

Please cite the ICERIE 2027 paper (Paper ID 87).

Repository DOI/URL: *to be added*

## Contact

Corresponding author: Md. Mohibul Islam, Department of IPE, RUET (mohibul@ipe.ruet.ac.bd)
