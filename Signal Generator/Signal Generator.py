import argparse, sys
import numpy as np
from InputSignalData import InputSignalData # type: ignore
from pathlib import Path
from datetime import datetime
import os

#Input arguments parser
def parse_args():
    parser = argparse.ArgumentParser(description="Parse signal parameters.")

    # Mandatory arguments
    parser.add_argument('--reference_frequency', type=float, required=True,
                        help='Reference frequency in Hz')
    parser.add_argument('--reference_amplitude', type=float, required=True,
                        help='Reference amplitude in Volts')
    parser.add_argument('--sample_rate', type=float, required=True,
                        help='Sample rate in Samples per second (S/s)')
    parser.add_argument('--signal_time_length', type=float, required=True,
                        help='Signal time length in seconds')
    parser.add_argument('--revolving_manner', type=str, required=True, choices=['arbitrary', 'non_arbitrary'],
                        help='Revolving manner: "arbitrary" or "non-arbitrary"')

    # Revolving frequency only required if manner == 'non_arbitrary'
    parser.add_argument('--revolving_frequency', type=float,
                        help='Revolving frequency in Hz (required if manner is non-arbitrary)')
    
    args, unknown = parser.parse_known_args()
    
    if unknown:
        print("Warning: Unknown arguments detected:", file=sys.stderr)
        for arg in unknown:
            print(f"  {arg}", file=sys.stderr)

    # Enforce conditional required argument
    if args.revolving_manner == 'non_arbitrary' and args.revolving_frequency is None:
        parser.error("--revolving_frequency is required when --revolving-manner is 'non_arbitrary'")

    return args 

args = parse_args()

# Example data
t = np.linspace(0, 1, 1000)
sin_values = np.sin(2 * np.pi * 100 * t)
cos_values = np.cos(2 * np.pi * 100 * t)

signal = InputSignalData(
    SIN=sin_values,
    COS=cos_values,
    t=t,
    metadata=dict(vars(args))
)

# Get current date/time as a string
timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

# Build filename with timestamp
filename = f"/InSig_{timestamp}.npz"

file_save_path = Path(__file__).parent.parent / 'Resources' / 'Input Signal Files'

np.savez(str(file_save_path)+filename,
         arr1=signal.SIN,
         arr2=signal.COS,
         arr3=signal.t)
         #metadata=np.array([str(signal.metadata)]))  # Save as string
