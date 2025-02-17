import numpy as np
from PIL import Image

def read_image(image_path):
    """Reads a 3x3 image and converts to grayscale pixel values."""
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    img = img.resize((3, 3))  # Ensure it's 3x3
    return np.array(img, dtype=np.uint8)


def normalize_ttfs(pixel_values, T_max=30e-6):
    """Convert pixel intensities to TTFS spike times."""
    max_intensity = 255  # Max grayscale value
    return T_max * (1 - (pixel_values / max_intensity))


def generate_pwl_files(spike_times, output_prefix="spikes"):
    """Generate PWL files for LTSpice."""
    # Define mapping of pixels to voltage sources
    pixel_map = {
        "V1": [(0, 0), (0, 1), (0, 2)],  # P1, P2, P3
        "V2": [(1, 0), (1, 1), (1, 2)],  # P4, P5, P6
        "V3": [(2, 0), (2, 1), (2, 2)]   # P7, P8, P9
    }
    for voltage_source, pixel_list in pixel_map.items():
        filename = f"{output_prefix}_{voltage_source}.txt"
        with open(filename, "w") as f:
            d=0
            for (row, col) in pixel_list:
                time = spike_times[row, col]

                f.write(f"{time + d :1.6e} 0.0\n")        # Voltage spike
                f.write(f"{time + 0.1e-6 + d :.6e} 1\n")  # Drop voltage
                f.write(f"{time + 1.9e-6 + d :.6e} 1\n")  # Drop voltage
                f.write(f"{time + 2e-6 + d:.6e} 0.0\n\n") # Restore voltage
                d+=30e-6

        print(f"PWL file saved: {filename}")