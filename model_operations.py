import pickle
from datetime import datetime, timedelta
import numpy as np

class ModelOperations:
    def __init__(self):
        # Load the pretrained model
        self.model = pickle.load(open("model.sav", "rb"))

    # Divides the past entries into 4 equally time-spaced bucket
    # Returns mean of each bucket
    @staticmethod
    def get_division_means(entries, past_time_limit):

        time_format = "%d-%m-%Y %H:%M:%S"

        # Divide the past data into 4 equally time spaced buckets
        time_window = past_time_limit / 4
        # 4 equally time spaced buckets
        timeshift_1, timeshift_2, timeshift_3, timeshift_4 = [], [], [], []

        # Datetime objects for marking breakpoints for all buckets
        now = datetime.now()
        now_minus_15 = now - timedelta(minutes=time_window)
        now_minus_30 = now - timedelta(minutes=2 * time_window)
        now_minus_45 = now - timedelta(minutes=3 * time_window)
        now_minus_60 = now - timedelta(minutes=4 * time_window)

        for entry in entries:
            # entry is of the form (key, {time, value})
            data = entry[1]

            # datetime object representing the time of entry
            entry_time_string = data["time"]
            entry_time = datetime.strptime(entry_time_string, time_format)

            entry_value = data["value"]

            # Segregate entry values into buckets
            if (entry_time > now_minus_15):
                timeshift_1.append(entry_value)
            elif (entry_time > now_minus_30):
                timeshift_2.append(entry_value)
            elif (entry_time > now_minus_45):
                timeshift_3.append(entry_value)
            elif (entry_time > now_minus_60):
                timeshift_4.append(entry_value)
            else:
                continue

        # Obtain mean of each bucket
        mean_ts1 = sum(timeshift_1) / len(timeshift_1)
        mean_ts2 = sum(timeshift_2) / len(
            timeshift_2) if timeshift_2 else mean_ts1
        mean_ts3 = sum(timeshift_3) / len(
            timeshift_3) if timeshift_3 else mean_ts2
        mean_ts4 = sum(timeshift_4) / len(
            timeshift_4) if timeshift_4 else mean_ts3

        division_means = {
            "1": mean_ts1,
            "2": mean_ts2,
            "3": mean_ts3,
            "4": mean_ts4
        }
        return division_means

    # Preprocesses the past data stored in firebase
    # Returns a properly formatted array as input for model prediction
    def pre_process(self, past_data, past_time_limit):

        # datetime object representing the time details that is ultimately passed to the model prediction
        # Month, Hour, and minute is passed to the model as these are relevant parameters to calculate
        # pollution during a given time in the day
        now = datetime.now()

        preprocessed = {}
        for attribute, value_dict in past_data.items():
            preprocessed[attribute] = self.get_division_means(
                value_dict.items(), past_time_limit)

        # Means of 4 equally time spaced buckets for every attribute
        pm25, pm10, temp, humidity = preprocessed["pm25"], preprocessed[
            "pm10"], preprocessed["temp"], preprocessed["humidity"]

        # Build final model input
        model_input = np.array([[
            now.month, now.hour, now.minute, pm25["1"], pm10["1"], temp["1"],
            humidity["1"], pm25["2"], pm10["2"], temp["2"], humidity["2"],
            pm25["3"], pm10["3"], temp["3"], humidity["3"], pm25["4"],
            pm10["4"], temp["4"], humidity["4"]
        ]])
        return model_input

    # Predicts the concentration of PM 2.5 and PM 10 particles 15 mins in the future
    def predict(self, model_input):
        result = self.model.predict(model_input)
        return result
