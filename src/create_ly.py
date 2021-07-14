from scipy.io.wavfile import write
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import math

# Config
csv_file = 'csv/demo-sound.csv'
unit_time = 0.046 # Read from csv for now, TODO [s]
bpm = 120 # TODO: How to find the BPM?
time = (4,4) # 4 beats a measure, fourth note as one beat
key_signature = ('c', 'major') # Key signature of the song
CAPO = 3 # Set minimum fret

class Note():
	def __init__(self, name):
		self.name = name
		self.counted = False
	def counted(self):
		self.counted = True
	def get_name(self):
		return self.name

def belong(note, l): # Decide if a Note object is in a list of Note objects, return the index of the matching Note
	note_name = note.get_name()
	for i in range(len(l)):
		name = l[i].get_name()
		if name == note_name:
			return i
	return "No"

def find_notes(line, threshold=3):
	notes = []
	data = line.split(',')
	time = float(data[0])
	for i in range(1, len(data)):
		if float(data[i]) > threshold:
			note_name = notes_dict[i-1]
			notes.append(Note(note_name))
			# notes.append(notes_dict[i-1])
	return notes

def convert_dict(header):
	d = {'C':'c', 'C#':'cis', 'D':'d', "D#":'dis', 'E':'e', 'E#':'eis', 'F':'f', "F#":'fis',\
	'G':'g', 'G#':'gis', 'A':'a', "A#":'ais', 'B':'b', 'B#':'bis', 'Cb':'ces', 'Db':'des',\
	'Eb':'ees', 'Gb':'ges','Ab':'aes','Bb': 'bes'}
	res = []
	elements = header.split(',')
	for i in range(1, len(elements)):
		if i == len(elements) -1 :
			note = elements[i][:-2]
		else:
			note = elements[i]
		res.append(d[note])
	return res


file = open(csv_file)
header = file.readline()
notes_dict = convert_dict(header)
# print(notes_dict)

def find_all():
	res = []
	line = file.readline()
	while line:
		add = find_notes(line)
		res.append(add) 
		line = file.readline()
	return res 

raw_notes = find_all()
# Test Section
Do = Note("c'")
Re = Note("d'")
Me = Note("e'")
Fa = Note("f'")
So = Note("g'")
La = Note("a'")
unit_time = 0.5 
bpm = 60 
test_raw_notes = [[],[],[Do], [Do],[So, La], [So,La], [Fa]]

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

def cal_duration(raw_notes):
	string = ""
	index = 0
	while index < len(raw_notes):
		count = 1
		start_notes = raw_notes[index]
		if len(start_notes) == 0:
			count = 0
			index += 1
			note = None
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

# output = cal_duration(raw_notes)
output = cal_duration(test_raw_notes)
# print(output)

def add_lilypond(main):
	string = '\\version "2.20.0"\n'
	string += '\\header{title = "Demo"}\n'
	string += "\\new TabStaff \\relative" + "{\n"
	if CAPO:
		string += "\\set TabStaff.minimumFret = #" + str(CAPO) + "\n" 
		string += "\\set TabStaff.restrainOpenStrings = ##t\n"
	string += main + "}"
	return string
# Add CAPO

     # \set TabStaff.minimumFret = #5
     # \set TabStaff.restrainOpenStrings = ##t
print(add_lilypond(output))

# To run on command:
# Go to lilypond directory
# $ python src/create_ly.py > 'lyfiles/demo.ly'
# $ lilypond lyfiles/demo.ly
# $ open demo.pdf


