import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def viscoelastic_model(stress, time, E1, E2, eta):
    """
    Kelvin-Voigt viscoelastic model
    """
    strain = stress / E1 * (1 - np.exp(-E2 * time / eta))
    return strain

def plastic_model(stress, yield_stress, E, n):
    """
    Ramberg-Osgood plasticity model
    """
    elastic_strain = stress / E
    plastic_strain = (stress / E) * (stress / yield_stress) ** n
    total_strain = elastic_strain + plastic_strain
    return total_strain

def analyze_advanced_material(model_type, parameters, stress_range, time_range=None):
    if model_type == "viscoelastic":
        E1, E2, eta = parameters
        time = np.linspace(0, time_range, 100)
        strain = [viscoelastic_model(stress, time, E1, E2, eta) for stress in stress_range]
        return time, strain
    elif model_type == "plastic":
        yield_stress, E, n = parameters
        strain = [plastic_model(stress, yield_stress, E, n) for stress in stress_range]
        return stress_range, strain
    else:
        raise ValueError("Invalid model type. Choose 'viscoelastic' or 'plastic'.")

def run_analysis(calculate_torus_stresses, fatigue_analysis, advanced_calculations, create_advanced_animation):
    print("Advanced Material Models Analysis")
    
    model_type = input("Choose model type (viscoelastic/plastic): ").lower()
    
    if model_type == "viscoelastic":
        E1 = float(input("Enter E1 (Pa): "))
        E2 = float(input("Enter E2 (Pa): "))
        eta = float(input("Enter eta (Pa*s): "))
        stress_range = np.linspace(0, 1e6, 100)
        time_range = float(input("Enter time range (s): "))
        
        time, strain = analyze_advanced_material(model_type, (E1, E2, eta), stress_range, time_range)
        
        plt.figure(figsize=(10, 6))
        plt.plot(time, strain)
        plt.xlabel("Time (s)")
        plt.ylabel("Strain")
        plt.title("Viscoelastic Material Response")
        plt.show()
        
    elif model_type == "plastic":
        yield_stress = float(input("Enter yield stress (Pa): "))
        E = float(input("Enter Young's modulus (Pa): "))
        n = float(input("Enter strain hardening exponent: "))
        stress_range = np.linspace(0, 2*yield_stress, 100)
        
        stress, strain = analyze_advanced_material(model_type, (yield_stress, E, n), stress_range)
        
        plt.figure(figsize=(10, 6))
        plt.plot(strain, stress)
        plt.xlabel("Strain")
        plt.ylabel("Stress (Pa)")
        plt.title("Plastic Material Response")
        plt.show()
        
    else:
        print("Invalid model type. Please choose 'viscoelastic' or 'plastic'.")
    
    input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    # This allows the module to be run standalone for testing
    run_analysis(None, None, None, None)
