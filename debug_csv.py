#!/usr/bin/env python3
import pandas as pd

# Load and inspect the CSV
df = pd.read_csv('crop_recommendation.csv')

print("CSV Info:")
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"Data types: {df.dtypes.to_dict()}")

print("\nFirst 3 rows:")
print(df.head(3))

print("\nLabel column info:")
print(f"Label column type: {df['label'].dtype}")
print(f"Label column unique values: {df['label'].unique()[:10]}")
print(f"Total unique crops: {df['label'].nunique()}")

print("\nChecking for NaN values:")
print(df.isnull().sum())

print("\nSample label values:")
print(df['label'].value_counts().head(10))
