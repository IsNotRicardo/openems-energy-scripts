import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

# Number of data points in the CSV file
# Unit: Minutes in a day
DATA_POINTS = 1440

# Variability of the data (to simulate realistic conditions)
# Unit: Percentage as a decimal (0 to 1)
VARIABILITY = 0.05

# Power value of a single solar panel
# Commercial solar panel power ranges from 250 to 600 Watts
# Source: https://www.solarnplus.com/how-much-energy-can-a-commercial-solar-panel-produce-for-your-business/
# Unit: Watts (W)
PANEL_POWER = 400

# Standard Test Condition (STC) Irradiance
# This value is a constant and equates to an irradiance of 1000 W/m² under certain conditions
# Source: https://sinovoltaics.com/learning-center/quality/standard-test-conditions-stc-definition-and-problems
# Unit: Watts per square meter (W/m²)
STANDARD_IRRADIANCE = 1000

# Hourly Global Tilted Irradiance (GTI)
# An array of hourly irradiance values, which depend on multiple factors
# Source: https://re.jrc.ec.europa.eu/pvg_tools/en/#MR
# The values were obtained as average daily with the following parameters:
# - Location: Helsinki, Finland
# - Solar radiation database: PVGIS-SARAH3
# - Month: May
# - Slope/Tilt: 49°
# - Azimuth: 0° (South)
# Unit: Watts per square meter (W/m²)
# Values start at 0:00 and end at 23:00 local time
HOURLY_GTI = np.array([
    0.0, 0.0, 0.0, 0.0, 1.69, 19.98, 55.87, 180.09, 341.57, 489.86, 632.75, 721.39,
    741.11, 722.58, 647.72, 527.44, 384.08, 239.04, 97.32, 37.89, 9.11, 0.0, 0.0, 0.0
])

# Performance Ratio
# An overall metric of how efficient the solar system is after accounting for real-world energy losses
# The performance ratio likely ranges between 70-90% and cannot realistically reach 100%
# Source: https://solex.in/blogs/what-is-a-good-performance-ratio-for-solar
# This value accounts for the following (non-extensive) situations:
# - Energy loss due to high temperatures
# - Energy loss from the inverter
# - Energy loss through wiring
# - Energy loss due to shading
# - Degradation of the components
# Unit: Percentage as a decimal (0 to 1)
PERFORMANCE_RATIO = 0.8

# Perform PCHIP interpolation on GTI data to reach the resolution given by DATA_POINTS
# PCHIP interpolation is used since the data follows a bell curve, and it provides more accurate values
original_x = np.linspace(0, 24, num=len(HOURLY_GTI), endpoint=False)
target_x = np.linspace(0, 24, num=DATA_POINTS, endpoint=False)
pchip = PchipInterpolator(original_x, HOURLY_GTI)
interpolated_gti = pchip(target_x)

# Add variability to the data
np.random.seed(48)
noise = np.random.normal(0, interpolated_gti * VARIABILITY)
variable_gti = np.maximum(interpolated_gti + noise, 0)

# Calculate power production
power_production = PANEL_POWER * (variable_gti / STANDARD_IRRADIANCE) * PERFORMANCE_RATIO

# Save to CSV
df = pd.DataFrame({"ActivePower": power_production})
df.to_csv("solar_panel.csv", index=False)

# Visualize
plt.figure(figsize=(12, 5))
plt.plot(target_x, df['ActivePower'])
plt.title("Solar Panel Power Production")
plt.xlabel("Hour of Day")
plt.ylabel("Power Production (W)")
plt.grid(True)
plt.tight_layout()
plt.show()

print(f"Solar panel CSV file generated successfully.")
