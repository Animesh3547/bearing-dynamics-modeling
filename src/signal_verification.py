import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq
from scipy.signal import hilbert, butter, filtfilt
# ---------------------------------------------------------
# 1. Load the Simulated Data
# ---------------------------------------------------------
data = np.load('healthy_baseline_signal.npz')
time = data['time']
acceleration = data['acceleration']

# Theoretical Ball Pass Frequency of Outer Race (BPFO) for N205EM at 1200 rpm
f_o = 108.1 # Hz
delta_t_theory = 1 / f_o # 0.00925 seconds (9.25 ms)

# ---------------------------------------------------------
# 2. Verification Test A: Time-Domain Peak Spacing
# ---------------------------------------------------------
plt.figure(figsize=(12, 8))

# Subplot 1: Time Domain (Zoomed to a 0.05s window)
plt.subplot(2, 1, 1)
# Create a boolean mask to isolate the window [0.20, 0.25] seconds
window_mask = (time >= 0.20) & (time <= 0.25)
t_window = time[window_mask]
acc_window = acceleration[window_mask]

plt.plot(t_window, acc_window, color='teal', linewidth=1)
plt.title('Verification A: Time-Domain Varying Compliance (0.05s Window)')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s^2)')
plt.grid(True)

# Plot vertical red dashed lines spaced exactly by the theoretical delta_t (9.25 ms)
# Align the first line with the approximate location of a peak to visualize the spacing
start_marker = 0.2065
for i in range(6):
    plt.axvline(x=start_marker + (i * delta_t_theory), color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    
plt.legend(['Simulated Signal', f'Theoretical BPFO Spacing ({delta_t_theory*1000:.2f} ms)'])



# ---------------------------------------------------------
# 3. Verification Test B: Professional Envelope Spectrum
# ---------------------------------------------------------
plt.subplot(2, 1, 2)

N = len(time)
dt = time[1] - time[0]
Fs = 1.0 / dt  # Sampling frequency

# Step 1: Bandpass Filter (Isolate the ~355 Hz structural resonance)
# We filter between 200 Hz and 500 Hz to capture the ringing
nyq = 0.5 * Fs
low = 200.0 / nyq
high = 500.0 / nyq
b, a = butter(4, [low, high], btype='band')
filtered_signal = filtfilt(b, a, acceleration)

# Step 2: Hilbert Transform (Extract envelope of the filtered resonance)
analytic_signal = hilbert(filtered_signal)
amplitude_envelope = np.abs(analytic_signal)

# Step 3: Remove DC offset and apply a Hanning Window
# The window forces the ends of the signal to zero, destroying the leakage artifact
envelope_no_dc = amplitude_envelope - np.mean(amplitude_envelope)
window = np.hanning(len(envelope_no_dc))
envelope_windowed = envelope_no_dc * window

# Step 4: Perform FFT on the conditioned envelope
yf_env = rfft(envelope_windowed)
xf_env = rfftfreq(N, dt)

# Multiply by 2.0/N for normalization, and by 2.0 again to compensate for energy lost to the Hanning window
amp_env = (2.0 / N) * np.abs(yf_env) * 2.0

# Plot the clean Envelope Spectrum
plt.plot(xf_env, amp_env, color='darkred')
plt.xlim(0, 400)
plt.title('Verification B: Demodulated Envelope Spectrum (Bandpass + Hanning)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.grid(True)

# Plot theoretical BPFO markers
plt.axvline(x=f_o, color='lime', linestyle='-', linewidth=2, label=f'Theoretical BPFO ({f_o} Hz)')
plt.axvline(x=2*f_o, color='lime', linestyle='--', linewidth=1, label='Harmonics (2x, 3x)')
plt.axvline(x=3*f_o, color='lime', linestyle='--', linewidth=1)

plt.legend()
plt.tight_layout()

plt.savefig('05_verification_results_envelope_fixed.png', dpi=300, bbox_inches='tight')
plt.show()