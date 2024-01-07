# Plate Girder Structural Analysis Python Script

This Python script performs structural analysis calculations for plate girders, taking user inputs for various parameters and providing appropriate measurements and checks. The calculations include effective length, plastic section modulus, plate size selection, beam or plate design, section classification, shear capacity, moment carrying capacity, and more.

## Plate Girder Overview

A plate girder is a steel beam built from plates of steel that are welded or bolted together. It typically consists of a deep vertical web joined to horizontal flanges at the top and bottom. The design of plate girders allows them to efficiently carry heavy loads over long spans, making them a popular choice for various construction projects.

### Applications of Plate Girders

Plate girders find applications in various structural engineering scenarios, including:

- **Bridges:** Plate girders are commonly used in the construction of bridge spans. Their ability to handle large loads and long spans makes them ideal for supporting bridge decks.

- **Buildings:** Plate girders are utilized as structural members in the construction of large industrial buildings, commercial structures, and multi-story buildings.

- **Industrial Structures:** Due to their high load-bearing capacity, plate girders are used in the construction of industrial facilities, such as manufacturing plants and warehouses.

## Script Usage

This Python script is designed to assist engineers and researchers in performing structural analysis and design calculations for plate girders. It covers various aspects of plate girder design, including effective length, plastic section modulus, plate size selection, section classification, shear capacity, moment-carrying capacity, and more.



## Getting Started

### Prerequisites

- Python 3.x
- Required Python packages: NumPy, Pandas (you can install them using `pip install numpy pandas`)

### Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/SwayamBadhe/Civil-Project.git
    ```

2. Run the script:

    ```bash
    python excell.py
    ```

3. Follow the prompts to input values or choose preset values for different calculations.

4. The results will be stored in a CSV file named `results.csv`.

## Input Data

The script takes the following input data from the user:

- Unsupported Length of the beam
- Yield strength of steel
- Partial safety factor
- Modulus of elasticity of steel
- Width of column or bearing support
- Max Bending moment at Mid Span
- Max Bending Moment at support
- Maximum Shear Force
- Plate Depth
- Plate Flange Depth
- Plate Flange Thickness
- Plate Web Thickness
- Ratio b/tf and d/tw for section classification
- Limiting Ratio h/tw for beam or plate design
- Stiffner ratio for shear buckling check
- c/d ratio, width of flat, and thickness of flat for minimum stiffeners
- Design Compressive Stress and Concentrated load acting for buckling check

## Configuration

You can modify the default values in the script if needed.

## File Structure

- `plate_girder_analysis.py`: The main Python script.
- `user_input.py`: Module containing user input functions.
- `methods.py`: Module containing calculation methods.
- `results.csv`: CSV file to store calculation results.

## Contributing

Contributions are welcome!
