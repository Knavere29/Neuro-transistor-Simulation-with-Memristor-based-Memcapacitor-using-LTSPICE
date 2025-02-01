import numpy as np
from PIL import Image

# Load image and convert to grayscale (28x28)
import os

print("Current working directory:", os.getcwd())  # Show where Python is looking
print("Files in directory:", os.listdir())  # Show available files
image = Image.open("image.png").convert("L")
image = image.resize((9, 9))  # Ensure correct size
pixels = np.array(image)

# Normalize intensities to TTFS timing (earlier for brighter pixels)
T_max = 10  # Maximum delay in ms
spike_times = T_max * (1 - pixels / 255.0)

# Group pixels into 3 clusters
cluster_1 = np.percentile(spike_times, 33)  # Early spikes (bright)
cluster_2 = np.percentile(spike_times, 66)  # Mid spikes
cluster_3 = np.percentile(spike_times, 100) # Late spikes (dark)

# Average delay for each cluster
V1_delay = np.mean(spike_times[spike_times <= cluster_1])
V2_delay = np.mean(spike_times[(spike_times > cluster_1) & (spike_times <= cluster_2)])
V3_delay = np.mean(spike_times[spike_times > cluster_2])

print(f"Voltage Source Delays: V1={V1_delay}ms, V2={V2_delay}ms, V3={V3_delay}ms")