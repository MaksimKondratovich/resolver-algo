import numpy as np
from InputSignalData import InputSignalData # type: ignore

# Example data
t = np.linspace(0, 1, 1000)
sin_values = np.sin(2 * np.pi * 100 * t)
cos_values = np.cos(2 * np.pi * 100 * t)

signal = InputSignalData(
    SIN=sin_values,
    COS=cos_values,
    t=t,
    metadata={
        "Reference frequency": 100.0,     # Hz
        "Reference amplitude": 1.0,       # V
        "Sample rate": 10000,              # S/s
        "Signal time length": 1.0,         # s
        "Revolving manner": "non-arbitrary",
        "Revolving frequency": 500.0,      # Hz
        "operator": "Alice"                # extra metadata
    }
)

print(signal.get_metadata("Reference frequency"))  # 100.0
print(signal)
