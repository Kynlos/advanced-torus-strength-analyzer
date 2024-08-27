import numpy as np

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

if __name__ == "__main__":
    from tui import run_tui
    run_tui()
