import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Disclaimer:
# There are very few sources concerning the details about the energy consumption of glass melting furnaces
# One of the main sources used as a basis for the following values was the following paper:
# https://www.glass-ts.com/site/assets/files/1015/2004_-_a_study_of_the_balance_between_furnace_operating_parameters_and_recycled_glass_in_glass_melting_furnaces.pdf

# Hours per day
HOURS_PER_DAY = 24

# Watts per kilowatt
WATTS_PER_KILOWATT = 1000

# Number of data points in the CSV file
# Unit: Minutes in a day
DATA_POINTS = 1440

# Age of the furnace
# Unit: Years
FURNACE_AGE = 5

# Furnace aging factor
# The year-on-year energy consumption increase of the furnace due to aging, wear and other factors
# Currently modeled as a linear function for simplicity
# Unit: Percentage as a decimal (0 to 1)
AGING_FACTOR = 0.02

# Production quantity of the furnace in one day
# This value can vary significantly, and depends mostly on downstream demand
# There is generally little to no correlation between time of day and production capacity
# There are few sources for production over hours, so average daily production is used instead
# This value is then spread throughout the day evenly, with some variability
# Unit: Tons (t)
PRODUCTION_QUANTITY = 400

# Production variability throughout the day
# This value should be small (<10%), as production does not usually drastically fluctuate
# Unit: Percentage as a decimal (0 to 1)
PRODUCTION_VARIABILITY = 0.03

# Base energy consumption of the furnace in one day
# The energy needed to keep the furnace running without producing any glass throughout the entire day
# Unit: Kilowatt-hour (kWh)
BASE_CONSUMPTION = 10_000

# Base energy variability throughout the day
# This value should be small (<5%), due to the very high thermal inertia of the furnace
# Unit: Percentage as a decimal (0 to 1)
BASE_VARIABILITY = 0.02

# Energy consumption per ton of glass produced
# Unit: Kilowatt-hour per ton (kWh/t)
GLASS_CONSUMPTION = 1100

# Amount of cullet in the raw material
# Unit: Percentage as a decimal (0 to 1)
CULLET_AMOUNT = 0.4

# Energy savings percentage per 1% of cullet
# Unit: Percentage as a decimal (0 to 1)
CULLET_SAVINGS = 0.002

# Map base power throughout the day with variability
np.random.seed(48)
base_power = BASE_CONSUMPTION / HOURS_PER_DAY
base_power_series = np.random.normal(base_power, base_power * BASE_VARIABILITY, DATA_POINTS)

# Map production throughout the day with variability
spread_production = PRODUCTION_QUANTITY / DATA_POINTS
production_series = np.random.normal(spread_production, spread_production * PRODUCTION_VARIABILITY, DATA_POINTS)

# Calculate power consumption
power_consumption = (1 + FURNACE_AGE * AGING_FACTOR) * (
        base_power_series + production_series * GLASS_CONSUMPTION * DATA_POINTS / HOURS_PER_DAY *
        (1 - 100 * CULLET_AMOUNT * CULLET_SAVINGS)) * WATTS_PER_KILOWATT

# Save to CSV
df = pd.DataFrame({"ActivePower": power_consumption})
df.to_csv("melting_furnace.csv", index=False)

# Visualize
target_x = np.linspace(0, HOURS_PER_DAY, num=DATA_POINTS, endpoint=False)
plt.figure(figsize=(12, 5))
plt.plot(target_x, df['ActivePower'])
plt.title("Melting Furnace Power Consumption")
plt.xlabel("Hour of Day")
plt.ylabel("Power Consumption (W)")
plt.grid(True)
plt.tight_layout()
plt.show()

print(f"Melting furnace CSV file generated successfully.")