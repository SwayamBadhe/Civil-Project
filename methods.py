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

g_stiffner_ratio = 3

g_c_d_ratio = 3
g_width_of_flat_bs = 70
g_thickness_of_flat_tq = 10

g_F_c_d_compressive_stress = 224
g_F_x_load_acting = 1000

g_stiff_bearing_length_b1_at_support = 200
g_stiff_bearing_length_b1_away_support = 0

g_flat_width_bs = 150
g_thickness_flat_tq = 20

g_max_deflection = 50

# Define calculation functions
def calculate_effective_length(unsupported_length_m, bearing_support_width_mm):
    L = unsupported_length_m - (bearing_support_width_mm / 1000)
    return L

def ZpFunc(max_moment_kNm, partial_safety_factor, yield_strength_MPa):
    Zp = (max_moment_kNm * 1000000 * partial_safety_factor) / yield_strength_MPa
    return Zp

def calculate_plate_properties(depth_mm, flange_depth_mm, flange_thickness_mm, web_thickness_mm, yield_strength_MPa):
    web_depth_mm = depth_mm - 2 * flange_thickness_mm

    Ix = (flange_depth_mm * depth_mm ** 3 / 12) - (((flange_depth_mm - web_thickness_mm) * (depth_mm - 2 * flange_thickness_mm) ** 3) / 12)

    Iy = ((2 * flange_thickness_mm * flange_depth_mm ** 3) / 12) + (((depth_mm - 2 * flange_thickness_mm) * web_thickness_mm ** 3) / 12)

    epsilon = (250 / yield_strength_MPa) ** 0.5

    Ze = Ix / (depth_mm / 2)

    Zp = Ze * 1.135

    return {
        "web_depth_mm": web_depth_mm,
        "Ix": Ix,
        "Iy": Iy,
        "epsilon": epsilon,
        "Ze": Ze,
        "Zp": Zp
    }

def VdFunc(yield_strength_MPa, web_depth_mm4, web_thickness_mm, partial_safety_factor):
    Vd = yield_strength_MPa * web_depth_mm4 * web_thickness_mm / (1000 * partial_safety_factor * (3 ** 0.5))
    return Vd

def moment_MdFunc(Zp3, yield_strength_MPa, partial_safety_factor):
    moment_Md = ((1 * Zp3 * yield_strength_MPa) / partial_safety_factor) / 1000000
    return moment_Md

def moment_limitFunc(Ze, yield_strength_MPa, partial_safety_factor):
    moment_limit = ((1.2 * Ze * yield_strength_MPa) / partial_safety_factor) / 1000000
    return moment_limit

def Tau_cr_eFunc(Kv, web_depth_mm4, web_thickness_mm):
    Tau_cr_e = (Kv * 3.14**2 * 200000) / (12 * (1 - 0.3**2) * ((web_depth_mm4 / web_thickness_mm)**2))
    return Tau_cr_e

def Is_immediateFunc(thickness_of_flat_tq, width_of_flat_bs, web_thickness_mm):
    Is = ((thickness_of_flat_tq * ((2 * width_of_flat_bs + web_thickness_mm) ** 3) / 12) - (thickness_of_flat_tq * (web_thickness_mm ** 3) / 12))
    return Is

def FwFunc(n2, stiff_bearing_length_b1, web_thickness_mm4, yield_strength_MPa, partial_safety_factor):
    Fw = (n2 + stiff_bearing_length_b1) * web_thickness_mm4 * yield_strength_MPa / (partial_safety_factor * 1000)
    return Fw

def IsFunc(thickness_flat_tq, flat_width_bs, web_thickness_mm4):
    Is = ((thickness_flat_tq * ((flat_width_bs * 2 + web_thickness_mm4) ** 3) / 12) - (thickness_flat_tq * (web_thickness_mm4 ** 3) / 12))
    return Is

def D3_TefFunc(a_s, depth_mm, flange_thickness_mm):
    D3_Teff = 0.34 * a_s * (depth_mm ** 3) * flange_thickness_mm
    return D3_Teff

def a_sFunc(LLT_ry):
    if LLT_ry <= 50:
        a_s = 0.006
    elif 50 < LLT_ry <= 100:
        a_s = 0.3 / LLT_ry
    else:
        a_s = 30 / (LLT_ry * LLT_ry)
    
    return a_s


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

# -------get and set function for Shear Buckling (case 9)
def getLocalValues9():
    return{
        "stiffner_ratio": g_stiffner_ratio
    }

def setLocalValues9(stiffner_ratio):
    global g_stiffner_ratio
    g_stiffner_ratio = stiffner_ratio


# -------get and set function for Minimum Stiffners (case 10.1)
def setLocalValues10_1(c_d_ratio, width_of_flat_bs, thickness_of_flat_tq):
    global g_c_d_ratio, g_width_of_flat_bs, g_thickness_of_flat_tq
    g_c_d_ratio = c_d_ratio
    g_width_of_flat_bs = width_of_flat_bs
    g_thickness_of_flat_tq = thickness_of_flat_tq

def getLocalValues10_1():
    return {
        "c_d_ratio": g_c_d_ratio,
        "width_of_flat_bs": g_width_of_flat_bs,
        "thickness_of_flat_tq": g_thickness_of_flat_tq
    }

# -------get and set function for Buckling Check of Stiffners (case 10.5)
def setLocalValues10_5(F_c_d_compressive_stress, F_x_load_acting):
    global g_F_c_d_compressive_stress, g_F_x_load_acting
    g_F_c_d_compressive_stress = F_c_d_compressive_stress
    g_F_x_load_acting = F_x_load_acting

def getLocalValues10_5():
    return {
        "F_c_d_compressive_stress": g_F_c_d_compressive_stress,
        "F_x_load_acting": g_F_x_load_acting
    }

# -------get and set function for Stiff Bearing Length (case 10.6.1)
def setLocalValues10_6_1(stiff_bearing_length_b1):
    global g_stiff_bearing_length_b1_at_support, g_stiff_bearing_length_b1_away_support
    g_stiff_bearing_length_b1_at_support = stiff_bearing_length_b1
    g_stiff_bearing_length_b1_away_support = stiff_bearing_length_b1

def getLocalValues10_6_1():
    return {
        "stiff_bearing_length_b1_at_support": g_stiff_bearing_length_b1_at_support,
        "stiff_bearing_length_b1_away_support": g_stiff_bearing_length_b1_away_support
    }

# -------get and set function for Torisional Stiffeners (case 10.7)
def setLocalValues10_7(flat_width_bs, thickness_flat_tq):
    global g_flat_width_bs, g_thickness_flat_tq
    g_flat_width_bs = flat_width_bs
    g_thickness_flat_tq = thickness_flat_tq

def getLocalValues10_7():
    return {
        "flat_width_bs": g_flat_width_bs,
        "thickness_flat_tq": g_thickness_flat_tq
    }

# -------get and set function for Check for deflection (case 10.11)
def setLocalValues11(max_deflection):
    global g_max_deflection
    g_max_deflection = max_deflection

def getLocalValues11():
    return {
        "max_deflection": g_max_deflection
    }

