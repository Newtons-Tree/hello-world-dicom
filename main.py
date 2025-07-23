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


def process_dicom(input_dir: str, output_dir: str) -> None:
    """Add a DICOM tag for demonstration purposes.

    Args:
        input_dir (str): path to input
        output_dir (str): path to output

    """
    # Create the output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    print(f"Loading files in {input_dir} recursively:")
    p = Path(input_dir)

    # Recursively find .dcm files
    for dcm_file in p.glob("**/**.dcm"):
        print(f"Processing {dcm_file.name}")
        # Load the DICOM file
        ds: FileDataset = pydicom.dcmread(str(dcm_file))

        # Update image comments tag
        ds.ImageComments = "Touched by AI"

        # Update the ContentDate/ContentTime
        dt = datetime.now()
        ds.ContentDate = dt.strftime("%Y%m%d")
        ds.ContentTime = dt.strftime("%H%M%S.%f")

        # Save the updated DICOM file
        # Note this will not respect original subfolder hierarchy, if present
        # Note this will not respect duplicate file names, if present
        out_path = Path(output_dir) / dcm_file.name
        ds.save_as(str(out_path))


# Main function
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_dir> <output_dir>")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    log_gpu_info()
    process_dicom(input_dir, output_dir)
