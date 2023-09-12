"""Common util calculations"""

import numpy as np

def custom_floor(x: float, precision: float = 0) -> float:
    return np.round(precision * np.floor(np.round(x / precision, 2)), 2)