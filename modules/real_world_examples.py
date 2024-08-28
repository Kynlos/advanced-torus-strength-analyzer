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
    },
        {
        "name": "Nuclear Reactor Containment",
        "params": (10.0, 3.0, 0.5, 200e9, 0.3, 5e6, 1e5, 0, 0, -9.81e6, 1e7, 1e7, 1e7, 300)
    },
    {
        "name": "Particle Accelerator Ring",
        "params": (50.0, 0.5, 0.05, 200e9, 0.3, 1e-9, 1e5, 0, 0, 0, 1e5, 1e5, 1e5, 20)
    },
    {
        "name": "Offshore Oil Pipeline",
        "params": (500.0, 0.5, 0.05, 200e9, 0.3, 10e6, 20e6, 1e6, 1e6, 1e6, 1e7, 1e7, 1e7, 5)
    },
    {
        "name": "Wind Turbine Blade Root",
        "params": (2.0, 0.5, 0.1, 70e9, 0.33, 1e5, 1e5, 1e5, 1e5, 1e5, 1e7, 1e7, 1e7, 30)
    },
    {
        "name": "Aircraft Engine Nacelle",
        "params": (1.5, 1.0, 0.02, 70e9, 0.33, 1e5, 8e4, 1e4, 1e4, 1e4, 1e5, 1e5, 1e5, 100)
    },
    {
        "name": "Hydroelectric Dam Penstock",
        "params": (5.0, 2.0, 0.1, 200e9, 0.3, 2e6, 1e5, 0, 0, -9.81e5, 1e6, 1e6, 1e6, 15)
    },
    {
        "name": "Cryogenic Storage Tank",
        "params": (3.0, 1.5, 0.05, 200e9, 0.3, 5e5, 1e5, 0, 0, -9.81e4, 1e5, 1e5, 1e5, -200)
    },
    {
        "name": "Roller Coaster Loop",
        "params": (10.0, 1.0, 0.05, 200e9, 0.3, 1e5, 1e5, 1e5, 1e5, 1e5, 1e6, 1e6, 1e6, 25)
    },
    {
        "name": "Satellite Fuel Tank",
        "params": (0.5, 0.25, 0.005, 70e9, 0.33, 2e6, 0, 100, 100, 100, 1e3, 1e3, 1e3, 50)
    },
    {
        "name": "Superconducting Magnet Coil",
        "params": (1.0, 0.2, 0.02, 100e9, 0.3, 1e5, 1e5, 1e4, 1e4, 1e4, 1e5, 1e5, 1e5, -270)
    },
    {
        "name": "Bicycle Tire",
        "params": (0.3, 0.025, 0.003, 0.01e9, 0.45, 8e5, 1e5, 500, 0, 500, 10, 10, 10, 25)
    },
    {
        "name": "Industrial Centrifuge",
        "params": (0.5, 0.2, 0.01, 200e9, 0.3, 1e5, 1e5, 1e4, 1e4, 1e4, 1e5, 1e5, 1e5, 50)
    },
    {
        "name": "Spacecraft Heat Shield",
        "params": (2.0, 1.0, 0.1, 50e9, 0.3, 1e5, 0, 1e4, 1e4, 1e4, 1e5, 1e5, 1e5, 1500)
    },
    {
        "name": "Underwater Habitat",
        "params": (5.0, 2.0, 0.1, 200e9, 0.3, 1e5, 3e6, 1e5, 1e5, 1e5, 1e6, 1e6, 1e6, 10)
    },
    {
        "name": "MRI Machine Bore",
        "params": (1.0, 0.5, 0.05, 200e9, 0.3, 1e5, 1e5, 1e4, 1e4, 1e4, 1e5, 1e5, 1e5, 20)
    },
    {
        "name": "Hypersonic Aircraft Fuselage",
        "params": (20.0, 2.0, 0.1, 200e9, 0.3, 1e5, 5e4, 1e5, 1e5, 1e5, 1e6, 1e6, 1e6, 800)
    },
    {
        "name": "Geothermal Well Casing",
        "params": (1.0, 0.1, 0.02, 200e9, 0.3, 20e6, 50e6, 1e5, 1e5, 1e5, 1e6, 1e6, 1e6, 300)
    },
    {
        "name": "Vacuum Chamber",
        "params": (2.0, 1.0, 0.05, 200e9, 0.3, 0, 1e5, 1e4, 1e4, 1e4, 1e5, 1e5, 1e5, 25)
    },
    {
        "name": "Inflatable Space Habitat",
        "params": (5.0, 2.5, 0.001, 0.5e9, 0.45, 1e5, 0, 100, 100, 100, 1e3, 1e3, 1e3, 25)
    },
    {
        "name": "Hyperloop Tube Section",
        "params": (5.0, 1.5, 0.05, 200e9, 0.3, 1e3, 1e5, 1e5, 1e5, 1e5, 1e6, 1e6, 1e6, 30)
    }
]

def run_analysis(calculate_torus_stresses, fatigue_analysis, advanced_calculations, create_advanced_animation):
    print("Real World Examples")
    for i, example in enumerate(examples):
        print(f"{i + 1}. {example['name']}")
    
    choice = int(input("Enter the number of the example you want to visualize: ")) - 1
    
    if 0 <= choice < len(examples):
        chosen_example = examples[choice]
        R, r, t, E, nu, p_int, p_ext, F_x, F_y, F_z, M_x, M_y, M_z, T = chosen_example['params']
        
        # Add default values for missing parameters
        N_cycles = 1e6
        S_ut = 500e6
        yield_stress = 250e6
        n = 1.5
        T_inner = T
        T_outer = T
        rho = 7800
        omega = 0
        K_IC = 50e6

        variables = [
            ('R', R), ('r', r), ('t', t), ('E', E), ('nu', nu),
            ('p_int', p_int), ('p_ext', p_ext), ('F_x', F_x), ('F_y', F_y), ('F_z', F_z),
            ('M_x', M_x), ('M_y', M_y), ('M_z', M_z), ('T', T), ('N_cycles', N_cycles),
            ('S_ut', S_ut), ('yield_stress', yield_stress), ('n', n),
            ('T_inner', T_inner), ('T_outer', T_outer), ('rho', rho), ('omega', omega), ('K_IC', K_IC)
        ]

        create_advanced_animation(variables, yield_stress, calculate_torus_stresses, fatigue_analysis)
    else:
        print("Invalid example index")
    
    input("\nPress Enter to return to the main menu...")
if __name__ == "__main__":
    # This allows the module to be run standalone for testing
    run_analysis(None, None, None, None)
