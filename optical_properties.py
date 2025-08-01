import numpy as np

from constants import eps_hb, eps_hbo2, eps_water, eps_melanin


def get_layer_mu_a(wavelength, C_blood, C_water, C_melanin, S_O2):
    """Calculates the absorption coefficient mu_a for a given wavelength."""

    # Absorption from blood
    mu_a_blood_term = C_blood * (
        S_O2 * eps_hbo2(wavelength) + (1 - S_O2) * eps_hb(wavelength)
    )

    # Absorption from water
    mu_a_water_term = C_water * eps_water(wavelength)

    # Absorption from melanin
    mu_a_melanin_term = C_melanin * eps_melanin(wavelength)

    # Background absorption
    mu_a_other = 7.84e7 * (wavelength**-3.255)  # Assuming wavelength in nm

    # Total mu_a in mm^-1
    total_mu_a = mu_a_blood_term + mu_a_water_term + mu_a_melanin_term + mu_a_other
    return total_mu_a


def get_layer_mu_s(wavelength, a_scatter, b_scatter, g):
    """Calculates the scattering coefficient mu_s from the reduced scattering model."""
    # Wavelength-dependent reduced scattering [9]
    mu_s_prime = a_scatter * (wavelength / 500.0) ** (-b_scatter)

    # Convert back to mu_s
    mu_s = mu_s_prime / (1 - g) if (1 - g) > 1e-6 else mu_s_prime
    return mu_s
