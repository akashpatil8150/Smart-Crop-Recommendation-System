from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
import calendar

# Load model and data
model = pickle.load(open("crop.pkl", "rb"))
crop_data = pd.read_csv("crop_recommendation.csv")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        N = int(request.form['N'])
        P = int(request.form['P'])
        K = int(request.form['K'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])

        # Prediction
        features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        prediction = model.predict(features)[0]

        # Get crop insights
        crop_insights = get_crop_insights(prediction)
        
        # Return JSON response for AJAX handling
        return jsonify({
            'crop': prediction,
            'insights': crop_insights,
            'input_data': {
                'N': N, 'P': P, 'K': K,
                'temperature': temperature,
                'humidity': humidity,
                'ph': ph, 'rainfall': rainfall
            }
        })

@app.route('/api/monthly-recommendations')
def monthly_recommendations():
    current_month = datetime.now().month
    month_name = calendar.month_name[current_month]
    
    # Get seasonal recommendations based on current month
    seasonal_crops = get_seasonal_recommendations(current_month)
    
    return jsonify({
        'month': month_name,
        'recommendations': seasonal_crops
    })

@app.route('/api/crop-insights/<crop_name>')
def crop_insights(crop_name):
    insights = get_crop_insights(crop_name)
    return jsonify(insights)

def get_crop_insights(crop_name):
    """Get detailed insights for a specific crop"""
    crop_subset = crop_data[crop_data['label'] == crop_name]
    
    if crop_subset.empty:
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


if __name__ == '__main__':
    app.run(debug=True)
