from general import add_CAPO, add_guitar, add_tempo, add_time, add_key, add_treb, add_header

class Note():
	def __init__(self, name, time, type, m_id):
		self.name = name
		self.counted = False
		self.type = type 
		self.measure_id = m_id
		self.beat_id = None
		self.time = time
	def counted(self):
		self.counted = True
	def get_name(self):
		return self.name
	def set_type(self, t):
		self.type = t 
	def get_type(self):
		return self.type 
	def get_measure_id(self):
		return self.measure_id
	def set_measure_id(self, num):
		self.measure_id = num 
	def set_beat_id(self, i):
		self.beat_id = i
	def print_note(self):
		return self.name + self.type 
	def __str__(self):
		return self.name + self.type
def same_time(n, ns):
	res = []
	beat = n.beat_id
	for other in ns:
		if other.beat_id == beat:
			res.append(other)
	return res 
class Measure():
	id = 0
	def __init__(self):
		self.chord = []
		self.id = Measure.id
		self.notes = []
		Measure.id += 1
	def get_id(self):
		return self.id
	def add_note(self, note):
		self.notes.append(note)
	def print_measure(self):
		string = ""
		for i in range(len(self.notes)):
			simultaneous_notes = same_time(self.notes[i], self.notes[i:])
			if len(simultaneous_notes) > 1:
				string += "< "
				for note in simultaneous_notes:
					string += note.get_name() + ' '
				string += "> "
				string += self.notes[i].get_type() + ' '
			else:
				string += self.notes[i].get_name() + self.notes[i].get_type() + ' '

		return string

	def get_num_notes(self):
		return len(self.notes)


class Song(): 
	def __init__(self, total_duration, bpm, Time, key_signature):
		self.measures = []
		self.bpm = bpm 
		self.measure_duration = int(Time[0]) * 60 / bpm
		self.total_duration = total_duration
		self.num_measure = round(self.total_duration / self.measure_duration)
		for i in range(self.num_measure):
			m = Measure()
			self.measures.append(m)
		self.tot_beats = int(total_duration / (60 / bpm)) + 1
	def add_measure(self, Measure):
		self.measures.append(Measure)
	def get_total_duration(self):
		return self.total_duration
	def get_measure(self, measure_id):
		return self.measures[measure_id]
	def get_num_notes(self):
		count = 0 
		for m in self.measures:
			count += m.get_num_notes()
		return count 
	def print_song(self, CAPO, title):
		string = ""
		for m in self.measures:
			string += m.print_measure() + ' '
		if CAPO:
			string = add_CAPO(string, CAPO)
		string = add_guitar(string)
		string = add_header(string, title)
		return string


