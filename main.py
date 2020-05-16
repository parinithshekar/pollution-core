import time
import numpy as np
from datetime import datetime, timedelta

# Firebase imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Custom imports
import utils
import model_operations
import read_operations

# Authenticate Firebase
cred = credentials.Certificate("./serviceAccountKey.json")
# Initialize firebase with project URL
firebase_admin.initialize_app(
    cred, {'databaseURL': 'https://pollution-pkdoesml.firebaseio.com'})

# Time threshold to save old entries (in minutes)
# Recommended: 60 minutes
past_time_limit = 4
predicted_time_limit = 4


# Updates realtime storage on firebase
# Deletes values that are older than time threshold specified
# Adds new values specified in the arguments with the timestamp
def update_firebase(root_path, sub_paths, values, entry_time, time_threshold):
    # root_path is either "/past" or "/predicted"
    root_name = root_path.lstrip('/').upper()
    print(f"📝 {root_name} WRITE STARTED\n...")

    root_ref = db.reference(root_path)
    root_result = root_ref.get()

    # payload to give update information to firebase
    updated_root = {}

    for (path, value) in zip(sub_paths, values):
        # Get path for one of (temp, humidity, pm25, pm10, aqi)
        path_ref = db.reference(f"{root_path}/{path}")

        # Records of current path
        path_result = root_result[path]
        path_result_list = list(path_result.items())

        # If number of entries in firebase exceeds the time threshold (only entries in past 1 hour)
        # Remove the oldest entries (remove entries older than 1 hour ago)
        older_than_limit = list(
            filter(
                lambda entry: utils.TimeUtils.older_entries(
                    entry[1], time_threshold), path_result_list))

        if (older_than_limit):
            keys_to_remove = [entry[0] for entry in older_than_limit]
            for delete_key in keys_to_remove:
                # Setting value to None in update_payload removes the key
                updated_root[f"{path}/{delete_key}"] = None

        # Generate key for new value entry
        push_key = path_ref.push().key

        # Input new value in update_payload
        updated_root[f"{path}/{push_key}"] = {
            "time": entry_time,
            "value": int(value)
        }

    # Update firebase with the update_payload
    root_ref.update(updated_root)

    print(f"✅ {root_name} WRITE SUCCESS")
    print(f"🕓 {datetime.now()}")
    print("\n")


if __name__ == "__main__":

    model_ops = model_operations.ModelOperations()
    sensor = read_operations.ReadOperations()

    while True:
        # store timestamps for now and 15 mins in future
        now = datetime.now()
        now_plus_15 = now + timedelta(minutes=15)

        # Format timestamp to standard
        now = now.strftime("%d-%m-%Y %H:%M:%S")
        now_plus_15 = now_plus_15.strftime("%d-%m-%Y %H:%M:%S")

        # Read values from the sensor
        # NOTE As we are reading from CSV, we can return the row and consider it
        # as a preprocessed input to the model
        reading, row = sensor.get_next_reading()

        # NOTE only for simulation
        # make row as pre processed model input
        csv_pre_processed_model_input = np.array(
            row.drop(["PM25", "PM10", "Temp", "RH"]))
        csv_pre_processed_model_input = csv_pre_processed_model_input.reshape(
            1, -1)

        # Find AQI from formula
        current_aqi = utils.AQIUtils.get_aqi(reading["pm25"], reading["pm10"])

        past_to_update = ['temp', 'humidity', 'pm25', 'pm10', 'aqi']
        past_values = [
            reading["temp"], reading["humidity"], reading["pm25"],
            reading["pm10"], current_aqi
        ]

        # Write currently read values to firebase
        update_firebase('/past', past_to_update, past_values, now,
                        past_time_limit)
        """ SENSOR DATA WRITE TO FIREBASE DONE """

        # Get past data
        past_ref = db.reference("/past")
        past_result = past_ref.get()

        # Pre process past data and get properly formatted input for model
        model_input = model_ops.pre_process(past_result, past_time_limit)

        # Pass formatted data into model and get predictions
        prediction = model_ops.predict(model_input)

        # Extract predicted pm25 and pm10 values
        predicted_pm25, predicted_pm10 = prediction[0]
        # Find AQI from formula
        predicted_aqi = utils.AQIUtils.get_aqi(predicted_pm25, predicted_pm10)

        predicted_to_update = ['pm25', 'pm10', 'aqi']
        predicted_values = [predicted_pm25, predicted_pm10, predicted_aqi]

        # Write predicted values to firebase
        update_firebase('/predicted', predicted_to_update, predicted_values,
                        now_plus_15, predicted_time_limit)
        """ PREDICTED DATA WRITE TO FIREBASE DONE """

        # Delay for some time before next sensor reading
        print("💤 ***DELAYING***\n")
        time.sleep(10)
