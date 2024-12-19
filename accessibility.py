import csv
import os
import subprocess

# Input and output file paths
input_csv = "accessibility_report.csv"
output_csv = "output.csv"
html_directory = "html_files"

# Create directory for HTML files
os.makedirs(html_directory, exist_ok=True)

# Read CSV, process rows, and save HTML files
rows = []
with open(input_csv, "r", encoding="utf-8") as infile:
    reader = csv.DictReader(infile)
    if "body" not in reader.fieldnames:
        raise KeyError("The CSV file does not contain a 'body' column.")
    rows = list(reader)

# Prepare data for output
output_rows = []

for row in rows:
    try:
        body_content = row["body"]
    except KeyError:
        body_content = ""
        print(
            f"Warning: Missing 'body' for row with ID {row.get('wikipageid', 'unknown')}."
        )

    file_name = f"{html_directory}/{row['wikipageid']}.html"

    # Save body content to an HTML file
    with open(file_name, "w", encoding="utf-8") as html_file:
        html_file.write(body_content)

    # Run Pa11y and capture results
    try:
        result = subprocess.run(["pa11y", file_name], capture_output=True, text=True)
        raw_output = result.stdout

        # Process Pa11y output to extract errors
        errors = []
        for line in raw_output.splitlines():
            if line.startswith(" • Error:"):
                errors.append(line.strip())

        # Add the errors and error count to output
        for error in errors:
            output_row = row.copy()
            output_row["pa11y_error"] = error
            output_row["error_count"] = len(errors)
            output_rows.append(output_row)

    except Exception as e:
        output_row = row.copy()
        output_row["pa11y_error"] = f"Error: {str(e)}"
        output_row["error_count"] = 0
        output_rows.append(output_row)

# Write updated rows to the new CSV
with open(output_csv, "w", encoding="utf-8", newline="") as outfile:
    fieldnames = list(rows[0].keys()) + ["pa11y_error", "error_count"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output_rows)

print("Processing complete. Results saved to output.csv.")
