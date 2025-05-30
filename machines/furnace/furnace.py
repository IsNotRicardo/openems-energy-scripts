import pandas as pd
import numpy as np

# Set the number of data points (minutes in a day)
num_minutes = 1440

# Base energy consumption (arbitrary units, representing high continuous consumption)
# Let's say, an average of 1000 units per minute. This is just for demonstration.
# In reality, this could be in kWh or MWh depending on the furnace size.
base_consumption = 1000

# Generate energy consumption data
# Add some small random noise to simulate fluctuations
# The noise standard deviation is set to be a small percentage of the base consumption
np.random.seed(42) # for reproducibility
energy_consumption = base_consumption + np.random.normal(0, base_consumption * 0.01, num_minutes)

# Ensure no negative energy consumption values (though highly unlikely with this setup)
energy_consumption[energy_consumption < 0] = 0

# Create a DataFrame
df = pd.DataFrame(energy_consumption, columns=['Energy_Consumption'])

# Generate the CSV file
df.to_csv('glass_furnace_energy_consumption.csv', index=False)

print("CSV file 'glass_furnace_energy_consumption.csv' generated successfully with 1440 data points.")