import math

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Disclaimer:
# There are almost no sources concerning energy consumption of batch mixers used in the glass industry
# The only source which contained measured and reliable data is the following link:
# (AUTOMATIC PDF DOWNLOAD) https://cn.glassglobal.com/directory/glass/profile/documents/file.asp?AdrID=7953&ID=1614

HOURS_PER_DAY = 24

WATTS_PER_KILOWATT = 1000

NUMBER_OF_MACHINES = 2

# Number of data points in the CSV file
# Unit: Minutes in a day
DATA_POINTS = 1440

# Variability of the data (to simulate realistic conditions)
# Unit: Percentage as a decimal (0 to 1)
VARIABILITY = 0.03

# Time it takes to mix the raw materials in minutes
# Unit: Minutes
MIXING_TIME = 3

# Time it takes to transfer raw materials to and from the mixer in minutes
# Unit: Minutes
TRANSFER_TIME = 2

# Mixer power draw per ton of raw material mixed
# This value was obtained as a middle point from the values present in the document at the beginning
# It states a consumption value of 1 kW/100 kg or 2 kW/ 100 kg depending on mixer type
# The mixers depicted seem significantly smaller than the ones required to process 100 tons per day
# Therefore, a higher power value was chosen
# Unit: Kilowatt per ton (kW/t)
MIXER_POWER = 30

# Amount of glass produced in one day
# This value should match the value produced by the furnace, as one mixer generally feeds one furnace
# Unit: Tons (t)
PRODUCTION_QUANTITY = 100

# Raw material yield
# Represents the amount of raw material that is converted into molten glass
# The remaining percentage is lost in the melting process and escapes mostly as gas
PRODUCTION_YIELD = 0.85

# Calculate production duration
cycle_time = MIXING_TIME + TRANSFER_TIME
mixing_percentage = MIXING_TIME / cycle_time
production_duration = mixing_percentage * DATA_POINTS

# Calculate batch size
material_amount = PRODUCTION_QUANTITY / PRODUCTION_YIELD
batch_size = MIXING_TIME * material_amount / production_duration

def generate_data(machine_number):
    # Create a production segment
    if machine_number % 2 == 0:
        production_segment = [batch_size] * MIXING_TIME
        production_segment.extend([0] * TRANSFER_TIME)
    else:
        production_segment = [0.0] * TRANSFER_TIME
        production_segment.extend([batch_size] * MIXING_TIME)

    # Create the production time series
    production_repetition = math.ceil(DATA_POINTS / cycle_time)
    production_series = np.tile(production_segment, production_repetition)
    production_series = production_series[:DATA_POINTS]

    # Calculate power consumption
    power_consumption = production_series * MIXER_POWER * WATTS_PER_KILOWATT

    # Introduce variability to power consumption
    np.random.seed(48 + machine_number)
    variable_power_consumption = np.round(
        np.random.normal(power_consumption, power_consumption * VARIABILITY)).astype(int)

    # Save to CSV
    df = pd.DataFrame({"ActivePower": variable_power_consumption})
    df.to_csv(f"batch_mixer{machine_number}.csv", index=False)

    # Visualize
    target_x = np.linspace(0, HOURS_PER_DAY, num=DATA_POINTS, endpoint=False)
    plt.figure(figsize=(12, 5))
    plt.plot(target_x, df['ActivePower'])
    plt.title(f"Batch Mixer {machine_number} Power Consumption")
    plt.xlabel("Hour of Day")
    plt.ylabel("Power Consumption (W)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    print(f"Batch mixer {machine_number} CSV file generated successfully.")

for i in range(NUMBER_OF_MACHINES):
    generate_data(i)
