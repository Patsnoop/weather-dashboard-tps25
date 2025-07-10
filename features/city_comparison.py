import csv
from pathlib import Path

class CityComparison:
    def __init__(self, file_paths):
        self.file_paths = file_paths

    def get_top_line_data(self):
        comparisons = []

        for file_path in self.file_paths:
            path = Path(file_path)
            if not path.exists():
                comparisons.append(f"{file_path}: File not found.")
                continue

            try:
                with open(path, 'r') as file:
                    reader = csv.DictReader(file)
                    first_row = next(reader, None)

                    if first_row:
                        comparisons.append(
                            f"{first_row['city']}: {first_row['temp']}°F, "
                            f"Humidity: {first_row['humidity']}%, "
                            f"{first_row['description']}"
                        )
                    else:
                        comparisons.append(f"{file_path}: No data.")
            except Exception as e:
                comparisons.append(f"{file_path}: Error reading file ({e})")

        return "\n".join(comparisons)