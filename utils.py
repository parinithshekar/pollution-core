from datetime import datetime, timedelta
import json

class TimeUtils():

    # Method to identify entries older than the allowed time_limit
    # Return True if the entry should be discarded
    @staticmethod
    def older_entries(entry, past_time_limit):

        # If there a faulty entry in Firebase
        try:
            assert ("time" in entry)
        except Exception:
            return True

        time_format = "%d-%m-%Y %H:%M:%S"

        # datetime object for entry time
        entry_time_string = entry["time"]
        entry_time = datetime.strptime(entry_time_string, time_format)

        # datetime object for specified minutes in the past
        now = datetime.now()
        threshold_time = now - timedelta(minutes=past_time_limit)

        if (entry_time < threshold_time):
            # Entry is older than threshold
            return True
        else:
            # Entry is within threshold
            return False


class AQIUtils():

    # Calculate AQI according to the breakpoints specifid in the table
    @staticmethod
    def calculate_aqi(pm_value, table):
        aqi = 0

        # Assign the pm_value to a category based on the concentration breakpoints
        category = [
            level for level in table.items()
            if (pm_value >= level[1]["conc"]["low"]
                and pm_value <= level[1]["conc"]["high"])
        ]

        try:
            # If the pm_value belongs to more than one category,
            # there is a faulty overlap in the table.json file
            assert (len(category) == 1)
        except AssertionError:
            print(
                "Error deciding the pollution category. Ensure breakpoints do not overlap in table.json"
            )
            return aqi

        # Get breakpoint values for identified category
        category_values = category[0][1]
        conc_low = category_values["conc"]["low"]
        conc_high = category_values["conc"]["high"]
        aqi_low = category_values["aqi"]["low"]
        aqi_high = category_values["aqi"]["high"]

        # Calculate AQI according breakpoints
        aqi = (aqi_high - aqi_low) / (conc_high - conc_low)
        aqi = aqi * (pm_value - conc_low)
        aqi = aqi + aqi_low
        return aqi

    @staticmethod
    def get_aqi(pm25, pm10):
        with open("table.json") as file:
            table = json.load(file)
        aqi25 = AQIUtils.calculate_aqi(pm25, table["pm25"])
        aqi10 = AQIUtils.calculate_aqi(pm10, table["pm10"])

        # AQI is calculated as the max of the individual AQIs due to all types of particles
        final_aqi = max(aqi25, aqi10)
        # AQI must always be an integer
        return round(final_aqi)
