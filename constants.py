import numpy as np
from scipy.interpolate import interp1d

# Extinction coefficients (in mm^-1)
# Data is taken from the literature (e.g., Scott Prahl's website, Jacques, S. L. (2013). Optical properties of biological tissues: a review. Physics in Medicine & Biology, 58(11), R37–R61.)

extinction_coefficients = {
    "hb": {  # Deoxyhemoglobin
        470: 30.8,
        495: 9.0,
        520: 8.5,
        560: 13.0,
        580: 10.5,
        630: 2.8,
        660: 3.0,
        800: 1.0,
        850: 0.8,
        880: 0.7,
    },
    "hbo2": {  # Oxyhemoglobin
        470: 5.0,
        495: 12.0,
        520: 15.0,
        540: 18.0,
        580: 20.0,
        630: 0.7,
        660: 0.9,
        800: 0.3,
        850: 0.4,
        880: 0.5,
    },
    "water": {  # Water
        470: 0.0002,
        495: 0.0003,
        520: 0.0005,
        630: 0.003,
        660: 0.004,
        800: 0.01,
        850: 0.02,
        880: 0.03,
    },
    "melanin": {  # Melanin
        470: 0.08,
        495: 0.06,
        520: 0.05,
        630: 0.02,
        660: 0.015,
        800: 0.005,
        850: 0.004,
        880: 0.003,
    },
}


# Create interpolation functions for each chromophore
def create_interp_func(data):
    wavelengths = sorted(data.keys())
    values = [data[wl] for wl in wavelengths]
    return interp1d(wavelengths, values, kind="linear", fill_value="extrapolate")


eps_hb = create_interp_func(extinction_coefficients["hb"])
eps_hbo2 = create_interp_func(extinction_coefficients["hbo2"])
eps_water = create_interp_func(extinction_coefficients["water"])
eps_melanin = create_interp_func(extinction_coefficients["melanin"])

# Skin layer parameters for the 7-layer model
# Based on data from the literature (e.g., "Computer simulation of the skin reflectance spectra" paper)
layer_params = [
    {
        "name": "Stratum Corneum",
        "d": 0.02,
        "n": 1.5,
        "C_blood": 0.0,
        "C_water": 0.05,
        "g": 0.9,
        "a_scatter": 1.2,
        "b_scatter": 0.5,
    },
    {
        "name": "Epidermis",
        "d": 0.08,
        "n": 1.4,
        "C_blood": 0.0,
        "C_water": 0.1,
        "g": 0.8,
        "a_scatter": 1.0,
        "b_scatter": 0.6,
    },
    {
        "name": "Papillary Dermis",
        "d": 0.1,
        "n": 1.4,
        "C_blood": 0.05,
        "C_water": 0.2,
        "g": 0.8,
        "a_scatter": 1.5,
        "b_scatter": 0.7,
    },
    {
        "name": "Reticular Dermis 1",
        "d": 0.2,
        "n": 1.38,
        "C_blood": 0.03,
        "C_water": 0.3,
        "g": 0.7,
        "a_scatter": 2.0,
        "b_scatter": 0.8,
    },
    {
        "name": "Reticular Dermis 2",
        "d": 0.5,
        "n": 1.38,
        "C_blood": 0.02,
        "C_water": 0.4,
        "g": 0.7,
        "a_scatter": 2.5,
        "b_scatter": 0.9,
    },
    {
        "name": "Deep Dermis",
        "d": 1.0,
        "n": 1.36,
        "C_blood": 0.01,
        "C_water": 0.5,
        "g": 0.6,
        "a_scatter": 3.0,
        "b_scatter": 1.0,
    },
    {
        "name": "Subcutaneous Fat",
        "d": 2.0,
        "n": 1.44,
        "C_blood": 0.005,
        "C_water": 0.6,
        "g": 0.5,
        "a_scatter": 4.0,
        "b_scatter": 1.2,
    },
]

# Hemangioma parameters
# These are multipliers and additions to the normal skin parameters
hemangioma_params = {"blood_multiplier": 5.0, "s_o2_increase": 0.05}
