import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Disclaimer:
# There are virtually no sources concerning the energy consumption of glass forming machines
# A single source was found which included one power value, and this source is used as a basis for the data
# Source: https://www.sklostroj.cz/files/attachments/leaflet-is-machines-iss.pdf
# Due to the lack of data, no formula can be created to more accurately represent the energy consumption

HOURS_PER_DAY = 24

WATTS_PER_KILOWATT = 1000

NUMBER_OF_MACHINES = 4

# Number of data points in the CSV file
# Unit: Minutes in a day
DATA_POINTS = 1440

# Variability of the data (to simulate realistic conditions)
# Unit: Percentage as a decimal (0 to 1)
VARIABILITY = 0.005

# Power output
# The power output of the machine while operating
# Unit: Kilowatt (kW)
POWER_OUTPUT = 20

def generate_data(machine_number):
    # Setup values
    power_watts = POWER_OUTPUT * WATTS_PER_KILOWATT
    np.random.seed(48 + machine_number)

    # Calculate power consumption
    power_consumption = np.random.normal(power_watts, power_watts * VARIABILITY, DATA_POINTS)

    # Save to CSV
    df = pd.DataFrame({"ActivePower": power_consumption})
    df.to_csv(f"forming_machine{machine_number}.csv", index=False)

    # Visualize
    target_x = np.linspace(0, HOURS_PER_DAY, num=DATA_POINTS, endpoint=False)
    plt.figure(figsize=(12, 5))
    plt.plot(target_x, df['ActivePower'])
    plt.title(f"Forming Machine {machine_number} Power Consumption")
    plt.xlabel("Hour of Day")
    plt.ylabel("Power Consumption (W)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    print(f"Forming machine {machine_number} CSV file generated successfully.")

for i in range(NUMBER_OF_MACHINES):
    generate_data(i)
