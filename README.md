# Advanced Torus Strength Analyzer

## Description

The Advanced Torus Strength Analyzer is a comprehensive tool for analyzing and visualizing stress distributions in torus-shaped structures. It offers both real-world examples and custom analysis capabilities, making it suitable for engineers, researchers, and students working with toroidal geometries. The analyzer now includes advanced calculations and simulations for a more in-depth analysis of torus structures.

## Features

- Real-world examples of torus structures (e.g., Pressure Vessel, Tokamak Fusion Reactor)
- Custom analysis with user-defined parameters
- Advanced stress calculations using thin-walled torus theory
- Interactive 3D visualizations of stress distributions
- Fatigue analysis capabilities
- Calculation of von Mises, hoop, and meridional stresses
- Consideration of thermal stresses
- Polar stress distribution plots
- Finite Element Analysis (FEA) for more accurate stress predictions
- Non-linear material modeling
- Thermal stress analysis with heat transfer considerations
- Dynamic stress analysis for rotating structures
- Fracture mechanics analysis including fatigue crack growth
- Probabilistic analysis using Monte Carlo simulation
- Design optimization to minimize weight while meeting stress constraints

## Installation

1. Clone this repository:
   
   `git clone https://github.com/Kynlos/advanced-torus-strength-analyzer.git`
   

2. Navigate to the project directory:
   
   `cd advanced-torus-strength-analyzer`
   

3. Install the required dependencies:
   
   `pip install -r requirements.txt`
   

## Usage

Run the main script to start the analyzer:

`python main.py`


Use the arrow keys to navigate the menu, Enter to select an option, and 'q' to quit.

## Real-world Examples

The analyzer includes the following pre-defined examples:
1. Pressure Vessel
2. Tokamak Fusion Reactor
3. Submarine Hull Section
4. Space Station Module
5. Pneumatic Tire

Each example comes with specific parameters tailored to its use case, including dimensions, material properties, and applied loads.

## Custom Analysis

Input your own parameters to analyze custom torus structures. Adjust values such as:
- Major radius (R)
- Minor radius (r)
- Thickness (t)
- Young's modulus (E)
- Poisson's ratio (nu)
- Internal and external pressures
- Applied forces (F_x, F_y, F_z)
- Applied moments (M_x, M_y, M_z)
- Temperature change (T)
- Number of cycles (for fatigue analysis)
- Ultimate tensile strength
- Failure criteria (von Mises stress)
- Yield stress
- Strain hardening exponent (n)
- Inner and outer temperatures (T_inner, T_outer)
- Density (rho)
- Angular velocity (omega)
- Fracture toughness (K_IC)

## Visualization

The analyzer provides several visualization options:
- 3D stress distribution on the torus surface
- 2D stress distribution plots (von Mises, hoop, and meridional stresses)
- 2D cross-section view of the torus
- Polar plot of stress distribution
- Animation of stress evolution with changing parameters
- FEA displacement plot
- Temperature distribution plot
- Dynamic stress analysis results

## Advanced Features

- Fatigue analysis using simplified S-N curve and Goodman mean stress correction
- Thermal stress consideration in calculations
- Interactive animation showing stress evolution with changing parameters
- Finite Element Analysis for more accurate stress predictions
- Non-linear material modeling combining Ramberg-Osgood and Chaboche models
- Thermal stress analysis with heat transfer considerations
- Dynamic stress analysis for rotating structures
- Fracture mechanics analysis including fatigue crack growth using Paris law
- Probabilistic analysis using Monte Carlo simulation to account for parameter uncertainties
- Design optimization to minimize weight while meeting stress constraints

## Advanced Calculations

The `advanced_calculations.py` module provides the following advanced analyses:

1. `advanced_stress_tensor`: Calculates the full 3D stress tensor
2. `finite_element_analysis`: Performs a simplified FEA for the torus structure
3. `non_linear_material_model`: Implements an advanced non-linear material model
4. `thermal_stress_analysis`: Calculates thermal stresses with heat transfer considerations
5. `dynamic_stress_analysis`: Analyzes dynamic stresses due to rotation and vibration
6. `fracture_mechanics`: Performs fracture mechanics analysis including fatigue crack growth
7. `probabilistic_analysis`: Conducts a Monte Carlo simulation for probabilistic analysis
8. `optimization_analysis`: Performs design optimization to minimize weight

These advanced calculations provide a more comprehensive analysis of the torus structure, considering various aspects of material behavior, thermal effects, dynamics, and uncertainties.

## Contributing

Contributions to improve the Advanced Torus Strength Analyzer are welcome. Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.