# Multi-CPOW Plotter

Multi-CPOW Plotter is intended for use on Time Synchronised CPOW files 
produced by OpenPMU devices.  Usually these files are in WAVE or FLAC audio 
formats.  This programme will concatenate several such files together, and 
construct a time axis for plotting.

Usage:
* Place all the files to be plotted in one directory with no other files.
* Set "cpowPath" to that directory
* Run code
    
The code will produce a large array of the CPOW sampled value data called 
"bigCPOW".  May contain more than one waveform.

To-do:
-------
Since Python's "datetime" objects are limited to microsecond resolution, 
need to investigate better solution for time-axis (e.g. Pandas datetime).
