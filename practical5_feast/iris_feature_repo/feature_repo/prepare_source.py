import pandas as pd
from pathlib import Path

# Experiment 4 output
input_file = Path("../../../data/processed/iris_features.csv")

# Feast source file
output_file = Path("data/iris_features.parquet")

# Read CSV
df = pd.read_csv(input_file)
df = df.rename(columns={
    "sepal length (cm)": "sepal_length",
    "sepal width (cm)": "sepal_width",
    "petal length (cm)": "petal_length",
    "petal width (cm)": "petal_width",
})

# Create entity ID
df.insert(0, "sample_id", range(len(df)))

# Create timestamps
start_time = pd.Timestamp("2026-08-15 15:20:02", tz="UTC")

df["event_timestamp"] = pd.date_range(
    start=start_time,
    periods=len(df),
    freq="min"
)

df["created_timestamp"] = df["event_timestamp"]

# Create output directory
output_file.parent.mkdir(parents=True, exist_ok=True)

# Save as Parquet
df.to_parquet(output_file, index=False)

print(f"Saved {len(df)} rows to {output_file}")
print(f"Columns: {list(df.columns)}")