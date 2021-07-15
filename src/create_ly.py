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

### General functions to use ###
def belong(note, l): # Decide if a Note object is in a list of Note objects, return the index of the matching Note
	note_name = note.get_name()
	for i in range(len(l)):
		name = l[i].get_name()
		if name == note_name:
			return i
	return "No"

def find_notes(line):
	notes = []
	data = line.split(',')
	time = float(data[0])
	max_amp = float(max(data[1:]))
	threshold = relative_strength * max_amp
	for i in range(1, len(data)):
		if (float(data[i]) > threshold) and (float(data[i]) >= absolute_threshold):
			note_name = notes_dict[i-1]
			notes.append(Note(note_name))
			# notes.append(notes_dict[i-1])
	return notes

def convert_dict(first_line, start_octave):
	d = {'C':'c', 'C#':'cis', 'D':'d', "D#":'dis', 'E':'e', 'E#':'eis', 'F':'f', "F#":'fis',\
	'G':'g', 'G#':'gis', 'A':'a', "A#":'ais', 'B':'b', 'B#':'bis', 'Cb':'ces', 'Db':'des',\
	'Eb':'ees', 'Gb':'ges','Ab':'aes','Bb': 'bes'}
	# d = {'C':"c'", 'C#':"cis'", 'D':"d'", "D#":"dis'", 'E':"e'", 'E#':"eis'", 'F':"f'", "F#":"fis'",\
	# 'G':"g'", 'G#':"gis'", 'A':"a'", "A#":"ais'", 'B':"b'", 'B#':"bis'", 'Cb':"ces'", 'Db':"des'",\
	# 'Eb':"ees'", 'Gb':"ges'",'Ab':"aes'",'Bb': "bes'"}
	octave = start_octave
	notes_dict = []
	elements = first_line.split(',') # Usually: ['TIME', 'A', 'Bb', 'B', 'C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab\n']
	for i in range(1, len(elements)):
		if elements[i] == 'C': # Decide when the notes cross an octave
			octave += 1
		if i == len(elements) -1 : #The last one is in the form 'Ab\n'
			note = elements[i][:-1]
		else:
			note = elements[i]
		add = d[note] # The next element in notes_dict
		if octave != 0: # Post-processing the note format
			if octave > 0: # Add "'" to denote higher octaves
				for i in range(octave):
					add += "'"
			else:			# Add "," to denote lower octaves
				for i in range(abs(octave)):
					add += ","
		notes_dict.append(add)
	return notes_dict

def find_raw_collection():
	raw_notes = []
	if max_line:
		count = 0 
		for i in range(max_line):
			line = file.readline()
			add = find_notes(line)
			raw_notes.append(add)
	else:
		line = file.readline()
		while line:
			add = find_notes(line)
			raw_notes.append(add) 
			line = file.readline()
	return raw_notes

# Test Section
Do = Note("c'")
Re = Note("d'")
Me = Note("e'")
Fa = Note("f'")
So = Note("g'")
La = Note("a'")
# unit_time = 0.5 
# bpm = 60 
test_raw_notes = [[],[],[Do], [Do],[So, La], [So,La], [Fa]]
# End of test section

def find_type(d): #input:duration [s], output: '16' or '8' ...etc
	type_dict = {0.25:'16', 0.333:'16.', 0.5:'8', 1:'4', 2:'2', 3:'2.', 4:'1'}
	template_d = np.array([0.25, 0.333, 0.5, 1, 2, 3, 4])
	one_beat_duration = 60 / bpm
	delta_d = np.abs(template_d * one_beat_duration - d)
	imin = np.argmin(delta_d)
	identified_d = template_d[imin]
	# print("identified_d", identified_d)
	return type_dict[identified_d]

def same_type(note_types):
	t = note_types[0]
	for i in range(1, len(note_types)):
		if not t == note_types[i]:
			return False
	return True 
def print_raw_notes(raw_notes):
	res = []
	for notes in raw_notes:
		add = []
		for note in notes:
			add.append(note.get_name())
		res.append(add)
	return res 
def cal_duration(raw_notes):
	string = ""
	index = 0
	while index < len(raw_notes):
		count = 1
		start_notes = raw_notes[index]
		if len(start_notes) == 0:
			next_notes = raw_notes[index+1]
			while len(next_notes) == 0:
				index += 1
				count += 1
				next_notes = raw_notes[index+1]
			index += 1
			note = 'r'
			duration = unit_time * count
			note_type = find_type(duration)
			string = string + note + note_type + ' '

		elif len(start_notes) == 1:
			if index == len(raw_notes) - 1:
				note = start_notes
				index += 1 # End the while loop 
			else:
				next_notes = raw_notes[index+1]
				while start_notes == next_notes:
					index += 1
					count += 1
					start_notes = raw_notes[index]
					next_notes = raw_notes[index+1]
				index += 1
				note = start_notes

		# print(note, count, index)

			if note:
				duration = unit_time * count 
				note_type = find_type(duration)
				string = string + note[0].get_name() + note_type + ' '
		else:
			notes = []
			note_types = []
			initial_index = index 
			for start_note in start_notes:
				index = initial_index
				if start_note.counted: # If this note is already counted before
					continue
				start_note.counted = True
				next_notes = raw_notes[index+1]
				next_index = belong(start_note, next_notes)
				while type(next_index) != str : # If start_note inside next_notes
					index += 1
					count += 1
					next_notes[next_index].counted = True
					# start_note = raw_notes[index]
					next_notes = raw_notes[index+1]
					next_index = belong(start_note, next_notes)
				index += 1
				note = start_note
				duration = unit_time * count 
				note_type = find_type(duration)
				notes.append(note)
				note_types.append(note_type)

			if same_type(note_types):
				notes_str = ""
				for note in notes:
					notes_str = notes_str + note.get_name() + " "
				string = string + "<" + notes_str + ">" + note_types[0] + ' '
			else:
				raise ValueError("Notes with different durations not implemented")

		# print("Current string:", string)
		# print("Current index:", index)

	string += '\\bar "|."'
	return string

### Add functions ###
def add_CAPO(string, CAPO):
	copy_str = "\\set TabStaff.minimumFret = #" + str(CAPO) + "\n" + "\\set TabStaff.restrainOpenStrings = ##t\n" + string
	return copy_str
def add_omit_stringNum(string):
	copy_str = '\\layout { \\omit Voice.StringNumber }\n' + string
	return copy_str
def add_header(string, title):
	header = '\\version "2.20.0"\n' + '\\header{title = "'+ str(title) + '"}\n'
	return header + string
def add_guitar(string):
	copy_str = "\\new TabStaff \\relative" + "{\n" + string + '}'
	return copy_str
def add_piano(string):
	copy_str = "\\new Staff \\relative {\n" + string + '}'
	return copy_str
def multiple_ins(string):
	copy_str = "\\new StaffGroup <<" + string + ">>"
	return copy_str
def add_key(string):
	return "\\key "+ str(key_signature[0]) + ' \\' + str(key_signature[1]) + ' '+ string 
def add_treb(string):
	return '\\clef "treble"' + ' '+ string
def add_time(string):
	return "\\time " + str(time[0]) + "/" + str(time[1]) + ' ' + string 
def add_tempo(string):
	return '\\tempo "Andante" ' + str(time[1])+  ' = ' + str(bpm) +'\n' + string 

### Create lilypond codes ###
def add_lilypond(main):
	main = str(main)
	string = main 
	if instruments == "guitar":
		if CAPO:
			string = add_CAPO(string, CAPO)
		string = add_guitar(string)
	elif instruments == "piano":
		string = add_tempo(string)
		string = add_time(string)
		string = add_key(string)
		string = add_treb(string)
		string = add_piano(string)
	elif instruments == "both":
		if CAPO:
			string = add_CAPO(string, CAPO)
		guitar_str = add_guitar(string)

		piano_str = add_tempo(main)
		piano_str = add_time(piano_str)
		piano_str = add_key(piano_str)
		piano_str = add_treb(piano_str)
		piano_str = add_piano(piano_str)
		string = piano_str + '\n' + guitar_str + '\n'
		string = multiple_ins(string)
		if omit_stringNum:
			string = add_omit_stringNum(string)
	else:
		raise ValueError("Unknown instruments:", instruments)
	string = add_header(string, title)
	return string


min_block = int(60/ (bpm * 4 * unit_time)) # A note should last for at least two blocks in raw
file = open(csv_file)
first_line = file.readline()
notes_dict = convert_dict(first_line, start_octave)
raw_notes = find_raw_collection()
print(print_raw_notes(raw_notes))
# output = cal_duration(raw_notes)
# print(add_lilypond(output))

# To get the csv file:
# In Sonic Visulizer:
# Transform -> Analysis by Category -> Visulization -> Chromogram 
# File -> Export annotation layer -> 
# Save in $HOME/create-lilypond-files/csv/"your_csv.csv"
# Check: Include a header row before the data rows & 
# 	   Include a timestamp column before the data columns &
# 	   Export the full height of the layer


# To run on command:
# Go to lilypond directory
# $ python src/create_ly.py > 'lyfiles/demo.ly'
# $ lilypond lyfiles/demo.ly
# $ open demo.pdf

# TODO: Allow transpose
# TODO: test simple song from YT
# TODO: Add 打版
# TODO: Add chords
# TODO: change unit_time based on window
# TODO: allow 8th note as a beat (change type_dict)



