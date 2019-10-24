"""
I have added a method which could help reduce any errors in the received signal, so that
the Rover would not do an unintended action even if the signal received is incorrectly decoded.
So the signal will be sent twice, and if they don't match up after decoding, then the Rover
will not act. (This option can be switched off)

For the signal, we are using binary 2-bit AM for transmission.

Things to do:
SD of AWGN
Sending power
SNR
BER - calculation
"""
import numpy as np
import math
import matplotlib.pyplot as plt

def signal_encode(bit_multi, ori_bit):
	"""
	Returns a list of encoded digital values (will be sent twice)

	ori_bit - list of digital values for transmission
	bit_multi (odd) - number of times each value is replicated (should be synchronised with rover)
	"""

	bits = []
	for i in range(len(ori_bit)):
		for j in range(bit_multi):
			bits.append(ori_bit[i])
	
	return bits

def AM_modulate(bits, freq, min_A, max_A):
	"""
	This function modulates a list of bits with a 2-bit AM into a signal of frequency freq
	"""
	sig_t = []
	time = []

	n = 0

	for bit in bits:
		if bit == 0:
			A = min_A
		elif bit == 1:
			A = max_A
		else:
			raise ValueError("Invalid value in input bits.")

		k = np.linspace(0, 2*np.pi, 100)
		wave = [A*np.sin(i) for i in k]
		t = np.linspace(n/freq, (n+1)/freq, 100)

		n += 1

		for i in wave:
			sig_t.append(i)

		for j in t:
			time.append(j)

	return sig_t, time, n
	
def calc_path_loss(dishtrans_r, dist, send_area_r):
	"""
	Assuming that the terminal resistances of the transmitter and the receiver are very large, such
	that their ratio will be approximately 1:1. The signal is sent in a conic shape towards Jupiter,
	such that it could cover an area containing the probe, with the addition of some guard radius.
	The angle of the sides of the signal to the normal of a flat plane across the transmitting dish is
	"angle". We can ignore the radius of the dish of the receiver as it will be insignificant when
	compared to the area of spread of the signal.
	"""
	angle = np.arctan(send_area_r/dist)
	volt_path_loss_dB = 10*(np.log10(dishtrans_r) - np.log10(send_area_r))

	return angle, volt_path_loss_dB

def compute_rec_sig(sig_t, volt_path_loss_dB):
	volt_drop = 10**(volt_path_loss_dB/10)

	sig_rec = [volt_drop*sig for sig in sig_t]
		
	return sig_rec

def AWGN_channel(sig_rec, G_sd, n):
	"""
	We assume the noise in space to have constant parameters, although in reality it is not the case.
	So an improvement to this would be to take into account of the variables involved in altering the
	standard deviation of the noise. Also, we have assumed that there is only one type of noise (AWGN)
	"""
	noise = np.random.normal(0, G_sd, n*100)
	sig_r = noise + sig_rec
	return sig_r

def AM_demodulate(sig_r, freq, n):
	"""
	This function utilises Fourier Theorem to extract the original bit values
	"""
	sine = []
	time = []
	for a in range(n):
		k = np.linspace(0, 2*np.pi, 100)
		wave = [np.sin(i) for i in k]
		t = np.linspace(a/freq, (a+1)/freq, 100)

		for i in wave:
			sine.append(i)

		for j in t:
			time.append(j)

	product = []
	for i in range(len(sine)):
		product.append(sine[i]*sig_r[i])

	output = []
	for i in range(n):
		raw_val = 2*(sum(product[i*100: (i+1)*100 - 1]))/100
		output.append(raw_val)
	
	bound = (max(output) + min(output))/2

	bit_output = []
	for i in output:
		if i > bound:
			k = 1
		else:
			k = 0
		bit_output.append(k)

	return bound, output, bit_output

def signal_decode(bit_multi, rec_signal1, rec_signal2 = None):
	"""
	Returns a list of decoded digital values, if both received signals produce the same result
	after decoding

	signal1 - list of digital values received by rover
	bit_multi (odd) - number of times each value is replicated (should be synchronised with probe)
	"""

	signal1 = []
	signal2 = []

	for i in range(int(len(rec_signal1)/bit_multi)):
		average = 0.0
		for j in range(bit_multi):
			average += float(rec_signal1[bit_multi*i + j])
		average = average/bit_multi
		if average > 0.5:
			signal1.append(1)
		else:
			signal1.append(0)

	if rec_signal2 is not None:
		if rec_signal1 != rec_signal2:
			for i in range(int(len(rec_signal2)/bit_multi)):
				average = 0.0
				for j in range(n):
					average += float(rec_signal2[bit_multi*i + j])
				average = average/bit_multi
				if average > 0.5:
					signal2.append(1)
				else:
					signal2.append(0)
	else:
		signal2 = signal1

	if signal1 == signal2:
		return signal1
	else:
		return [0, 0, 0, 0]	#Insert action that would tell Rover to not do anything yet










def calc_r(M_j, v, b, a):
	"""This function calculates the radius of the circular lunar 
	orbit of Ganeymede about Jupiter. 
	It also calculates the radius between Jupiter and the probe at any time.
	Then it returns the distance between the probe and the rover"""
	G=6.764e-11
	e=math.sqrt(1-(b/a)**2)
	r_rover=(G*M_j)/v #in the e_r direction
	r_probe_max=b**2/(a*(1+e))
	r_probe_min=b**2/(a*(1-e))
	r_worst=abs(r_probe_max+r_rover)
	r_best=abs(r_probe_min-r_rover)
	return r_worst, r_best





def STNR(d,e_a, N_0, N_t, N_g, P_t, r_worst,r_best, f):
	"""This function calculates the approximate signal to noise ratio 
	between the output signal from the probe and the input signal to the rover"""
	G_t=((d*np.pi)/lambd)**2*e_a #d is transmitting dish diameter, e_a is efficiency ratio of antenna 
	c=3.0e6
	N=N_0+N_t+N_g #Assuming given noise constants as temperature calculations are trivial in outer space.
	SNR_best= (P_t*G_t*(c**2))/((N)*((4*np.pi*f*r_best)**2)) #Friis Transmission Formula
	SNR_worst=(P_t*G_t*(c**2))/((N)*((4*np.pi*f*r_worst)**2))
	return SNR_best, SNR_worst


#def calc_n(STNR):
	"""
	With a value for STNR, we calculate a suitable value of n such that the accuracy of the signal
	received will be at least 95%

	STNR - signal-to-noise ratio
	"""