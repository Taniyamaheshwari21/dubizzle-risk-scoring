import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.predict import predict_risk

st.set_page_config(page_title="Dubizzle Trust & Safety MVP", layout="wide")

st.title("🔍 Dubizzle Trust & Safety MVP")
st.markdown("""
This demo flags suspicious listings using text, price anomalies, and other signals.
""")

uploaded_file = st.file_uploader("Upload listings CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.info("Using default synthetic dataset")
    df = pd.read_csv("dubizzle_synthetic_listings.csv")


st.header("📊 Scoring Listings...")
df_scored = predict_risk(df)

st.success(f"Scored {len(df_scored)} listings successfully!")

st.subheader("🚨 Top 20 Suspicious Listings")
top_susp = df_scored.sort_values("risk_score", ascending=False).head(20)
st.dataframe(top_susp[["listing_id","title","category","price_aed","risk_score","predicted_suspicious","suspicious_reason"]])


st.subheader("📈 Risk Score Distribution")
fig, ax = plt.subplots(figsize=(5, 2.5))  
ax.hist(df_scored["risk_score"], bins=20, color="tomato", edgecolor="black")
ax.set_xlabel("Risk Score")
ax.set_ylabel("Number of Listings")
st.pyplot(fig)

st.subheader("📊 Suspicious Listings by Category")
cat_counts = df_scored[df_scored["predicted_suspicious"]==1]["category"].value_counts()
fig2, ax2 = plt.subplots(figsize=(5, 2.5)) 
cat_counts.plot(kind="bar", ax=ax2, color="skyblue")
ax2.set_ylabel("Number of Suspicious Listings")
ax2.set_xlabel("Category")
st.pyplot(fig2)


st.subheader("ℹ️ Quick Stats")
st.write(f"Total listings: {len(df_scored)}")
st.write(f"Suspicious listings: {df_scored['predicted_suspicious'].sum()}")
st.write(f"Normal listings: {len(df_scored) - df_scored['predicted_suspicious'].sum()}")


st.subheader("💾 Download Scored Listings")
csv = df_scored.to_csv(index=False).encode("utf-8")
st.download_button(label="Download CSV", data=csv, file_name="scored_listings.csv", mime="text/csv")

st.markdown("---")
st.markdown("✅ Built by Taniya Maheshwari | ML Engineer Intern MVP Demo")
