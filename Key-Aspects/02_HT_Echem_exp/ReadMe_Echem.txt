____________________Key Aspects in Designing High-Throughput Workflows in Electrocatalysis Research: A Case Study on IrCo Mixed-Metal Oxides____________________

Last updated: 2024-10-16

______Contact______
* Joanna Przybysz
* j.przybysz@fz-juelich.de
* +49 9131-12538187
* ORCID: 0009-0000-8402-5691
* Helmholtz Institute Erlangen-Nürnberg for Renewable Energy
* Cauerstraße 1, 91058 Erlangen, Germany 

______Licence______
*Dataset for "Key Aspects in Designing High-Throughput Workflows in Electrocatalysis Research: A Case Study on IrCo Mixed-Metal Oxides" © 2024 by Joanna Przybysz is licensed under CC BY 4.0
*licence information: https://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1

------------------------------------------------------------------------------------------------

______About the dataset______
Electrochemical measurements were performed by: 
* Joanna Przybysz
* ORCID: 0009-0000-8402-5691
* Helmholtz Institute Erlangen-Nürnberg for Renewable Energy
* Cauerstraße 1, 91058 Erlangen, Germany 

______Methods of data collection______
All electrochemical measurements were performed using an SFC setup coupled to ICP-MS for on-line stability measurements. In an SFC, the scanning cell is mounted above an xyz-translational stage housing a working electrode. It is connected via tubing with an Ag|AgCl|3 M KCl reference electrode on the cell outlet and a glassy carbon counter electrode (SIGRADUR G, HTW) on the cell inlet. A separate channel in the cell delivers argon gas around the measured area of the working electrode. The electrolyte flow was controlled using a peristaltic pump (Reglo ICC, Ismatec). The electrolyte was purged with argon gas in a purging reservoir prior to entering the SFC. All elements of the system were connected by Tygon tubing.
All hardware was controlled using software developed in-house, which enables measurement automation. Electrochemical measurements were performed using a potentiostat (Ref600, Gamry). After initial calibration of the position of the first spot (located in the upper left corner of the material library) by alignment with the SFC opening, the SFC is capable of accurate navigation over the whole ML using spot coordinates extracted from ML overview images recorded using the LSM with a Python script and loaded into the SFC software. A detailed description of the automated SFC(-ICP-MS) operation can be found in the following reference (Jenewein, K. J.; Akkoc, G. D.; Kormányos, A.; Cherevko, S. Automated high-throughput activity and stability screening of electrocatalysts. Chem Catalysis 2022, 2 (10), 2778–2794. DOI: 10.1016/j.checat.2022.09.019.).
The combined activity and stability measurements were performed using the SFC coupled to an ICP-MS (Nexion 350X, PerkinElmer) by Tygon tubing, where all outflowing electrolyte was introduced into the ICP-MS. The ICP-MS was optimized daily, prior to the measurements, using a NexION Setup Solution (Perkin Elmer), and the dissolution signals of 193Ir and 59Co were quantified using a four-point calibration curve (0, 0.5, 1, 5 μg L-1). Calibration solutions were prepared daily. 187Re and 74Ge were used as internal standards at a 10 μg L-1 concentration (Certipur ICP-MS Standard, Merck).
The measurements were conducted in 0.05 M H2SO4 electrolyte, with a galvanostatic protocol composed of a hold at open circuit potential (OCP) for 300s, 5x CP holds @ 1 mA cm-2geom, each one for 60s, followed by 60s at open circuit potential (OCP), a CP ramp consisting of a sequence of 30s CP holds at 0.1, 0.2, 0.4, 1, 2, 4, and 10 mA cm-2, and OCP. The chosen low current densities allow for stability screening within reasonable measurement time and prevent overloads that might occur due to bubble formation during measurements. Two spots were measured for each composition.



______Methods of data processing______
All electrochemical potentials reported in this work were recalculated against the reversible hydrogen electrode (RHE). Full iR compensation was applied. 
The material capacitance was obtained by measuring CVs at 50 mV s-1, 100 mV s-1, and 200 mV s-1 scan rates in a 0.4 – 1.4 VRHE potential window in 0.05 M H2SO4, extracting capacitive current at 0.5 VRHE and 1.2 VRHE, plotting it over the scan rate and extracting the slope of the obtained linear function ic = Cν, where ic is capacitive current, C is capacitance and ν is the scan rate.
The used capacitive current was half of the net difference between the anodic and cathodic sweep at a given potential.

------------------------------------------------------------------------------------------------
______File formats______
.txt

______Abbreviations______
E	potential
j	current density
j C	current normalized by capacitance 
j Ageo	current normalized by geometrical area
XRF	X-ray fluorescence
Overpot	overpotential
at.-%	atomic percent
S-number	stability number
std	standard deviation

------------------------------------------------------------------------------------------------
______List of files______

Activity (LSV):
Co.txt
Ir.txt 
IrCo2080.txt
IrCo4060.txt
IrCo6040.txt
IrCo8020.txt

Dissolution_exp:
Co.txt
Ir.txt 
IrCo2080.txt
IrCo4060.txt
IrCo6040.txt
IrCo8020.txt

Dissolution_analysis:
Dissolution%.txt
Overpot_change.txt
Snumber.txt
Tafel_slopes.txt
