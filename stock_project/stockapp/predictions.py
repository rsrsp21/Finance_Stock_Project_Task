import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from .models import StockData

def parse_timestamp(timestamp_str):
    return pd.to_datetime(timestamp_str, format='%b. %d, %Y, midnight')

def predict_stock_prices(symbol, days=30):
    # Fetch historical stock data from your database
    historical_data = StockData.objects.filter(symbol=symbol).order_by('timestamp')

    # Convert to DataFrame
    df = pd.DataFrame(list(historical_data.values('timestamp', 'close_price')))
    
    # Parse the timestamp strings to datetime
    df['timestamp'] = df['timestamp'].apply(parse_timestamp)
    
    # Ensure the data is sorted by timestamp
    df.set_index('timestamp', inplace=True)
    
    # Check if data is available
    if df.empty:
        return pd.DataFrame(columns=['predicted_price'])

    # Prepare features for the model
    df['days'] = (df.index - df.index.min()).days  # Create a 'days' feature
    X = df[['days']]
    y = df['close_price']
    
    # Train a simple Linear Regression model on historical data
    model = LinearRegression()
    model.fit(X, y)
    
    # Predicting future prices
    # Start predicting from today
    today_days = (pd.to_datetime('today') - df.index.min()).days
    future_days = np.array([[today_days + i] for i in range(1, days + 1)])
    predicted_prices = model.predict(future_days)
    
    # Create a DataFrame for predictions
    future_dates = pd.date_range(start=pd.to_datetime('today'), periods=days, freq='D')
    predictions = pd.DataFrame(data=predicted_prices, index=future_dates, columns=['predicted_price'])
    
    # Convert the index to string format for JSON serialization
    predictions.index = predictions.index.strftime('%b. %d, %Y, midnight')
    
    return predictions