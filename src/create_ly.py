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


def find_notes(line, threshold=3):
	notes = []
	data = line.split(',')
	time = float(data[0])
	for i in range(1, len(data)):
		if float(data[i]) > threshold:
			notes.append(notes_dict[i-1])
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
# print(raw_notes)

def find_type(d):
	type_dict = {0.25:'16', 0.333:'16.', 0.5:'8', 1:'4', 2:'2', 3:'2.', 4:'1'}
	template_d = np.array([0.25, 0.333, 0.5, 1, 2, 3, 4])
	one_beat_duration = 60 / bpm
	delta_d = np.abs(template_d * one_beat_duration - d)
	imin = np.argmin(delta_d)
	identified_d = template_d[imin]
	# print("identified_d", identified_d)
	return type_dict[identified_d]

def cal_duration(raw_notes):
	string = ""
	index = 0
	while index < len(raw_notes):
		count = 1
		start_note = raw_notes[index]
		next_note = raw_notes[index+1]
		if not start_note:
			# string += ""
			count = 0
			index += 1
			note = None
		else:
			while start_note == next_note:
				index += 1
				count += 1
				start_note = raw_notes[index]
				next_note = raw_notes[index+1]
			index += 1
			note = start_note

		# print(note, count, index)
		if index == len(raw_notes) - 1:
			break
		if note:
			duration = unit_time * count 
			note_type = find_type(duration)
			string = string + note[0] + note_type + ' '
	string += '\\bar "|."'
	return string

output = cal_duration(raw_notes)
# print(output)

def add_lilypond(main):
	string = '\\version "2.20.0"\n'
	string += '\\header{title = "Demo"}\n'
	string += "\\new TabStaff \\relative" + "{" + main + "}"
	return string

print(add_lilypond(output))

# To run on command:
# Go to lilypond directory
# $ python src/create_ly.py > 'lyfiles/demo.ly'
# $ lilypond lyfiles/demo.ly
# $ open demo.pdf


