# -*- coding: utf-8 -*-
"""
OpenPMU - Multi-CSV Plotter
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
Multi-CSV Plotter is intended for use of Synchrophasor CSV files produced
by OpenPMU devices.  It will also work on CSV files produced by other devices
using the same CSV file format and data structure.

Usage:
    - Place all the files to be plotted in one directory with no other files.
    - Set "csvPath" to that directory
    - Run code
    
The code will produce a large "list of dictionaries" called "bigList".  This 
data can be plotted using list comprehension.  See example which plots "Freq0".
"""

import glob
import csv
from datetime import datetime
import matplotlib.pyplot as plt

csvPath = "C:\\2022-08-29\\2022-08-29_Phasors\\"

bigList = []

# Parse through all the CSV files in the given path
for csvFilePath in glob.glob(csvPath + "*"):
    
    # Print name of file presently in use
    print(csvFilePath)
    
    # Open the CSV file using the "Dictionary Reader", uses the first row for keys
    with open(csvFilePath) as csvFile:
    
        reader = csv.DictReader(csvFile)
        
        for row in reader:
            
            # Convert the individual Date and Time strings to Python Datetime Object
            try:
                timeDT = datetime.strptime(row["Date"] + " " + row["Time"], "%Y-%m-%d %H:%M:%S.%f")
            except:
                timeDT = datetime.strptime(row["Date"] + " " + row["Time"], "%Y-%m-%d %H:%M:%S")
            
            row["timeDT"] = timeDT
            
            # Convert strings to floats
            for key in row:                
                try:
                    row[key] = float(row[key])
                except:
                    pass
            
            # Frame number is always an integer
            row["Frame"] = int(row["Frame"])
            
            # Append current row to "bigList"
            bigList.append(row)
            
            # Print time so progress can be seen (faster not to!)
            # print(row["timeDT"])


# Example plotting function for "Freq0" against "timeDT" using list comprehension
plt.figure(1)
plt.plot([data['timeDT'] for data in bigList], \
    [data['Freq0'] for data in bigList])
plt.grid(True)
plt.show()
    
