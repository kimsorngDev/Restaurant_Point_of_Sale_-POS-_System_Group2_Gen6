import json
import os 

def load_menu():
    try:
        with open("data/menu.json", "r") as file:
            menu = json.load(file)
        return menu

    except FileNotFoundError:
        print("Menu file not found.")
        return []

    except json.JSONDecodeError:
        print("Menu file contains invalid JSON.")
        return []

def load_tables():
    try:
        with open("data/tables.json", "r") as file:
            tables = json.load(file)
        return tables

    except FileNotFoundError:
        print("Tables file not found.")
        return []

    except json.JSONDecodeError:
        print("Tables file contains invalid JSON.")
        return []

def save_json(filename, data):
    try:
        with open("data/" + filename, "w") as file:
            json.dump(data, file, indent=4)
        print("Data saved successfully.")

    except OSError:
        print("Error saving data.")

