import numpy as np
import pandas as pd
import methods
import user_input

# default value for calculated values here
# make changes if necesssary
Zp_case3 =  39034485.58
web_depth_mm4 = 1640
epsilon4 = 1
max_moment_kNm3 = 7031
Ze4 = 34391617.25
c_10_1 = 4920
web_thickness_mm4 = 34
d_tw_ratio10_3 = 48.24
c_d_ratio_spacing10_3 = 3
Vcr9 = 8048.26
Is_intermediate10_1 = 4357266.67
LLT_ry = 219.2

# Function to write data to CSV
def write_to_csv(filename, data):
    df = pd.DataFrame(data, columns=['Parameter', 'Value'])
    df.to_csv(filename, index=False)

def append_to_csv(filename, data):
    df = pd.DataFrame(data, columns=['Parameter', 'Value'])
    separator = "-" * 60 + "\n"
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        file.write(separator)  # Write separator line
        df.to_csv(file, index=False, header=False, encoding='utf-8')

initial_values_input_bool = input("Do you want to use preset values?: ")
if (initial_values_input_bool == "n" or initial_values_input_bool == "N"):
    unsupported_length_m, yield_strength_MPa, partial_safety_factor, modulus_of_elasticity_N_per_mm2, bearing_support_width_mm = user_input.inputDefaultValues()
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
                            11. Check For Deflection
                                (Type - 11)
                            Enter your choice: 
                        ''')

    def switch(calculation_type): 
        global Zp_case3, web_depth_mm4, epsilon4, max_moment_kNm3, Ze4, Vcr9

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
        web_thickness_mm4 = web_thickness_mm = plate_size_initial_values["web_thickness_mm"]

        beam_or_plate_initial_values = methods.getLocalValues5()
        limiting_ratio_h_tw = beam_or_plate_initial_values["limiting_ratio_h_tw"]

        section_classification_initial_values = methods.getLocalValues6()
        b_tf_ratio = section_classification_initial_values["b_tf_ratio"]
        d_tw_ratio = section_classification_initial_values["d_tw_ratio"]

        shear_buckling_initial_values = methods.getLocalValues9()
        stiffner_ratio = shear_buckling_initial_values["stiffner_ratio"] 

        check_for_deflection_initial_values = methods.getLocalValues11()
        max_deflection = check_for_deflection_initial_values["max_deflection"] 


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
                max_moment_mid_span_kNm, max_moment_support_kNm, max_shear_force_kN = user_input.input_bending_moment()
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
                depth_mm, flange_width_mm, flange_thickness_mm, web_thickness_mm = user_input.input_plate_sizes()
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
                limiting_ratio_h_tw = user_input.inputBeamOrPlate()
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
                b_tf_ratio, d_tw_ratio = user_input.inputSectionClassification()
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
                stiffner_ratio = float(user_input("Enter the stiffener ratio: "))
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
            Vcr9 = Vcr = (Tau_b * web_depth_mm4 * web_thickness_mm) / 1000

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
                            2. Check For Outstand
                                (Type - 2)
                            3. Spacing Of Stiffners
                                (Type - 3)
                            4. Completion Flange Buckling Requirement
                                (Type - 4)
                            5. Buckling Check Of Stiffners
                                (Type - 5)
                            6. Bearing Stiffeners (local capacity of web)
                                (Type - 6)
                            7. Torsional stiffeners
                                (Type - 7)
                            Enter your choice: 
                        ''')
            
            def innerSwitch(calculation_type10):
                global web_depth_mm4, epsilon4, web_thickness_mm4 , c_10_1, d_tw_ratio10_3, c_d_ratio_spacing10_3, Is_intermediate10_1

                minimum_stiffners_initial_values = methods.getLocalValues10_1()
                c_d_ratio = minimum_stiffners_initial_values["c_d_ratio"]
                width_of_flat_bs = minimum_stiffners_initial_values["width_of_flat_bs"]
                thickness_of_flat_tq = minimum_stiffners_initial_values["thickness_of_flat_tq"]

                buckling_check_initial_values = methods.getLocalValues10_5()
                F_c_d_compressive_stress = buckling_check_initial_values["F_c_d_compressive_stress"]
                F_x_load_acting = buckling_check_initial_values["F_x_load_acting"]

                torisional_stiffener_initial_values = methods.getLocalValues10_7()
                flat_width_bs = torisional_stiffener_initial_values["flat_width_bs"]
                thickness_flat_tq = torisional_stiffener_initial_values["thickness_flat_tq"]


                

                if (calculation_type10 == "1"):
                    minimum_stiffners_input_bool = input("Do you want to use preset values?: ")
                    if (minimum_stiffners_input_bool == "n" or minimum_stiffners_input_bool == "N"):
                        c_d_ratio, width_of_flat_bs, thickness_of_flat_tq = user_input.input_minimum_stiffners()
                        methods.setLocalValues10_1(c_d_ratio, width_of_flat_bs, thickness_of_flat_tq)
                    
                    c10_1 = c = c_d_ratio * web_depth_mm4
                    Is_intermediate10_1 =  Is_intermediate = methods.Is_intermediateFunc(thickness_of_flat_tq, width_of_flat_bs, web_thickness_mm)

                    Is_minimum_stiffner_msg = 0

                    if c_d_ratio < 1.4142136 or c_d_ratio == 1.4142136:
                        Is_minimum_stiffner_msg = "Is=0.75dtw3"
                    else:
                        Is_minimum_stiffner_msg = "Is=(1.5d3tw3/c2)" 

                    Is_minimum_stiffner = 0

                    if c_d_ratio < 1.4142136 or c_d_ratio == 1.4142136:
                        Is_minimum_stiffner = 0.75 * web_depth_mm4 * (web_thickness_mm**3)
                    else:
                        Is_minimum_stiffner = 1.5 * (web_depth_mm4**3) * (web_thickness_mm**3) / (c**2)

                    if Is_intermediate > Is_minimum_stiffner or Is_intermediate == Is_minimum_stiffner:
                        msg = "Provided Stiffener is ok"
                    else:
                        msg = "Revise the size of stiffener"    
                 
                    # Print the calculated values
                    print(f"c/d ratio: {c_d_ratio} mm")
                    print(f"Spacing of Transverse stiffener (c): {c} mm")
                    print(f"Second moment of inertia of the section (Is): {Is_intermediate} mm^4")
                    print(f"Minimum Stiffner (Is) message: {Is_minimum_stiffner_msg} mm^4")
                    print(f"Minimum Stiffner (Is): {Is_minimum_stiffner} mm^4")
                    print("Message: ", msg)

                    data = [
                        ("c/d ratio: ", c_d_ratio),
                        ("Spacing of Transverse stiffener (c): ", c),
                        ("Second moment of inertia of the section (Is): ", Is_intermediate),
                        ("Minimum Stiffner (Is) message: ", Is_minimum_stiffner_msg),
                        ("Minimum Stiffner (Is): ", Is_minimum_stiffner),
                        ("Message: ", msg)

                    ]

                    # Append data to CSV file
                    append_to_csv('results.csv', data)  

                elif (calculation_type10 == "2"):
                    bs = width_of_flat_bs
                    limiting_value = 14 * thickness_of_flat_tq * epsilon4

                    print(f"Outstand of Stiffener, bs: {bs} mm")
                    print(f"Limiting value 14tqε: {limiting_value} mm")

                    if limiting_value > bs:
                        print("Hence, the outstand provisions of the code are satisfied")
                        msg = "Hence, the outstand provisions of the code are satisfied"
                    else:
                        print("Check for outstand is not satisfied")
                        msg = "Check for outstand is not satisfied"

                    data = [
                        ("Outstand of Stiffener, bs (mm): ", bs),
                        ("Limiting value 14tqε (mm): ", limiting_value),
                        ("Message: ", msg)
                    ]

                    # Append data to CSV file
                    append_to_csv('results.csv', data)

                elif (calculation_type10 == "3"):
                    c_d_ratio_spacing10_3 = c_d_ratio_spacing = c_10_1 / web_depth_mm4
    
                    d_tw_condition = 0
                    
                    if 1 <= c_d_ratio_spacing <= 3:
                        d_tw_condition = 200 * epsilon4
                    elif c_d_ratio_spacing < 1:
                        d_tw_condition = 270 * epsilon4
                    else:
                        d_tw_condition = " "

                    d_tw_ratio10_3 = d_tw_ratio = web_depth_mm4 / web_thickness_mm
                    
                    print(f"c/d ratio: {c_d_ratio_spacing} mm")
                    print(f"d/tw <= 200ε: {d_tw_condition} mm")
                    print(f"Section d/tw Ratio: {d_tw_ratio}")

                    if (d_tw_ratio < d_tw_condition):
                        msg = "Spacing of stiffner and Web Thickness provided is ok"
                    else:
                        msg = "Revise the spacing of stiffners or  thickness of web"
                    
                    print("Message: ", msg)
                    
                    data = [
                        ("c/d ratio: ", c_d_ratio_spacing),
                        ("d/tw <= 200ε: ", d_tw_condition),
                        ("Section d/tw Ratio: ", d_tw_ratio),
                        ("Message: ", msg)
                    ]

                    # Append data to CSV file
                    append_to_csv('results.csv', data)

                elif (calculation_type10 == "4"):    
                    d_tw_ratio_compression = 0
                    
                    if 10_3 < 1.5:
                        d_tw_ratio_compression = 345 * epsilon4
                    elif c_d_ratio_spacing10_3 >= 1.5:
                        d_tw_ratio_compression = 345 * epsilon4 * epsilon4
                    else:
                        d_tw_ratio_compression = " "
                    
                    if d_tw_ratio10_3 < d_tw_ratio_compression:
                        msg = "Thicknes of web provided is ok"
                    else:
                        msg = "Revise the web thickness"
                    
                    print(f"d/tw ratio: {d_tw_ratio10_3}")
                    print(f"d/tw ratio_compression: {d_tw_ratio_compression} mm")
                    print(f"Message: {msg}")

                    data = [
                        ("d/tw ratio: ", d_tw_ratio10_3),
                        ("d/tw ratio_compression: ", d_tw_ratio_compression),
                        ("Message: ", msg)
                    ]

                    append_to_csv('results.csv', data)

                elif (calculation_type10 == "5"):
                    buckling_check_input_bool = input("Do you want to use preset values?: ")
                    if (buckling_check_input_bool == "n" or buckling_check_input_bool == "N"):
                        F_c_d_compressive_stress, F_x_load_acting = user_input.input_buckling_check()
                        methods.setLocalValues10_5(F_c_d_compressive_stress, F_x_load_acting)

                    Fq_Stiffner_Force = (max_shear_force_kN - Vcr9) / partial_safety_factor

                    Effective_Length_of_Web = 20 * web_thickness_mm4

                    Ix = Is_intermediate10_1 + ((Effective_Length_of_Web * 2 * (web_thickness_mm4**3)) / 12)

                    Area = (Effective_Length_of_Web * 2 * web_thickness_mm4) + ((web_thickness_mm4 + width_of_flat_bs * 2) * thickness_of_flat_tq)

                    rx = (Ix / Area)**0.5

                    Le = 0.7 * web_depth_mm4

                    l = Le / rx

                    Fqd = (F_c_d_compressive_stress * Area) / 1000

                    last_expression = 0
                    if Fq_Stiffner_Force < F_x_load_acting:
                        last_expression = F_x_load_acting / Fqd
                    else:
                        last_expression = ((Fq_Stiffner_Force - F_x_load_acting) / Fqd) + (F_x_load_acting / Fqd)

                    if Fqd > Fq_Stiffner_Force:
                        msg1 = "Stiffener is safe against buckling" 
                    else:
                        msg1 = "Stiffener is not safe against buckling"
                     
                    if last_expression <= 1:
                        msg2 = "The stiffener is safe against buckling for concentrated load"
                    else:
                        msg2 = "The stiffener is not safe"

                    print(f"Fq Stiffner Force: {Fq_Stiffner_Force}")
                    print(f"Effective Length of Web (20tw): {Effective_Length_of_Web} mm")
                    print(f"Moment of Inertia (Ix): {Ix} mm^4")
                    print(f"Area: {Area} mm^2")
                    print(f"rx (radius of gyration): {rx} mm")
                    print(f"Le (Effective length): {Le} mm")
                    print(f"l: {l}")
                    print(f"Fqd (Design resistance): {Fqd} kN")
                    print(f"((Fq - Fx) / Fqd) + (Fx / Fxd): {last_expression}")
                    print("Message1: ", msg1)
                    print("Message2: ", msg2)


                    data = [
                        ("Fq Stiffner Force: ", Fq_Stiffner_Force),
                        ("Effective Length of Web (20tw): ", Effective_Length_of_Web),
                        ("Moment of Inertia (Ix): ", Ix),
                        ("Area: ", Area),
                        ("rx (radius of gyration): ", rx),
                        ("Le (Effective length): ", Le),
                        ("l: ", l),
                        ("Fqd (Design resistance): ", Fqd),
                        ("((Fq - Fx) / Fqd) + (Fx / Fxd): ", last_expression),
                        ("Message 1: ", msg1),
                        ("Message 2: ", msg2)
                    ]

                    # Append data to CSV file
                    append_to_csv('results.csv', data)
                
                elif (calculation_type10 == "6"):

                    calculation_Type10_6 = input('''
                            1. At Support
                                (Type - 1)
                            2. Away From The Support
                                (Type - 2)
                            Enter your choice: 
                        ''')
                    
                    def innerInnerSwitch(calculation_Type10_6):

                        at_support_initial_values = methods.getLocalValues10_6_1()
                        stiff_bearing_length_b1_at_support = at_support_initial_values["stiff_bearing_length_b1_at_support"]
                        stiff_bearing_length_b1_away_support = at_support_initial_values["stiff_bearing_length_b1_away_support"]

                        if (calculation_Type10_6 == "1"):
                            at_support_input_bool = input("Do you want to use preset values?: ")
                            if (at_support_input_bool == "n" or at_support_input_bool == "N"):
                                stiff_bearing_length_b1_at_support = float(input("Enter the stiffener ratio: "))
                                methods.setLocalValues10_6_1(stiff_bearing_length_b1_at_support)

                            n2 = flange_thickness_mm * 2.5

                            Fw = methods.FwFunc(n2, stiff_bearing_length_b1_at_support, web_thickness_mm4, yield_strength_MPa, partial_safety_factor)

                            if (Fw > max_shear_force_kN):
                                msg = "Hence it is ok"
                            else:
                                msg = "Hece it is not ok"
                            
                            print(msg)

                            print(f"n2 length obtained by dispersion through the flange to the web junction at slope of 1: 2.5 to the plane of the flange.: {n2} mm")
                            print(f"Fw: {Fw} kN")
                            print("Message: ", msg)

                            # Prepare data for appending to CSV
                            data = [
                                ("n2 n2 length obtained by dispersion through the flange to the web junction at slope of 1: 2.5 to the plane of the flange: ", n2),
                                ("Fw: ", Fw),
                                ("Message: ", msg)
                            ]

                            # Append data to CSV file
                            append_to_csv('results.csv', data)        



                        elif (calculation_Type10_6 == "2"):
                            away_support_input_bool = input("Do you want to use preset values?: ")
                            if (away_support_input_bool == "n" or away_support_input_bool == "N"):
                                stiff_bearing_length_b1_away_support = float(input("Enter the stiffener ratio: "))
                                methods.setLocalValues10_6_1(stiff_bearing_length_b1_away_support)

                            n2 = flange_thickness_mm * 2 * 2.5

                            Fw = methods.FwFunc(n2, stiff_bearing_length_b1_away_support, web_thickness_mm4, yield_strength_MPa, partial_safety_factor)
                                                    
                            if (Fw > max_shear_force_kN):
                                msg = "Hence it is ok"
                            else:
                                msg = "Hece it is not ok"
                            
                            print(msg)

                            print(f"n2 length obtained by dispersion through the flange to the web junction at slope of 1: 2.5 to the plane of the flange.: {n2} mm")
                            print(f"Fw: {Fw} kN")
                            print("Message: ", msg)

                            # Prepare data for appending to CSV
                            data = [
                                ("n2 n2 length obtained by dispersion through the flange to the web junction at slope of 1: 2.5 to the plane of the flange: ", n2),
                                ("Fw: ", Fw),
                                ("Message: ", msg)
                            ]

                            # Append data to CSV file
                            append_to_csv('results.csv', data)
                            

                    innerInnerSwitch(calculation_Type10_6)

                elif (calculation_type10 == "7"):
                    torsional_stiffeners_input_bool = input("Do you want to use preset values?: ")
                    if (torsional_stiffeners_input_bool == "n" or torsional_stiffeners_input_bool == "N"):
                        flat_width_bs = float(input("Enter the width of flat bs: "))
                        thickness_flat_tq = float(input("Enter the thockness of flat Tq: "))
                        methods.setLocalValues10_7(flat_width_bs, thickness_flat_tq)

                    Is = methods.IsFunc(thickness_flat_tq, flat_width_bs, web_thickness_mm4)

                    a_s = methods.a_sFunc(LLT_ry)

                    D3_Tef = methods.D3_TefFunc(a_s, depth_mm, flange_thickness_mm)

                    if (Is >= D3_Tef):
                        msg = "Hence provided stiffener has the necessary torsional restraint"
                    else:
                        msg = "provided stiffener are not torsionally restrained"
                    
                    print(f"Is: {Is} mm4")
                    print(f"a_s:  {a_s} ")
                    print(f"D3_Tef: {D3_Tef} mm4")
                    print(f"Message: {msg}")

                    data = [
                        ("Is: ", Is),
                        ("a_s: ", a_s),
                        ("D3_Tef: ", D3_Tef),
                        ("Message: ", msg)
                    ]

                    # Append data to CSV file
                    append_to_csv('results.csv', data) 

                    

            innerSwitch(calculation_type10)                

        elif (calculation_type == "11"):
            check_for_deflection_input_bool = input("Do you want to use preset values?: ")
            if (check_for_deflection_input_bool == "n" or check_for_deflection_input_bool == "N"):
                max_deflection = float(user_input("Enter the max deflection unde service road: "))
                methods.setLocalValues9(max_deflection)

            max_permisiable_deflection = unsupported_length_m * 1000 / 300

            if (max_deflection < max_permisiable_deflection):
                msg = "Section is safe in deflection"
            else:
                msg = "Section is not safe in deflection"

            print(f"Max Deflection: {max_deflection}")
            print(f"Max permissiable deflection: {max_permisiable_deflection}")
            print(f"Message: {msg}")

            data = [
                ("Max Deflection: ", max_deflection),
                ("Max permissiable deflection: ", max_permisiable_deflection),
                ("Message: ", msg)
            ]

            # Write data to CSV file
            write_to_csv('results.csv', data)

    switch(calculation_type)

