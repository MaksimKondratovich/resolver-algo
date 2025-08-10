import numpy as np
from dataclasses import dataclass, field
from typing import Dict, Any

	
@dataclass
class InputSignalData:
    SIN: np.ndarray
    COS: np.ndarray
    t: np.ndarray
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        # Convert arrays to float64
        self.SIN = np.asarray(self.SIN, dtype=np.float64)
        self.COS = np.asarray(self.COS, dtype=np.float64)
        self.t = np.asarray(self.t, dtype=np.float64)

        # Mandatory fields
        mandatory_fields = [
            "reference_frequency",   # Hz
            "reference_amplitude",   # V
            "sample_rate",           # S/s
            "signal_time_length",    # s
            "revolving_manner",      # "arbitrary" or "non_arbitrary"
            "revolving_frequency"    # Hz (only if manner == non_arbitrary)
        ]
        missing = [f for f in mandatory_fields if f not in self.metadata]
        if missing:
            raise ValueError(f"Missing mandatory metadata fields: {missing}")

        # Validate fields
        self._validate_metadata()

    def _validate_metadata(self):
        m = self.metadata

        # Reference frequency: 50 Hz – 50 kHz
        if not (50 <= m["reference_frequency"] <= 50_000):
            raise ValueError("Reference frequency must be between 50 Hz and 50 kHz.")

        # Reference amplitude: 0.1 V – 110 V
        if not (0.1 <= m["reference_amplitude"] <= 110):
            raise ValueError("Reference amplitude must be between 0.1 V and 110 V.")

        # Sample rate: 100 S/s – 1 MS/s
        if not (100 <= m["sample_rate"] <= 1_000_000):
            raise ValueError("Sample rate must be between 100 S/s and 1 MS/s.")

        # Signal time length: 100 µs – 100 s
        if not (1e-4 <= m["signal_time_length"] <= 100):
            raise ValueError("Signal time length must be between 100 µs and 100 s.")

        # Revolving manner: "arbitrary" or "non-arbitrary"
        if m["revolving_manner"] not in ("arbitrary", "non_arbitrary"):
            raise ValueError('Revolving manner must be "arbitrary" or "non-arbitrary".')

        # Revolving frequency check only if manner is "non-arbitrary"
        if m["revolving_manner"] == "non_arbitrary":
            if not (0 <= m["reference_frequency"] <= 25_000):
                raise ValueError("Revolving frequency must be between 0 Hz and 25 kHz for non-arbitrary manner.")

    def add_metadata(self, key: str, value: Any):
        self.metadata[key] = value
        # If updating a mandatory field, re-validate
        self._validate_metadata()

    def get_metadata(self, key: str, default=None):
        return self.metadata.get(key, default)
