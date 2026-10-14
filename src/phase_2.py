import numpy as np 
from scipy.integrate import solve_ivp 
import matplotlib.pyplot as plt

# 1. Physical Variables 
m = 1.0       # Mass (kg)
K = 1e5       # Hertzian Contact Stiffness (N/m^(10/9))
c = 2.0       # Damping (Ns/m)
g = 9.81      # Gravity (m/s^2)
W = m * g     # Constant Static Load (N)

# 2. State-Space Function (Non-Linear Logic)
def non_linear_drop(t, X):
    x1 = X[0] # Current position (x > 0 is compression, x < 0 is air gap)
    x2 = X[1] # Current velocity
    
    # Vectorized Slack Zone Logic: Force only exists if x1 is positive
    contact_force = K * (max(0, x1) ** (10/9))
    
    # Calculate rates of change
    x1_dot = x2
    x2_dot = (1 / m) * (W - contact_force - c * x2)
    
    return [x1_dot, x2_dot]

# 3. Time Setup and Initial Conditions
t_span = (0, 3)                          # Run for 3 seconds (impacts happen fast)
t_eval = np.linspace(0, 3, 3000)         # High resolution to capture sharp bounces
X0 = [-0.01, 0.0]                        # Start 10 mm (-0.01 m) above the roller, at rest

# 4. Call the Solver (Using 'Radau' for stiff non-linear equations)
solution = solve_ivp(non_linear_drop, t_span, X0, t_eval=t_eval, method='Radau')

# 5. Extract and Plot the Data
time = solution.t            
position = solution.y[0]     

plt.figure(figsize=(10, 5))
plt.plot(time, position, label='Displacement x(t)', color='red')
plt.axhline(0, color='black', linewidth=1.2, linestyle='--', label='Contact Surface (x=0)')
plt.fill_between(time, 0, position, where=(position < 0), color='gray', alpha=0.2, label='Slack Zone (Free Fall)')
plt.title('Phase 2: Non-Linear Hertzian Impact & Bouncing')
plt.xlabel('Time (seconds)')
plt.ylabel('Displacement (meters)')
plt.legend()
plt.grid(True)

# Save and Show
plt.savefig('hertzian_bounce_response.png', dpi=300, bbox_inches='tight')
plt.show()