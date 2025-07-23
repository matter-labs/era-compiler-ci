import os
import json
import pandas as pd

# Define all compiler directories
compiler_dirs = [
    "solc",
    "solc-via-ir",
    "solx",
    "solx-via-ir"
]

# Dictionary to collect all data
all_data = []

for compiler in compiler_dirs:
    for filename in os.listdir(compiler):
        if not (filename.startswith("build_sizes_") and filename.endswith(".json")):
            continue
        project = filename.replace("build_sizes_", "").replace(".json", "")
        path = os.path.join(compiler, filename)
        with open(path, 'r') as f:
            content = json.load(f)
            for contract, sizes in content.items():
                entry = {
                    "Project": project,
                    "Contract": contract,
                    f"{compiler}_runtime": sizes.get("runtime_size"),
                    f"{compiler}_init": sizes.get("init_size")
                }
                all_data.append(entry)

# Merge all entries on Project + Contract
df = pd.DataFrame(all_data)
df = df.groupby(["Project", "Contract"], as_index=False).first()

# Add an ID column
df.insert(0, "Id", range(1, len(df) + 1))

# Save to Excel
output_file = "codesize.xlsx"
df.to_excel(output_file, index=False)
print(f"Codesize excel file written to {output_file}")
