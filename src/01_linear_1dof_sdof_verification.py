import numpy as np 
from scipy.integrate import solve_ivp 
import matplotlib.pyplot as plt

# 1. Physical Variables 
m = 1.0    # Mass (kg)
k = 100.0  # Stiffness (N/m)
c = 2.0    # Damping (Ns/m)
f = 10.0   # Excitation Force Amplitude (N)
w = 5.0    # Excitation Frequency (rad/s)

# 2. State-Space Function (The Core Logic)
def vibration_system(t, X):
    x1 = X[0] # Current position
    x2 = X[1] # Current velocity
    
    # Define external force before using it
    ft = f * np.sin(w * t)
    
    # Calculate rates of change
    x1_dot = x2
    x2_dot = (1 / m) * (-k * x1 - c * x2 + ft)
    
    return [x1_dot, x2_dot]

# 3. Time Setup and Initial Conditions
t_span = (0, 10)                         # Run for 10 seconds
t_eval = np.linspace(0, 10, 1000)        # 1,000 smooth evaluation points
X0 = [0.0, 0.0]                          # System starts from rest at equilibrium

# 4. Call the Solver
solution = solve_ivp(vibration_system, t_span, X0, t_eval=t_eval)

# 5. Extract and Plot the Data
time = solution.t            
position = solution.y[0]     

plt.figure(figsize=(9, 4.5))
plt.plot(time, position, label='Displacement x(t)', color='blue')
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
plt.title('Phase 1: 1-DOF Damped Forced Vibration')
plt.xlabel('Time (seconds)')
plt.ylabel('Displacement (meters)')
plt.legend()
plt.grid(True)

# Save the figure
plt.savefig('ft_damped_vibration_response.png', dpi=300, bbox_inches='tight')
plt.show()


f = 