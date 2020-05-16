import pandas as pd

class ReadOperations():
    def __init__(self):
        self.simulated_sensor = pd.read_csv("sensor.csv")

    # Simulate obtaining the next reading from a sensor
    # Cycles through the csv entries, never running out of half-dummy data
    def get_next_reading(self):
        sensor = self.simulated_sensor

        # Use this to insert back the first row
        last_row_index = sensor.shape[0]

        # Get first row
        row = sensor.loc[0]

        # Remove first row from dataframe and add it to the last
        sensor = sensor.drop([0])
        sensor.loc[last_row_index] = row
        # Reset index values to start from 0
        sensor = sensor.reset_index(drop=True)

        # Update the class variable
        self.simulated_sensor = sensor

        # Return the values from the read row
        reading = {
            "pm25": row["PM25"],
            "pm10": row["PM10"],
            "temp": row["Temp"],
            "humidity": row["RH"]
        }

        return reading, row
