import curses
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint
from scipy.interpolate import interp1d
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import real_world_examples

# Constants
G = 9.81  # Gravitational acceleration (m/s^2)

def calculate_torus_stresses(R, r, t, E, nu, p_int, p_ext, F_x, F_y, F_z, M_x, M_y, M_z, T, theta, phi):
    # Calculate stresses using advanced thin-walled torus theory
    r_m = r + t/2  # Mean radius
    A = 2 * np.pi * r_m * t  # Cross-sectional area
    I = np.pi * r_m**3 * t  # Moment of inertia
    J = 2 * I  # Polar moment of inertia

    # Membrane forces
    N_phi = (p_int - p_ext) * r_m / 2
    N_theta = (p_int - p_ext) * r_m * (2 + (r_m/R) * np.cos(theta)) / (2 + (r_m/R) * np.cos(theta))

    # Bending moments
    M_phi = E * I * (1/r_m + np.cos(theta)/R) / (1 - nu**2)
    M_theta = nu * M_phi

    # Stresses due to external forces and moments
    sigma_x = F_x / A + (M_y * np.cos(phi) + M_z * np.sin(phi)) * r_m / I
    sigma_y = F_y / A + (M_z * np.cos(phi) - M_y * np.sin(phi)) * r_m / I
    sigma_z = F_z / A
    tau_xy = M_x * r_m / J

    # Thermal stress
    alpha = 12e-6  # Thermal expansion coefficient (example value for steel)
    sigma_thermal = -E * alpha * T / (1 - nu)

    # Combine stresses
    sigma_phi = N_phi / t + 6 * M_phi / t**2 + sigma_thermal
    sigma_theta = N_theta / t + 6 * M_theta / t**2 + sigma_thermal

    # Calculate von Mises stress
    sigma_vm = np.sqrt(sigma_phi**2 + sigma_theta**2 - sigma_phi*sigma_theta + 3*tau_xy**2)

    return sigma_vm, sigma_phi, sigma_theta

def fatigue_analysis(sigma_max, sigma_min, N_cycles, S_ut):
    # Simplified S-N curve for steel
    S_e = 0.5 * S_ut  # Endurance limit
    b = -0.085  # Fatigue strength exponent
    sigma_a = (sigma_max - sigma_min) / 2  # Stress amplitude
    sigma_m = (sigma_max + sigma_min) / 2  # Mean stress

    # Goodman mean stress correction
    if S_ut != 0:
        sigma_ar = sigma_a / (1 - sigma_m/S_ut)
    else:
        return np.inf  # Avoid division by zero

    # Calculate cycles to failure
    if sigma_ar > 0 and S_e > 0:
        N_f = (sigma_ar / S_e)**(1/b)
    else:
        return np.inf  # Infinite life for non-positive stress

    # Calculate damage
    if N_f > 0:
        damage = N_cycles / N_f
    else:
        damage = np.inf  # Immediate failure

    return damage

def create_advanced_animation(variables, failure_criteria):
    R, r, t, E, nu, p_int, p_ext, F_x, F_y, F_z, M_x, M_y, M_z, T, N_cycles, S_ut = [v[1] for v in variables]
    
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

def custom_analysis(stdscr):
    variables = [
        ("Major radius (R)", 1.0),
        ("Minor radius (r)", 0.25),
        ("Thickness (t)", 0.01),
        ("Young's modulus (E)", 200e9),
        ("Poisson's ratio (nu)", 0.3),
        ("Internal pressure (p_int)", 1e6),
        ("External pressure (p_ext)", 1e5),
        ("Force X (F_x)", 1000),
        ("Force Y (F_y)", 1000),
        ("Force Z (F_z)", 1000),
        ("Moment X (M_x)", 1000),
        ("Moment Y (M_y)", 1000),
        ("Moment Z (M_z)", 1000),
        ("Temperature change (T)", 50),
        ("Number of cycles (N_cycles)", 1e6),
        ("Ultimate tensile strength (S_ut)", 500e6),
        ("Failure criteria (von Mises)", 250e6)
    ]
    
    current_var = 0
    
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        stdscr.addstr(0, 0, "Custom Torus Analysis")
        stdscr.addstr(1, 0, "Use up/down arrows to navigate, enter to select, 'q' to return to main menu")
        
        for i, (name, value) in enumerate(variables):
            if i == current_var:
                stdscr.addstr(i+3, 0, f"> {name}: {value}", curses.A_REVERSE)
            else:
                stdscr.addstr(i+3, 0, f"  {name}: {value}")
        
        stdscr.addstr(height-1, 0, "Press 'c' to calculate and visualize")
        
        stdscr.refresh()
        
        key = stdscr.getch()
        
        if key == ord('q'):
            break
        elif key == curses.KEY_UP:
            current_var = (current_var - 1) % len(variables)
        elif key == curses.KEY_DOWN:
            current_var = (current_var + 1) % len(variables)
        elif key == 10:  # Enter key
            stdscr.addstr(height-2, 0, f"Enter new value for {variables[current_var][0]}: ")
            curses.echo()
            new_value = stdscr.getstr().decode('utf-8')
            curses.noecho()
            try:
                variables[current_var] = (variables[current_var][0], float(new_value))
            except ValueError:
                stdscr.addstr(height-2, 0, "Invalid input. Press any key to continue.")
                stdscr.getch()
        elif key == ord('c'):
            failure_criteria = variables[-1][1]
            stdscr.clear()
            stdscr.addstr(0, 0, "Calculating and visualizing. Please wait...")
            stdscr.refresh()
            curses.endwin()
            create_advanced_animation(variables[:-1], failure_criteria)
            stdscr = curses.initscr()

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()

    menu_options = [
        "1. Real World Examples",
        "2. Custom Analysis"
    ]

    current_option = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        stdscr.addstr(0, 0, "Advanced Torus Strength Analyzer")
        stdscr.addstr(1, 0, "Use up/down arrows to navigate, enter to select, 'q' to quit")

        for i, option in enumerate(menu_options):
            if i == current_option:
                stdscr.addstr(i+3, 0, option, curses.A_REVERSE)
            else:
                stdscr.addstr(i+3, 0, option)

        stdscr.refresh()

        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == curses.KEY_UP:
            current_option = (current_option - 1) % len(menu_options)
        elif key == curses.KEY_DOWN:
            current_option = (current_option + 1) % len(menu_options)
        elif key == 10:  # Enter key
            if current_option == 0:
                curses.endwin()
                real_world_examples.list_examples()
                choice = int(input("Enter the number of the example you want to visualize: ")) - 1
                real_world_examples.visualize_example(choice)
                stdscr = curses.initscr()
            else:
                custom_analysis(stdscr)

    curses.endwin()

if __name__ == "__main__":
    curses.wrapper(main)
