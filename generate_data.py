import pandas as pd
import numpy as np

np.random.seed(42)

rows = 300

data = {
    "user_id": np.random.randint(1000, 1100, rows),
    "hour": np.random.randint(0, 24, rows),
    "file_type": np.random.choice(["pdf", "docx", "xlsx", "exe"], rows),
    "data_size": np.random.normal(50, 10, rows),
    "destination": np.random.choice(["internal", "external"], rows, p=[0.8, 0.2])
}

df = pd.DataFrame(data)

# Inject anomalies
anomaly_indices = np.random.choice(df.index, size=30)

df.loc[anomaly_indices, "data_size"] = np.random.uniform(100, 200, 30)
df.loc[anomaly_indices, "destination"] = "external"
df.loc[anomaly_indices, "hour"] = np.random.choice([1,2,3,4], 30)

df["label"] = 0
df.loc[anomaly_indices, "label"] = 1

df.to_csv("dlp_dataset.csv", index=False)

print("Dataset created ✅")
