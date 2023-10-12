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

def input_buckling_check():
    F_c_d_compressive_stress = float(input("Enter the value of Design Compressive Stress (Fcd): "))
    F_x_load_acting = float(input("Enter the value of Concentrated load acting (Fcd): "))
    return (F_c_d_compressive_stress, F_x_load_acting)
