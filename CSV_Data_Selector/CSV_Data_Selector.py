# -*- coding: utf-8 -*-
"""
OpenPMU - CSV Phasor Data Selector
Copyright (C) 2024  www.OpenPMU.org

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
CSV Phasor Data Selector is intended for use of continuous CSV phasor record
files produced by OpenPMU devices. It will also work on such files 
produced by other devices using the same CSV phasor file format and 
data structure.

Usage:

- Place all the files to be plotted in one directory with no other files.
- Set "start_time" and "duration_ms"
- Run code
"""

from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, AutoLocator, AutoMinorLocator, MultipleLocator

# Uses datetime object to select appropriate CSV file
def select_file_from_timestamp(time_in, extension='.csv', file_interval=10):
    
    # Round down start time to the nearest 5 minutes
    file_minute = time_in.minute - (time_in.minute % file_interval)
    file_time = time_in.replace(minute=file_minute, second=0, microsecond=0)
    
    # Convert start time to filename
    filename = file_time.strftime("%Y-%m-%d_%H-%M-%S") + extension
    
    return filename

# Rounds datetime object down to nearest phasor report based on reporting rate
def round_datetime_down(dt, phasor_rate=50):
    
    # Calculate the period between phasors, use integer division (//)
    # Note: 60th of a second is approximately 16.6667 milliseconds or 16,666.67 microseconds
    period_ms = 1000000 // phasor_rate  # 1 second = 1,000,000 microseconds
    
    # Find the remainder of the current microsecond count when divided by the phasor period
    remainder = dt.microsecond % period_ms
    
    # Subtract the remainder from the current datetime to round down
    rounded_dt = dt - timedelta(microseconds=remainder)
    
    return rounded_dt

# Opens the CSV file and returns a Pandas dataframe (df) filtered by datetime
def open_and_filter_file(csv_filename, start_time, end_time):
    # Open the CSV file
    try:
        df = pd.read_csv(csv_filename)
    except:
        print("File does not exist:", csv_filename)
        return None
        
    # Create Pandas Datetime object (NB: This is NOT the same as Python datetime!)
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    
    # Filter the data by time stamps
    df_filtered = df[(df['Datetime'] >= start_time) & (df['Datetime'] <= end_time)]
    
    return df_filtered
    

def extract_phasor_section(start_time, duration_ms, phasor_rate=50, file_interval=10, directory=''):
    
    # Calculate the end time of the phasor data requested
    end_time = round_datetime_down(start_time + timedelta(milliseconds=duration_ms), phasor_rate)
    
    # Open the first CSV file and get filtered Pandas dataframe   
    df_filtered = open_and_filter_file(directory + select_file_from_timestamp(start_time), start_time, end_time)

    # Check to see if there is remaining data required
    remaining_duration_ms = int( (end_time - max(df_filtered['Datetime'])).total_seconds() * 1000 )
     
    loop_count = 0 # While loop failsafe
    
    while remaining_duration_ms > 0:
        
        # Get the next filename
        next_file_time = start_time + timedelta(seconds=len(df_filtered) * (1/phasor_rate))

        # Get the next filename
        next_df_filtered = open_and_filter_file(directory + select_file_from_timestamp(next_file_time), start_time, end_time)
        
        # Concatenate new data with existing data, ignore old index and create new one      
        df_filtered = pd.concat([df_filtered, next_df_filtered], ignore_index=True)
        
        # Check if loop needs to continue        
        remaining_duration_ms = int( (end_time - max(df_filtered['Datetime'])).total_seconds() * 1000 )
    
        # While loop failsafe
        loop_count += 1
        if loop_count > 12:
            break
    
    return df_filtered

# # Custom formatter function for time axis labels
# def format_time(x, pos=None):
#     total_seconds = x / 1000  # Convert milliseconds to seconds
#     hours = int(total_seconds // 3600)
#     total_seconds %= 3600
#     minutes = int(total_seconds // 60)
#     seconds = int(total_seconds % 60)
#     milliseconds = int(x % 1000)
#     # return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
#     return f"{seconds:02d}.{milliseconds:03d}"

if __name__ == "__main__":
    # Example usage
    start_time = datetime(2024, 6, 25, 0, 9, 56, microsecond=500000)
    duration_ms = 600*1000 + 3520  # duration in milliseconds
    
    # Get phasor data as Pandas dataframe
    phasor_df = extract_phasor_section(start_time, duration_ms, directory='Phasors/')

    print(len(phasor_df))
    print(min(phasor_df['Datetime']))
    print(max(phasor_df['Datetime']))



    phasor_dict= phasor_df.to_dict('records')
    
    for phasor in phasor_dict:
        phasor["Datetime"] = phasor["Datetime"].to_pydatetime()
 


    # Generate time axis in seconds
    time_s = np.arange(len(phasor_df)) * 1/50
    time_s += start_time.microsecond / 1000000

    # # Plot the frequency data
    plt.figure(figsize=(10, 4))
    #plt.plot(phasor_df['Datetime'], phasor_df['Freq0'])
    plt.plot(time_s, phasor_df['Freq0'])
    plt.xlabel(f"Time (s) - (Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S.%f')} UTC)")


    # Customize the time axis labels

    plt.gca().xaxis.set_major_locator(AutoLocator())
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator())

    plt.ylabel("Frequency (Hz)")
    plt.grid(True)

    # Enable minor gridlines
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')

    plt.show()


