import json

def load_alerts(file_path):
    with open(file_path, "r") as file:
        alerts = json.load(file)
    return alerts