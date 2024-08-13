# -*- coding: utf-8 -*-
"""
OpenPMU - TSSV Data Selector
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
Time Synchronised Sampled Value (TSSV) Data Selector
TSSV Data Selector is intended for use of continuous TSSV files 
produced by OpenPMU devices. It will also work on such files 
produced by other devices using the same TSSV file format and 
data structure (i.e. WAVE and FLAC).

Usage:

- Place all the files to be plotted in one directory with no other files.
- Set "start_time" and "duration_ms"
- Run code
"""

import soundfile as sf
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, AutoLocator, AutoMinorLocator, MultipleLocator

def select_file_from_timestamp(time_in, extension='.flac', file_interval=5):
    
    # Round down start time to the nearest 5 minutes
    file_minute = time_in.minute - (time_in.minute % file_interval)
    file_time = time_in.replace(minute=file_minute, second=0, microsecond=0)
    
    # Convert start time to filename
    filename = file_time.strftime("%Y-%m-%d_%H-%M-%S") + extension
    
    return filename

def extract_audio_section(start_time, duration_ms, file_interval=5, directory=''):

    # Open the first audio file
    audio_file = sf.SoundFile(directory + select_file_from_timestamp(start_time))
    
    # Calculate the start position in samples
    start_seconds = (start_time.minute % file_interval)*60 + start_time.second + start_time.microsecond / 1000000
    start_sample = int(start_seconds * audio_file.samplerate)
    
    # print(start_seconds)
    # print(start_sample)
    
    # Seek to the start position in the file
    audio_file.seek(start_sample)
    
    # Read audio data for the specified duration
    duration_samples = int(duration_ms * audio_file.samplerate / 1000)
    audio_section = audio_file.read(duration_samples)
    
    remaining_duration_ms = duration_ms - (len(audio_section) / audio_file.samplerate * 1000)
    
    loop_count = 0 # While loop failsafe
    
    while remaining_duration_ms > 0:
        
        # Get the next filename
        next_start_time = start_time + timedelta(seconds=len(audio_section) / audio_file.samplerate)
        next_filename = next_start_time.strftime("%Y-%m-%d_%H-%M-%S.flac")
        
        # Open the next audio file
        next_audio_file = sf.SoundFile(select_file_from_timestamp(next_start_time))
        
        # Read the remaining audio data
        remaining_duration_samples = int(remaining_duration_ms * next_audio_file.samplerate / 1000)
        remaining_audio_section = next_audio_file.read(remaining_duration_samples)
        
        # Append the remaining audio to the current section
        audio_section = np.concatenate((audio_section, remaining_audio_section))
        
        # Close the next audio file
        next_audio_file.close()
        
        remaining_duration_ms = duration_ms - (len(audio_section) / audio_file.samplerate * 1000)
    
        # While loop failsafe
        loop_count += 1
        if loop_count > 12:
            break
    
    audio_file.close()
    
    return audio_section, audio_file.samplerate

# Custom formatter function for time axis labels
def format_time(x, pos=None):
    total_seconds = x / 1000  # Convert milliseconds to seconds
    hours = int(total_seconds // 3600)
    total_seconds %= 3600
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    milliseconds = int(x % 1000)
    # return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    return f"{seconds:02d}.{milliseconds:03d}"

if __name__ == "__main__":
    # Example usage
    start_time = datetime(2024, 3, 17, 9, 4, 56, microsecond=450000)
    duration_ms = 200  # duration in milliseconds

    TSSV_data, samplerate = extract_audio_section(start_time, duration_ms)
    # print("TSSV data:", TSSV_data)
    # print("Sample rate:", samplerate)




    # Generate time axis in milliseconds
    time_ms = np.arange(len(TSSV_data)) / samplerate * 1000

    time_ms += start_time.microsecond / 1000

    # Plot the audio data
    plt.figure(figsize=(10, 4))
    plt.plot(time_ms, TSSV_data)
    plt.xlabel(f"Time (ms) - (Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S.%f')} UTC)")


    # Customize the time axis labels

    # plt.gca().xaxis.set_major_locator(AutoLocator())
    # plt.gca().xaxis.set_minor_locator(AutoMinorLocator())

    plt.ylabel("Amplitude")
    plt.grid(True)

    # Enable minor gridlines
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')

    # Add vertical gridlines at every 20 ms interval
    base_frequency = 50                         # Nomiinal system frequency in Hertz
    base_period = (1 / base_frequency) * 1000   # Period in ms
    first_synchrotick = int(((start_time.microsecond / 1000) // base_period ) * base_period)
    for t in range(first_synchrotick, int(max(time_ms)), 20):
        plt.axvline(x=t, color='green', linestyle='--', linewidth=0.5)


    # Customize the time axis ticks
    major_locator = MultipleLocator(20)  # Preferred tick locations at 20 ms intervals
    major_locator = AutoLocator()
    plt.gca().xaxis.set_major_locator(major_locator)
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator())
    plt.gca().xaxis.set_major_formatter(lambda x, pos: f"{x:.0f}")  # Format tick labels as integers
    plt.gca().xaxis.set_major_formatter(FuncFormatter(format_time))


    # Use AutoLocator and AutoMinorLocator for minor ticks

    plt.gca().yaxis.set_minor_locator(AutoMinorLocator())


    plt.show()


