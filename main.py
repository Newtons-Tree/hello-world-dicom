"""Example script."""

import sys
from datetime import datetime
from pathlib import Path

import pydicom
import torch
from pydicom.dataset import FileDataset


def log_gpu_info() -> None:
    """Log simple CUDA debugging information."""
    if torch.cuda.is_available():
        print(f"CUDA is available. {torch.cuda.device_count()} GPU(s) found.")
    else:
        print("CUDA is not available. Running on CPU.")


def touch_dicom(input_dir: str, output_dir: str) -> None:
    """Add a DICOM tag for demonstration purposes.

    Args:
        input_dir (str): path to input
        output_dir (str): path to output

    """
    # Create the output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    print(f"Loading files in {input_dir}:")
    # For each file in the input directory
    for file_path in Path(input_dir).iterdir():
        # Skip non-DICOM files, and subdirectories
        if not file_path.name.lower().endswith(".dcm"):
            print(f"Skipping {file_path}")
            continue

        # Load the DICOM file
        ds: FileDataset = pydicom.dcmread(str(file_path))

        # Update image comments tag
        ds.ImageComments = "Touched by AI"

        # Update the ContentDate/ContentTime
        dt = datetime.now()
        ds.ContentDate = dt.strftime("%Y%m%d")
        ds.ContentTime = dt.strftime("%H%M%S.%f")

        # Save the updated DICOM file
        out_path = Path(output_dir) / file_path.name
        ds.save_as(str(out_path))
        print(f"Processed: {file_path.name}")


# Main function
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_dir> <output_dir>")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    log_gpu_info()
    touch_dicom(input_dir, output_dir)
