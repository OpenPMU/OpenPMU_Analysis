# -*- coding: utf-8 -*-
"""
OpenPMU - Multi-CPOW Plotter
Copyright (C) 2022  www.OpenPMU.org

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
Multi-CPOW Plotter is intended for use on Time Synchronised CPOW files 
produced by OpenPMU devices.  Usually these files are in WAVE or FLAC audio 
formats.  This programme will concatenate several such files together, and 
construct a time axis for plotting.

Usage:
    - Place all the files to be plotted in one directory with no other files.
    - Set "cpowPath" to that directory
    - Run code
    
The code will produce a large array of the CPOW sampled value data called 
"bigCPOW".  May contain more than one waveform.

Since the Python datetime object is limited to microsecond resolution, 
it is necessary to use the Pandas datetime to plot sampled values with 
the required resolution.
"""

import glob
import soundfile as sf
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

cpowPath = "C:\\2022-08-29\\2022-08-29_CPOW\\"


bigCPOW = np.empty(0)   # Initialise an empty array to append new CPOW sampled value data to
startTime = None        # Initialise an empty startTime

# Parse through all the CPOW files in the given path
for cpowFilePath in glob.glob(cpowPath + "*"):

    # Use the date and time of the filename of the first file to set "startTime"
    if startTime == None:
        startTime = datetime.strptime(cpowFilePath.split("\\")[-1].split(".")[0], "%Y-%m-%d_%H-%M-%S")

    print(cpowFilePath)
    
    cpowData, sampleRate = sf.read(cpowFilePath)    # Read CPOW data from audio file
    
    bigCPOW = np.append(bigCPOW, cpowData)          # Append CPOW data to "bigCPOW" array
   

# Calculate duration of CPOW data
duration = len(bigCPOW) / sampleRate     
endTime = startTime + timedelta(seconds=duration)

print("Duration of bigCPOW: ", duration, "seconds")
print("START Time:          ", startTime)
print("END Time:            ", endTime)


# Prepare a time axis for plotting data
timeAxis = np.arange(0, duration, (1.0/sampleRate))             # Time starts at "0"
timeAxisPD = pd.date_range(startTime, endTime, len(bigCPOW))    # Time starts at "startTime" and uses Pandas datetime object

# Example plotting function
plt.figure(1)
plt.plot(timeAxisPD, bigCPOW)
plt.grid(True)
plt.show()
    
    

    
    

