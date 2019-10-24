from Encode import *
import matplotlib.pyplot as plt

freq = 100
min_A = 100
max_A = 250 

bit_multi = 3
G_sd = 5

dishtrans_r = 10
dist = 100000
send_area_r = 800

ori_bit = [0, 1, 1, 0, 1, 0, 0, 1, 1, 0]



bits = signal_encode(bit_multi, ori_bit)
sig_t, time, n = AM_modulate(bits, freq, min_A, max_A)

angle, volt_path_loss_dB = calc_path_loss(dishtrans_r, dist, send_area_r)
sig_rec = compute_rec_sig(sig_t, volt_path_loss_dB)

sig_r = AWGN_channel(sig_rec, G_sd, n)

bound, output, bit_output = AM_demodulate(sig_r, freq, n)

bit_out = signal_decode(bit_multi, bit_output)


print("Original bits                               : {}".format(ori_bit))
print("Bits received using decoded signal data     : {}".format(bit_out))
print("Raw signal received                         : {}".format(output))
print("Boundary                                    : {}".format(bound))
print("Encoded signal for transimission            : {}".format(bits))
print("Decoded signal from raw signal received.    : {}".format(bit_output))
print("---------------------------")
print("Dish angle:              {}".format(angle))
print("Voltage path loss in dB: {}".format(volt_path_loss_dB))



plt.plot(time, sig_r, label = "received signal")
plt.plot(time, sig_t, label = "original signal")
plt.plot(time, sig_rec, label = "signal with loss")
plt.xlabel("time (s)")
plt.ylabel("voltage (V)")
plt.legend()
plt.show()