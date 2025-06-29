import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Disclaimer:
# There are nearly no sources concerning the energy consumption of glass forehearths
# The only source which contains some data is a PDF with some energy consumption values:
# https://glassmanevents.com/content-images/main/2-Electroglass.pdf
# The values also include the pull rate and the temperature drop, which are taken into account
# The formula used below is likely unreliable due to how little data is available

HOURS_PER_DAY = 24

WATTS_PER_KILOWATT = 1000

NUMBER_OF_MACHINES = 4

# Number of data points in the CSV file
# Unit: Minutes in a day
DATA_POINTS = 1440

# Age of the forehearth
# It is taken into account as the refractory lining gradually wears down due to the intense heat
# Unit: Years
FOREHEARTH_AGE = 2

# Forehearth aging factor
# The year-on-year energy consumption increase of the forehearth due to aging, wear and other factors
# This value would have to be calculated depending on the specific forehearth system, and how it is used
# Currently modeled as a linear function, for simplicity
# There are no sources for this value
# Unit: Percentage as a decimal (0 to 1)
AGING_FACTOR = 0.02

# Production quantity of the forehearth in one day
# This value depends on product demand and on the furnace output
# In most factories, production from the furnace is split across multiple forehearths
# Therefore, production values are likely a fraction than those of the furnace
# This value is then spread throughout the day evenly, with some variability
# Unit: Tons (t)
PRODUCTION_QUANTITY = 50

# Production variability throughout the day
# The value is likely similar to that of the furnace, since the forehearth depends on the furnace output
# The forehearth needs to feed the forming machine, which requires constant output while handling the variable input
# Unit: Percentage as a decimal (0 to 1)
PRODUCTION_VARIABILITY = 0.03

# Energy consumption per ton of glass produced per degree Celsius
# Estimations for these values were calculated from the four situations present in the PDF at the beginning
# Values for all-electric forehearths range from 0.057 to 0.347 kWh/t/°C with an average of 0.256
# Values for gas-heated forehearths range from 1.499 to 3.585 kWh/t/°C with an average of 2.074
# Base energy consumption (energy required while idling) is already included in this value
# Unit: Kilowatt-hour per ton per degree Celsius (kWh/t/°C)
GLASS_CONSUMPTION = 0.25

# Temperature drop done in the forehearth
# How much the temperature is reduced in the forehearth to achieve the desired temperature/viscosity
# Unit: Degrees Celsius (°C)
TEMPERATURE_DROP = 50

def generate_data(machine_number):
    # Map production throughout the day with variability
    np.random.seed(48 + machine_number)
    spread_production = PRODUCTION_QUANTITY / DATA_POINTS
    production_series = np.random.normal(spread_production, spread_production * PRODUCTION_VARIABILITY, DATA_POINTS)

    # Calculate power consumption
    power_consumption = np.round((1 + FOREHEARTH_AGE * AGING_FACTOR) * WATTS_PER_KILOWATT * (
            production_series * GLASS_CONSUMPTION * TEMPERATURE_DROP * DATA_POINTS / HOURS_PER_DAY)).astype(int)

    # Save to CSV
    df = pd.DataFrame({"ActivePower": power_consumption})
    df.to_csv(f"forehearth{machine_number}.csv", index=False)

    # Visualize
    target_x = np.linspace(0, HOURS_PER_DAY, num=DATA_POINTS, endpoint=False)
    plt.figure(figsize=(12, 5))
    plt.plot(target_x, df['ActivePower'])
    plt.title(f"Forehearth {machine_number} Power Consumption")
    plt.xlabel("Hour of Day")
    plt.ylabel("Power Consumption (W)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    print(f"Forehearth {machine_number} CSV file generated successfully.")

for i in range(NUMBER_OF_MACHINES):
    generate_data(i)
