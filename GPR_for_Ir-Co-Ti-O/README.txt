This repository contains the data, code, and related files associated with the following publication:

Joanna M. Przybysz, Felix Thelen, Florian Lourens, Ken Jenewein, Alfred Ludwig, and Serhiy Cherevko
Gaussian Process Regression-Enhanced Screening of Ir–Co–Ti Mixed-Oxide Thin-Film Electrocatalyst Libraries for Acidic Oxygen Evolution
Digital Discovery (2026)
DOI: 10.1039/D6DD00127K

The dataset associated with this publication is available on Zenodo.
Dataset DOI: 10.5281/zenodo.19001670

Joanna M. Przybysz, Felix Thelen, Florian Lourens, Ken Jenewein, Alfred Ludwig, and Serhiy Cherevko
Gaussian Process Regression-Enhanced Screening of Ir–Co–Ti Mixed-Oxide Thin-Film Electrocatalyst Libraries for Acidic Oxygen Evolution
Digital Discovery (2026), DOI: 10.1039/D6DD00127K
The dataset was published on Zenodo with the following DOI: 10.5281/zenodo.19001670

Licensed under Creative Commons Attribution 4.0 International

The code was developed using: 
python=3.12.3
numpy=1.26.4
pandas=2.2.2
scikit-learn=1.5.0
numpy==1.26.4
torch==2.3.0
gpytorch==1.11
botorch==0.11.0
The environment is provided in GP-project-environment.yml
Before running the script, update the file paths PATH_DATA, PATH_COMP_EDX, to point to the desired experimental dataset and composition space.

The script
1. loads the experimental dataset,
2. splits the data into training and testing sets,
3. performs repeated cross-validation for kernel selection,
4. trains the final Gaussian process models,
5. evaluates prediction performance,
6. predicts material properties for all compositions in the supplied composition dataset,
7. exports the predictions in CSV format.

Input files: 
HT_summary_xxx.txt	Tab-delimited file containing elemental composition (Co, Ir, Ti; at.% excluding oxygen), overpotential, elemental dissolution.
EDX_xxx.csv	CSV containing compositions for which Gaussian process predictions are required.

Output files: 
DataandPredsxxx.csv	(or the corresponding filename selected by the user) CSV containing composition, predicted property values, and predictive standard deviations.

Citation:
If you use these data or code, please cite the publication and the Zenodo DOI: https://doi.org/10.5281/zenodo.19001670

List of all files and their descriptions: 

Filename	|Type	|Comments
---------------------------------------------------------------------------------------------------------------------
GPR_withkernelchoice.py	GPR code used in publication	Run in environment specified in GP-project-environment.yml
GP-project-environment.yml	environment setup file	Contains all the Python packages with versions used for the GPR predictions
EDX_500C.csv	experimental data	Results of EDX measurements of the 500C library. Measurement areas are referred to as 'spots' and have unique numbers.
EDX_RTemp.csv	experimental data	Results of EDX measurements of the RT library. Measurement areas are referred to as 'spots' and have unique numbers.
HT_summary_500C.txt	experimental data	Summary of SFC-ICP-MS high-throughput screening of activity (overpotential) and electrochemical dissolution (of Ir, Co and Ti) of the 500C library.
HT_summary_RTemp.txt	experimental data	Summary of SFC-ICP-MS high-throughput screening of activity (overpotential) and electrochemical dissolution (of Ir, Co and Ti) of the RT library.
XPS_500C_Pre-echem.csv	experimental data + GPR predicted data	Results of XPS measurements and predicted datapoints of the 'as prepared' 500C library. 
XPS_RTemp_Pre-echem.csv	experimental data + GPR predicted data	Results of XPS measurements and predicted datapoints of the 'as prepared' RT library.
XPS_500C_Post-echem.csv	experimental data + GPR predicted data	Results of XPS measurements and predicted datapoints of the 500C library measured after SFC-ICP-MS screening.
XPS_RTemp_Post-echem.csv	experimental data + GPR predicted data	Results of XPS measurements and predicted datapoints of the RT library measured after SFC-ICP-MS screening.
XRD_500C_main_peaks.csv	experimental data	Mapping of most probable crystalline phases that occur on the surface of the 500C library, as suggested by XRD analysis. Values are range-normalized peak intensities. 
XRD_RTemp_main_peaks.csv	experimental data	Mapping of most probable crystalline phases that occur on the surface of the RT library, as suggested by XRD analysis. Values are range-normalized peak intensities. 
XRD_500C_peak_1_17.1-19.6_deg_Co3O4.csv	experimental data	Mapping of the XRD peak position and intensity of the peak in range 17.1-19.6 deg assigned to Co3O4 in the 500C library.
XRD_500C_peak_2_26-30_deg_IrO2+Ti2O.csv	experimental data	Mapping of the XRD peak position and intensity of the peak in range 26-30 deg assigned to IrO2+Ti2O in the 500C library.
XRD_500C_peak_3_31.8-34.2_deg_Ir3Ti.csv	experimental data	Mapping of the XRD peak position and intensity of the peak in range 31.8-34.2 deg assigned to Ir3Ti in the 500C library.
XRD_500C_peak_4_33.5-36.3_deg_IrO2+Ti2O+Co3O4.csv	experimental data	Mapping of the XRD peak position and intensity of the peak in range 33.5-36.3 deg assigned to IrO2+Ti2O+Co3O4 in the 500C library.
XRD_500C_peak_5_36-37.9_deg_Co3O4+Ti2O.csv	experimental data	Mapping of the XRD peak position and intensity of the peak in range 36-37.9 deg assigned to Co3O4+Ti2O in the 500C library.
XRD_500C_peak_6_37-43_deg_Pt111+IrO2+Ti2O.csv	experimental data	Mapping of the XRD peak position and intensity of the peak in range 37-43 deg assigned to Pt111+IrO2+Ti2O in the 500C library.
XRD_500C_peak_7_40.35-43_deg_Ir3Ti.csv	experimental data	Mapping of the XRD peak position and intensity of the peak in range 40.35-43 deg assigned to Ir3Ti in the 500C library.
XRD_500C_peak_8_46-48.5_deg_Ir3Ti.csv	experimental data	Mapping of the XRD peak position and intensity of the peak in range 46-48.5 deg assigned to Ir3Ti in the 500C library.
XRD_500C_peak_9_53-55.5_deg_IrO2.csv	experimental data	Mapping of the XRD peak position and intensity of the peak in range 53-55.5 deg assigned to IrO2 in the 500C library.
XRD_500C_peak_10_64.5-66.5_deg_IrO2.csv	experimental data	Mapping of the XRD peak position and intensity of the peak in range 64.5-66.5 deg assigned to IrO2 in the 500C library.
XRD_500C_peak_11_66.5-68.5_deg_IrO2.csv	experimental data	Mapping of the XRD peak position and intensity of the peak in range 66.5-68.5 deg assigned to IrO2 in the 500C library.
XRD_500C_peak_12_81.5-84_deg_IrO2.csv	experimental data	Mapping of the XRD peak position and intensity of the peak in range 81.5-84 deg assigned to IrO2 in the 500C library.
XRD_RTemp_peak_1_26-28.5_deg_TiO2.csv	experimental data	Mapping of the XRD peak position and intensity of the peak in range 26-28.5 deg assigned to TiO2 in the RT library.
XRD_RTemp_peak_2_32-45_deg_Pt111.csv	experimental data	Mapping of the XRD peak position and intensity of the peak in range 32-45 deg assigned to Pt111 in the RT library.
DataandPreds500C.csv	GPR predicted data	Data predicted using GPR for the 500C library, including uncertainties
DataandPredsRT.csv	GPR predicted data	Data predicted using GPR for the RT library, including uncertainties
Preds1at.csv	GPR predicted data	Data predicted using GPR for the entire ternary composition range with 1at% intervals, using the GPR model trained on the 500C dataset.