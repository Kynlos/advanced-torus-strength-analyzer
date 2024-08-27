import numpy as np
from scipy.integrate import odeint, solve_ivp
from scipy.optimize import fsolve, minimize
from scipy.interpolate import interp1d
from scipy.stats import norm
import sympy as sp

def advanced_stress_tensor(sigma_vm, sigma_phi, sigma_theta, tau_xy, tau_yz, tau_xz):
    """Calculate the full 3D stress tensor with all components"""
    stress_tensor = np.array([
        [sigma_phi, tau_xy, tau_xz],
        [tau_xy, sigma_theta, tau_yz],
        [tau_xz, tau_yz, sigma_vm]
    ])
    return stress_tensor

def finite_element_analysis(R, r, t, E, nu, p_int, p_ext, F_x, F_y, F_z, M_x, M_y, M_z, n_elements):
    # Set up the mesh
    theta = np.linspace(0, 2*np.pi, n_elements+1)
    phi = np.linspace(0, 2*np.pi, n_elements+1)
    theta, phi = np.meshgrid(theta, phi)
    
    # Element stiffness matrix
    def element_stiffness(R, r, t, E, nu):
        D = E / (1 - nu**2) * np.array([[1, nu, 0], [nu, 1, 0], [0, 0, (1-nu)/2]])
        B = np.array([[1/R, 0, 0], [0, 1/r, 0], [0, 0, 1/(R*r)]])
        return t * np.pi * R * r * B.T @ D @ B
    
    K = np.zeros((3*n_elements**2, 3*n_elements**2))
    F = np.zeros(3*n_elements**2)
    
    # Assemble global stiffness matrix and force vector
    for i in range(n_elements):
        for j in range(n_elements):
            k_e = element_stiffness(R, r, t, E, nu)
            idx = 3*(i*n_elements + j)
            K[idx:idx+3, idx:idx+3] += k_e
            F[idx:idx+3] += np.array([p_int - p_ext, 0, 0]) * np.pi * R * r / n_elements**2
    
    # Apply boundary conditions and solve
    K[0, 0] += 1e10  # Fix a point to remove rigid body motion
    U = np.linalg.solve(K, F)
    
    return U.reshape((n_elements, n_elements, 3))

def non_linear_material_model(strain, E, yield_stress, n, C, gamma):
    """Advanced non-linear material model combining Ramberg-Osgood and Chaboche models"""
    if strain <= yield_stress / E:
        stress = E * strain
    else:
        stress = yield_stress + E * (strain - yield_stress / E) ** n
        # Add kinematic hardening component (Chaboche model)
        stress += C * (1 - np.exp(-gamma * (strain - yield_stress / E)))
    return stress

def thermal_stress_analysis(R, r, t, E, alpha, k, T_inner, T_outer, q):
    """Calculate thermal stresses with heat transfer considerations"""
    # Solve heat conduction equation
    def heat_equation(r, T):
        return [T[1], -T[1]/r - q/(k*r)]
    
    r_span = [r - t/2, r + t/2]
    bc = [(1, T_inner), (2, T_outer)]
    sol = solve_ivp(heat_equation, r_span, [T_inner, 0], dense_output=True, events=None, vectorized=True)
    
    T_distribution = sol.sol(np.linspace(r - t/2, r + t/2, 100))
    
    # Calculate thermal stresses
    sigma_thermal_hoop = E * alpha * (T_distribution - np.mean(T_distribution)) / (1 - nu)
    sigma_thermal_radial = E * alpha * (T_distribution - np.mean(T_distribution))
    
    return sigma_thermal_hoop, sigma_thermal_radial, T_distribution

def dynamic_stress_analysis(R, r, t, E, rho, omega, time_span):
    """Calculate dynamic stresses due to rotation and vibration"""
    # Natural frequencies
    n = 2  # Number of modes to consider
    freq = np.sqrt(E / (rho * R**2)) * np.arange(1, n+1)
    
    # Mode shapes (simplified)
    def mode_shape(theta, n):
        return np.sin(n * theta)
    
    # Solve equations of motion
    def eom(t, y):
        displacement = y[:n]
        velocity = y[n:]
        acceleration = -freq**2 * displacement - 2 * omega * velocity
        return np.concatenate([velocity, acceleration])
    
    sol = solve_ivp(eom, time_span, np.zeros(2*n), t_eval=np.linspace(time_span[0], time_span[1], 1000))
    
    # Calculate stresses
    theta = np.linspace(0, 2*np.pi, 100)
    stress = np.zeros((len(sol.t), len(theta)))
    for i, t in enumerate(sol.t):
        for j in range(n):
            stress[i] += E * r / R**2 * sol.y[j][i] * mode_shape(theta, j+1)
    
    return stress, sol.t, theta

def fracture_mechanics(K_IC, sigma, a, Y, da_dN_params):
    """Advanced fracture mechanics analysis including fatigue crack growth"""
    # Paris law parameters
    C, m = da_dN_params
    
    # Critical crack length
    a_crit = (K_IC / (Y * sigma * np.sqrt(np.pi)))**2
    
    # Fatigue crack growth
    def crack_growth(a, N):
        K = Y * sigma * np.sqrt(np.pi * a)
        return C * K**m
    
    N_span = [0, 1e6]  # Number of cycles
    a0 = a  # Initial crack length
    sol = solve_ivp(crack_growth, N_span, [a0], dense_output=True, events=lambda N, a: a[0] - a_crit)
    
    return a_crit, sol.t, sol.y[0]

def probabilistic_analysis(R, r, t, E, nu, p_int, p_ext, F_x, F_y, F_z, M_x, M_y, M_z, T, param_uncertainties):
    """Perform probabilistic analysis using Monte Carlo simulation"""
    n_samples = 10000
    results = []
    
    for _ in range(n_samples):
        # Sample input parameters from their distributions
        R_sample = norm.rvs(R, param_uncertainties['R'])
        r_sample = norm.rvs(r, param_uncertainties['r'])
        t_sample = norm.rvs(t, param_uncertainties['t'])
        E_sample = norm.rvs(E, param_uncertainties['E'])
        nu_sample = norm.rvs(nu, param_uncertainties['nu'])
        p_int_sample = norm.rvs(p_int, param_uncertainties['p_int'])
        p_ext_sample = norm.rvs(p_ext, param_uncertainties['p_ext'])
        
        # Calculate stresses for this sample
        sigma_vm, _, _ = calculate_torus_stresses(R_sample, r_sample, t_sample, E_sample, nu_sample, 
                                                  p_int_sample, p_ext_sample, F_x, F_y, F_z, M_x, M_y, M_z, T, 0, 0)
        results.append(np.max(sigma_vm))
    
    # Analyze results
    mean_stress = np.mean(results)
    std_stress = np.std(results)
    prob_failure = np.sum(np.array(results) > param_uncertainties['yield_stress']) / n_samples
    
    return mean_stress, std_stress, prob_failure

def optimization_analysis(R, r, t, E, nu, p_int, p_ext, F_x, F_y, F_z, M_x, M_y, M_z, T, constraints):
    """Perform design optimization to minimize weight while meeting stress constraints"""
    def objective(x):
        R, r, t = x
        volume = 2 * np.pi**2 * R * r * t
        return volume * 7800  # Assuming steel density
    
    def constraint(x):
        R, r, t = x
        sigma_vm, _, _ = calculate_torus_stresses(R, r, t, E, nu, p_int, p_ext, F_x, F_y, F_z, M_x, M_y, M_z, T, 0, 0)
        return constraints['max_stress'] - np.max(sigma_vm)
    
    x0 = [R, r, t]
    bounds = ((0.5*R, 1.5*R), (0.5*r, 1.5*r), (0.5*t, 1.5*t))
    cons = {'type': 'ineq', 'fun': constraint}
    
    result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=cons)
    
    return result.x, result.fun

def advanced_torus_analysis(R, r, t, E, nu, p_int, p_ext, F_x, F_y, F_z, M_x, M_y, M_z, T, yield_stress, n, T_inner, T_outer, rho, omega, K_IC):
    """Perform comprehensive advanced torus stress analysis"""
    # Basic stress calculation
    sigma_vm, sigma_phi, sigma_theta = calculate_torus_stresses(R, r, t, E, nu, p_int, p_ext, F_x, F_y, F_z, M_x, M_y, M_z, T, 0, 0)
    
    # Advanced stress tensor
    stress_tensor = advanced_stress_tensor(sigma_vm, sigma_phi, sigma_theta, M_x * r / (2 * np.pi * r**3 * t), 0, 0)
    
    # Finite element analysis
    U = finite_element_analysis(R, r, t, E, nu, p_int, p_ext, F_x, F_y, F_z, M_x, M_y, M_z, 100)
    
    # Non-linear material behavior
    strain = sigma_vm / E
    C, gamma = 1e5, 50  # Example Chaboche model parameters
    sigma_nl = non_linear_material_model(strain, E, yield_stress, n, C, gamma)
    
    # Thermal stress analysis
    k = 50  # Thermal conductivity (W/m·K)
    q = 1000  # Heat flux (W/m²)
    sigma_thermal_hoop, sigma_thermal_radial, T_distribution = thermal_stress_analysis(R, r, t, E, 12e-6, k, T_inner, T_outer, q)
    
    # Dynamic stress analysis
    time_span = [0, 10]  # Analyze for 10 seconds
    dynamic_stress, time, theta = dynamic_stress_analysis(R, r, t, E, rho, omega, time_span)
    
    # Fracture mechanics
    Y = 1.0  # Geometry factor, simplified
    da_dN_params = (1e-11, 3)  # Paris law parameters (C, m)
    a_crit, N, a = fracture_mechanics(K_IC, sigma_vm, t/10, Y, da_dN_params)
    
    # Probabilistic analysis
    param_uncertainties = {
        'R': 0.01*R, 'r': 0.01*r, 't': 0.05*t, 'E': 0.05*E, 'nu': 0.1*nu,
        'p_int': 0.1*p_int, 'p_ext': 0.1*p_ext, 'yield_stress': 0.1*yield_stress
    }
    mean_stress, std_stress, prob_failure = probabilistic_analysis(R, r, t, E, nu, p_int, p_ext, F_x, F_y, F_z, M_x, M_y, M_z, T, param_uncertainties)
    
    # Optimization analysis
    constraints = {'max_stress': yield_stress}
    opt_dimensions, opt_weight = optimization_analysis(R, r, t, E, nu, p_int, p_ext, F_x, F_y, F_z, M_x, M_y, M_z, T, constraints)
    
    return {
        'stress_tensor': stress_tensor,
        'fem_displacement': U,
        'non_linear_stress': sigma_nl,
        'thermal_stress_hoop': sigma_thermal_hoop,
        'thermal_stress_radial': sigma_thermal_radial,
        'temperature_distribution': T_distribution,
        'dynamic_stress': dynamic_stress,
        'critical_crack_length': a_crit,
        'crack_growth': (N, a),
        'probabilistic_results': (mean_stress, std_stress, prob_failure),
        'optimized_dimensions': opt_dimensions,
        'optimized_weight': opt_weight
    }

def run_analysis(calculate_torus_stresses, fatigue_analysis, advanced_calculations, create_advanced_animation):
    print("Advanced Calculations Analysis")
    
    # Get user input for parameters
    R = float(input("Enter major radius (R): "))
    r = float(input("Enter minor radius (r): "))
    t = float(input("Enter thickness (t): "))
    E = float(input("Enter Young's modulus (E): "))
    nu = float(input("Enter Poisson's ratio (nu): "))
    p_int = float(input("Enter internal pressure (p_int): "))
    p_ext = float(input("Enter external pressure (p_ext): "))
    F_x = float(input("Enter Force X (F_x): "))
    F_y = float(input("Enter Force Y (F_y): "))
    F_z = float(input("Enter Force Z (F_z): "))
    M_x = float(input("Enter Moment X (M_x): "))
    M_y = float(input("Enter Moment Y (M_y): "))
    M_z = float(input("Enter Moment Z (M_z): "))
    T = float(input("Enter temperature change (T): "))
    yield_stress = float(input("Enter yield stress: "))
    n = float(input("Enter strain hardening exponent (n): "))
    T_inner = float(input("Enter inner temperature (T_inner): "))
    T_outer = float(input("Enter outer temperature (T_outer): "))
    rho = float(input("Enter density (rho): "))
    omega = float(input("Enter angular velocity (omega): "))
    K_IC = float(input("Enter fracture toughness (K_IC): "))

    # Perform advanced analysis
    results = advanced_torus_analysis(R, r, t, E, nu, p_int, p_ext, F_x, F_y, F_z, M_x, M_y, M_z, T, yield_stress, n, T_inner, T_outer, rho, omega, K_IC)

    # Display results
    print("\nAdvanced Analysis Results:")
    for key, value in results.items():
        print(f"{key}: {value}")

    input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    # This allows the module to be run standalone for testing
    from main import calculate_torus_stresses, fatigue_analysis
    from visualization import create_advanced_animation
    run_analysis(calculate_torus_stresses, fatigue_analysis, None, create_advanced_animation)
