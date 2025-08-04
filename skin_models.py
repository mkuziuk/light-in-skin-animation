# skin_models.py
import numpy as np

import xopto.mcml as mc
from xopto.mcbase.mcpf.hg import Hg
import optical_properties as op
from constants import layer_params, hemangioma_params


def create_normal_skin_model(wavelength):
    """Creates a pyxopto Layers object for the 7-layer normal skin model."""

    # Top layer (air)
    # layers_list = [mc.mclayer.Layer(n=1.0, d=np.inf)]
    layers_list = [mc.mclayer.Layer(n=1.0, d=np.inf, mua=0, mus=0, pf=Hg(0))]

    # Build the 7 skin layers
    for params in layer_params:
        mu_a = op.get_layer_mu_a(
            wavelength, params["C_blood"], params["C_water"], 0, 0.7
        )  # Assume C_melanin=0 and SO2=0.7 for now
        mu_s = op.get_layer_mu_s(
            wavelength, params["a_scatter"], params["b_scatter"], params["g"]
        )

        layer = mc.mclayer.Layer(
            n=params["n"],
            d=params["d"],  # thickness in mm
            mua=mu_a,
            mus=mu_s,
            # g=params["g"],
            pf=Hg(params["g"]),  # Use Henyey-Greenstein phase function
        )
        layers_list.append(layer)

    # Bottom layer (air)
    # layers_list.append(mc.mclayer.Layer(n=1.0, d=np.inf))
    layers_list.append(mc.mclayer.Layer(n=1.0, d=np.inf, mua=0, mus=0, pf=Hg(0)))

    return mc.mclayer.Layers(layers_list)


def create_hemangioma_model(wavelength):
    """
    Creates a pyxopto Layers object for a hemangioma model.
    Starts with the normal skin model and modifies blood-rich layers.
    """

    # Create a deep copy of the normal skin layer parameters to modify
    hemangioma_layer_params = [dict(p) for p in layer_params]

    # Modify the parameters for the hemangioma
    for params in hemangioma_layer_params:
        # Increase blood concentration in dermal layers for hemangioma
        if "Dermis" in params["name"]:
            params["C_blood"] *= hemangioma_params["blood_multiplier"]

    # Top layer (air)
    # layers_list = [mc.mclayer.Layer(n=1.0, d=np.inf)]
    layers_list = [mc.mclayer.Layer(n=1.0, d=np.inf, mua=0, mus=0, pf=Hg(0))]

    # Build the 7 skin layers for hemangioma
    for params in hemangioma_layer_params:
        # Increase oxygen saturation for hemangioma
        s_o2 = (
            0.7 + hemangioma_params["s_o2_increase"]
            if "Dermis" in params["name"]
            else 0.7
        )

        mu_a = op.get_layer_mu_a(
            wavelength, params["C_blood"], params["C_water"], 0, s_o2
        )  # Assume C_melanin=0
        mu_s = op.get_layer_mu_s(
            wavelength, params["a_scatter"], params["b_scatter"], params["g"]
        )

        layer = mc.mclayer.Layer(
            n=params["n"],
            d=params["d"],  # thickness in mm
            mua=mu_a,
            mus=mu_s,
            # g=params["g"],
            pf=Hg(params["g"]),  # Use Henyey-Greenstein phase function
        )
        layers_list.append(layer)

    # Bottom layer (air)
    # layers_list.append(mc.mclayer.Layer(n=1.0, d=np.inf))
    layers_list.append(mc.mclayer.Layer(n=1.0, d=np.inf, mua=0, mus=0, pf=Hg(0)))

    return mc.mclayer.Layers(layers_list)
