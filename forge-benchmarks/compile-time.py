import os
import json
import pandas as pd

# Define paths
base_dirs = {
    "solc": "solc",
    "solc-via-ir": "solc-via-ir",
    "solx": "solx",
    "solx-via-ir": "solx-via-ir"
}

# Helper to extract project name from filename
def get_project_name(filename):
    return filename.replace("build_", "").replace(".json", "")

# Collect data
data = {}

for compiler, dir_path in base_dirs.items():
    for filename in os.listdir(dir_path):
        if filename.startswith("build_") and filename.endswith(".json"):
            project = get_project_name(filename)
            filepath = os.path.join(dir_path, filename)
            with open(filepath, "r") as f:
                content = json.load(f)
                compile_time = content.get("compile_time", None)
                if project not in data:
                    data[project] = {}
                data[project][compiler] = compile_time

# Create DataFrame
rows = []
for idx, (project, times) in enumerate(sorted(data.items()), start=1):
    row = {
        "Id": idx,
        "Project": project,
        "solc": times.get("solc"),
        "solc-via-ir": times.get("solc-via-ir"),
        "solx": times.get("solx"),
        "solx-via-ir": times.get("solx-via-ir")
    }
    rows.append(row)

df = pd.DataFrame(rows)

# Export to Excel
output_file = "compile-time.xlsx"
df.to_excel(output_file, index=False)
print(f"Compile time data written to {output_file}")
