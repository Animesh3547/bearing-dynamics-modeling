import numpy as np
import matplotlib.pyplot as plt

# 1. Bearing Geometry (N205EM Cylindrical Roller Bearing parameters)
D = 38.5e-3      # Pitch diameter (meters)
d = 6.5e-3       # Roller diameter (meters)
n_b = 13         # Number of rollers[cite: 33]
alpha = 0.0      # Contact angle (radians)[cite: 33]

# 2. Operating Conditions
rpm = 1200.0     # Shaft speed[cite: 34]
omega_s = rpm * (2 * np.pi / 60)  # Convert to rad/s

# 3. Fundamental Kinematics
# Calculate the cage speed (the rate at which the centers of the rollers orbit)
omega_c = (omega_s / 2) * (1 - (d * np.cos(alpha)) / D)

# 4. Vectorized Angle Generation
t = np.linspace(0, 0.1, 1000)  # Simulate 0.1 seconds
j = np.arange(n_b)             # Array of roller indices: [0, 1, 2, ..., 12]

# Matrix Broadcasting:
# t[:, np.newaxis] turns a 1D array of 1000 time steps into a (1000, 1) column.
# Adding the (13,) phase array automatically generates a (1000, 13) matrix.
theta_matrix = omega_c * t[:, np.newaxis] + (2 * np.pi * j) / n_b

# 5. Visualize Orbital Motion (Vertical Position)
# In standard polar coordinates, sin(theta) gives the vertical Y-axis position.
# -1 represents the bottom dead-center (the heaviest part of the load zone).
plt.figure(figsize=(10, 5))

# Plot the vertical oscillation of just the first 3 rollers to keep the graph clean
for i in range(3):
    plt.plot(t, np.sin(theta_matrix[:, i]), label=f'Roller {i+1}')

plt.axhline(-1, color='black', linestyle='--', linewidth=1, label='Bottom Dead Center (Peak Load)')
plt.title('Phase 3: Roller Kinematics (Orbiting Through the Load Zone)')
plt.xlabel('Time (seconds)')
plt.ylabel('Vertical Coordinate: sin(θ)')
plt.legend(loc='upper right')
plt.grid(True)

plt.savefig('roller_kinematics.png', dpi=300, bbox_inches='tight')
plt.show()