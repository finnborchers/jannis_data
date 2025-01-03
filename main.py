import pandas as pd
from scipy.ndimage import median_filter
import os
import matplotlib.pyplot as plt

def read_txt_file(file_path):
    # Read the TXT file into a DataFrame
    data = pd.read_csv(
        file_path,
        sep='\t',
        header=None,
        names=["Time", "Ch1", "Ch2", "Ch3", "Ch4", "Ch5", "Ch6", "Ch7", "Ch8"],
        decimal=',',
        comment='#',  # Skip lines starting with #
        on_bad_lines='skip',  # Skip malformed lines
        low_memory=False
    )
    # Convert channel columns to numeric, coercing errors to NaN
    for column in ["Ch1", "Ch2", "Ch3", "Ch4", "Ch5", "Ch6", "Ch7", "Ch8"]:
        data[column] = pd.to_numeric(data[column], errors='coerce')
    return data

def extract_section(data, start_time, end_time):
    # Filter rows based on the Time column
    extracted_data = data[(data["Time"] >= start_time) & (data["Time"] <= end_time)]
    return extracted_data

def calculate_averages(data, channels):
    return {channel: data[channel].mean() for channel in channels}

def calculate_std_dev(data, channels):
    return {channel: data[channel].std() for channel in channels}

def calculate_smoothed(data, channels, window_size=5):
    smoothed = {}
    for channel in channels:
        smoothed_data = median_filter(data[channel].values, size=window_size)
        smoothed[channel] = smoothed_data.mean()
        print(f"\nRaw Data ({channel}):", data[channel].head(10).values)  # Print raw data for inspection
        print(f"Smoothed Data ({channel}):", smoothed_data[:10])          # Print first 10 smoothed values
    return smoothed

def display_stats(label, averages, std_devs, smoothed):
    print(f"\n{label}:")
    for channel in averages.keys():
        print(f"{channel}: Avg={averages[channel]:.2f}, StdDev={std_devs[channel]:.2f}, Smoothed={smoothed[channel]:.2f}")

def save_channel_plots(data, output_dir="channel_plots"):
    os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
    for channel in ["Ch1", "Ch2", "Ch3", "Ch4", "Ch5", "Ch6", "Ch7", "Ch8"]:
        plt.figure(figsize=(10, 6))
        plt.plot(data["Time"], data[channel], label=f"{channel} Data")
        plt.title(f"{channel} Graph")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        # Save plot
        plot_path = os.path.join(output_dir, f"{channel}_graph.png")
        plt.savefig(plot_path)
        plt.close()

# File path to the TXT file
file_path = "your_file_path.txt"  # Replace with the actual path to your file

# Read the TXT file
data = read_txt_file(file_path)

# Define the time range for extraction
start_time = 3.25
end_time = 604.7495

# Extract data for the specified time range
extracted_data = extract_section(data, start_time, end_time)

# Define temperature and perfusion channels
temperature_channels = ["Ch1", "Ch4", "Ch6", "Ch8"]
perfusion_channels = ["Ch2", "Ch3", "Ch5", "Ch7"]

# Calculate statistics for temperature
temperature_averages = calculate_averages(extracted_data, temperature_channels)
temperature_std_devs = calculate_std_dev(extracted_data, temperature_channels)
temperature_smoothed = calculate_smoothed(extracted_data, temperature_channels)

# Calculate statistics for perfusion
perfusion_averages = calculate_averages(extracted_data, perfusion_channels)
perfusion_std_devs = calculate_std_dev(extracted_data, perfusion_channels)
perfusion_smoothed = calculate_smoothed(extracted_data, perfusion_channels)

# Display the statistics
display_stats("Blood Temperature (in °C)", temperature_averages, temperature_std_devs, temperature_smoothed)
display_stats("Blood Perfusion (in Perfusion Units)", perfusion_averages, perfusion_std_devs, perfusion_smoothed)

# Save channel plots
save_channel_plots(extracted_data)