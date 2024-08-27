import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

def create_advanced_animation(variables, failure_criteria, calculate_torus_stresses, fatigue_analysis):
    R, r, t, E, nu, p_int, p_ext, F_x, F_y, F_z, M_x, M_y, M_z, T, N_cycles, S_ut, yield_stress, n, T_inner, T_outer, rho, omega, K_IC = [v[1] for v in variables]
    
    theta = np.linspace(0, 2*np.pi, 100)
    phi = np.linspace(0, 2*np.pi, 100)
    theta, phi = np.meshgrid(theta, phi)
    
    x = (R + r*np.cos(theta)) * np.cos(phi)
    y = (R + r*np.cos(theta)) * np.sin(phi)
    z = r * np.sin(theta)
    
    sigma_vm, sigma_phi, sigma_theta = calculate_torus_stresses(R, r, t, E, nu, p_int, p_ext, F_x, F_y, F_z, M_x, M_y, M_z, T, theta, phi)
    
    # Calculate fatigue damage
    sigma_max = np.max(sigma_vm)
    sigma_min = np.min(sigma_vm)
    damage = fatigue_analysis(sigma_max, sigma_min, N_cycles, S_ut)

    # Handle infinite or NaN damage
    if np.isinf(damage) or np.isnan(damage):
        damage_str = "Inf" if np.isinf(damage) else "NaN"
    else:
        damage_str = f"{damage:.4f}"
    
    fig = plt.figure(figsize=(16, 8))
    ax1 = fig.add_subplot(121, projection='3d')
    ax2 = fig.add_subplot(122)
    ax3 = ax2.twinx()
    
    cmap = plt.get_cmap('viridis')
    norm = plt.Normalize(vmin=np.min(sigma_vm), vmax=np.max(sigma_vm))
    
    def update(frame):
        ax1.clear()
        ax2.clear()
        ax3.clear()
        
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        ax1.set_title('Torus Stress Visualization')
        ax1.grid(True)
        
        threshold = failure_criteria * (frame + 1) / 100
        mask = sigma_vm > threshold
        
        scatter = ax1.scatter(x[mask], y[mask], z[mask], c=sigma_vm[mask], cmap=cmap, norm=norm)
        if frame == 0:
            fig.colorbar(scatter, ax=ax1, label='von Mises Stress (Pa)')
        
        ax2.plot(theta[0], sigma_vm[:, 0], label='von Mises', color='#1f77b4')
        ax2.plot(theta[0], sigma_phi[:, 0], label='Hoop', color='#ff7f0e')
        ax2.plot(theta[0], sigma_theta[:, 0], label='Meridional', color='#2ca02c')
        ax2.set_xlabel('Theta (radians)')
        ax2.set_ylabel('Stress (Pa)')
        ax2.set_title('Stress Distribution')
        ax2.legend(loc='upper left')
        ax2.grid(True)
        
        ax3.plot(theta[0], np.full_like(theta[0], damage), label='Damage', color='#d62728', linestyle='--')
        ax3.set_ylabel('Damage')
        ax3.legend(loc='upper right')
        
        return scatter,
    
    anim = FuncAnimation(fig, update, frames=100, interval=50, blit=False)
    plt.tight_layout()
    plt.show()
