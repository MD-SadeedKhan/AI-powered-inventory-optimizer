# 📊 AI-Powered Inventory Forecast System

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-success?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Visualization-orange?logo=plotly&logoColor=white)](https://plotly.com/)
[![Prophet](https://img.shields.io/badge/Prophet-TimeSeries-purple?logo=apache&logoColor=white)](https://facebook.github.io/prophet/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🚀 Project Overview
The **AI-Powered Inventory Forecast System** is an intelligent web application that leverages **time series forecasting** and **machine learning** to help businesses predict inventory demand, optimize stock levels, and make data-driven decisions.  

With this system, users can:
- Forecast hourly inventory demand using historical data.
- Upload any CSV dataset to predict outputs using machine learning.
- Get **smart reorder suggestions** based on predicted demand.
- Visualize predictions with **interactive dashboards**.

---

## 🧠 Key Features

### 1. Inventory Forecasting
- Uses **Prophet** for accurate time series predictions.
- Supports **hourly, daily, and weekly seasonality**.
- Interactive plots with **Plotly**.
- Provides **forecast metrics**: Last Hour Demand, Average Demand, Forecast Horizon.

### 2. Smart CSV Predictor
- Upload any CSV dataset and predict outputs automatically.
- **Detects task type** (classification or regression).
- Uses **Random Forest** for high-performance predictions.
- Displays model performance metrics:
  - Accuracy (classification)
  - R² Score (regression)

### 3. AI-Driven Decision Support
- Recommends **reorder quantity** based on forecasted demand.
- Flags urgency levels: **High / Moderate / Safe Stock**.
- Treats negative forecasts realistically (as 0 units).

---

## 📂 Tech Stack

| Layer | Technology |
|-------|------------|
| Backend & ML | Python, pandas, scikit-learn, Prophet |
| Visualization | Plotly |
| Web App | Streamlit |
| Deployment | Local / Cloud (Streamlit Share, Heroku, etc.) |

---

## 🎯 Skills Highlighted
- Python Programming & Data Analysis
- Time Series Forecasting (Prophet)
- Machine Learning (Random Forest)
- Data Visualization & Interactive Dashboards (Plotly + Streamlit)
- AI-Powered Decision Making

---

## 🖥️ Demo
![Dashboard Demo](assets/demo.gif)  
*(Add a GIF or screenshots of your Streamlit dashboard here)*

---

## 💻 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/AI-Inventory-Forecast.git
cd AI-Inventory-Forecast

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 📂 File Structure
```
AI-Inventory-Forecast/
│
├── data/processed/      # Sample CSV data
├── app.py               # Main Streamlit app
├── requirements.txt     # Python dependencies
├── assets/              # Images/GIFs for README
└── README.md
```

---

## 🔗 Future Enhancements
- Add **multi-item forecasting** with bulk CSV upload.
- Integrate **real-time stock updates** from databases.
- Deploy on **cloud platforms** for remote access.

---

## 📌 Author
**Sadeed Khan**  
- Data Science & Machine Learning Enthusiast  
- GitHub: [github.com/sadeed](https://github.com/MD-SadeedKhan)  
- LinkedIn: [linkedin.com/in/sadeed](https://www.linkedin.com/in/sadeed-khan29/)

---

## 📜 License
This project is licensed under the **MIT License**.  
