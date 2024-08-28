```python
"""
## Advanced Torus Stress Analysis Script

This script performs comprehensive stress analysis of a torus under various loading conditions.

**1. Script Name:** 
   advanced_torus_analysis.py

**2. Description:**

This script provides a suite of advanced engineering analysis tools for a torus, including:

   - **Basic Stress Calculation:** Computes the von Mises stress, hoop stress, and radial stress.
   - **Advanced Stress Tensor:**  Calculates the full 3D stress tensor considering bending moments.
   - **Finite Element Analysis:**  Performs basic FEA to determine displacements under load.
   - **Non-Linear Material Model:**  Incorporates material non-linearity (plasticity) using Ramberg-Osgood and Chaboche models.
   - **Thermal Stress Analysis:**  Calculates thermal stresses due to temperature gradients, considering heat transfer.
   - **Dynamic Stress Analysis:**  Computes dynamic stresses arising from rotation and vibration.
   - **Fracture Mechanics:**  Analyzes crack growth under fatigue using Paris Law and determines critical crack length.
   - **Probabilistic Analysis:**  Performs Monte Carlo simulation to assess the impact of input parameter uncertainties.
   - **Optimization Analysis:**  Finds optimal torus dimensions (major radius, minor radius, thickness) to minimize weight while satisfying stress constraints.

**3. Usage:**

The script is intended to be run within a larger Python application or directly from the command line (see `if __name__ == "__main__":`). It takes input parameters either from user input or passed as arguments to the `advanced_torus_analysis()` function. 

**4. Parameters:**

**Main Function (advanced_torus_analysis):**

   - `R`: Major radius of the torus (m).
   - `r`: Minor radius of the torus (m).
   - `t`: Thickness of the torus (m).
   - `E`: Young's modulus of the material (Pa).
   - `nu`: Poisson's ratio of the material.
   - `p_int`: Internal pressure (Pa).
   - `p_ext`: External pressure (Pa).
   - `F_x`: Force in the x-direction (N).
   - `F_y`: Force in the y-direction (N).
   - `F_z`: Force in the z-direction (N).
   - `M_x`: Moment about the x-axis (N·m).
   - `M_y`: Moment about the y-axis (N·m).
   - `M_z`: Moment about the z-axis (N·m).
   - `T`: Temperature change (K).
   - `yield_stress`: Yield stress of the material (Pa).
   - `n`: Strain hardening exponent.
   - `T_inner`: Inner surface temperature (K).
   - `T_outer`: Outer surface temperature (K).
   - `rho`: Density of the material (kg/m³).
   - `omega`: Angular velocity (rad/s).
   - `K_IC`: Fracture toughness (Pa·m^0.5).

**Other Important Functions:**

   - `advanced_stress_tensor()`: Calculates the full 3D stress tensor.
   - `finite_element_analysis()`: Performs basic finite element analysis.
   - `non_linear_material_model()`: Applies Ramberg-Osgood and Chaboche material models.
   - `thermal_stress_analysis()`: Calculates thermal stresses.
   - `dynamic_stress_analysis()`: Calculates dynamic stresses.
   - `fracture_mechanics()`: Performs fracture mechanics analysis.
   - `probabilistic_analysis()`: Conducts probabilistic analysis using Monte Carlo simulation.
   - `optimization_analysis()`: Performs design optimization.

**5. Functions:**

   - **`advanced_torus_analysis(...)`:** Main function orchestrating all analysis types. Returns a dictionary of results.
   - **`advanced_stress_tensor(...)`:** Computes the full 3D stress tensor.
   - **`finite_element_analysis(...)`:** Performs basic FEA using a simplified element.
   - **`non_linear_material_model(...)`:**  Calculates stress considering material non-linearity.
   - **`thermal_stress_analysis(...)`:**  Calculates thermal stresses with heat transfer.
   - **`dynamic_stress_analysis(...)`:**  Calculates dynamic stresses due to rotation and vibration.
   - **`fracture_mechanics(...)`:**  Performs fracture mechanics analysis, including fatigue crack growth.
   - **`probabilistic_analysis(...)`:**  Conducts probabilistic analysis to account for parameter uncertainties.
   - **`optimization_analysis(...)`:**  Finds optimal torus dimensions to minimize weight under stress constraints.
   - **`run_analysis(...)`:** This function gets user input, calls the advanced analysis functions, and displays the results. It is called when the script is run standalone.

**6. Dependencies:**

   - `numpy`
   - `scipy`
   - `sympy` 

**7. Example Usage:**

   ```python
   from main import calculate_torus_stresses, fatigue_analysis
   from visualization import create_advanced_animation

   # Example parameters
   R = 1.0 
   r = 0.2
   # ... other parameters

   results = advanced_torus_analysis(R, r, t, E, nu, p_int, p_ext, F_x, F_y, F_z, M_x, M_y, M_z, T, yield_stress, n, T_inner, T_outer, rho, omega, K_IC)

   print(results) 
   ```

**8. Important Notes:**

   - The script uses simplified models and assumptions for some analyses (e.g., FEA, dynamic analysis). For more accurate results, use dedicated FEA or dynamic analysis software.
   - The probabilistic analysis assumes normal distributions for the uncertain parameters. You can modify this for different probability distributions.
   - Adjust the number of samples in the probabilistic analysis and the number of elements in the FEA for desired accuracy and computational time trade-offs.
   - Units should be consistent throughout the script (SI units are recommended).
   - The `run_analysis` function and its call at the end of the script are specifically designed for standalone execution. When integrating this script into a larger application, you likely want to remove or modify these parts.
```
