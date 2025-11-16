import os
import csv
import json

def csv_to_json(csv_file, json_file, num_entries):
    data = []
    csv_path = os.path.join(os.path.dirname(__file__), csv_file)
    with open(csv_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for i, row in enumerate(csvreader):
            if i >= num_entries:
                break
            data.append(row)
    
    with open(json_file, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)

# Example usage:
csv_to_json('../test/archive/tmdb_5000_movies.csv', '../test/data/movies_data.json', num_entries=3854)
