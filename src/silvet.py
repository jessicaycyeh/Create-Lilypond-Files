import matplotlib.pyplot as plt
import numpy as np
import math
from Note import Note, Measure, Song 
from general import find_type, post_process, get_template_t, find_beat_id

# Config
csv_file = "csv/spectrogram.csv"
unit_time = 0.046439909 # Based on the selected window time
bpm = 124 # Find BPM at https://songbpm.com/
Time = (4,4) # 4 beats a measure, fourth note as one beat
key_signature = ('ees', 'major') # Key signature of the song, can also be found at https://songbpm.com/
title = "Test"
CAPO = 3 # Set minimum fret
instruments = "both" # Specify the instruments "guitar", "piano", or "both"
omit_stringNum = True
max_line = 100 # Only create a subset of the score
absolute_threshold = 0.1 # To filter out the rests
# relative_strength = 0.75 # Decide how loud can be counted as a new note
start_octave = 0 # The lowest octave. Default: 0 (C3-B3)
plugin = "silvet"
total_duration = 100 # [s]
offset = 0.68 # The time song starts [s]

notes_dict = {'C':'c', 'C#':'cis', 'D':'d', "D#":'dis', 'E':'e', 'E#':'eis', 'F':'f', "F#":'fis',\
	'G':'g', 'G#':'gis', 'A':'a', "A#":'ais', 'B':'b', 'B#':'bis', 'Cb':'ces', 'Db':'des',\
	'Eb':'ees', 'Gb':'ges','Ab':'aes','Bb': 'bes'}

def load_notes(filename, my_song): 
	# Load notes from silvet plugin
	# TIME,VALUE,DURATION,LEVEL,LABEL
	# 0.500000000,155.563,1.480000000,0.181102,D#3

	file = open(filename)
	first_line = file.readline()
	line = file.readline()
	count = 1
	while line:
		count += 1
		time, val, duration, level, label = line.split(',')
		time = float(time) - offset
		if float(level) > absolute_threshold:
			note_type = find_type(float(duration), bpm)
			if count == row_count:
				octave = int(label[-1]) - 3
				_note = label[:-1]
			else:
				octave = int(label[-2]) - 3
				_note = label[:-2]
			# print("octave:", octave, "_note:", _note)
			note_name = notes_dict[_note]
			note_name = post_process(note_name, octave)
			template_t = get_template_t(my_song.tot_beats)
			beat_id = find_beat_id(time, bpm, template_t)
			measure_id = int(beat_id / Time[0])
			# measure_id = int(time / my_song.measure_duration)  # Maybe another way to decide?
			# t = (time - measure_id * my_song.measure_duration) 
			# beat_in_measure = find_beat_in_measure(t, my_song.measure_duration)
			n = Note(note_name, time, note_type, measure_id)
			n.set_beat_id(beat_id)
			m = my_song.get_measure(measure_id)
			m.add_note(n)
			# print(n.print_note())
		line = file.readline()
def cal_offset(filename):
	file = open(filename)
	first_line = file.readline()
	line = file.readline()
	# found = False
	while True:
		time, val, duration, level, label = line.split(',')
		if float(level) > absolute_threshold:
			return float(time)
file = open(csv_file)
row_count = sum(1 for row in file)
my_song = Song(total_duration, bpm, Time, key_signature)
load_notes(csv_file, my_song)
print(my_song.print_song(3, 'sun'))
# print(my_song.get_num_notes())
# print(my_song.num_measure)
# for i in range(10,20):
# 	m = my_song.get_measure(i)
# 	print("This is measure:", m.id)
# 	print(m.print_measure())
	# for n in m.notes:
		# print("name:", n.name, "type:", n.type, "beat_id:", n.beat_id)

