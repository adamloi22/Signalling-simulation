from Encode import *
import random
import matplotlib.pyplot as plt

freq = 100
min_A = 100
max_A = 250

sig_size = 1000

bit_multi = 3
G_sd = 10

dishtrans_r = 10
dist = 100000
send_area_r = 1000

example = []

def calc_BER(sig_size, bit_multi, min_A, max_A, freq, G_sd, dishtrans_r, dist, send_area_r):
	for i in range(sig_size):
		example.append(random.randint(0, 1))

	bits = signal_encode(bit_multi, example)
	sig_t, time, n = AM_modulate(bits, freq, min_A, max_A)

	angle, volt_path_loss_dB = calc_path_loss(dishtrans_r, dist, send_area_r)
	sig_rec = compute_rec_sig(sig_t, volt_path_loss_dB)

	sig_r = AWGN_channel(sig_rec, G_sd, n)

	bound, output, bit_output = AM_demodulate(sig_r, freq, n)

	bit_out = signal_decode(bit_multi, bit_output)

	n_errors = 0
	for i in range(len(bit_out)):
		if bit_out[i] != example[i]:
			n_errors += 1

	BER = n_errors/len(bit_out)

	return BER

BER = calc_BER(sig_size, bit_multi, min_A, max_A, freq, G_sd, dishtrans_r, dist, send_area_r)

print("Signal size:             {}".format(sig_size))
print("SD of noise:             {}".format(G_sd))
print("Bit multiplier:          {}".format(bit_multi))
print("Transmission distance:   {}".format(dist))
print("Target area radius:      {}".format(send_area_r))
print("Bit error rate:          {}".format(BER))


#plot BER against bit multiplier:
multi_BER = []
multi = []
for i in range(4):
	bit_multi = 1 + 2*i
	BER = calc_BER(sig_size, bit_multi, min_A, max_A, freq, G_sd, dishtrans_r, dist, send_area_r)
	multi.append(bit_multi)
	multi_BER.append(BER)

print(multi)
print(multi_BER)

plt.plot(multi, multi_BER, "x-")
plt.xlabel("Multiplier value")
plt.ylabel("BER")
plt.title("Multiplier vs BER for \n Noise SD: {}\n Target area radius: {}".format(G_sd, send_area_r))
plt.show()


#plot BER against SD of noise:
sd_BER = []
sd = []
for i in range(10):
	G_sd = i + 40
	BER = calc_BER(sig_size, bit_multi, min_A, max_A, freq, G_sd, dishtrans_r, dist, send_area_r)
	sd.append(G_sd)
	sd_BER.append(BER)

print(sd)
print(sd_BER)

plt.plot(sd, sd_BER, "x-")
plt.xlabel("Noise SD")
plt.ylabel("BER")
plt.title("Noise SD vs BER for \n Multiplier: {}\n Target area radius: {}".format(bit_multi, send_area_r))
plt.show()


#plot BER against target area radius
target_radius_BER = []
target_radius = []
for i in range(10):
	send_area_r = i*50
	BER = calc_BER(sig_size, bit_multi, min_A, max_A, freq, G_sd, dishtrans_r, dist, send_area_r)
	target_radius.append(target_radius)
	target_radius_BER.append(BER)

print(target_radius)
print(target_radius_BER)

plt.plot(target_radius, target_radius_BER, "x-")
plt.xlabel("Target area radius")
plt.ylabel("BER")
plt.title("Target area radius vs BER for \n Multiplier: {}\n Noise SD: {}".format(bit_multi, G_sd))
plt.show()






