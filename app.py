import streamlit as st
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, r2_score

# ------------------------
# 🎨 Page Config & Theme
# ------------------------
st.set_page_config(page_title="AI Inventory Forecast", layout="wide")
st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: #5AC8FA;'>📊 AI-Powered Inventory System</h1>
        <p style='color: gray; font-size: 18px;'>Forecast Inventory & Predict Outputs from Any Dataset</p>
    </div>
    <hr style='border: 1px solid #A1E3D8;'>
""", unsafe_allow_html=True)

# ------------------------
# 📁 Tabs: Forecast | Smart CSV
# ------------------------
tabs = st.tabs(["📦 Inventory Forecast", "🧠 Smart CSV Predictor"])

# ====================================================
# 📦 TAB 1: Inventory Forecast (your existing code)
# ====================================================
with tabs[0]:

    @st.cache_data
    def load_data():
        df = pd.read_csv("data/processed/final_data.csv")
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df

    df = load_data()
    items = df["item_name"].unique().tolist()

    st.sidebar.markdown("## ⚙️ Forecast Settings")
    selected_item = st.sidebar.selectbox("📦 Choose an Item", items)
    forecast_hours = st.sidebar.slider("⏰ Forecast Horizon (Hours)", 6, 48, 24)

    df_item = df[df["item_name"] == selected_item]
    df_hourly = df_item.groupby(pd.Grouper(key="timestamp", freq="h"))["quantity"].sum().reset_index()
    df_hourly = df_hourly.set_index("timestamp").asfreq("h", fill_value=0).reset_index()
    df_prophet = df_hourly.rename(columns={"timestamp": "ds", "quantity": "y"})

    # ➤ Metrics
    latest_demand = int(df_hourly["quantity"].iloc[-1])
    avg_demand = round(df_hourly["quantity"].mean(), 2)
    col1, col2, col3 = st.columns(3)
    col1.metric("🕐 Last Hour Demand", f"{latest_demand} units")
    col2.metric("📊 Avg. Hourly Demand", f"{avg_demand} units")
    col3.metric("🔮 Forecast Period", f"{forecast_hours} hrs")

    # ➤ Prophet Forecast
    with st.spinner("🧠 Training Prophet model..."):
        model = Prophet(
            yearly_seasonality=False,
            weekly_seasonality=True,
            daily_seasonality=True
        )
        model.fit(df_prophet)
        future = model.make_future_dataframe(periods=forecast_hours, freq="h")
        forecast = model.predict(future)

    st.markdown(f"### 📈 Forecast Graph for: {selected_item}")
    fig = plot_plotly(model, forecast)
    fig.update_layout(
        title=f"{selected_item} - Forecasted Demand",
        xaxis_title="Timestamp (Hourly)",
        yaxis_title="Predicted Demand (Units)",
        template="plotly_white",
        title_font=dict(size=20, color="#5AC8FA")
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📄 View Raw Forecast Data"):
        st.dataframe(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(forecast_hours))
        st.download_button(
            label="📥 Download Forecast CSV",
            data=forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_csv(index=False),
            file_name=f"{selected_item}_forecast.csv",
            mime="text/csv"
        )

    st.markdown("### 🤖 Smart Reorder Suggestion")
    current_stock = st.number_input(f"Enter current stock for {selected_item}:", min_value=0, value=50)
    safety_buffer = 10
    total_forecast = int(forecast["yhat"][-forecast_hours:].clip(lower=0).sum())

    if total_forecast > (current_stock - safety_buffer):
        st.error(f"🔁 Reorder Needed!\n📦 Forecasted demand = {total_forecast} units")
        urgency = "🔥 High" if (total_forecast - current_stock) > 20 else "⚠️ Moderate"
        st.markdown(f"<span style='color: red; font-weight: bold;'>📛 Urgency: {urgency}</span>", unsafe_allow_html=True)
        reorder_qty = max((total_forecast - current_stock + safety_buffer), 0)
        st.info(f"🔄 Recommended Reorder Quantity: **{int(reorder_qty)} units**")
    else:
        st.success(f"✅ Stock is OK.\n📦 Forecasted demand = {total_forecast} units")
        st.markdown("<span style='color: green; font-weight: bold;'>👍 No immediate action required.</span>", unsafe_allow_html=True)

    st.caption("📌 *Note: Negative forecasts are treated as 0 to reflect real-world demand.*")

# ====================================================
# 🧠 TAB 2: Smart CSV ML Predictor
# ====================================================
with tabs[1]:
    st.markdown("### 📂 Upload Your Dataset")

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")

        st.markdown("### 🧬 Data Preview")
        st.dataframe(data.head())

        target = st.selectbox("🎯 Select Target Column (Output Variable)", data.columns)

        X = data.drop(columns=[target])
        y = data[target]

        # Handle categorical
        X = pd.get_dummies(X)

        # Detect task type
        task_type = "classification" if y.nunique() <= 10 else "regression"
        st.info(f"🔍 Detected Task Type: **{task_type.capitalize()}**")

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        if task_type == "classification":
            model = RandomForestClassifier()
        else:
            model = RandomForestRegressor()

        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        st.markdown("### 📊 Model Performance")
        if task_type == "classification":
            score = accuracy_score(y_test, predictions)
            st.metric("🎯 Accuracy", f"{score*100:.2f}%")
        else:
            score = r2_score(y_test, predictions)
            st.metric("📈 R² Score", f"{score:.2f}")

        with st.expander("🔍 View Predictions"):
            pred_df = pd.DataFrame({
                "Actual": y_test.values,
                "Predicted": predictions
            }).reset_index(drop=True)
            st.dataframe(pred_df)

# ====================================================
# Footer
# ====================================================
st.markdown("""
    <hr style='margin-top: 30px;'>
    <div style='text-align: center; color: gray;'>
        🚀 Built by <b>Sadeed</b> | Powered by <b>Prophet + ML + Streamlit</b>
    </div>
""", unsafe_allow_html=True)
