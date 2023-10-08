# ------------------------------global variable declaration-----------------------------------
# default value for input values here
# make changes if necesssary
g_unsupported_length_m = 20
g_yield_strength_MPa = 250
g_partial_safety_factor = 1.1
g_modulus_of_elasticity_N_per_mm2 = 200000
g_bearing_support_width_mm = 200

g_max_moment_mid_span_kNm = 7031
g_max_moment_support_kNm = 0
g_max_shear_force_kN = 1012.50

g_depth_mm = 1700
g_flange_width_mm = 400
g_flange_thickness_mm = 30
g_web_thickness_mm = 34

g_b_tf_ratio = 8.40
g_d_tw_ratio = 84.0

g_limiting_ratio_h_tw = 67

# Define calculation functions
def calculate_effective_length(unsupported_length_m, bearing_support_width_mm):
    L = unsupported_length_m - (bearing_support_width_mm / 1000)
    return L

def ZpFunc(max_moment_kNm, partial_safety_factor, yield_strength_MPa):
    Zp = (max_moment_kNm * 1000000 * partial_safety_factor) / yield_strength_MPa
    return Zp

def calculate_plate_properties(depth_mm, flange_depth_mm, flange_thickness_mm, web_thickness_mm, yield_strength_MPa):
    # Calculate web depth
    web_depth_mm = depth_mm - 2 * flange_thickness_mm

    # Calculate Moment of Inertia about major axis (Ix)
    Ix = (flange_depth_mm * depth_mm ** 3 / 12) - (((flange_depth_mm - web_thickness_mm) * (depth_mm - 2 * flange_thickness_mm) ** 3) / 12)

    # Calculate Moment of Inertia about weak or minor axis (Iy)
    Iy = ((2 * flange_thickness_mm * flange_depth_mm ** 3) / 12) + (((depth_mm - 2 * flange_thickness_mm) * web_thickness_mm ** 3) / 12)

    # Calculate epsilon
    epsilon = (250 / yield_strength_MPa) ** 0.5

    # Calculate Elastic Section Modulus (Ze)
    Ze = Ix / (depth_mm / 2)

    # Calculate Plastic Section Modulus (Zp)
    Zp = Ze * 1.135

    return {
        "web_depth_mm": web_depth_mm,
        "Ix": Ix,
        "Iy": Iy,
        "epsilon": epsilon,
        "Ze": Ze,
        "Zp": Zp
    }


# -------get and set function for intial values (case 1)
def getInitialValues():
    return {
        "unsupported_length_m": g_unsupported_length_m,
        "bearing_support_width_mm": g_bearing_support_width_mm,
        "yield_strength_MPa": g_yield_strength_MPa,
        "partial_safety_factor": g_partial_safety_factor,
        "modulus_of_elasticity_N_per_mm2": g_modulus_of_elasticity_N_per_mm2
    }

def setInitialValues(unsupported_length_m, yield_strength_MPa, partial_safety_factor, modulus_of_elasticity_N_per_mm2, bearing_support_width_mm):
    global g_unsupported_length_m
    global g_bearing_support_width_mm
    global g_yield_strength_MPa
    global g_partial_safety_factor
    global g_modulus_of_elasticity_N_per_mm2
    g_unsupported_length_m = unsupported_length_m
    g_bearing_support_width_mm = bearing_support_width_mm
    g_yield_strength_MPa = yield_strength_MPa
    g_partial_safety_factor = partial_safety_factor
    g_modulus_of_elasticity_N_per_mm2 = modulus_of_elasticity_N_per_mm2

# -------get and set function for Bending Moment (case 2)
def getLocalValues2():
    return {
        "max_moment_mid_span_kNm": g_max_moment_mid_span_kNm,
        "max_moment_support_kNm": g_max_moment_support_kNm,
        "max_shear_force_kN": g_max_shear_force_kN
    }

def setLocalValues2(max_moment_mid_span_kNm, max_moment_support_kNm, max_shear_force_kN):
    global g_max_moment_mid_span_kNm, g_max_moment_support_kNm, g_max_shear_force_kN
    g_max_moment_mid_span_kNm = max_moment_mid_span_kNm
    g_max_moment_support_kNm = max_moment_support_kNm
    g_max_shear_force_kN = max_shear_force_kN


# -------get and set function for plastic section modulus (case 3)
# def getLocalValues3(): 
#     return {
#         "max_moment_mid_span_kNm": g_max_moment_mid_span_kNm,
#         "max_moment_support_kNm": g_max_moment_support_kNm,
#     }

def setLocalValues3(max_moment_mid_span_kNm, max_moment_support_kNm):
    global g_max_moment_mid_span_kNm
    global g_max_moment_support_kNm
    g_max_moment_mid_span_kNm = max_moment_mid_span_kNm
    g_max_moment_support_kNm = max_moment_support_kNm
    
# -------get and set function for suitable Plate Sizes (case 4)
def getLocalValues4():
    return {
        "depth_mm": g_depth_mm,
        "flange_width_mm": g_flange_width_mm,
        "flange_thickness_mm": g_flange_thickness_mm,
        "web_thickness_mm": g_web_thickness_mm
    }

def setLocalValues4(depth_mm, flange_width_mm, flange_thickness_mm, web_thickness_mm):
    global g_depth_mm, g_flange_width_mm, g_flange_thickness_mm, g_web_thickness_mm
    g_depth_mm = depth_mm
    g_flange_width_mm = flange_width_mm
    g_flange_thickness_mm = flange_thickness_mm
    g_web_thickness_mm = web_thickness_mm

# -------get and set function for Section Classification (case 6)
def getLocalValues5():
    return{
        "limiting_ratio_h_tw": g_limiting_ratio_h_tw
    }

def setLocalValues5(limiting_ratio_h_tw):
    global g_limiting_ratio_h_tw
    g_limiting_ratio_h_tw = limiting_ratio_h_tw

# -------get and set function for Section Classification (case 6)
def getLocalValues6():
    return{
        "b_tf_ratio": g_b_tf_ratio, 
        "d_tw_ratio": g_d_tw_ratio
    }

def setLocalValues6(b_tf_ratio, d_tw_ratio):
    global g_b_tf_ratio, g_d_tw_ratio
    g_b_tf_ratio = b_tf_ratio
    g_d_tw_ratio = d_tw_ratio
