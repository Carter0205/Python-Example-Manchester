"""
fruityvice_lookup.py

RSE Interview Task
------------------
This script interacts with the FruityVice API to fetch fruit data.

Features:
- Command line usage
- Library function usage
- Human-readable output
- Machine-readable (JSON) output
- Graceful error handling
- Simple and extendable structure

Author: YourGitHubUsername
"""

# =========================
# Standard Library Imports
# =========================

import sys              # For command line arguments
import json             # For machine-readable JSON output
import urllib.request   # For making HTTP requests
import urllib.error     # For handling HTTP errors


# =========================
# Configuration Section
# =========================

# Base URL for FruityVice API
BASE_URL = "https://www.fruityvice.com/api/fruit/"


# =========================
# Core Function
# =========================

def get_fruit_data(fruit_name):
    """
    Fetch fruit data from FruityVice API.

    Parameters:
        fruit_name (str): Name of the fruit (e.g., "Strawberry")

    Returns:
        dict: Parsed JSON response from API

    Raises:
        ValueError: If fruit not found (404)
        ConnectionError: If API unavailable
    """

    # Construct full API URL
    url = BASE_URL + fruit_name.lower()

    try:
        # Open the URL and read response
        with urllib.request.urlopen(url) as response:
            data = response.read()

            # Convert JSON response into Python dictionary
            fruit_data = json.loads(data.decode("utf-8"))

            return fruit_data

    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise ValueError("Fruit not recognised.")
        else:
            raise ConnectionError("Service unavailable.")

    except urllib.error.URLError:
        raise ConnectionError("Service unavailable.")


# =========================
# Data Formatting Function
# =========================

def extract_required_fields(fruit_data):
    """
    Extract only the required fields from API response.

    Returns:
        dict: Clean dictionary with required fields only
    """

    return {
        "name": fruit_data.get("name"),
        "id": fruit_data.get("id"),
        "family": fruit_data.get("family"),
        "sugar": fruit_data.get("nutritions", {}).get("sugar"),
        "carbohydrates": fruit_data.get("nutritions", {}).get("carbohydrates"),
    }


# =========================
# Output Functions
# =========================

def print_human_readable(data):
    """
    Print output in human-friendly format.
    """

    print("\nFruit Information")
    print("-----------------")
    print(f"Full Name       : {data['name']}")
    print(f"ID              : {data['id']}")
    print(f"Family          : {data['family']}")
    print(f"Sugar (g)       : {data['sugar']}")
    print(f"Carbohydrates(g): {data['carbohydrates']}")
    print()


def print_machine_readable(data):
    """
    Print output in JSON format.
    This is suitable for machine parsing.
    """

    print(json.dumps(data, indent=4))


# =========================
# Main Program Logic
# =========================

def main():
    """
    Main entry point for command line usage.
    """

    # If script is run with command line arguments
    if len(sys.argv) >= 3:
        fruit_name = sys.argv[1]
        output_format = sys.argv[2].lower()
    else:
        # If not enough arguments, ask user interactively
        fruit_name = input("Enter fruit name: ")
        output_format = input("Output format (human/json): ").lower()

    try:
        # Fetch data from API
        raw_data = get_fruit_data(fruit_name)

        # Extract only required fields
        clean_data = extract_required_fields(raw_data)

        # Print in requested format
        if output_format == "human":
            print_human_readable(clean_data)
        elif output_format == "json":
            print_machine_readable(clean_data)
        else:
            print("Invalid output format. Use 'human' or 'json'.")

    except ValueError as ve:
        print(f"Error: {ve}")

    except ConnectionError as ce:
        print(f"Error: {ce}")

    except Exception as e:
        # Catch any unexpected errors
        print("Unexpected error occurred:", str(e))


# =========================
# Allow Script + Library Use
# =========================

# This ensures:
# - Runs main() if executed directly
# - Does NOT run if imported as a module
if __name__ == "__main__":
    main()
