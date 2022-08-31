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

Since the Python datetime object is limited to microsecond resolution, 
it is necessary to use the Pandas datetime to plot sampled values with 
the required resolution.
