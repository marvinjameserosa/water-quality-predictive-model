import csv
from typing import Dict, Any
from datetime import datetime

def dict_to_csv(data_dict: Dict[str, Any], output_file: str) -> None:
    """
    Convert a dictionary of sensor data to a CSV file.
    
    :param data_dict: Dictionary containing sensor data
    :param output_file: Name of the output CSV file
    """
    # Define the order of columns in the CSV
    fieldnames = ['timestamp', 'pH', 'temperature', 'do', 'turbidity', 'exception']
    
    # Open the CSV file for writing
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header
        writer.writeheader()
        
        # Prepare the row data
        row_data = {
            'timestamp': datetime.now().isoformat(),
            'pH': data_dict.get('ph', 'None'),
            'temperature': data_dict.get('temperature', 'None'),
            'do': data_dict.get('do', 'None'),
            'turbidity': data_dict.get('turbidity', 'None'),
            'exception': data_dict.get('exception', '')
        }
        
        # Write the data row
        writer.writerow(row_data)

    print(f"Data has been written to {output_file}")
