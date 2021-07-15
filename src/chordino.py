import matplotlib.pyplot as plt
import numpy as np
import math
from Note import Note  

# Config
csv_file = 'csv/test-sound.csv'
unit_time = 0.046439909 # Based on the selected window time
bpm = 124 # Find BPM at https://songbpm.com/
time = (4,4) # 4 beats a measure, fourth note as one beat
key_signature = ('ees', 'major') # Key signature of the song, can also be found at https://songbpm.com/
title = "Test"
CAPO = 3 # Set minimum fret
instruments = "both" # Specify the instruments "guitar", "piano", or "both"
omit_stringNum = True
max_line = 100 # Only create a subset of the score
absolute_threshold = 2.5 # To filter out the rests
relative_strength = 0.75 # Decide how loud can be counted as a new note
start_octave = 0 # The lowest octave. Default: 0 (C3-B3)
plugin = "chrodino"
