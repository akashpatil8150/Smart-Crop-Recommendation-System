import streamlit as st
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
import calendar

# Load model and data
@st.cache_data
def load_model_and_data():
    try:
        model = pickle.load(open("crop.pkl", "rb"))
        crop_data = pd.read_csv("crop_recommendation.csv")
        
        # Verify the CSV has the expected columns
        expected_columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label']
        if not all(col in crop_data.columns for col in expected_columns):
            st.error(f"CSV file is missing expected columns. Found: {crop_data.columns.tolist()}")
            st.stop()
        
        return model, crop_data
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

def get_crop_insights(crop_name):
    """Get detailed insights for a specific crop"""
    try:
        crop_subset = crop_data[crop_data['label'] == crop_name]
        
        # Debug information
        st.info(f"🔍 **Debug:** Found {len(crop_subset)} records for crop '{crop_name}'")
        
        if crop_subset.empty:
            st.warning(f"No data found for crop: {crop_name}")
            # Show available crops for debugging
            available_crops = crop_data['label'].unique()[:10]
            st.write(f"Available crops (first 10): {list(available_crops)}")
            return None
        
        # Ensure we have data before calculating ranges
        if len(crop_subset) == 0:
            st.warning(f"No data available for crop: {crop_name}")
            return None
        
        # Ensure numeric columns are properly converted
        numeric_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        for col in numeric_cols:
            if col in crop_subset.columns:
                crop_subset[col] = pd.to_numeric(crop_subset[col], errors='coerce')
        
        # Remove any rows with NaN values after conversion
        crop_subset = crop_subset.dropna(subset=numeric_cols)
        
        if crop_subset.empty:
            st.warning(f"No valid numeric data found for crop: {crop_name}")
            return None
        
        insights = {
            'name': crop_name,
            'optimal_conditions': {
                'N_range': f"{int(crop_subset['N'].min())} - {int(crop_subset['N'].max())}",
                'P_range': f"{int(crop_subset['P'].min())} - {int(crop_subset['P'].max())}",
                'K_range': f"{int(crop_subset['K'].min())} - {int(crop_subset['K'].max())}",
                'temperature_range': f"{crop_subset['temperature'].min():.1f}°C - {crop_subset['temperature'].max():.1f}°C",
                'humidity_range': f"{crop_subset['humidity'].min():.1f}% - {crop_subset['humidity'].max():.1f}%",
                'ph_range': f"{crop_subset['ph'].min():.2f} - {crop_subset['ph'].max():.2f}",
                'rainfall_range': f"{crop_subset['rainfall'].min():.1f}mm - {crop_subset['rainfall'].max():.1f}mm"
            },
            'avg_conditions': {
                'N': int(crop_subset['N'].mean()),
                'P': int(crop_subset['P'].mean()),
                'K': int(crop_subset['K'].mean()),
                'temperature': round(crop_subset['temperature'].mean(), 1),
                'humidity': round(crop_subset['humidity'].mean(), 1),
                'ph': round(crop_subset['ph'].mean(), 2),
                'rainfall': round(crop_subset['rainfall'].mean(), 1)
            }
        }
        
        return insights
        
    except Exception as e:
        st.error(f"Error getting insights for {crop_name}: {str(e)}")
        return None

def get_seasonal_recommendations(month):
    """Get crop recommendations based on current month"""
    # Simple seasonal logic - you can enhance this based on your data
    if month in [12, 1, 2]:  # Winter
        return ['wheat', 'barley', 'oats', 'peas']
    elif month in [3, 4, 5]:  # Spring
        return ['rice', 'corn', 'cotton', 'sugarcane']
    elif month in [6, 7, 8]:  # Summer
        return ['rice', 'cotton', 'sugarcane', 'maize']
    else:  # Fall (Sep, Oct, Nov)
        return ['maize', 'groundnut', 'mustard', 'gram']

model, crop_data = load_model_and_data()

# Page configuration
st.set_page_config(
    page_title="Smart Crop Recommendation System",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title
st.title("🌱 Smart Crop Recommendation System")
st.markdown("---")

# Sidebar for input parameters
st.sidebar.header("📊 Soil & Weather Parameters")

# Input fields
col1, col2 = st.sidebar.columns(2)

with col1:
    N = st.number_input("Nitrogen (N)", min_value=0, max_value=200, value=50, step=1)
    P = st.number_input("Phosphorus (P)", min_value=0, max_value=200, value=50, step=1)
    K = st.number_input("Potassium (K)", min_value=0, max_value=200, value=50, step=1)

with col2:
    temperature = st.number_input("Temperature (°C)", min_value=0.0, max_value=50.0, value=25.0, step=0.1)
    humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=50.0, step=0.1)
    ph = st.number_input("pH Level", min_value=0.0, max_value=14.0, value=7.0, step=0.1)
    rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=1000.0, value=100.0, step=1.0)

# Prediction button
if st.sidebar.button("🔮 Get Crop Recommendation", type="primary"):
    try:
        # Prediction
        features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        prediction = model.predict(features)[0]
        
        # Debug information
        st.info(f"🔍 **Debug Info:** Predicted crop: '{prediction}' (type: {type(prediction)})")
        
        # Get crop insights
        crop_insights = get_crop_insights(prediction)
        
        # Display results
        st.success(f"🎯 **Recommended Crop: {prediction.title()}**")
        
        if crop_insights:
            st.subheader("📈 Crop Insights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Optimal Conditions:**")
                st.write(f"• Nitrogen: {crop_insights['optimal_conditions']['N_range']}")
                st.write(f"• Phosphorus: {crop_insights['optimal_conditions']['P_range']}")
                st.write(f"• Potassium: {crop_insights['optimal_conditions']['K_range']}")
                st.write(f"• Temperature: {crop_insights['optimal_conditions']['temperature_range']}")
            
            with col2:
                st.write(f"• Humidity: {crop_insights['optimal_conditions']['humidity_range']}")
                st.write(f"• pH Level: {crop_insights['optimal_conditions']['ph_range']}")
                st.write(f"• Rainfall: {crop_insights['optimal_conditions']['rainfall_range']}")
            
            st.markdown("**Average Conditions for this crop:**")
            avg_conditions = crop_insights['avg_conditions']
            st.write(f"• N: {avg_conditions['N']}, P: {avg_conditions['P']}, K: {avg_conditions['K']}")
            st.write(f"• Temperature: {avg_conditions['temperature']}°C, Humidity: {avg_conditions['humidity']}%")
            st.write(f"• pH: {avg_conditions['ph']}, Rainfall: {avg_conditions['rainfall']}mm")
        else:
            st.warning("No detailed insights available for this crop.")
            
    except Exception as e:
        st.error(f"Error during prediction: {str(e)}")
        st.write("Please check your input values and try again.")

# Monthly recommendations section
st.subheader("📅 Monthly Recommendations")
current_month = datetime.now().month
month_name = calendar.month_name[current_month]
seasonal_crops = get_seasonal_recommendations(current_month)

st.write(f"**Recommended crops for {month_name}:**")
for i, crop in enumerate(seasonal_crops, 1):
    st.write(f"{i}. {crop.title()}")

# Data overview
st.subheader("📊 Dataset Overview")
st.write(f"Total crops in dataset: {len(crop_data['label'].unique())}")
st.write(f"Total records: {len(crop_data)}")

# Display sample data
if st.checkbox("Show sample data"):
    st.dataframe(crop_data.head(10))
