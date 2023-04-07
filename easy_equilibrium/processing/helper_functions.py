import json
from typing import Tuple

import numpy as np
import plotly
import plotly.graph_objects as go


def chemical_equilibrium(pKa: float, pH_range: np.array) -> Tuple[np.array, np.array]:
    # Calculate concentrations of acid and conjugate base as a function of pH
    acid_fractions = []
    base_fractions = []
    for pH in pH_range:
        acid_fraction = 1 / (1 + 10 ** (pH - pKa))
        acid_fractions.append(acid_fraction)
        base_fractions.append(1 - acid_fraction)

        # Return pH and mole fraction arrays
    return acid_fractions, base_fractions


def get_pka_data():
    pka_dict = {
        "H2S": {"HS-": 7,
                "S(2-)": 12},

        "CH3COOH": {"CH3COO-": 4.76},
        "H2CO3": {"HCO3-": 6.35,
                  "CO3(2-)": 10.33},
        "H2SO4": {"HSO4-": -3,
                  "SO4(2-)": 1.99},
        "NH4+": {"NH3": 9.25},

    }
    return pka_dict
