#!/usr/bin/env python3
"""Test script to verify the app works correctly"""

import pandas as pd
import pickle
import numpy as np

def test_csv_loading():
    """Test if CSV loads correctly"""
    try:
        df = pd.read_csv('crop_recommendation.csv')
        print(f"✅ CSV loaded successfully")
        print(f"   Shape: {df.shape}")
        print(f"   Columns: {df.columns.tolist()}")
        print(f"   Unique crops: {len(df['label'].unique())}")
        return True
    except Exception as e:
        print(f"❌ CSV loading failed: {e}")
        return False

def test_model_loading():
    """Test if model loads correctly"""
    try:
        model = pickle.load(open("crop.pkl", "rb"))
        print(f"✅ Model loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False

def test_prediction():
    """Test if prediction works"""
    try:
        df = pd.read_csv('crop_recommendation.csv')
        model = pickle.load(open("crop.pkl", "rb"))
        
        # Test prediction
        features = np.array([[90, 42, 43, 20.8, 82.0, 6.5, 202.9]])
        prediction = model.predict(features)[0]
        print(f"✅ Prediction works: {prediction}")
        return True
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Smart Crop Recommendation System...")
    print("=" * 50)
    
    csv_ok = test_csv_loading()
    model_ok = test_model_loading()
    prediction_ok = test_prediction()
    
    print("=" * 50)
    if csv_ok and model_ok and prediction_ok:
        print("🎉 All tests passed! App should work correctly.")
    else:
        print("❌ Some tests failed. Check the errors above.")
