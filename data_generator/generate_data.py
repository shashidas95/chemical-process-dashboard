import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# --- Configuration ---
NUM_DATA_POINTS = 5000  # Number of historical data points to generate
OUTPUT_FILE = '../data/process_data.csv' # Output CSV file relative to project root
PROCESS_PARAMS = {
    "Temperature": {"mean": 150, "std": 5, "anomaly_range": (165, 175), "unit": "°C"},
    "Pressure": {"mean": 5, "std": 0.5, "anomaly_range": (6.5, 7.5), "unit": "Bar"},
    "Flow_Rate": {"mean": 100, "std": 10, "anomaly_range": (125, 135), "unit": "L/min"},
    "pH_Value": {"mean": 7.0, "std": 0.2, "anomaly_range": (5.0, 6.0), "unit": ""},
    "Concentration": {"mean": 0.15, "std": 0.01, "anomaly_range": (0.20, 0.22), "unit": "mol/L"}
}
ANOMALY_FREQUENCY = 0.02 # 2% chance of an anomaly per data point for a given parameter
TIME_INTERVAL_SECONDS = 5 # Data point every 5 seconds

# --- Data Generation Logic ---
def generate_process_data(num_points, params, anomaly_freq, time_interval):
    data = []
    start_time = datetime.now() - timedelta(seconds=num_points * time_interval)

    for i in range(num_points):
        current_time = start_time + timedelta(seconds=i * time_interval)
        row = {"timestamp": current_time.isoformat(timespec='milliseconds') + 'Z'} 
        for param_name, config in params.items():
            mean = config["mean"]
            std = config["std"]
            anomaly_range = config["anomaly_range"]

            value = np.random.normal(mean, std)

            # Introduce anomalies sporadically
            if np.random.rand() < anomaly_freq:
                # Generate anomaly within defined range
                value = np.random.uniform(anomaly_range[0], anomaly_range[1])
                # Ensure anomaly is clearly outside normal range
                if value < mean - 3 * std or value > mean + 3 * std:
                    pass # Keep the generated anomaly
                else:
                    value = np.random.normal(mean, std) # Revert if not sufficiently anomalous
            row[param_name] = round(value, 3) # Round for cleaner data

        data.append(row)

    df = pd.DataFrame(data)
    # Ensure timestamp is the first column and correctly formatted
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df[['timestamp'] + [col for col in df.columns if col != 'timestamp']]
    return df

# --- Main Execution ---
if __name__ == "__main__":
    print("Generating simulated chemical process data...")

    # Create the data directory if it doesn't exist
    output_dir = os.path.dirname(OUTPUT_FILE)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    df = generate_process_data(NUM_DATA_POINTS, PROCESS_PARAMS, ANOMALY_FREQUENCY, TIME_INTERVAL_SECONDS)

    # Save to CSV
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Data generation complete. {len(df)} data points saved to {OUTPUT_FILE}")
    print("\nFirst 5 rows of generated data:")
    print(df.head())
    print(f"\nLast 5 rows of generated data:")
    print(df.tail())