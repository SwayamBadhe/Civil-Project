# ------------------------------global variable declaration-----------------------------------
g_max_moment_mid_span_kNm = 0
g_max_moment_support_kNm = 0
g_unsupported_length_m = 20
g_yield_strength_MPa = 250
g_partial_safety_factor = 1.1
g_modulus_of_elasticity_N_per_mm2 = 200000
g_bearing_support_width_mm = 200

# Define calculation functions
def calculate_effective_length(unsupported_length_m, bearing_support_width_mm):
    L = unsupported_length_m - (bearing_support_width_mm / 1000)
    return L

def ZpFunc(max_moment_kNm, partial_safety_factor, yield_strength_MPa):
    Zp = (max_moment_kNm * 1000000 * partial_safety_factor) / yield_strength_MPa
    return Zp

# -------get and set function for intial values (case 1)
def getInitialValues():
    return (g_unsupported_length_m, g_bearing_support_width_mm, g_yield_strength_MPa, g_partial_safety_factor, g_modulus_of_elasticity_N_per_mm2)

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

# -------get and set function for plastic section modulus (case 3)
def getLocalValues3(): 
    return (g_max_moment_mid_span_kNm, g_max_moment_support_kNm)

def setLocalValues3(max_moment_mid_span_kNm, max_moment_support_kNm):
    global g_max_moment_mid_span_kNm
    global g_max_moment_support_kNm
    g_max_moment_mid_span_kNm = max_moment_mid_span_kNm
    g_max_moment_support_kNm = max_moment_support_kNm
    