# Dubizzle Trust & Safety MVP

This project demonstrates a Machine Learning MVP to flag suspicious listings for Dubizzle.  
It uses text + price anomaly features to predict high-risk listings.

## Quick Start

1. Clone repo
2. Install dependencies: `pip install -r requirements.txt`
3. Run Streamlit demo: `streamlit run app.py`

## Features
- Text features: spam keywords, caps ratio, emojis, repeated words
- Price anomaly detection
- Seller type & posting recency
- Risk scoring & top suspicious listings dashboard

![Dashboard Screenshot](screenshots/dashboard.png)
