import json
import time
import math
import winsound
import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np
import scipy
import wavio
import scipy.fftpack as fft
from scipy.io import wavfile

plt.switch_backend('Qt5Agg')


# This Project reads signal from user and compares it to the results of training model to classify it as 'yes' or
# 'no' The training model has 50 samples of yes and 50 samples of no wav files stored in the project, Then energy,
# zero crossing count, power spectral density and correlation between signals are computed and saved with their
# averages in json file, each class has it's own data.
# Each time the user presses speak and talks, The spoken signal is compared to averages of training data and classified
# according to the Euclidean distance netween the feature vectors.
# And result is displayed on screen.


######################################################################################################
######################################################################################################
# Here are time domain related functions


def find_energy(x):
	"""Return Energy in signal"""
	x = np.reshape(x, (1, 2 * len(x)))
	e = np.sum(x * x, 1)
	return e


def find_ZCR(s):
	"""This Function find the zero crossing count in a signal"""
	s = np.reshape(s, (1, 2 * len(s)))
	s = np.sign(s)
	s = s.tolist()
	s = s[0]
	diff = []
	for i in range(0, len(s) - 1):
		diff.append(s[i + 1] - s[i])
	diff = np.array(diff, dtype=int)
	zcr = np.sum(abs(diff / 2))
	return zcr


def find_correlation(signal1, signal2):
	"""Find correlation between two signals in time domain"""
	c = np.correlate(signal1, signal2)
	return c


######################################################################################################
######################################################################################################
# Here are frequency domain related functions
######################################################################################################
######################################################################################################


def psd(data):
	"""Find power spectral density in a signal"""
	data = np.reshape(data, (1, 2 * len(data)))
	dft = fft.fftshift(fft.fft(data))
	psd = np.abs(dft) ** 2
	return psd


def plot_ft(y):
	N = len(y)
	T = 1.0
	x = np.linspace(0.0, N * T, N)
	yf = scipy.fftpack.fft(y)
	xf = np.linspace(0.0, 1.0 / (2.0 * T), int(N))

	fig, ax = plt.subplots()
	ax.plot(xf, 2.0 / N * np.abs(yf[:N]))
	plt.savefig("./images/test_ft.png")
	plt.show()


######################################################################################################
######################################################################################################
# Here are data storing and training functions

def add_training_data(type):
	records = {}
	for i in range(0, 51):
		dir = "./wav_samples/{}/{}_{}.wav".format(type, type, i)
		print(dir)
		data = read_wav_signal(dir)
		records["{}".format(i)] = {}
		records["{}".format(i)]["energy"] = find_energy(data)[0]
		records["{}".format(i)]["zcc"] = find_ZCR(data)
		psd_ = psd(data)
		psd_ = psd_[0]
		low = psd_[0:int(len(data) / 2)]
		high = psd_[int(len(data) / 2):]
		records["{}".format(i)]["psd"] = np.sum(psd_)
		records["{}".format(i)]["psd_low"] = np.sum(low)
		records["{}".format(i)]["psd_high"] = np.sum(high)
	records = json.dumps(records)
	loaded_data = json.loads(records)
	write_json("./data_record/{}_data.json".format(type), loaded_data)


def distance(v1, v2):
	"""Euclidean distance between the received feature vectors"""
	sum = 0
	for i in range(1, 2):
		sum += ((v1[i] - v2[i]) ** 2)
	d = math.sqrt(sum)
	return d


def read_training_data():
	for i in range(41, 51):
		record_and_save("./wav_samples/yes/yes_{}.wav".format(i))
		time.sleep(1)


def write_wav_signal(y, file_name):
	length = len(y)
	wavio.write(file_name, y, length, sampwidth=1)


def read_wav_signal(file_name):
	"""This function reads wav signal into array format"""
	rate, data = wavfile.read(file_name)
	y_data = []
	length = len(data)
	for i in range(0, length):
		y_data.append(0.019961328125 * data[i] - 2.090138671875)
	y_data = np.array(y_data, dtype=float)
	return y_data


def play_sound(filename):
	winsound.PlaySound(filename, winsound.SND_FILENAME)


def record_and_save(filename):
	"""Record audio from user and save as filename.wav"""
	chunk = 1024  # Record in chunks of 1024 samples
	sample_format = pyaudio.paInt16  # 16 bits per sample
	channels = 2
	fs = 44100  # Record at 44100 samples per second
	seconds = 1.5
	p = pyaudio.PyAudio()  # Create an interface to PortAudio
	print('Recording')
	stream = p.open(format=sample_format,
			  channels=channels,
			  rate=fs,
			  frames_per_buffer=chunk,
			  input=True)

	frames = []  # Initialize array to store frames
	for i in range(0, int(fs / chunk * seconds)):
		data = stream.read(chunk)
		frames.append(data)
	stream.stop_stream()
	stream.close()
	p.terminate()
	print('Finished recording')
	# Save the recorded data as a WAV file
	wf = wave.open(filename, 'wb')
	wf.setnchannels(channels)
	wf.setsampwidth(p.get_sample_size(sample_format))
	wf.setframerate(fs)
	wf.writeframes(b''.join(frames))
	wf.close()


def read_json(name):
	with open(name, "r") as file:
		data = json.load(file)
	return data


def write_json(json_file_name, data):
	a_file = open(json_file_name, "w")
	json.dump(data, a_file)
	a_file.close()


def convert(lst):
	res_dct = {i: lst[i] for i in range(0, len(lst), 1)}
	return res_dct


def refresh_avg_energy(data):
	"""Find average of training data"""
	sum = 0
	for i in range(0, len(data) - 1):
		sum += data["{}".format(i)]["energy"]
	return sum / (len(data) - 1)


def refresh_avg_psd(data):
	"""Find average of Power Spectral Density"""
	sum = 0
	for i in range(0, len(data) - 1):
		sum += data["{}".format(i)]["psd"]
	return sum / (len(data) - 1)


def refresh_avg_psd_low(data):
	sum = 0
	for i in range(0, len(data) - 1):
		sum += data["{}".format(i)]["psd_low"]
	return sum / (len(data) - 1)


def refresh_avg_psd_high(data):
	sum = 0
	for i in range(0, len(data) - 1):
		sum += data["{}".format(i)]["psd_high"]
	return sum / (len(data) - 1)


def refresh_avg_zcc(data):
	"""Find average of Zero Crossing Count"""

	sum = 0
	for i in range(0, len(data) - 1):
		sum += data['{}'.format(i)]["zcc"]
	return sum / (len(data) - 1)


def refresh_yes_data():
	yes_data = read_json("./data_record/yes_data.json")
	yes_data['average'] = {}
	yes_data['average']["avg_energy"] = refresh_avg_energy(yes_data)
	yes_data['average']["avg_zcc"] = refresh_avg_zcc(yes_data)
	yes_data['average']["avg_psd"] = refresh_avg_psd(yes_data)
	yes_data['average']["avg_psd_low"] = refresh_avg_psd_low(yes_data)
	yes_data['average']["avg_psd_high"] = refresh_avg_psd_high(yes_data)
	write_json("./data_record/yes_data.json", yes_data)


def refresh_no_data():
	no_data = read_json("./data_record/no_data.json")
	no_data['average'] = {}
	no_data['average']["avg_energy"] = refresh_avg_energy(no_data)
	no_data['average']["avg_zcc"] = refresh_avg_zcc(no_data)
	no_data['average']["avg_psd"] = refresh_avg_psd(no_data)
	no_data['average']["avg_psd_low"] = refresh_avg_psd_low(no_data)
	no_data['average']["avg_psd_high"] = refresh_avg_psd_high(no_data)
	write_json("./data_record/no_data.json", no_data)


def test():
	"""This function Tests the input audio and classifies it based on the distance function"""
	record_and_save("test.wav")
	data = read_wav_signal("test.wav")
	yes_data = read_json("./data_record/yes_data.json")
	no_data = read_json("./data_record/no_data.json")
	data_energy = find_energy(data)
	data_zcc = find_ZCR(data)
	psd_ = psd(data)
	psd_ = psd_[0]
	# my_plot(psd_, "PSD")
	low = psd_[0:int(len(data) / 2)]
	high = psd_[int(len(data) / 2):]
	psd_ = np.sum(psd_)
	low = np.sum(low)
	high = np.sum(high)
	print("Energy = {}, ZCC = {}, PSD = {}, low = {}, high = {}".format(data_energy[0], data_zcc, psd_, low,
										     high))
	yes_vector = [yes_data["average"]["avg_energy"], yes_data["average"]["avg_zcc"], yes_data["average"]["avg_psd"],
			yes_data["average"]["avg_psd_high"], yes_data["average"]["avg_psd_high"]]
	no_vector = [no_data["average"]["avg_energy"], no_data["average"]["avg_zcc"], no_data["average"]["avg_psd"],
		      no_data["average"]["avg_psd_high"], no_data["average"]["avg_psd_high"]]
	sample_vector = [data_energy[0], data_zcc, psd_, low, high]
	d_yes = distance(yes_vector, sample_vector)
	d_no = distance(no_vector, sample_vector)
	if d_yes < d_no:
		print("YES")
	else:
		print("NO")


def my_plot(x, string):
	"""This function plots signals"""
	n = np.arange(len(x))
	plt.plot(n, x)
	plt.title(string)
	plt.savefig("./images/test.png")

######################################################################################################
######################################################################################################
