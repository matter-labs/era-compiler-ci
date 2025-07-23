import os
import json
import pandas as pd
from collections import defaultdict

# Compiler directories and column names
compiler_dirs = {
    "solc": "Mean (solc)",
    "solc-via-ir": "Mean (solc-via-ir)",
    "solx": "Mean (solx)",
    "solx-via-ir": "Mean (solx-via-ir)"
}

# Structure: {(test, contract, function): {compiler: mean_value}}
data = defaultdict(dict)

for compiler, column in compiler_dirs.items():
    for file_name in os.listdir(compiler):
        if file_name.startswith(("build_", "test_")):
            continue
        test_name = file_name.replace(".json", "")
        file_path = os.path.join(compiler, file_name)

        if not os.path.isfile(file_path):
            continue

        with open(file_path, "r") as f:
            try:
                contracts = json.load(f)
            except json.JSONDecodeError:
                print(f"Error parsing {file_path}")
                continue

            for contract_entry in contracts:
                contract_name = contract_entry["contract"]

                # Deployment gas (as a function "deployment")
                deployment_gas = contract_entry.get("deployment", {}).get("gas")
                if deployment_gas is not None:
                    data[(test_name, contract_name, "deployment")][column] = deployment_gas

                # Function gas data
                for function_name, stats in contract_entry.get("functions", {}).items():
                    data[(test_name, contract_name, function_name)][column] = stats.get("mean")

# Build final table rows
rows = []
for (test, contract, function), values in sorted(data.items()):
    row = {
        "Test": test,
        "Contract": contract,
        "Function": function,
        "Mean (solc)": values.get("Mean (solc)"),
        "Mean (solc-via-ir)": values.get("Mean (solc-via-ir)"),
        "Mean (solx)": values.get("Mean (solx)"),
        "Mean (solx-via-ir)": values.get("Mean (solx-via-ir)")
    }
    rows.append(row)

# Create a DataFrame
df = pd.DataFrame(rows)

# Save to Excel
output_file = "gas.xlsx"
df.to_excel(output_file, index=True)
print(f"Gas excel file written to {output_file}")
