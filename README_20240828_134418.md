# Advanced Torus Strength Analyzer

## Description

The Advanced Torus Strength Analyzer is a comprehensive tool designed to analyze and visualize stress distributions in torus-shaped structures. This tool caters to engineers, researchers, and students working with toroidal geometries by providing both real-world examples and custom analysis capabilities. The analyzer employs advanced thin-walled torus theory for stress calculations and delivers interactive 3D visualizations of the results.

## Features

- **Real-world Examples:**
    - Pressure Vessel
    - Tokamak Fusion Reactor
    - Submarine Hull Section
    - Space Station Module
    - Pneumatic Tire
    - And many more! (See `modules/real_world_examples.py`)
- **Custom Analysis:** Analyze torus structures with user-defined parameters.
- **Advanced Stress Calculations:** Utilizes thin-walled torus theory for accurate stress estimations.
- **Interactive 3D Visualizations:** Visualize stress distributions on the torus surface.
- **Fatigue Analysis:** Simplified S-N curve and Goodman mean stress correction for fatigue life prediction.
- **Advanced Material Models:**
    - Viscoelastic material behavior using the Kelvin-Voigt model.
    - Plastic material behavior using the Ramberg-Osgood model.
- **Composite Material Analysis:** Analyzes laminated composite torus structures.
- **3D Finite Element Analysis:** Simplified 3D FEM implementation for more detailed stress analysis.
- **Vibration Analysis:** Calculates natural frequencies for the first `n` modes and provides a placeholder for visualizing mode shapes of the torus.
- **Modular Design:** Easily extensible with new analysis modules.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Kynlos/advanced-torus-strength-analyzer.git
   ```
2. **Navigate to the Project Directory:**
   ```bash
   cd advanced-torus-strength-analyzer
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Analyzer:**
   ```bash
   python main.py
   ```
2. **Navigate the Text-Based User Interface (TUI):**
    - Use the **up/down arrow keys** to browse the menu.
    - Press **Enter** to select an option.
    - Press **'q'** to quit.

## File Structure

```
advanced-torus-strength-analyzer/
├── main.py                # Main script, entry point of the application
├── tui.py                  # TUI implementation for user interaction
├── visualization.py        # Visualization functions for stress distribution
├── modules/                # Directory for analysis modules
│   ├── advanced_calculations.py # Advanced calculation functions
│   ├── advanced_material_models.py # Module for advanced material models
│   ├── composite_analysis.py # Module for composite material analysis
│   ├── fem_3d_analysis.py     # Module for 3D finite element analysis
│   ├── module_template.py    # Template for creating new modules
│   └── real_world_examples.py # Predefined real-world examples
├── requirements.txt          # List of project dependencies
├── README.md               # Project documentation
└── TODO.txt                # List of future improvements (optional)
```

## Dependencies

- numpy
- matplotlib
- scipy
- pandas
- windows-curses

## Configuration

The analyzer does not have a separate configuration file. Parameters for analysis are inputted directly through the TUI.

## Contributing

Contributions to the Advanced Torus Strength Analyzer are highly appreciated! 

To contribute:
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some awesome feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact Information

For any questions or feedback, please feel free to open an issue on the GitHub repository. 
