import numpy as np
import pandas as pd
import methods

# default value for calculated values here
# make changes if necesssary
Zp_case3 = 0
web_depth_mm4 = 0
epsilon4 = 0
max_moment_kNm3 = 0
Ze4 = 0

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

def input_plate_sizes():
    depth_mm = float(input("Enter Plate Depth (in mm): "))
    flange_width_mm = float(input("Enter Plate Flange Depth (in mm): "))
    flange_thickness_mm = float(input("Enter Plate Flange Thickness (in mm): "))
    web_thickness_mm = float(input("Enter Plate Web Thickness (in mm): "))

    return (depth_mm, flange_width_mm, flange_thickness_mm, web_thickness_mm)

def inputSectionClassification():
    b_tf_ratio = float(input("Enter the value of Ratio b/tf: "))
    d_tw_ratio = float(input("Enter the value of Ratio d/tw: "))
    return (b_tf_ratio, d_tw_ratio)

def inputBeamOrPlate():
    limiting_ratio_h_tw = float(input("Enter Liminting Ratio, h/tw: "))
    return limiting_ratio_h_tw

def input_shear_buckling():
    stiffner_ratio = float(input("Enter Stiffner ratio c/d"))
    return stiffner_ratio

def input_minimum_stiffners():
    c_d_ratio = float(input("Enter the c/d ratio: "))
    width_of_flat_bs = float(input("Enter the Width of Flat (bs) in mm: "))
    thickness_of_flat_tq = float(input("Enter the Thickness of Flat (tq) in mm: "))

    return (c_d_ratio, width_of_flat_bs, thickness_of_flat_tq)


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
                                (Type - 1)
                            2. Input Calculations of Bending Moment 
                                (Type - 2)
                            3. Plastic Section Modulus Required,Zp
                                (Type - 3)
                            4. Selection of suitable Plate Sizes
                                (Type - 4)
                            5. Design of Beam or Plate Grinder
                                (Type - 5)
                            6. Classification of Seciton
                                (Type - 6)
                            7. Calculation of shear capacity of the section
                                (Type - 7)
                            8. Check for Moment Caryying Capacity
                                (Type - 8)
                            9. Shear buckling design or Sheer Capacity
                                (Type - 9)
                            10. Design of Transverse or intermediate or vertical stiffners
                                (Type - 10)
                            Enter your choice: 
                        ''')

    def switch(calculation_type): 
        global Zp_case3, web_depth_mm4, epsilon4, max_moment_kNm3, Ze4

        initial_values = methods.getInitialValues()
        unsupported_length_m = initial_values["unsupported_length_m"]
        yield_strength_MPa = initial_values["yield_strength_MPa"]
        partial_safety_factor = initial_values["partial_safety_factor"]
        modulus_of_elasticity_N_per_mm2 = initial_values["modulus_of_elasticity_N_per_mm2"]
        bearing_support_width_mm = initial_values["bearing_support_width_mm"]  

        bending_moment_inital_values = methods.getLocalValues2()
        max_moment_mid_span_kNm = bending_moment_inital_values["max_moment_mid_span_kNm"]
        max_moment_support_kNm = bending_moment_inital_values["max_moment_support_kNm"]
        max_shear_force_kN = bending_moment_inital_values["max_shear_force_kN"]

        plate_size_initial_values = methods.getLocalValues4()
        depth_mm = plate_size_initial_values["depth_mm"]
        flange_width_mm = plate_size_initial_values["flange_width_mm"]
        flange_thickness_mm = plate_size_initial_values["flange_thickness_mm"]
        web_thickness_mm = plate_size_initial_values["web_thickness_mm"]

        beam_or_plate_initial_values = methods.getLocalValues5()
        limiting_ratio_h_tw = beam_or_plate_initial_values["limiting_ratio_h_tw"]

        section_classification_initial_values = methods.getLocalValues6()
        b_tf_ratio = section_classification_initial_values["b_tf_ratio"]
        d_tw_ratio = section_classification_initial_values["d_tw_ratio"]

        shear_buckling_initial_values = methods.getLocalValues9()
        stiffner_ratio = shear_buckling_initial_values["stiffner_ratio"]

        



        if (calculation_type == "Beam L" or calculation_type == "1"):            
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
            bending_moment_input_bool = input("Do you want to use preset values?: ")
            if (bending_moment_input_bool == "n" or bending_moment_input_bool == "N"):
                max_moment_mid_span_kNm, max_moment_support_kNm, max_shear_force_kN = input_bending_moment()
                methods.setLocalValues2(max_moment_mid_span_kNm, max_moment_support_kNm, max_shear_force_kN)
            
            methods.setLocalValues3(max_moment_mid_span_kNm, max_moment_support_kNm)
            

            data = [
                ("Max Bending moment at Mid Span (kNm): ", max_moment_mid_span_kNm),
                ("Max Bending Moment at support (KNm): ", max_moment_support_kNm),
                ("Maximum Shear Force (Kn): ", max_shear_force_kN)
            ]

            # append data to CSV file
            append_to_csv('results.csv', data)
        
        elif (calculation_type == "Plastic Section" or calculation_type == "3"):
            max_moment_kNm3 = max_moment_kNm = max(max_moment_mid_span_kNm, max_moment_support_kNm)

            # Calculate Zp
            Zp_case3 =  Zp = methods.ZpFunc(max_moment_kNm, partial_safety_factor, yield_strength_MPa)

            print(f"Max Moment of mid and support Moment: {max_moment_kNm} KNm")
            print(f"Plastic Section Modulus Required (Zp): {Zp} mm^3")


            # Prepare data for writing to CSV
            data = [
                ("Max Moment (kNm): ", max_moment_kNm),
                ("Partial Safety Factor: ", partial_safety_factor),
                ("Yield Strength of Steel (MPa): ", yield_strength_MPa),
                ("MAx Moment of mid nad support Moment: ", max_moment_kNm),
                ("Plastic Section Modulus Required (mm^3): ", Zp)
            ]

            # Append data to CSV file
            append_to_csv('results.csv', data)

        elif (calculation_type == "Suitable Plate Sizes" or calculation_type == "4"):
            plate_size_input_bool = input("Do you want to use preset values?: ")
            if (plate_size_input_bool == "n" or plate_size_input_bool == "N"):
                depth_mm, flange_width_mm, flange_thickness_mm, web_thickness_mm = input_plate_sizes()
                methods.setLocalValues4(depth_mm, flange_width_mm, flange_thickness_mm, web_thickness_mm)
            
            plate_properties = methods.calculate_plate_properties(depth_mm, flange_width_mm, flange_thickness_mm, web_thickness_mm, yield_strength_MPa)

            web_depth_mm4 = web_depth_mm = plate_properties["web_depth_mm"]
            Ix = plate_properties["Ix"]
            Iy = plate_properties["Iy"]
            epsilon4 = epsilon = plate_properties["epsilon"]
            Ze4 = Ze = plate_properties["Ze"]
            Zp = plate_properties["Zp"]

            print(f"Web Depth: {web_depth_mm} mm")
            print(f"Moment of Inertia about major axis (Ix): {Ix} mm^4")
            print(f"Moment of Inertia about weak or minor axis (Iy): {Iy} mm^4")
            print(f"Epsilon: {epsilon}")
            print(f"Elastic Section Modulus (Ze): {Ze} mm^3")
            print(f"Plastic Section Modulus (Zp): {Zp} mm^3")    

            if (Zp >= Zp_case3):
                print("Provided section is ok")
                msg = "Provided section is ok"
            else:
                print("Revise the section")
                msg = "Revise the section"

            data = [
                ("Web Depth (mm): ", web_depth_mm),
                ("Moment of Inertia about major axis (Ix) (mm^4): ", Ix),
                ("Moment of Inertia about weak or minor axis (Iy) (mm^4): ", Iy),
                ("Epsilon: ", epsilon),
                ("Elastic Section Modulus (Ze) (mm^3): ", Ze),
                ("Plastic Section Modulus (Zp) (mm^3): ", Zp),
                ("Message: ", msg)
            ]

            # Append data to CSV file
            append_to_csv('results.csv', data)

        elif (calculation_type == "Beam or Plate" or calculation_type == "5"):
            beam_or_plate_input_bool = input("Do you want to use preset values?: ")
            if (beam_or_plate_input_bool == "n" or beam_or_plate_input_bool == "N"):
                limiting_ratio_h_tw = inputBeamOrPlate()
                methods.setLocalValues5(limiting_ratio_h_tw)

            h_tw_x_e = limiting_ratio_h_tw * epsilon4
            section_h_tw_ratio = web_depth_mm4 / web_thickness_mm

            print(f"h/tw X e: {h_tw_x_e}")
            print(f"Section h/tw Ratio: {section_h_tw_ratio}")

            data = [
                ("Web Depth (mm): ", web_depth_mm4),
                ("Web Thickness (mm): ", web_thickness_mm),
                ("Epsilon: ", epsilon4),
                ("Limiting Ratio (h/tw): ", limiting_ratio_h_tw),
                ("h/tw X e: ", h_tw_x_e),
                ("Section h/tw Ratio: ", section_h_tw_ratio)
            ]

            # Append data to CSV file
            append_to_csv('results.csv', data)
            
        elif (calculation_type == "Section Classification" or calculation_type == "6"):
            section_classification_input_bool = input("Do you want to use preset values?: ")
            if (section_classification_input_bool == "n" or section_classification_input_bool == "N"):
                b_tf_ratio, d_tw_ratio = inputSectionClassification()
                methods.setLocalValues6(b_tf_ratio, d_tw_ratio)

            ratio_b2_tf = flange_width_mm / 2 / flange_thickness_mm
            ratio_d_tw = web_depth_mm4 / web_thickness_mm
            b_tf_x_e = b_tf_ratio * epsilon4

            print(f"Ratio (b/2)/tf: {ratio_b2_tf}")
            print(f"Ratio d/tw: {ratio_d_tw}")
            print(f"b/tf X e: {b_tf_x_e}")

            if (ratio_b2_tf <= (8.4 * epsilon4) and ratio_d_tw <= (84 * epsilon4)):
                print("Section is plastic")
                msg = "Section is plastic"
            elif (ratio_b2_tf > (8.4 * epsilon4) and ratio_b2_tf <= b_tf_ratio and ratio_d_tw > (84 * epsilon4) and ratio_d_tw <= (d_tw_ratio * epsilon4)):
                print("Section is compact")
                msg = "Section is compact"
            else:
                print("Revise the section to make it plastic or compact")
                msg = "Revise the section to make it plastic or compact"

            data = [
                ("Flange Width (mm): ", flange_width_mm),
                ("Flange Thickness (mm): ", flange_thickness_mm),
                ("Web Depth (mm): ", web_depth_mm4),
                ("Web Thickness (mm): ", web_thickness_mm),
                ("Epsilon: ", epsilon4),
                ("Ratio (b/2)/tf: ", ratio_b2_tf),
                ("Ratio d/tw: ", ratio_d_tw),
                ("b/tf X e: ", b_tf_x_e),
                ("Message: ", msg)
            ]

            # Append data to CSV file
            append_to_csv('results.csv', data)
            
        elif (calculation_type == "Shear Capacity" or calculation_type == "7"):
            Vd = methods.VdFunc(yield_strength_MPa, web_depth_mm4, web_thickness_mm, partial_safety_factor)

            if (max_shear_force_kN < 0.6 * Vd):
                msg1 = "Low shear load"
            else:
                msg1 = "High shear load"

            if (msg1 == "Low shear load"):
                msg2 = "Moment carrying capacity of section is calculated from step 7(i)"
            else:
                msg2 = "Moment Carrying capacity of section is calculated from step 7(ii)"        

            print(f"Vd: {Vd}")
            print(msg1)
            print(msg2)

            data = [
                ("Vd: ", Vd),
                ("Message1: ", msg1),
                ("Message2: ", msg2)

            ]

            # Append data to CSV file
            append_to_csv('results.csv', data)

        elif (calculation_type == "Momement Carrying Capacity" or calculation_type == "8"):
            moment_Md = methods.moment_MdFunc(Zp_case3, yield_strength_MPa, partial_safety_factor)
            moment_limit = methods.moment_limitFunc(Ze4, yield_strength_MPa, partial_safety_factor)

            print(f"Moment Md: {moment_Md} kNm")
            print(f"Moment Limit: {moment_limit} kNm")

            if min([moment_Md, moment_limit]) >= max_moment_kNm3:
                msg = "Moment carrying capacity is safe"
            else:
                msg = "Revise the section"

            print(msg)


            data = [
                ("Moment Md (kNm): ", moment_Md),
                ("Moment Limit (kNm): ", moment_limit),
                ("Message: ", msg)
            ]

            # Append data to CSV file
            append_to_csv('results.csv', data)

        elif (calculation_type == "9"):
            shear_buckling_input_bool = input("Do you want to use preset values?: ")
            if (shear_buckling_input_bool == "n" or shear_buckling_input_bool == "N"):
                stiffner_ratio = float(input("Enter the stiffener ratio: "))
                methods.setLocalValues9(stiffner_ratio)

            Kv = 0
            Tau_cr_e = 0
            lw = 0
            Tau_b = 0
            Vcr = 0

            if stiffner_ratio < 1:
                Kv = 4 + (5.35 / stiffner_ratio**2)
            else:
                Kv = 5.35 + (4 / stiffner_ratio**2)


            # Calculate Tau_cr_e
            Tau_cr_e = methods.Tau_cr_eFunc(Kv, web_depth_mm4, web_thickness_mm)

            # Calculate lw
            lw = ((yield_strength_MPa /((3**0.5) * Tau_cr_e)))**0.5

            # Calculate Tau_b
            if lw <= 0.8:
                Tau_b = yield_strength_MPa / (3**0.5)
            elif 0.8 < lw < 1.2:
                Tau_b = (1 - 0.8 * (lw - 0.8)) * (yield_strength_MPa / (3**0.5))
            else:
                Tau_b = (yield_strength_MPa / (3**0.5 * lw**2))

            # Calculate Vcr
            Vcr = (Tau_b * web_depth_mm4 * web_thickness_mm) / 1000

            print(f"Kv: {Kv}")
            print(f"Elastic Critical shear Stress of the web, Tau_cr_e: {Tau_cr_e} N/mm^2")
            print(f"Non Dimensional Web Slenderness for shear buckling, lw: {lw}")
            print(f"Shear Stress corresponding to web buckling, Tau_b: {Tau_b} N/mm^2")
            print(f"Shear force corresponding to Web Buckling, Vcr: {Vcr} kN")

            if (Vcr > max_shear_force_kN):
                msg = "No need to provide intermediate stiffners for web buckling"
            else:
                msg = "Provide intermediate stiffners to improve the buckling strength of slender web"

            print(msg)



            data = [
                ("Stiffener Ratio: ", stiffner_ratio),
                ("Kv: ", Kv),
                ("Elastic Critical shear Stress of the web, Tau_cr_e (N/mm^2): ", Tau_cr_e),
                ("Non-Dimensional Web Slenderness for shear buckling, lw: ", lw),
                ("Shear Stress corresponding to web buckling, Tau_b (N/mm^2): ", Tau_b),
                ("Shear force corresponding to Web Buckling, Vcr (kN): ", Vcr),
                ("Message: ", msg)
            ]

            # Append data to CSV file
            append_to_csv('results.csv', data)

        elif (calculation_type == "10"):
            calculation_type10 = input('''
                            1. Minimum Stiffners
                                (Type - 1)
                            Enter your choice: 
                        ''')
            
            def innerSwitch(calculation_type10):

                minimum_stiffners_initial_values = methods.getLocalValues10_1()
                c_d_ratio = minimum_stiffners_initial_values["c_d_ratio"]
                width_of_flat_bs = minimum_stiffners_initial_values["width_of_flat_bs"]
                thickness_of_flat_tq = minimum_stiffners_initial_values["thickness_of_flat_tq"]

                if (calculation_type10 == "1"):
                    minimum_stiffners_input_bool = input("Do you want to use preset values?: ")
                    if (minimum_stiffners_input_bool == "n" or minimum_stiffners_input_bool == "N"):
                        c_d_ratio, width_of_flat_bs, thickness_of_flat_tq = input_minimum_stiffners()
                        methods.setLocalValues10_1(c_d_ratio, width_of_flat_bs, thickness_of_flat_tq)
                    
                    c = c_d_ratio * web_depth_mm4
                    Is = methods.IsFunc(thickness_of_flat_tq, width_of_flat_bs, web_thickness_mm)
                 
                    # Print the calculated values
                    print(f"Spacing of Transverse stiffener (c): {c} mm")
                    print(f"Second moment of inertia of the section (Is): {Is} mm^4")

                    data = [
                        ("Spacing of Transverse stiffener: ", c),
                        ("Second moment of inertia of the section (Is): ", Is)
                    ]

                    # Append data to CSV file
                    append_to_csv('results.csv', data)  

            innerSwitch(calculation_type10)                




    switch(calculation_type)

