# Handling Exceptions in save_to_csv Method in organism.py

In the `save_to_csv` method provided, there are potential exceptions that could occur during the file writing process. It is important to handle these exceptions properly to ensure robustness and reliability of the code.

## Exception Handling Strategy

1. **Identifying Potential Exceptions**:
   - IOError: This exception can occur when there are issues with file operations such as opening or writing to a file.

2. **Handling the Exception**:
   - Catch the `IOError` exception using a `try-except` block to handle any errors that may arise during file writing.
   - Print an informative error message to indicate the specific issue encountered.

3. **Rationale for Exception Handling**:
   - By catching and handling the `IOError` exception, we can prevent the program from crashing and provide feedback to the user about the error.
   - This approach ensures graceful error handling, stopping the simulation from crashing just because there is a problem saving one organism and thus improving the overall robustness of the code.

## Code Snippet for Exception Handling

```python
import os
import csv
from settings import settings

def save_to_csv(self):
    file_exists = os.path.isfile(settings.database.database_csv_filename)
    try:
        with open(settings.database.database_csv_filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(self.get_headers())
            writer.writerow(self.get_stats())
    except IOError as e:
        print(f"Error writing to CSV: {e}")
```