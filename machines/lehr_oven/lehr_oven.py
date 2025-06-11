import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Disclaimer:
# There are very few sources concerning the details about the energy consumption of lehr annealing ovens
# Most of the sources are non-scientific papers or publications by lehr-making companies or glass institutions

HOURS_PER_DAY = 24

WATTS_PER_KILOWATT = 1000

# Number of data points in the CSV file
# Unit: Minutes in a day
DATA_POINTS = 1440

# Age of the lehr oven
# It is taken into account as the refractory lining gradually wears down due to the intense heat
# Unit: Years
OVEN_AGE = 2

# Oven aging factor
# The year-on-year energy consumption increase of the oven due to aging, wear and other factors
# This value would have to be calculated depending on the specific oven model, and how it is used
# Currently modeled as a linear function, for simplicity
# There are no sources for this value
# Unit: Percentage as a decimal (0 to 1)
AGING_FACTOR = 0.02

# Production quantity of the oven in one day
# This value depends on product demand, and is also limited by the input coming from the forming machine
# There is generally little to no correlation between time of day and production capacity
# Production values are likely similar to those of the furnace, so the same value is used here
# Lehr ovens have a rated maximum capacity, and the production quantity should take that into account
# This value is then spread throughout the day evenly, with some variability
# Unit: Tons (t)
PRODUCTION_QUANTITY = 50

# Production variability throughout the day
# The value is likely similar to that of the furnace, since the oven depends on the furnace output
# Unit: Percentage as a decimal (0 to 1)
PRODUCTION_VARIABILITY = 0.03

# Energy consumption per ton of glass produced
# Typical value ranges from 10 kWh/t of electricity to 25 kWh/t of primary energy
# Source: https://belglas.com/wp-content/uploads/2016/06/energy-consumption-glass-international.pdf
# Values of 14 and 21 kWh calculated from oven consumption in this publication: https://mu.lehrs.be/uncategorized/test/
# Base energy consumption (energy required while idling) is already included in this value
# Unit: Kilowatt-hour per ton (kWh/t)
GLASS_CONSUMPTION = 10

# Map production throughout the day with variability
np.random.seed(48)
spread_production = PRODUCTION_QUANTITY / DATA_POINTS
production_series = np.random.normal(spread_production, spread_production * PRODUCTION_VARIABILITY, DATA_POINTS)

# Calculate power consumption
power_consumption = (1 + OVEN_AGE * AGING_FACTOR) * (
        production_series * GLASS_CONSUMPTION * DATA_POINTS / HOURS_PER_DAY) * WATTS_PER_KILOWATT

# Save to CSV
df = pd.DataFrame({"ActivePower": power_consumption})
df.to_csv("lehr_oven.csv", index=False)

# Visualize
target_x = np.linspace(0, HOURS_PER_DAY, num=DATA_POINTS, endpoint=False)
plt.figure(figsize=(12, 5))
plt.plot(target_x, df['ActivePower'])
plt.title("Lehr Oven Power Consumption")
plt.xlabel("Hour of Day")
plt.ylabel("Power Consumption (W)")
plt.grid(True)
plt.tight_layout()
plt.show()

print(f"Lehr oven CSV file generated successfully.")