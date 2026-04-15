import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title="AI DLP Dashboard", layout="wide")

st.title("🔐 AI-Driven Data Loss Prevention System")

# Load Data
df = pd.read_csv("dlp_dataset.csv")

# Sidebar filters
st.sidebar.header("⚙️ Filters")
selected_user = st.sidebar.selectbox("Select User", ["All"] + list(df["user_id"].unique()))

if selected_user != "All":
    df = df[df["user_id"] == selected_user]

# Encoding
le_file = LabelEncoder()
le_dest = LabelEncoder()

df["file_type"] = le_file.fit_transform(df["file_type"])
df["destination"] = le_dest.fit_transform(df["destination"])

# Model
features = ["hour", "file_type", "data_size", "destination"]

model = IsolationForest(contamination=0.1)
df["anomaly"] = model.fit_predict(df[features])
df["anomaly"] = df["anomaly"].map({1: 0, -1: 1})

# Metrics
total = len(df)
anomalies = df["anomaly"].sum()
normal = total - anomalies

col1, col2, col3 = st.columns(3)

col1.metric("Total Events", total)
col2.metric("Normal Activity", normal)
col3.metric("Anomalies 🚨", anomalies)

# Visualization
st.subheader("📈 Data Transfer Behavior")

fig, ax = plt.subplots()
colors = ["blue" if x == 0 else "red" for x in df["anomaly"]]

ax.scatter(df.index, df["data_size"], c=colors)
ax.set_xlabel("Index")
ax.set_ylabel("Data Size")
ax.set_title("Anomaly Detection (Red = Suspicious)")

st.pyplot(fig)

# Suspicious Activity
st.subheader("🚨 Suspicious Activities")

anomaly_df = df[df["anomaly"] == 1]
st.dataframe(anomaly_df)

# Download
st.download_button(
    "📥 Download Results",
    df.to_csv(index=False),
    "dlp_results.csv"
)
