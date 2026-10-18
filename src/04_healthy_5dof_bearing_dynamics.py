import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# 1. Bearing Geometry (N205EM)
D = 38.5e-3      # Pitch diameter (m)
d = 6.5e-3       # Roller diameter (m)
n_b = 13         # Number of rollers
alpha = 0.0      # Contact angle (rad)
gamma = 10e-6    # Radial clearance (10 micrometers)

# 2. Operating Conditions
rpm = 1200.0
omega_s = rpm * (2 * np.pi / 60)
omega_c = (omega_s / 2) * (1 - (d * np.cos(alpha)) / D)
W = 500.0        # Static radial load (N)
g = 9.81

# 3. Dynamic Parameters (Nominal values for stability)
m_i, m_o, m_r = 1.0, 2.5, 0.5       # Masses (kg)
k_i, k_o, k_r = 1e7, 1e7, 5e7       # Structural stiffness (N/m)
c_i, c_o, c_r = 500, 500, 1000      # Damping (Ns/m)
K_c = 1e9                           # Hertzian Contact Stiffness (N/m^(10/9))

# 4. The 10-State Core Logic
def healthy_bearing_5dof(t, X):
    # Unpack the 10 states
    x_i, v_xi, y_i, v_yi, x_o, v_xo, y_o, v_yo, y_r, v_yr = X
    
    # Vectorized Roller Kinematics
    j = np.arange(n_b)
    theta_j = omega_c * t + (2 * np.pi * j) / n_b
    
    # Vectorized Hertzian Contact (Slack Zone Logic)
    # delta_j = (xi - xo)*cos(theta) + (yi - yo)*sin(theta) - clearance
    delta_j = (x_i - x_o) * np.cos(theta_j) + (y_i - y_o) * np.sin(theta_j) - gamma
    contact_forces = K_c * (np.maximum(0, delta_j) ** (10/9))
    
    # Sum internal forces across all 13 rollers
    F_x = np.sum(contact_forces * np.cos(theta_j))
    F_y = np.sum(contact_forces * np.sin(theta_j))
    
    # 5-DOF Differential Equations isolated for acceleration
    a_xi = (1/m_i) * (-c_i*v_xi - k_i*x_i - F_x)
    a_yi = (1/m_i) * (W + m_i*g - c_i*v_yi - k_i*y_i - F_y)
    
    a_xo = (1/m_o) * (-c_o*v_xo - k_o*x_o + F_x)
    a_yo = (1/m_o) * (m_o*g + F_y + k_r*y_r + c_r*v_yr - (c_o + c_r)*v_yo - (k_o + k_r)*y_o)
    
    a_yr = (1/m_r) * (-c_r*(v_yr - v_yo) - k_r*(y_r - y_o))
    
    # Return [velocity, acceleration] for all 5 DOFs
    return [v_xi, a_xi, v_yi, a_yi, v_xo, a_xo, v_yo, a_yo, v_yr, a_yr]

# 5. Execution
t_span = (0, 0.5) 
t_eval = np.linspace(0, 0.5, 10000)
X0 = np.zeros(10) # Start from rest

# Stiff solvers (Radau or BDF) are mandatory for 10/9 contact exponents
solution = solve_ivp(healthy_bearing_5dof, t_span, X0, t_eval=t_eval, method='Radau')

# Extract Accelerometer Signal (Resonator Acceleration)
# The sensor physically measures a_yr. We calculate it using the final state data.
time = solution.t
y_o_final = solution.y[6]
y_r_final = solution.y[8]
v_yo_final = solution.y[7]
v_yr_final = solution.y[9]

# Reconstruct acceleration from the returned states
a_yr_final = (1/m_r) * (-c_r*(v_yr_final - v_yo_final) - k_r*(y_r_final - y_o_final))

#  Data Storage: Save as a compressed NumPy archive
# This packages both the time and acceleration arrays into a single fast-loading file
np.savez_compressed(
    'healthy_baseline_signal.npz', 
    time=time, 
    acceleration=a_yr_final
)
print("Steady-state signal saved successfully as 'healthy_baseline_signal.npz'")

# 6. Plotting
# Create a mask to filter out the first 0.1 seconds of transient data
mask = time > 0.1
time_steady = time[mask]
a_yr_steady = a_yr_final[mask]

# Plot only the steady-state data so the Y-axis scales correctly
plt.figure(figsize=(10, 4))
plt.plot(time_steady, a_yr_steady, color='teal', linewidth=0.8)
plt.title('Phase 4: Healthy 5-DOF Bearing Acceleration (Varying Compliance)')
plt.xlabel('Time (seconds)')
plt.ylabel('Sensor Acceleration (m/s^2)')
plt.grid(True)
plt.xlim(0.1, 0.5)

# Save and show
plt.savefig('healthy_bearing_5dof_fixed.png', dpi=300, bbox_inches='tight')
plt.show()