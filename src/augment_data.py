import pandas as pd
import numpy as np

path = "data/raw/iris_v1.csv"

df = pd.read_csv(path)

rng = np.random.default_rng(42)

synthetic = df.sample(20, random_state=42).copy()

numeric_cols = df.select_dtypes(include="number").columns

for col in numeric_cols:
    synthetic[col] += rng.normal(0, 0.05, size=len(synthetic))

df = pd.concat([df, synthetic], ignore_index=True)

df.to_csv(path, index=False)

print(f"Augmented dataset: {len(df)} rows")