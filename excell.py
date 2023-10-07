import numpy as np
import pandas as pd
import methods


# Input data from the user
def inputDefaultValues():
    unsupported_length_m = float(input("Enter the Unsupported Length of the beam (in meters): "))
    yield_strength_MPa = float(input("Enter the Yield strength of steel (in MPa): "))
    partial_safety_factor = float(input("Enter the Partial Safety Factor: "))
    modulus_of_elasticity_N_per_mm2 = float(input("Enter the Modulus of elasticity of Steel (in N/mm^2): "))
    bearing_support_width_mm = float(input("Enter the Width of column or bearing support (in millimeters): "))
    
    return (unsupported_length_m, yield_strength_MPa, partial_safety_factor, modulus_of_elasticity_N_per_mm2, bearing_support_width_mm)

def input_bending_moment():
    max_moment_mid_span_kNm = float(input("Enter Max Bending moment at Mid Span (in kNm): "))
    max_moment_support_kNm = float(input("Enter Max Bending Moment at support (in kNm): "))
    max_shear_force_kN = float(input("Enter Maximum Shear Force (in kN): "))

    return (max_moment_mid_span_kNm, max_moment_support_kNm, max_shear_force_kN)  


# Function to write data to CSV
def write_to_csv(filename, data):
    df = pd.DataFrame(data, columns=['Parameter', 'Value'])
    df.to_csv(filename, index=False)

def append_to_csv(filename, data):
    df = pd.DataFrame(data, columns=['Parameter', 'Value'])
    with open(filename, 'a', newline='') as file:
        file.write("-" * 60 + "\n")  # Add separator line
        df.to_csv(file, index=False, header=False)

initial_values_input_bool = input("Do you want to use preset values?: ")
if (initial_values_input_bool == "n" or initial_values_input_bool == "N"):
    unsupported_length_m, yield_strength_MPa, partial_safety_factor, modulus_of_elasticity_N_per_mm2, bearing_support_width_mm = inputDefaultValues()
    methods.setInitialValues(unsupported_length_m, yield_strength_MPa, partial_safety_factor, modulus_of_elasticity_N_per_mm2, bearing_support_width_mm)

while (True):

    calculation_type = input('''
                            1. Effective length of Beam L (c/c of column support)
                                (Type - Beam L)
                            2. Input Calculations of Bending Moment 
                                (Type - Bending Moment Input)
                            3. Plastic Section Modulus Required,Zp
                                (Type - Plastic Section)
                            Enter your choice: 
                        ''')

    def switch(calculation_type):        

        if (calculation_type == "Beam L" or calculation_type == "1"):
            initial_values = methods.getInitialValues()
            unsupported_length_m = initial_values["unsupported_length_m"]
            yield_strength_MPa = initial_values["yield_strength_MPa"]
            partial_safety_factor = initial_values["partial_safety_factor"]
            modulus_of_elasticity_N_per_mm2 = initial_values["modulus_of_elasticity_N_per_mm2"]
            bearing_support_width_mm = initial_values["bearing_support_width_mm"]
            L = methods.calculate_effective_length(unsupported_length_m, bearing_support_width_mm)
            print(f"Effective length of Beam L (c/c of column support): {L} meters")

            # Prepare data for writing to CSV
            data = [
                ("Unsupported Length of the beam (m): ", unsupported_length_m),
                ("Yield strength of steel (MPa): ", yield_strength_MPa),
                ("Partial Safety Factor: ", partial_safety_factor),
                ("Modulus of elasticity of Steel (N/mm^2): ", modulus_of_elasticity_N_per_mm2),
                ("Width of column or bearing support (mm): ", bearing_support_width_mm),
                ("Effective length of Beam L (m): ", L)
            ]

            # Write data to CSV file
            write_to_csv('results.csv', data)

        elif (calculation_type == "Bending Moment" or calculation_type == "2"):
            max_moment_mid_span_kNm, max_moment_support_kNm, max_shear_force_kN = input_bending_moment()
            methods.setLocalValues3(max_moment_mid_span_kNm, max_moment_support_kNm)
            

            data = [
                ("Max Bending moment at Mid Span (kNm): ", max_moment_mid_span_kNm),
                ("Max Bending Moment at support (KNm): ", max_moment_support_kNm),
                ("Maximum Shear Force (Kn): ", max_shear_force_kN)
            ]

            # append data to CSV file
            append_to_csv('results.csv', data)
        
        elif (calculation_type == "Plastic Section" or calculation_type == "3"):
            max_moment_mid_span_kNm, max_moment_support_kNm = methods.getLocalValues3()
            max_moment_kNm = max(max_moment_mid_span_kNm, max_moment_support_kNm)

            # Calculate Zp
            Zp = methods.ZpFunc(max_moment_kNm, partial_safety_factor, yield_strength_MPa)

            print(f"Plastic Section Modulus Required (Zp): {Zp} mm^3")

            # Prepare data for writing to CSV
            data = [
                ("Max Moment (kNm): ", max_moment_kNm),
                ("Partial Safety Factor: ", partial_safety_factor),
                ("Yield Strength of Steel (MPa): ", yield_strength_MPa),
                ("Plastic Section Modulus Required (mm^3): ", Zp)
            ]

            # Append data to CSV file
            append_to_csv('results.csv', data)

    switch(calculation_type)

