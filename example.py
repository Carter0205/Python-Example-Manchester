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

import sys              # Import sys module for command line arguments handling
import json             # Import json module for parsing and outputting JSON data
import urllib.request   # Import urllib.request for making HTTP requests to APIs
import urllib.error     # Import urllib.error for handling HTTP errors during requests


# =========================
# Configuration Section
# =========================

# Base URL for FruityVice API to fetch fruit data
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

    # Construct the full API URL by appending the fruit name
    url = BASE_URL + fruit_name.lower()

    try:
        # Open the URL and read the HTTP response
        with urllib.request.urlopen(url) as response:
            data = response.read()  # Read the response data

            # Convert JSON response into a Python dictionary
            fruit_data = json.loads(data.decode("utf-8"))

            return fruit_data  # Return the parsed data

    except urllib.error.HTTPError as e:
        if e.code == 404:  # Check if the error is a "not found" error
            raise ValueError("Fruit not recognised.")
        else:  # Handle other HTTP errors
            raise ConnectionError("Service unavailable.")

    except urllib.error.URLError:
        # Handle URL errors (e.g., connection issues)
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

    # Return a dictionary with only the necessary fields extracted
    return {
        "name": fruit_data.get("name"),  # Get the fruit name
        "id": fruit_data.get("id"),      # Get the fruit ID
        "family": fruit_data.get("family"),  # Get the family of the fruit
        "sugar": fruit_data.get("nutritions", {}).get("sugar"),  # Get sugar content
        "carbohydrates": fruit_data.get("nutritions", {}).get("carbohydrates"),  # Get carbohydrates content
    }


# =========================
# Output Functions
# =========================

def print_human_readable(data):
    """
    Print output in human-friendly format.
    """

    # Print the fruit information in a clear, readable format
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

    # Convert the data to JSON format and print it with indentation for clarity
    print(json.dumps(data, indent=4))


# =========================
# Main Program Logic
# =========================

def main():
    """
    Main entry point for command line usage.
    """

    # Check if the script is run with command line arguments
    if len(sys.argv) >= 3:
        fruit_name = sys.argv[1]  # Get the fruit name from command line arguments
        output_format = sys.argv[2].lower()  # Get the output format (human/json)
    else:
        # If not enough arguments, ask user for input interactively
        fruit_name = input("Enter fruit name: ")
        output_format = input("Output format (human/json): ").lower()

    try:
        # Fetch data from API using the fruit name
        raw_data = get_fruit_data(fruit_name)

        # Extract only the required fields from the fetched data
        clean_data = extract_required_fields(raw_data)

        # Print the data in the requested format
        if output_format == "human":
            print_human_readable(clean_data)  # Print in human-readable format
        elif output_format == "json":
            print_machine_readable(clean_data)  # Print in JSON format
        else:
            print("Invalid output format. Use 'human' or 'json'.")  # Handle invalid format input

    except ValueError as ve:
        print(f"Error: {ve}")  # Print error if fruit not found

    except ConnectionError as ce:
        print(f"Error: {ce}")  # Print error if there are connection issues

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
    main()  # Execute the main function
