# Multi-CSV Plotter

Multi-CSV Plotter is intended for use of Synchrophasor CSV files produced
by OpenPMU devices.  It will also work on CSV files produced by other devices
using the same CSV file format and data structure.

Usage:
* Place all the files to be plotted in one directory with no other files.
* Set "csvPath" to that directory
* Run code
    
The code will produce a large "list of dictionaries" called "bigList".  This 
data can be plotted using list comprehension.  See example which plots "Freq0".
