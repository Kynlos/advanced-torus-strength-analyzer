import numpy as np
from scipy.linalg import solve

def run_analysis(calculate_torus_stresses, fatigue_analysis, advanced_calculations, create_advanced_animation):
    print("Composite Material Analysis")

    # Get user input for parameters
    n_layers = int(input("Enter number of layers: "))
    layers = []
    for i in range(n_layers):
        print(f"\nLayer {i+1}:")
        thickness = float(input("Enter thickness: "))
        angle = float(input("Enter fiber orientation angle (degrees): "))
        E1 = float(input("Enter longitudinal Young's modulus (E1): "))
        E2 = float(input("Enter transverse Young's modulus (E2): "))
        G12 = float(input("Enter in-plane shear modulus (G12): "))
        nu12 = float(input("Enter major Poisson's ratio (nu12): "))
        layers.append((thickness, angle, E1, E2, G12, nu12))

    # Perform laminate analysis
    ABD_matrix, strains, stresses = laminate_analysis(layers)

    # Display results
    print("\nComposite Analysis Results:")
    print("ABD Matrix:")
    print(ABD_matrix)
    print("\nMid-plane Strains and Curvatures:")
    print(strains)
    print("\nStresses in each layer:")
    for i, layer_stress in enumerate(stresses):
        print(f"Layer {i+1}:")
        print(layer_stress)

    # Visualize results
    create_advanced_animation(layers, strains, stresses)

    input("\nPress Enter to return to the main menu...")

def laminate_analysis(layers):
    n_layers = len(layers)
    total_thickness = sum(layer[0] for layer in layers)
    z = np.cumsum([0] + [layer[0] for layer in layers]) - total_thickness/2

    A = np.zeros((3, 3))
    B = np.zeros((3, 3))
    D = np.zeros((3, 3))

    for i in range(n_layers):
        thickness, angle, E1, E2, G12, nu12 = layers[i]
        Q = calculate_stiffness_matrix(E1, E2, G12, nu12)
        Q_bar = transform_stiffness_matrix(Q, angle)

        A += Q_bar * (z[i+1] - z[i])
        B += 0.5 * Q_bar * (z[i+1]**2 - z[i]**2)
        D += (1/3) * Q_bar * (z[i+1]**3 - z[i]**3)

    ABD_matrix = np.block([[A, B], [B, D]])

    # Apply loads/moments (example values, can be user inputs)
    N = np.array([1000, 500, 0])  # Force resultants
    M = np.array([0, 0, 100])  # Moment resultants
    loads = np.concatenate((N, M))

    # Solve for mid-plane strains and curvatures
    strains = solve(ABD_matrix, loads)

    # Calculate stresses in each layer
    stresses = []
    for i in range(n_layers):
        thickness, angle, E1, E2, G12, nu12 = layers[i]
        Q = calculate_stiffness_matrix(E1, E2, G12, nu12)
        Q_bar = transform_stiffness_matrix(Q, angle)
        
        eps_0 = strains[:3]
        kappa = strains[3:]
        z_mid = (z[i] + z[i+1]) / 2
        
        eps = eps_0 + z_mid * kappa
        stress = Q_bar @ eps
        stresses.append(stress)

    return ABD_matrix, strains, stresses

def calculate_stiffness_matrix(E1, E2, G12, nu12):
    nu21 = nu12 * E2 / E1
    Q = np.array([
        [E1 / (1 - nu12 * nu21), nu12 * E2 / (1 - nu12 * nu21), 0],
        [nu12 * E2 / (1 - nu12 * nu21), E2 / (1 - nu12 * nu21), 0],
        [0, 0, G12]
    ])
    return Q

def transform_stiffness_matrix(Q, angle):
    theta = np.radians(angle)
    c, s = np.cos(theta), np.sin(theta)
    T = np.array([
        [c**2, s**2, 2*c*s],
        [s**2, c**2, -2*c*s],
        [-c*s, c*s, c**2 - s**2]
    ])
    return T.T @ Q @ T

if __name__ == "__main__":
    from main import calculate_torus_stresses, fatigue_analysis
    from modules import advanced_calculations
    from visualization import create_advanced_animation
    run_analysis(calculate_torus_stresses, fatigue_analysis, advanced_calculations, create_advanced_animation)
