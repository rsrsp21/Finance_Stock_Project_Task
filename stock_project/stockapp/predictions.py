import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from .models import StockData

def parse_timestamp(timestamp_str):
    return pd.to_datetime(timestamp_str, format='%b. %d, %Y, midnight')

def predict_stock_prices(symbol, days=30):
    """
    Predict stock prices for the given symbol for the next specified number of days.
    
    Parameters:
    - symbol (str): The stock symbol to predict.
    - days (int): The number of days to predict prices for.

    Returns:
    - DataFrame: A DataFrame containing predicted prices indexed by future dates.
    """
    try:
        # Fetch historical stock data from the database
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
        
        # Get the minimum date from the index
        min_date = df.index.min().tz_localize(None)  # Make it naive if it’s aware
        
        # Predict future prices
        today_days = (pd.to_datetime('today').tz_localize(None) - min_date).days  # Make 'today' naive
        future_days = np.array([[today_days + i] for i in range(1, days + 1)])
        predicted_prices = model.predict(future_days)
        
        # Create a DataFrame for predictions
        future_dates = pd.date_range(start=pd.to_datetime('today').tz_localize(None), periods=days, freq='D')  # Make future dates naive
        predictions = pd.DataFrame(data=predicted_prices, index=future_dates, columns=['predicted_price'])
        
        # Convert the index to string format for JSON serialization
        predictions.index = predictions.index.strftime('%b. %d, %Y, midnight')
        
        return predictions

    except Exception as e:
        # Handle exceptions (logging, re-raising, etc.)
        print(f"An error occurred: {e}")
        return pd.DataFrame(columns=['predicted_price'])