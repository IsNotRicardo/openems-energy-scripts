import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Disclaimer:
# There are very few sources concerning the energy consumption of glass forming machines
# Only a single source was found containing an energy value per quantity, which is mentioned later
# Additionally, the following source also states that forming accounts for 10.3% of the total energy
# consumption and 43.1% of the total electricity consumption:
# https://openjicareport.jica.go.jp/pdf/11187481_04.pdf

HOURS_PER_DAY = 24

WATTS_PER_KILOWATT = 1000

NUMBER_OF_MACHINES = 4

# Number of data points in the CSV file
# Unit: Minutes in a day
DATA_POINTS = 1440

# Increase in energy consumption of the machine due to a fault
# Unit: Percentage as a decimal (>0)
FAULT_EXCESS = 0.2

# Production quantity of the forming machine in a day
# This value depends on demand and on the number of forming machines that are used
# Unit: Tons (t)
PRODUCTION_QUANTITY = 50

# Production variability of the data (to simulate realistic conditions)
# Unit: Percentage as a decimal (0 to 1)
PRODUCTION_VARIABILITY = 0.01

# Energy consumption per ton of glass produced
# Two sources were found, which contained energy-related consumption values
# The following source only contained a power value with no reference to quantity or time:
# https://www.sklostroj.cz/files/attachments/leaflet-is-machines-iss.pdf
# The following source contained a value of 278.8 BTU/pound, which corresponds to around 160 kWh/t:
# https://www.aceee.org/files/proceedings/1999/data/papers/SS99_Panel1_Paper56.pdf
# The latter value was used because it aligns better with the percentages stated at the beginning
# Unit: Kilowatt-hour per ton (kWh/t)
GLASS_CONSUMPTION = 160

def generate_data(machine_number, is_faulty):
    # Map production throughout the day with variability
    np.random.seed(48 + machine_number)
    spread_production = PRODUCTION_QUANTITY / DATA_POINTS
    production_series = np.random.normal(spread_production, spread_production * PRODUCTION_VARIABILITY, DATA_POINTS)

    # Calculate power consumption
    power_consumption = (production_series * GLASS_CONSUMPTION * DATA_POINTS / HOURS_PER_DAY) * WATTS_PER_KILOWATT

    if is_faulty:
        power_consumption *= 1 + FAULT_EXCESS

    power_consumption = np.round(power_consumption).astype(int)

    # Save to CSV
    df = pd.DataFrame({"ActivePower": power_consumption})
    df.to_csv(f"forming_machine{machine_number}{'_faulty' if is_faulty else ''}.csv", index=False)

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

i = 0

for i in range(NUMBER_OF_MACHINES):
    generate_data(i, False)

generate_data(i + 1, True)
