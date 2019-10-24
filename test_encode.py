from Encode import *

def test_signal_encode():
	signal = [0, 1, 1, 0, 1, 0, 1, 0]

	test1 = signal_encode(2, signal)
	test2 = signal_encode(3, signal)
	test3 = signal_encode(4, signal)

	assert test1 == [0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0]
	assert test2 == [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0]
	assert test3 == [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0]

def test_signal_decode():
	rec_signal1 = [0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1]
	rec_signal2 = [1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0]
	rec_signal3 = [0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0]

	assert signal_decode(3, rec_signal1) == [0, 1, 0, 1, 1]
	assert signal_decode(5, rec_signal1) == [1, 0, 1]
	assert signal_decode(3, rec_signal1, rec_signal2 = rec_signal2) == [0, 1, 0, 1, 1]
	assert signal_decode(5, rec_signal1, rec_signal2 = rec_signal2) == [1, 0, 1]
	assert signal_decode(3, rec_signal1, rec_signal2 = rec_signal3) == [0, 0, 0, 0]
	assert signal_decode(5, rec_signal1, rec_signal2 = rec_signal3) == [0, 0, 0, 0]