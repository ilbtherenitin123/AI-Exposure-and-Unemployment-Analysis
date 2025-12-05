# AI-Exposure-and-Unemployment-Analysis
# Data Directory

This folder is intentionally empty in the public repository.

Due to licensing restrictions, the underlying ILO datasets used in the analysis
cannot be redistributed. To reproduce the results, download the following files
and place them in this `data/` directory:

1. `ilo_employment_by_occupation.csv`  
   - Source: ILOSTAT (https://ilostat.ilo.org)  
   - Description: National employment by occupation (ISCO-08), most recent year

2. `ilo_2025_exposure_by_isco4.xlsx`  
   - Source: ILO AI exposure dataset (ILO, 2025)  
   - Description: Task-based exposure scores and gradient classification for
     ISCO-08 4-digit occupations

Once these files are placed here, the R script `code/ai_exposure_G4_analysis.R`
will read them and produce the outputs in `outputs/`.
