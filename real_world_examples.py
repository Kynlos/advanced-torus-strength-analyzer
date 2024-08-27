import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def calculate_torus_stresses(R, r, t, E, nu, p_int, p_ext, F_x, F_y, F_z, M_x, M_y, M_z, T, theta, phi):
    r_m = r + t/2
    A = 2 * np.pi * r_m * t
    I = np.pi * r_m**3 * t
    J = 2 * I

    N_phi = (p_int - p_ext) * r_m / 2
    N_theta = (p_int - p_ext) * r_m * (2 + (r_m/R) * np.cos(theta)) / (2 + (r_m/R) * np.cos(theta))

    M_phi = E * I * (1/r_m + np.cos(theta)/R) / (1 - nu**2)
    M_theta = nu * M_phi

    sigma_x = F_x / A + (M_y * np.cos(phi) + M_z * np.sin(phi)) * r_m / I
    sigma_y = F_y / A + (M_z * np.cos(phi) - M_y * np.sin(phi)) * r_m / I
    sigma_z = F_z / A
    tau_xy = M_x * r_m / J

    alpha = 12e-6
    sigma_thermal = -E * alpha * T / (1 - nu)

    sigma_phi = N_phi / t + 6 * M_phi / t**2 + sigma_thermal
    sigma_theta = N_theta / t + 6 * M_theta / t**2 + sigma_thermal

    sigma_vm = np.sqrt(sigma_phi**2 + sigma_theta**2 - sigma_phi*sigma_theta + 3*tau_xy**2)

    return sigma_vm, sigma_phi, sigma_theta

def create_example_visualization(example):
    R, r, t, E, nu, p_int, p_ext, F_x, F_y, F_z, M_x, M_y, M_z, T = example['params']
    
    theta = np.linspace(0, 2*np.pi, 200)
    phi = np.linspace(0, 2*np.pi, 200)
    theta, phi = np.meshgrid(theta, phi)
    
    x = (R + r*np.cos(theta)) * np.cos(phi)
    y = (R + r*np.cos(theta)) * np.sin(phi)
    z = r * np.sin(theta)
    
    sigma_vm, sigma_phi, sigma_theta = calculate_torus_stresses(R, r, t, E, nu, p_int, p_ext, F_x, F_y, F_z, M_x, M_y, M_z, T, theta, phi)
    
    fig = plt.figure(figsize=(16, 14))
    ax1 = fig.add_subplot(221, projection='3d')
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224, projection='polar')
    
    # 3D Visualization
    norm = plt.Normalize(vmin=np.min(sigma_vm), vmax=np.max(sigma_vm))
    colors = plt.cm.viridis(norm(sigma_vm))
    surf = ax1.plot_surface(x, y, z, facecolors=colors, shade=False)
    fig.colorbar(surf, ax=ax1, label='von Mises Stress (Pa)')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    ax1.set_title(f'3D Stress Visualization: {example["name"]}')
    
    # Stress Distribution
    ax2.plot(theta[0], sigma_vm[:, 0], label='von Mises', color='#1f77b4')
    ax2.plot(theta[0], sigma_phi[:, 0], label='Hoop', color='#ff7f0e')
    ax2.plot(theta[0], sigma_theta[:, 0], label='Meridional', color='#2ca02c')
    ax2.set_xlabel('Theta (radians)')
    ax2.set_ylabel('Stress (Pa)')
    ax2.set_title('Stress Distribution')
    ax2.legend()
    ax2.grid(True)
    
    # 2D Cross-section
    circle_outer = plt.Circle((R, 0), r+t/2, fill=False, color='blue')
    circle_inner = plt.Circle((R, 0), r-t/2, fill=False, color='red')
    ax3.add_artist(circle_outer)
    ax3.add_artist(circle_inner)
    ax3.set_xlim(R-2*r, R+2*r)
    ax3.set_ylim(-2*r, 2*r)
    ax3.set_aspect('equal')
    ax3.set_title('Torus Cross-section')
    ax3.grid(True)
    
    # Polar Plot
    ax4.plot(theta[0], sigma_vm[:, 0])
    ax4.set_title('Polar Stress Distribution')
    
    plt.tight_layout()
    plt.show()

# Define 5 real-world examples with improved parameters
examples = [
    {
        "name": "Pressure Vessel",
        "params": (1.0, 0.25, 0.02, 200e9, 0.3, 10e6, 1e5, 0, 0, -9.81*1000, 0, 0, 0, 25)
    },
    {
        "name": "Tokamak Fusion Reactor",
        "params": (6.2, 2.0, 0.05, 200e9, 0.3, 1e-6, 1e5, 0, 0, 0, 1e6, 1e6, 1e6, 100)
    },
    {
        "name": "Submarine Hull Section",
        "params": (5.0, 1.5, 0.1, 200e9, 0.3, 1e5, 2e7, 1e6, 1e6, 1e6, 1e7, 1e7, 1e7, -10)
    },
    {
        "name": "Space Station Module",
        "params": (2.0, 1.0, 0.01, 70e9, 0.33, 1e5, 0, 1e3, 1e3, 1e3, 1e4, 1e4, 1e4, 100)
    },
    {
        "name": "Pneumatic Tire",
        "params": (0.3, 0.1, 0.01, 0.01e9, 0.45, 2.5e5, 1e5, 5e3, 0, 5e3, 100, 100, 100, 30)
    }
]

def visualize_example(example_index):
    if 0 <= example_index < len(examples):
        create_example_visualization(examples[example_index])
    else:
        print("Invalid example index")

def list_examples():
    for i, example in enumerate(examples):
        print(f"{i + 1}. {example['name']}")

if __name__ == "__main__":
    list_examples()
    choice = int(input("Enter the number of the example you want to visualize: ")) - 1
    visualize_example(choice)
