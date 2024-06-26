# OpenPMU_Analysis
A set of tools which helps analysis the synchrophasor and CPOW data produced by OpenPMU devices.

The tools contained in this repository are intended for the file formats produced by OpenPMU V2 devices, but may prove useful for analysis of data from other PMUs which follow a similar file format and data structure.

## Tools

* **Multi-CSV Plotter:**  Allows multiple files of synchrophasors recorded in CSV format to be concatenated and plotted.
* **Multi-CPOW Plotter:**  Allows multiple time synchronised CPOW sampled value waveform files to be concatenated and plotted.
* **TSSV Data Selector:**  Allows selection of small sections TSSV data from OpenPMU's continuous recording of TSSV data.

### Note on Time

All times are in UTC.  

* Times **DO NOT** adjust for summer time / winter time.  
* Times **DO NOT** adjust for different time zones around the world.  

If you require presentation of the time in local time, this can be accomodated at the time of graph plotting.
